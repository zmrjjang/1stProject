#!/usr/bin/env python3
"""Run the discovered strategies locally (see STRATEGIES.md).

    python run_strategy.py backtest                 # re-run the backtests on data/ and check they match the research
    python run_strategy.py signal                   # latest Binance candles -> current positions + next actions
    python run_strategy.py paper --loop             # paper trade: re-check after every 30m candle close, forever
    python run_strategy.py signal --source local --now 2026-09-20T12:00   # replay local data as if it were that time
"""

import argparse
import time
from datetime import datetime, timezone

from strategies.rules import STRATEGIES


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["backtest", "signal", "paper"])
    p.add_argument("--strategies", default=",".join(STRATEGIES),
                   help="comma separated subset of: " + ", ".join(STRATEGIES))
    p.add_argument("--capital", type=float, default=1000.0, help="USDT allocated to EACH strategy")
    p.add_argument("--loop", action="store_true", help="repeat after every 30-minute candle close")
    p.add_argument("--notify", action="store_true", help="push new actions via ntfy/Telegram/Discord env vars")
    p.add_argument("--source", choices=["binance", "local"], default="binance")
    p.add_argument("--now", help="with --source local: pretend the current time is this UTC ISO time")
    p.add_argument("--paper-dir", default="paper")
    args = p.parse_args()

    if args.mode == "backtest":
        from strategies.backtest import report
        report(".")
        return

    from strategies.live import BinanceSource, LocalSource, Runner, seconds_to_next_close
    names = [n.strip() for n in args.strategies.split(",") if n.strip()]
    source = LocalSource() if args.source == "local" else BinanceSource()
    now_ms = None
    if args.now:
        now_ms = int(datetime.fromisoformat(args.now).replace(tzinfo=timezone.utc).timestamp() * 1000)
    # "signal" only shows the current state; "paper" keeps a paper account in --paper-dir.
    runner = Runner(source, capital=args.capital, paper_dir=args.paper_dir, notify=args.notify,
                    persist=args.mode == "paper")
    if args.mode == "signal":
        runner.state = {}
    while True:
        print(f"\n===== {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} UTC =====")
        runner.run_once(names, now_ms)
        if not args.loop:
            break
        wait = seconds_to_next_close()
        print(f"\n다음 확인까지 {wait / 60:.1f}분 대기 (Ctrl+C로 종료)")
        time.sleep(wait)


if __name__ == "__main__":
    main()
