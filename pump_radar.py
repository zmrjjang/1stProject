#!/usr/bin/env python3
"""Pump radar: ranks every Binance USDT-M perpetual by how likely a big upward move is in the next
3 days, using the model in strategies/pump_model.npz (see PUMP_RADAR.md). These are LONG candidates.

Tested long plan (out of sample 2025-07 .. 2026-10, top 10 at every 4h snapshot): buy, take profit
at +30%, stop at -40%, close after 7 days at the latest -> +1.4% per trade vs -0.4% for random coins.

    python pump_radar.py                 # top 20 right now
    python pump_radar.py --top 40
    python pump_radar.py --loop --notify # every 4 hours, push the top list via ntfy/Telegram/Discord

Uses fapi.binance.com, or www.binance.com where fapi is blocked (HTTP 451). Signals only, no orders.
Coins with a scheduled delisting (deliveryDate set) are left out.
"""

import argparse
import os
import time
from datetime import datetime, timezone

import numpy as np
import requests

from strategies.pump_features import FEATS, H, HISTORY_BARS, Model, features, non_crypto

LONG_PLAN = {"take": 0.30, "stop": 0.40, "days": 7}
BASE = "https://fapi.binance.com"
MIRROR = "https://www.binance.com"  # same API, reachable where fapi.binance.com answers 451
NO_DELIVERY = 4_000_000_000_000  # a perpetual's deliveryDate is ~2100 unless a delisting is scheduled
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "strategies", "pump_model.npz")


class Api:
    def __init__(self):
        self.s = requests.Session()
        self.base = BASE

    def get(self, path, **params):
        for attempt in range(6):
            try:
                r = self.s.get(self.base + path, params=params, timeout=20)
                if r.status_code == 451:
                    if self.base == MIRROR:
                        raise SystemExit("바이낸스 선물 API가 이 지역에서 차단되어 있습니다 (HTTP 451).")
                    self.base = MIRROR
                    continue
                if r.status_code in (418, 429):
                    time.sleep(int(r.headers.get("Retry-After", 60)))
                    continue
                r.raise_for_status()
                if int(r.headers.get("X-MBX-USED-WEIGHT-1M", 0)) > 1800:  # stay well below 2400/min
                    time.sleep(61 - time.time() % 60)
                return r.json()
            except requests.RequestException:
                time.sleep(2 ** attempt)
        raise RuntimeError(f"failed: {path} {params}")

    def series(self, path, symbol, bars, now_ms):
        """The last `bars` closed 1h candles (pages of 1000, weight 5 each)."""
        rows, end = [], (now_ms // H) * H - 1
        while len(rows) < bars:
            page = self.get(path, symbol=symbol, interval="1h", endTime=end, limit=1000)
            if not page:
                break
            rows = page + rows
            end = int(page[0][0]) - 1
            if len(page) < 1000:
                break
        return [k for k in rows if int(k[6]) < now_ms][-bars:]


def scan(api, min_volume):
    now = int(time.time() * 1000)
    info = api.get("/fapi/v1/exchangeInfo")["symbols"]
    vol = {x["symbol"]: float(x["quoteVolume"]) for x in api.get("/fapi/v1/ticker/24hr")}
    perps = [s for s in info
             if s.get("contractType") == "PERPETUAL" and s.get("quoteAsset") == "USDT" and s.get("status") == "TRADING"
             and s.get("underlyingType", "COIN") == "COIN" and not non_crypto(s["symbol"])]
    # a scheduled delisting sets deliveryDate to the settlement time: those coins are not candidates
    delisting = sorted(s["symbol"] for s in perps if int(s.get("deliveryDate", NO_DELIVERY)) < NO_DELIVERY)
    if delisting:
        print("상장폐지(정산) 예정이라 제외:", ", ".join(delisting))
    syms = [(s["symbol"], int(s.get("onboardDate", 0))) for s in perps
            if s["symbol"] not in delisting and vol.get(s["symbol"], 0) >= min_volume / 3]
    btc = api.series("/fapi/v1/klines", "BTCUSDT", HISTORY_BARS, now)
    bt, bc = np.array([int(k[0]) for k in btc]), np.array([float(k[4]) for k in btc])
    out = []
    for n, (sym, onboard) in enumerate(syms, 1):
        k = api.series("/fapi/v1/klines", sym, HISTORY_BARS, now)
        if len(k) < 200:
            continue
        a = np.array([[float(x[i]) for i in (0, 2, 3, 4, 7, 10)] for x in k])
        t = a[:, 0].astype(np.int64)
        prem_rows = api.series("/fapi/v1/premiumIndexKlines", sym, 800, now)
        pm = {int(x[0]): float(x[4]) for x in prem_rows}
        prem = np.array([pm.get(x, np.nan) for x in t])
        X = features(t, a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5], prem, onboard, bt, bc)
        x = X[-1]
        if not np.isfinite(x[FEATS.index("lqv")]) or 10 ** x[FEATS.index("lqv")] < min_volume:
            continue
        recent = prem[-48:]
        crash = float(np.nanmin(np.diff(recent))) if np.isfinite(recent).sum() > 2 else 0.0
        out.append((sym, x, float(a[-1, 3]), int(t[-1]) + H, crash))
        if n % 50 == 0:
            print(f"  {n}/{len(syms)} 확인", flush=True)
    return out


def why(x, prem_crash=0.0):
    f = dict(zip(FEATS, x))
    tags = []
    if prem_crash <= -0.03:
        # futures suddenly far below spot: typical right after a delisting announcement (e.g. PTB, 2026-10)
        tags.append(f"⚠ 48시간 내 프리미엄 급변 {prem_crash * 100:.0f}%p (공지·급변동 확인)")
    if f["r7d"] > 0.3:
        tags.append(f"7일 {f['r7d'] * 100:+.0f}% 상승 추세")
    if f["r1d"] < -0.2:
        tags.append(f"하루 {f['r1d'] * 100:+.0f}% 급락")
    if f["prem1"] < -0.002:
        tags.append(f"숏 과밀 → 스퀴즈 연료 (프리미엄 {f['prem1'] * 100:+.2f}%)")
    if f["qv_r1"] > 3:
        tags.append(f"거래량 {f['qv_r1']:.1f}배")
    if f["dd90"] < -0.6:
        tags.append(f"90일 고점 대비 {f['dd90'] * 100:.0f}%")
    if f["pumps90"] >= 3:
        tags.append(f"최근 90일 급등 {f['pumps90']:.0f}회")
    if f["age"] < 120:
        tags.append(f"상장 {f['age']:.0f}일")
    return ", ".join(tags) or "-"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--min-volume", type=float, default=1e6, help="minimum 30-day average daily volume in USDT")
    p.add_argument("--loop", action="store_true", help="repeat every --every hours")
    p.add_argument("--every", type=int, default=4, help="hours between scans with --loop (default 4, as tested)")
    p.add_argument("--notify", action="store_true", help="push the top list via ntfy/Telegram/Discord env vars")
    args = p.parse_args()
    model, api = Model(MODEL), Api()
    while True:
        print(f"\n바이낸스 선물 스캔 중... ({datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC)")
        rows = scan(api, args.min_volume)
        score, h50, h30 = model.score(np.vstack([r[1] for r in rows]))
        order = np.argsort(-score)[:args.top]
        L = LONG_PLAN
        print(f"\n===== 롱 후보 상위 {len(order)} / {len(rows)}개 (3일 안에 +50% / +30% 실측 비율) =====")
        print(f"검증된 롱 방식: 익절 +{L['take']:.0%}, 손절 -{L['stop']:.0%}, 최대 {L['days']}일 보유, 종목당 소액")
        lines = []
        for rank, i in enumerate(order, 1):
            sym, x, price = rows[i][0], rows[i][1], rows[i][2]
            line = (f"{rank:2d}. {sym:14s} 점수 {score[i]:.2f}  +50% {h50[i]:.0%} / +30% {h30[i]:.0%}  "
                    f"가격 {price:.6g} → 익절 {price * (1 + L['take']):.6g} / 손절 {price * (1 - L['stop']):.6g}  {why(x, rows[i][4])}")
            print(line)
            lines.append(line)
        print("\n참고: 아무 코인이나 3일 안에 +50% 오를 확률은 약 2%입니다. 상위 후보는 3일 안에 −30% 급락할 확률도 12~17%입니다.")
        print("익절 없이 들고 있으면 평균 손익이 0 근처로 떨어집니다 (펌핑 후 되돌림). 손절을 −15%처럼 짧게 두면 흔들기에 털려 손해입니다.")
        if args.notify:
            from lab.notify import notify
            notify(f"롱 후보 상위 {min(10, len(lines))}", "\n".join(lines[:10]), "\n".join(lines))
        if not args.loop:
            break
        step = 3600 * args.every
        time.sleep(step - time.time() % step + 120)


if __name__ == "__main__":
    main()
