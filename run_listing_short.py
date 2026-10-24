#!/usr/bin/env python3
"""New-listing short radar and paper trader (see NEW_LISTING_SHORT.md).

    python run_listing_short.py scan                    # new listings now: waiting / short signal / skipped
    python run_listing_short.py paper --loop --notify   # paper trade every signal, re-check after each 1h close
    python run_listing_short.py report                  # paper account and closed trades

Needs access to fapi.binance.com (run it on your own PC). Paper only: no orders are sent.
"""

import argparse
import time
from datetime import datetime, timezone

from strategies.listing_short import RULE, BinanceAPI, Radar


def show(rows, radar):
    print(f"\n===== {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC | 최근 {RULE['hold_h'] // 24 + 10}일 신규 상장 {len(rows)}개 =====")
    for sym, ob, icon, text, day1 in rows:
        age = (time.time() * 1000 - ob) / 86_400_000
        d1 = f"{day1 * 100:+6.1f}%" if day1 is not None else "   -   "
        print(f"{icon} {sym:16s} 상장 {age:4.1f}일 전  첫날 {d1}  {text}")
    print(radar.summary())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["scan", "paper", "report"])
    p.add_argument("--loop", action="store_true", help="repeat a minute after every 1h candle close")
    p.add_argument("--notify", action="store_true", help="push entries/exits via ntfy/Telegram/Discord env vars")
    p.add_argument("--capital", type=float, default=1000.0, help="paper account size in USDT")
    p.add_argument("--size", type=float, default=0.02, help="fraction of the account per short (default 2%%)")
    p.add_argument("--paper-dir", default="paper_listing")
    args = p.parse_args()

    radar = Radar(BinanceAPI(), args.paper_dir, args.capital, args.size, persist=args.mode != "scan",
                  notify=args.notify)
    if args.mode == "report":
        st = radar.state
        print(radar.summary())
        for x in st["closed"][-30:]:
            print(f"  {x['symbol']:16s} {x['reason']:8s} {x['ret'] * 100:+6.1f}%  {x['pnl']:+8.2f} USDT")
        for sym, pos in st["positions"].items():
            print(f"  보유 {sym:16s} 진입 {pos['entry_px']:.6g}  금액 {pos['notional']:.2f}")
        return
    while True:
        rows, _ = radar.run_once()
        show(rows, radar)
        if not args.loop:
            break
        wait = 3600 - time.time() % 3600 + 60
        print(f"다음 확인까지 {wait / 60:.0f}분 (Ctrl+C로 종료)")
        time.sleep(wait)


if __name__ == "__main__":
    main()
