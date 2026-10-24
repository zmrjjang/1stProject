"""New-listing short basket (see NEW_LISTING_SHORT.md).

Rule, tested on every crypto USDT-M perpetual listed 2024-01 .. 2026-07 (research_lowcap/):
  * 24 hours after a new perpetual is listed, if the first day's close is at or below the
    listing price (the first 1h candle's open), go short at the next candle's open
  * exit at +50% (stop), -50% (take profit), after 30 days, or once the short has paid more
    than 10% of the notional in funding
  * one small fixed fraction of the account per trade (default 2%, leverage 1x)

simulate() is used by both the study and the live/paper runner, so they cannot drift apart.
"""

import json
import os
import time

import numpy as np
import requests

H = 3_600_000
RULE = {"entry_after_h": 24, "stop": 0.50, "take": 0.50, "hold_h": 720, "funding_cap": 0.10, "cost": 0.002,
        "max_late_h": 24}

# USDT-M perpetuals on stocks, ETFs, commodities and pre-IPO companies are not crypto listings.
TRADFI = set("""SPY QQQ IWM EWJ EWT EWZ EWY XBI XLE SMH URNM TMF TBT TZA UVXY BITO NATGAS CL BZ COPPER ANTHROPIC OPENAI
MINIMAX ZHIPU SAMSUNG SKHYNIX SKHY HYUNDAI TENCENT SONY POPMART NVDA NVO MSTR TSM AVGO JPM HD DIS V NOK BRKB TXN DRAM
CHIP STRC SPCX GEV XAU XAG XAUT XPD XPT AAPL TSLA COIN AMZN GOOGL META MSFT NFLX AMD INTC MU ORCL PLTR HOOD CRCL""".split())


def signal(o, c):
    """o, c: 1h candles from the listing on. True = short, False = skip, None = first day not closed yet."""
    n = RULE["entry_after_h"]
    if c.size < n:
        return None
    return bool(c[n - 1] <= o[0])


def simulate(t, o, h, l, c, entry_i, entry_px, funding, rule=RULE):
    """Walk the CLOSED candles from entry_i on. funding: [(settlement_ms, rate)], a short receives +rate.
    Returns {"open": True, ...} while the trade is alive, else the exit."""
    fund = {}
    for ft, fr in funding:
        fund[(int(ft) // H) * H] = fund.get((int(ft) // H) * H, 0.0) + float(fr)
    e, facc = entry_px, 0.0
    stop, take = e * (1 + rule["stop"]), e * (1 - rule["take"])

    def done(px, j, why):
        return {"open": False, "exit_px": float(px), "exit_ms": int(t[j]) + H, "reason": why, "funding": facc,
                "ret": max(-1.0, 1 - px / e - 2 * rule["cost"] + facc)}

    for j in range(entry_i, c.size):
        if h[j] >= stop:
            return done(max(o[j], stop) if j > entry_i else stop, j, "stop")
        if l[j] <= take:
            return done(min(o[j], take) if j > entry_i else take, j, "take")
        facc += fund.get(int(t[j]), 0.0)
        if rule["funding_cap"] and facc <= -rule["funding_cap"]:
            return done(c[j], j, "funding")
        if j - entry_i + 1 >= rule["hold_h"]:
            return done(c[j], j, "time")
    last = c[-1] if c.size else e
    return {"open": True, "funding": facc, "last_px": float(last),
            "ret": 1 - last / e - 2 * rule["cost"] + facc}


# ---------------------------------------------------------------------------
class BinanceAPI:
    BASE = "https://fapi.binance.com"

    def __init__(self, delay=0.2):
        self.s = requests.Session()
        self.delay = delay

    def _get(self, path, **params):
        for attempt in range(6):
            try:
                r = self.s.get(self.BASE + path, params=params, timeout=20)
                if r.status_code == 451:
                    raise SystemExit("fapi.binance.com이 이 지역에서 차단되어 있습니다 (HTTP 451). "
                                     "바이낸스 접속이 되는 PC에서 실행하세요.")
                if r.status_code in (418, 429):
                    time.sleep(int(r.headers.get("Retry-After", 60)))
                    continue
                r.raise_for_status()
                time.sleep(self.delay)
                return r.json()
            except requests.RequestException:
                time.sleep(2 ** attempt)
        raise RuntimeError(f"failed: {path} {params}")

    def new_listings(self, now_ms, days):
        """[(symbol, onboard_ms)] crypto USDT perpetuals listed within `days`."""
        out = []
        for s in self._get("/fapi/v1/exchangeInfo")["symbols"]:
            if (s.get("contractType") != "PERPETUAL" or s.get("quoteAsset") != "USDT" or s.get("status") != "TRADING"
                    or s.get("underlyingType", "COIN") != "COIN" or s["baseAsset"] in TRADFI):
                continue
            ob = int(s.get("onboardDate", 0))
            if now_ms - days * 86_400_000 <= ob <= now_ms:
                out.append((s["symbol"], ob))
        return sorted(out, key=lambda x: x[1])

    def candles(self, symbol, start_ms, now_ms):
        """1h candles from start_ms: (closed arrays t,o,h,l,c, open price of the candle in progress or None)."""
        rows, start = [], start_ms
        while True:
            page = self._get("/fapi/v1/klines", symbol=symbol, interval="1h", startTime=start, limit=1500)
            rows += page
            if len(page) < 1500:
                break
            start = int(page[-1][0]) + H
        closed = [k for k in rows if int(k[6]) < now_ms]
        live = [k for k in rows if int(k[0]) <= now_ms <= int(k[6])]
        a = np.array([[float(k[i]) for i in range(5)] for k in closed]).reshape(-1, 5)
        return (a[:, 0].astype(np.int64), a[:, 1], a[:, 2], a[:, 3], a[:, 4],
                float(live[0][1]) if live else None)

    def funding(self, symbol, start_ms):
        return [(int(x["fundingTime"]), float(x["fundingRate"]))
                for x in self._get("/fapi/v1/fundingRate", symbol=symbol, startTime=start_ms, limit=1000)]


# ---------------------------------------------------------------------------
class Radar:
    """Scans new listings, keeps a paper account in paper_dir/state.json."""

    def __init__(self, api, paper_dir="paper_listing", capital=1000.0, size=0.02, persist=True, notify=False):
        self.api, self.dir, self.size, self.persist, self.notify = api, paper_dir, size, persist, notify
        self.path = os.path.join(paper_dir, "state.json")
        self.state = {"capital": capital, "equity": capital, "positions": {}, "closed": [], "seen": {}}
        if persist and os.path.exists(self.path):
            with open(self.path) as f:
                self.state = json.load(f)

    def save(self):
        if not self.persist:
            return
        os.makedirs(self.dir, exist_ok=True)
        with open(self.path + ".tmp", "w") as f:
            json.dump(self.state, f, indent=1, ensure_ascii=False)
        os.replace(self.path + ".tmp", self.path)

    def _alert(self, title, lines):
        if not self.notify:
            return
        from lab.notify import notify
        notify(title, "\n".join(lines), "\n".join(lines))

    def run_once(self, now_ms=None):
        now_ms = now_ms or int(time.time() * 1000)
        st, R = self.state, RULE
        rows, events = [], []
        listings = self.api.new_listings(now_ms, days=R["hold_h"] / 24 + 10)
        known = {sym for sym, _ in listings}
        # positions whose coin left the list (e.g. delisted) are still managed until they close
        listings += [(sym, p["onboard_ms"]) for sym, p in st["positions"].items() if sym not in known]
        for sym, ob in listings:
            t, o, h, l, c, live_open = self.api.candles(sym, ob, now_ms)
            if not t.size:
                rows.append((sym, ob, "⏳", "첫 봉 대기", None))
                continue
            sig = signal(o, c)
            day1 = c[R["entry_after_h"] - 1] / o[0] - 1 if sig is not None else c[-1] / o[0] - 1
            pos = st["positions"].get(sym)
            if pos:
                i = int(np.searchsorted(t, pos["entry_ms"]))
                res = simulate(t, o, h, l, c, i, pos["entry_px"], self.api.funding(sym, pos["entry_ms"]))
                if res["open"]:
                    rows.append((sym, ob, "🔻", f"보유 중 {res['ret'] * 100:+.1f}% (진입 {pos['entry_px']:.6g}, "
                                 f"손절 {pos['entry_px'] * (1 + R['stop']):.6g}, 익절 {pos['entry_px'] * (1 - R['take']):.6g})", day1))
                else:
                    pnl = pos["notional"] * res["ret"]
                    st["equity"] += pnl
                    st["closed"].append({**pos, **res, "symbol": sym, "pnl": pnl})
                    del st["positions"][sym]
                    st["seen"][sym] = "closed"
                    msg = f"{sym} 숏 청산 ({res['reason']}): {res['ret'] * 100:+.1f}%, {pnl:+.2f} USDT"
                    events.append(msg)
                    rows.append((sym, ob, "✅", msg, day1))
                continue
            if st["seen"].get(sym) in ("closed", "skip", "missed"):
                rows.append((sym, ob, "·", {"closed": "거래 종료", "skip": "제외 (첫날 상승)",
                                            "missed": "신호를 늦게 발견해 건너뜀"}[st["seen"][sym]], day1))
                continue
            if sig is None:
                left = (ob + R["entry_after_h"] * H - now_ms) / H
                rows.append((sym, ob, "⏳", f"첫날 마감까지 {max(0.0, left):.1f}시간", day1))
                continue
            if not sig:
                st["seen"][sym] = "skip"
                rows.append((sym, ob, "✖", "제외: 첫날 상승 마감 (숏 스퀴즈 위험)", day1))
                continue
            sig_ms = int(t[R["entry_after_h"] - 1]) + H
            late = (now_ms - sig_ms) / H
            if late > R["max_late_h"]:
                st["seen"][sym] = "missed"
                rows.append((sym, ob, "·", f"신호 후 {late:.0f}시간 지나 건너뜀", day1))
                continue
            entry_px = live_open if live_open else c[-1]
            entry_ms = (now_ms // H) * H
            notional = st["equity"] * self.size
            st["positions"][sym] = {"entry_ms": entry_ms, "entry_px": entry_px, "notional": notional, "onboard_ms": ob,
                                    "listing_open": float(o[0]), "day1_close": float(c[R["entry_after_h"] - 1])}
            st["seen"][sym] = "open"
            msg = (f"{sym} 숏 진입 {entry_px:.6g} (상장가 {o[0]:.6g} → 첫날 {day1 * 100:+.1f}%), "
                   f"손절 {entry_px * (1 + R['stop']):.6g} / 익절 {entry_px * (1 - R['take']):.6g} / "
                   f"최대 30일, 금액 {notional:.2f} USDT")
            events.append(msg)
            rows.append((sym, ob, "🎯", msg, day1))
        self.save()
        if events:
            self._alert(f"신규상장 숏: {len(events)}건", events)
        return rows, events

    def summary(self):
        st = self.state
        cl = st["closed"]
        wins = sum(x["ret"] > 0 for x in cl)
        return (f"자산 {st['equity']:.2f} USDT (시작 {st['capital']:.2f}, {st['equity'] / st['capital'] * 100 - 100:+.1f}%) | "
                f"보유 {len(st['positions'])}개 | 종료 {len(cl)}건, 승률 {wins / len(cl) * 100 if cl else 0:.0f}%")
