#!/usr/bin/env python3
"""Collect futures positioning data from data.binance.vision (public, no key):

  data/<SYMBOL>/<SYMBOL>_funding.csv.gz   funding rate history (every 8h, sometimes 4h)
      time, funding_rate
  data/<SYMBOL>/<SYMBOL>_metrics.csv.gz   open interest and long/short ratios, 30-minute snapshots
      time, open_interest, open_interest_value, top_account_ratio, top_position_ratio,
      global_account_ratio, taker_ratio
      (the last 5-minute snapshot inside each 30-minute window; `time` is that snapshot's time)

Symbols come from data/symbols.json. Re-running only downloads days that are missing.
"""

import argparse
import csv
import gzip
import io
import logging
import os
import re
import sys
import threading
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from binance_futures_collector import VISION_URL, Http, list_vision_keys

log = logging.getLogger("derivatives")
METRIC_COLS = ["time", "open_interest", "open_interest_value", "top_account_ratio",
               "top_position_ratio", "global_account_ratio", "taker_ratio"]
_local = threading.local()


def http(delay):
    if not hasattr(_local, "h"):
        _local.h = Http(delay, name="vision")
    return _local.h


def read_zip_rows(h, key):
    r = h.get(f"{VISION_URL}/{key}", allow_404=True)
    if r is None:
        return []
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        with z.open(z.namelist()[0]) as f:
            return list(csv.reader(io.TextIOWrapper(f, encoding="utf-8")))


def to_ms(text):
    if text.isdigit():
        return int(text)
    return int(datetime.strptime(text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp() * 1000)


def write_gz(path, header, rows):
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    os.replace(tmp, path)


def read_gz(path):
    if not os.path.exists(path):
        return []
    with gzip.open(path, "rt", newline="") as f:
        rows = list(csv.reader(f))
    return rows[1:]


def collect_funding(symbol, data_dir, delay):
    h = http(delay)
    keys = sorted(k for k in list_vision_keys(h, f"data/futures/um/monthly/fundingRate/{symbol}/")
                  if k.endswith(".zip"))
    rates = {}
    for key in keys:
        for row in read_zip_rows(h, key):
            if row and row[0].isdigit():
                t = int(row[0]) // 1000 * 1000  # some calc_times carry +1 ms
                rates[t] = row[2]
    path = os.path.join(data_dir, symbol, f"{symbol}_funding.csv.gz")
    write_gz(path, ["time", "funding_rate"], sorted(rates.items()))
    log.info("%s funding: %d rates (%d months)", symbol, len(rates), len(keys))


def collect_metrics(symbol, data_dir, delay, workers):
    path = os.path.join(data_dir, symbol, f"{symbol}_metrics.csv.gz")
    existing = read_gz(path)
    last = int(existing[-1][0]) if existing else 0
    prefix = f"data/futures/um/daily/metrics/{symbol}/"
    keys = sorted(k for k in list_vision_keys(http(delay), prefix) if k.endswith(".zip"))
    todo = []
    for k in keys:
        day = re.search(r"(\d{4}-\d{2}-\d{2})\.zip$", k).group(1)
        end = to_ms(day + " 23:59:59")
        if end > last:
            todo.append(k)
    log.info("%s metrics: %d daily files, %d to download", symbol, len(keys), len(todo))

    def fetch(key):
        out = []
        for row in read_zip_rows(http(delay), key):
            if len(row) >= 8 and row[0][:2] == "20":
                try:
                    out.append([to_ms(row[0])] + [float(x) if x else float("nan") for x in row[2:8]])
                except ValueError:
                    continue
        return out

    snaps = {}
    with ThreadPoolExecutor(workers) as pool:
        for i, rows in enumerate(pool.map(fetch, todo), 1):
            for r in rows:
                snaps[r[0]] = r
            if i % 200 == 0:
                log.info("%s metrics: %d/%d files", symbol, i, len(todo))
    # keep the last snapshot in each 30-minute window
    buckets = {}
    for t in sorted(snaps):
        if t > last:
            buckets[t // 1_800_000] = snaps[t]
    new = [[int(r[0])] + [repr(x) for x in r[1:]] for _, r in sorted(buckets.items())]
    write_gz(path, METRIC_COLS, existing + new)
    log.info("%s metrics: +%d rows (total %d)", symbol, len(new), len(existing) + len(new))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", default="data")
    p.add_argument("--delay", type=float, default=0.25, help="seconds between requests per worker")
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", stream=sys.stdout)
    import json
    with open(os.path.join(args.data_dir, "symbols.json")) as f:
        syms = [s["symbol"] for s in json.load(f)["symbols"]]
    for s in syms:
        collect_funding(s, args.data_dir, args.delay)
        collect_metrics(s, args.data_dir, args.delay, args.workers)
    log.info("done")


if __name__ == "__main__":
    main()
