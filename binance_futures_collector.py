#!/usr/bin/env python3
"""Binance USDT-M futures kline collector.

Picks the top-N coins by market cap (CoinGecko) that are listed as USDT-M
perpetual futures on Binance, then downloads their full kline history for
several intervals and stores one gzip CSV per symbol/interval:

    data/<SYMBOL>/<SYMBOL>_<interval>.csv.gz

History is fetched from two public, key-less sources:

* data.binance.vision  - Binance's official bulk dumps (monthly + daily zips).
                         Fast and complete, lags real time by about one day.
* fapi.binance.com     - REST /fapi/v1/klines, used to fill the gap up to now
                         (or for everything with --source api). Blocked in
                         some regions (HTTP 451); the collector then falls
                         back to data.binance.vision only.

Every request is throttled, retried with backoff on network errors/5xx, and
honours 429/418 Retry-After plus the X-MBX-USED-WEIGHT-1M header, so the run
is slow but safe. Re-running resumes from the last saved candle.
"""

import argparse
import csv
import gzip
import hashlib
import io
import json
import logging
import os
import random
import re
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
from datetime import date, datetime, timedelta, timezone

import requests

FAPI_URL = "https://fapi.binance.com"
VISION_URL = "https://data.binance.vision"
VISION_LIST_URL = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
COINPAPRIKA_URL = "https://api.coinpaprika.com/v1/tickers"

DEFAULT_INTERVALS = ["5m", "15m", "30m", "1h", "4h", "1d"]
INTERVAL_MS = {
    "1m": 60_000, "3m": 180_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "2h": 7_200_000, "4h": 14_400_000, "6h": 21_600_000,
    "8h": 28_800_000, "12h": 43_200_000, "1d": 86_400_000,
}

COLUMNS = [
    "datetime_utc", "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "trades", "taker_buy_volume", "taker_buy_quote_volume",
]

# Pegged / wrapped assets: they have a market cap but are not "coins" to chart.
EXCLUDED_COINS = {
    "usdt", "usdc", "usds", "dai", "fdusd", "usde", "usdd", "tusd", "pyusd", "usd1",
    "busd", "usdp", "gusd", "frax", "lusd", "susd", "usdx", "usdb", "usdg", "rlusd",
    "usd0", "susde", "bsc-usd", "eurc", "eurs", "wbtc", "weth", "steth", "wsteth",
    "weeth", "wbeth", "reth", "cbbtc", "cbeth", "lbtc", "solvbtc", "jitosol", "msol",
}

# Used only when CoinGecko cannot be reached (ordered by market cap, Oct 2026).
FALLBACK_COINS = ["BTC", "ETH", "BNB", "XRP", "SOL", "TRX", "ZEC", "HYPE", "DOGE", "LINK",
                  "ADA", "XLM", "BCH", "LTC", "AVAX"]

# Binance lists some low-priced coins as 1000x contracts (e.g. 1000PEPEUSDT).
SYMBOL_PREFIXES = ["", "1000", "1000000", "1M"]

KLINES_LIMIT = 1000           # weight 5 per request (>1000 costs 10)
WEIGHT_SOFT_LIMIT = 1200      # Binance allows 2400/min; stay at half of that

log = logging.getLogger("collector")


class RestrictedLocation(Exception):
    """fapi.binance.com answered HTTP 451 (region blocked)."""


class Http:
    """requests.Session wrapper with a minimum delay between calls and retries."""

    def __init__(self, min_interval, max_retries=8, name="http"):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "binance-futures-kline-collector/1.0"
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.name = name
        self._last = 0.0

    def _throttle(self):
        wait = self.min_interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def get(self, url, params=None, allow_404=False, timeout=60):
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            backoff = min(2 ** attempt, 120) + random.uniform(0, 1)
            try:
                r = self.session.get(url, params=params, timeout=timeout)
            except requests.RequestException as e:
                log.warning("[%s] %s (try %d/%d), retrying in %.0fs",
                            self.name, e, attempt, self.max_retries, backoff)
                time.sleep(backoff)
                continue

            if r.status_code == 200:
                self._respect_weight(r)
                return r
            if r.status_code == 404 and allow_404:
                return None
            if r.status_code == 451:
                raise RestrictedLocation(r.text[:200])
            if r.status_code in (418, 429):
                wait = int(r.headers.get("Retry-After") or 0) or max(60, backoff)
                log.warning("[%s] HTTP %d rate limited, sleeping %ds", self.name, r.status_code, wait)
                time.sleep(wait)
                continue
            if r.status_code >= 500 or r.status_code in (403, 408):
                log.warning("[%s] HTTP %d for %s (try %d/%d), retrying in %.0fs",
                            self.name, r.status_code, url, attempt, self.max_retries, backoff)
                time.sleep(backoff)
                continue
            r.raise_for_status()
        raise RuntimeError(f"[{self.name}] giving up on {url} after {self.max_retries} tries")

    @staticmethod
    def _respect_weight(r):
        used = r.headers.get("X-MBX-USED-WEIGHT-1M")
        if used and int(used) >= WEIGHT_SOFT_LIMIT:
            wait = 61 - datetime.now(timezone.utc).second
            log.info("API weight %s/min used, pausing %ds for the window to reset", used, wait)
            time.sleep(wait)


# ---------------------------------------------------------------------------
# Symbol selection
# ---------------------------------------------------------------------------

def fetch_market_cap_ranking(http):
    """Top 100 coins by market cap: CoinGecko, then CoinPaprika, then a static list."""
    try:
        r = http.get(COINGECKO_URL, params={
            "vs_currency": "usd", "order": "market_cap_desc", "per_page": 100, "page": 1,
        })
        return [{"coin": c["symbol"].upper(), "name": c["name"],
                 "market_cap_rank": c["market_cap_rank"], "market_cap_usd": c["market_cap"]}
                for c in r.json() if c.get("market_cap_rank")], "coingecko"
    except Exception as e:  # noqa: BLE001
        log.warning("CoinGecko unavailable (%s); trying CoinPaprika", e)
    try:
        r = http.get(COINPAPRIKA_URL, params={"limit": 100})
        return [{"coin": c["symbol"].upper(), "name": c["name"], "market_cap_rank": c["rank"],
                 "market_cap_usd": c["quotes"]["USD"]["market_cap"]}
                for c in sorted(r.json(), key=lambda c: c["rank"]) if c.get("rank")], "coinpaprika"
    except Exception as e:  # noqa: BLE001
        log.warning("CoinPaprika unavailable (%s); using built-in fallback list", e)
    return [{"coin": c, "name": c, "market_cap_rank": None, "market_cap_usd": None}
            for c in FALLBACK_COINS], "fallback"


def futures_symbols_from_api(api):
    info = api.get(f"{FAPI_URL}/fapi/v1/exchangeInfo").json()
    return {
        s["symbol"] for s in info["symbols"]
        if s.get("contractType") == "PERPETUAL" and s.get("quoteAsset") == "USDT"
        and s.get("status") == "TRADING"
    }


def is_listed_on_vision(vision, symbol):
    """True if data.binance.vision has a daily 1d kline for SYMBOL in the last 10 days."""
    prefix = f"data/futures/um/daily/klines/{symbol}/1d/"
    since = (datetime.now(timezone.utc).date() - timedelta(days=10)).isoformat()
    keys = list_vision_keys(vision, prefix, marker=f"{prefix}{symbol}-1d-{since}")
    return any(k.endswith(".zip") for k in keys)


def resolve_futures_symbol(coin, api_symbols, vision):
    for prefix in SYMBOL_PREFIXES:
        symbol = f"{prefix}{coin}USDT"
        if api_symbols is not None:
            if symbol in api_symbols:
                return symbol
        elif is_listed_on_vision(vision, symbol):
            return symbol
    return None


def select_top_symbols(top_n, api, vision, ranking_http, api_ok):
    api_symbols = None
    if api_ok:
        try:
            api_symbols = futures_symbols_from_api(api)
        except (RestrictedLocation, RuntimeError, requests.RequestException) as e:
            log.warning("exchangeInfo unavailable (%s); checking listings on data.binance.vision", e)

    ranking, source = fetch_market_cap_ranking(ranking_http)

    selected, seen = [], set()
    for entry in ranking:
        coin = entry["coin"]
        if coin.lower() in EXCLUDED_COINS or coin in seen or not re.fullmatch(r"[A-Z0-9]+", coin):
            continue
        seen.add(coin)
        symbol = resolve_futures_symbol(coin, api_symbols, vision)
        if not symbol:
            log.info("  #%s %s: no USDT-M perpetual on Binance, skipped", entry["market_cap_rank"], coin)
            continue
        log.info("  #%s %s -> %s", entry["market_cap_rank"], coin, symbol)
        selected.append({**entry, "symbol": symbol})
        if len(selected) == top_n:
            break
    return selected, source


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

class KlineFile:
    """Append-only gzip CSV for one symbol/interval, resumable after crashes."""

    def __init__(self, data_dir, symbol, interval):
        self.path = os.path.join(data_dir, symbol, f"{symbol}_{interval}.csv.gz")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.last_open_time = self._scan()

    def _scan(self):
        if not os.path.exists(self.path):
            return None
        last, good_rows = None, []
        try:
            with gzip.open(self.path, "rt", newline="") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) != len(COLUMNS) or not row[1].isdigit():
                        raise ValueError("truncated row")
                    good_rows.append(row)
                    last = int(row[1])
            return last
        except (EOFError, OSError, ValueError, IndexError, gzip.BadGzipFile) as e:
            # Interrupted write: keep every complete row, drop the broken tail.
            # The row read just before the error may itself be cut short, so drop it too;
            # it is downloaded again on resume.
            good_rows = good_rows[:-1]
            log.warning("%s is damaged (%s); rewriting %d good rows", self.path, e, len(good_rows))
            tmp = self.path + ".tmp"
            with gzip.open(tmp, "wt", newline="") as f:
                w = csv.writer(f)
                w.writerow(COLUMNS)
                w.writerows(good_rows)
            os.replace(tmp, self.path)
            return int(good_rows[-1][1]) if good_rows else None

    def append(self, rows):
        """rows: raw Binance kline rows (open_time first). Only newer rows are kept."""
        new = []
        last = self.last_open_time
        for k in rows:
            open_time = int(k[0])
            if last is not None and open_time <= last:
                continue
            dt = datetime.fromtimestamp(open_time / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            new.append([dt, open_time, k[1], k[2], k[3], k[4], k[5], int(k[6]), k[7], k[8], k[9], k[10]])
            last = open_time
        if not new:
            return 0
        is_new_file = not os.path.exists(self.path)
        with gzip.open(self.path, "at", newline="") as f:
            w = csv.writer(f)
            if is_new_file:
                w.writerow(COLUMNS)
            w.writerows(new)
        self.last_open_time = last
        return len(new)


# ---------------------------------------------------------------------------
# data.binance.vision
# ---------------------------------------------------------------------------

def list_vision_keys(vision, prefix, marker=""):
    keys = []
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    while True:
        r = vision.get(VISION_LIST_URL, params={"delimiter": "/", "prefix": prefix, "marker": marker})
        root = ET.fromstring(r.content)
        page = [c.find("s3:Key", ns).text for c in root.findall("s3:Contents", ns)]
        keys.extend(page)
        if root.findtext("s3:IsTruncated", namespaces=ns) != "true" or not page:
            return keys
        marker = page[-1]


def read_vision_zip(vision, key, verify_checksum):
    r = vision.get(f"{VISION_URL}/{key}", allow_404=True)
    if r is None:
        return None
    if verify_checksum:
        c = vision.get(f"{VISION_URL}/{key}.CHECKSUM", allow_404=True)
        if c is not None:
            expected = c.text.split()[0].lower()
            actual = hashlib.sha256(r.content).hexdigest()
            if expected != actual:
                raise RuntimeError(f"checksum mismatch for {key}")
    rows = []
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:  # zipfile also verifies CRC32
        for name in z.namelist():
            with z.open(name) as f:
                for row in csv.reader(io.TextIOWrapper(f, encoding="utf-8")):
                    if not row or not row[0].isdigit():  # header line in newer files
                        continue
                    open_time, close_time = int(row[0]), int(row[6])
                    if open_time > 10 ** 14:  # microsecond timestamps -> ms
                        open_time, close_time = open_time // 1000, close_time // 1000
                    rows.append([open_time, *row[1:6], close_time, *row[7:11]])
    rows.sort(key=lambda k: k[0])
    return rows


def fill_month_gaps(vision, symbol, interval, ym, rows, resume_after, verify_checksum):
    """Some monthly dumps are cut short (e.g. 2022-02/03 for several coins) while the
    daily dumps are complete, so re-fetch any under-filled day from the daily files."""
    if not rows:
        return rows
    step = INTERVAL_MS[interval]
    per_day = max(1, 86_400_000 // step)
    counts = {}
    for k in rows:
        d = datetime.fromtimestamp(k[0] / 1000, timezone.utc).date()
        counts[d] = counts.get(d, 0) + 1
    start = resume_after + step if resume_after is not None else rows[0][0]
    day = max(datetime.fromtimestamp(start / 1000, timezone.utc).date(), date.fromisoformat(f"{ym}-01"))
    merged = {k[0]: k for k in rows}
    while day.strftime("%Y-%m") == ym:
        if counts.get(day, 0) < per_day:
            key = (f"data/futures/um/daily/klines/{symbol}/{interval}/"
                   f"{symbol}-{interval}-{day.isoformat()}.zip")
            daily = read_vision_zip(vision, key, verify_checksum)
            if daily and len(daily) > counts.get(day, 0):
                log.info("%s %s: monthly dump short on %s (%d/%d rows), filled from daily dump",
                         symbol, interval, day, counts.get(day, 0), len(daily))
                merged.update((k[0], k) for k in daily)
        day += timedelta(days=1)
    return [merged[t] for t in sorted(merged)]


def month_end_ms(ym):
    y, m = map(int, ym.split("-"))
    nxt = date(y + (m == 12), m % 12 + 1, 1)
    return int(datetime(nxt.year, nxt.month, 1, tzinfo=timezone.utc).timestamp() * 1000) - 1


def day_end_ms(d):
    return int(datetime.fromisoformat(d).replace(tzinfo=timezone.utc).timestamp() * 1000) + 86_400_000 - 1


def first_vision_month_ms(vision, symbol, interval):
    """Open time of the first monthly dump, or None if there is none."""
    prefix = f"data/futures/um/monthly/klines/{symbol}/{interval}/"
    months = sorted(re.search(r"(\d{4}-\d{2})\.zip$", k).group(1)
                    for k in list_vision_keys(vision, prefix) if k.endswith(".zip"))
    if not months:
        return None
    y, m = map(int, months[0].split("-"))
    return int(datetime(y, m, 1, tzinfo=timezone.utc).timestamp() * 1000)


def collect_from_vision(vision, store, symbol, interval, verify_checksum):
    base = f"data/futures/um/{{}}/klines/{symbol}/{interval}/"
    monthly = sorted(
        k for k in list_vision_keys(vision, base.format("monthly")) if k.endswith(".zip")
    )
    months = {re.search(r"(\d{4}-\d{2})\.zip$", k).group(1): k for k in monthly}
    last_month = max(months) if months else ""

    daily_prefix = base.format("daily")
    marker = f"{daily_prefix}{symbol}-{interval}-{last_month}-99" if last_month else ""
    daily = sorted(k for k in list_vision_keys(vision, daily_prefix, marker) if k.endswith(".zip"))
    days = {re.search(r"(\d{4}-\d{2}-\d{2})\.zip$", k).group(1): k for k in daily}

    jobs = [(month_end_ms(m), m, k) for m, k in sorted(months.items())]
    jobs += [(day_end_ms(d), None, k) for d, k in sorted(days.items()) if d[:7] > last_month]
    last = store.last_open_time
    todo = [(ym, k) for end, ym, k in jobs if last is None or end > last]
    log.info("%s %s: %d monthly + %d daily files on data.binance.vision, %d to download",
             symbol, interval, len(months), len([d for d in days if d[:7] > last_month]), len(todo))

    added = 0
    for i, (ym, key) in enumerate(todo, 1):
        rows = read_vision_zip(vision, key, verify_checksum)
        if ym:
            rows = fill_month_gaps(vision, symbol, interval, ym, rows, store.last_open_time,
                                   verify_checksum)
        if rows:
            added += store.append(rows)
        if i % 12 == 0 or i == len(todo):
            log.info("%s %s: %d/%d files, +%d rows (up to %s)", symbol, interval, i, len(todo),
                     added, fmt_ms(store.last_open_time))
    return added


# ---------------------------------------------------------------------------
# fapi.binance.com
# ---------------------------------------------------------------------------

def collect_from_api(api, store, symbol, interval, end_ms=None):
    """Fetch closed candles after the last stored one (from listing if empty), up to end_ms."""
    step = INTERVAL_MS[interval]
    start = store.last_open_time + step if store.last_open_time is not None else 0
    added = requests_made = 0
    while True:
        now_ms = int(time.time() * 1000)
        limit_ms = now_ms if end_ms is None else min(end_ms, now_ms)
        if start > limit_ms:
            break
        r = api.get(f"{FAPI_URL}/fapi/v1/klines", params={
            "symbol": symbol, "interval": interval, "startTime": start, "limit": KLINES_LIMIT,
        })
        requests_made += 1
        rows = r.json()
        # Drop the still-open candle and anything at/after end_ms (left to the next source).
        closed = [k for k in rows if int(k[6]) < now_ms and (end_ms is None or int(k[0]) < end_ms)]
        added += store.append(closed)
        if requests_made % 25 == 0:
            log.info("%s %s: API +%d rows (up to %s)", symbol, interval, added,
                     fmt_ms(store.last_open_time))
        if len(rows) < KLINES_LIMIT or len(closed) < len(rows):
            break
        start = int(rows[-1][0]) + step
    return added


def fmt_ms(ms):
    if ms is None:
        return "-"
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def api_reachable(api):
    try:
        api.get(f"{FAPI_URL}/fapi/v1/ping")
        return True
    except RestrictedLocation:
        log.warning("fapi.binance.com returned HTTP 451 (restricted location) - "
                    "using data.binance.vision only")
    except (RuntimeError, requests.RequestException) as e:
        log.warning("fapi.binance.com unreachable (%s) - using data.binance.vision only", e)
    return False


# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--top", type=int, default=10, help="number of coins by market cap (default 10)")
    p.add_argument("--symbols", help="comma separated futures symbols, overrides --top (e.g. BTCUSDT,ETHUSDT)")
    p.add_argument("--intervals", default=",".join(DEFAULT_INTERVALS),
                   help="comma separated intervals (default %(default)s)")
    p.add_argument("--source", choices=["auto", "vision", "api"], default="auto",
                   help="auto = bulk history from data.binance.vision + API for the latest candles")
    p.add_argument("--data-dir", default="data")
    p.add_argument("--api-delay", type=float, default=0.5, help="seconds between fapi requests")
    p.add_argument("--vision-delay", type=float, default=0.25,
                   help="seconds between data.binance.vision requests")
    p.add_argument("--verify-checksum", action="store_true",
                   help="also download .CHECKSUM files and verify SHA256 (doubles requests)")
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.data_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(os.path.join(args.data_dir, "collector.log"))],
    )
    intervals = [i.strip() for i in args.intervals.split(",") if i.strip()]
    for i in intervals:
        if i not in INTERVAL_MS:
            sys.exit(f"unsupported interval: {i}")

    api = Http(args.api_delay, name="fapi")
    vision = Http(args.vision_delay, name="vision")
    ranking_http = Http(3.0, max_retries=3, name="market-cap")

    api_ok = args.source != "vision" and api_reachable(api)
    if args.source == "api" and not api_ok:
        sys.exit("fapi.binance.com is not reachable from here; run with --source vision")

    if args.symbols:
        selection = [{"symbol": s.strip().upper()} for s in args.symbols.split(",") if s.strip()]
        source = "manual"
    else:
        log.info("Selecting top %d coins by market cap with Binance USDT-M perpetuals", args.top)
        selection, source = select_top_symbols(args.top, api, vision, ranking_http, api_ok)
    with open(os.path.join(args.data_dir, "symbols.json"), "w") as f:
        json.dump({"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "ranking_source": source, "intervals": intervals, "symbols": selection},
                  f, indent=2, ensure_ascii=False)
    log.info("Symbols: %s", ", ".join(s["symbol"] for s in selection))

    failures = []
    for entry in selection:
        symbol = entry["symbol"]
        for interval in intervals:
            try:
                store = KlineFile(args.data_dir, symbol, interval)
                if args.source == "auto" and api_ok and store.last_open_time is None:
                    # Bulk dumps start in 2020-01; older candles (e.g. BTC since 2019-09) exist
                    # only on the API, so backfill those first.
                    first_month = first_vision_month_ms(vision, symbol, interval)
                    if first_month:
                        collect_from_api(api, store, symbol, interval, end_ms=first_month)
                if args.source in ("auto", "vision"):
                    collect_from_vision(vision, store, symbol, interval, args.verify_checksum)
                if api_ok:
                    collect_from_api(api, store, symbol, interval)
                log.info("%s %s done: last candle %s -> %s", symbol, interval,
                         fmt_ms(store.last_open_time), store.path)
            except Exception as e:  # noqa: BLE001 - keep going with the other series
                log.exception("%s %s failed: %s", symbol, interval, e)
                failures.append(f"{symbol} {interval}")

    if failures:
        log.error("Finished with failures (re-run to resume): %s", ", ".join(failures))
        sys.exit(1)
    log.info("All done.")


if __name__ == "__main__":
    main()
