#!/usr/bin/env python3
"""Run the discovered strategies locally (see STRATEGIES.md).

    python run_strategy.py backtest                 # re-run the backtests on data/ and check they match the research
    python run_strategy.py signal                   # latest Binance candles -> current positions + next actions
    python run_strategy.py paper --loop             # paper trade: re-check after every 30m candle close, forever
    python run_strategy.py signal --source local --now 2026-09-20T12:00   # replay local data as if it were that time
    python run_strategy.py list                     # every discovery (#N) and candidate (CN) the search found
    python run_strategy.py paper --pick C3,C7,9 --loop   # paper trade discoveries/candidates by number
    python run_strategy.py paper --pick A --paper-dir paper_A --loop   # every A-grade strategy (B, C likewise)
"""

import argparse
import time
from datetime import datetime, timezone

from strategies.rules import STRATEGIES


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["backtest", "signal", "paper", "list"])
    p.add_argument("--pick", help="discoveries/candidates to run instead of the built-in strategies, "
                                  "e.g. C3,C7,9 - or a whole grade: A, B or C")
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
    if args.mode == "list":
        from strategies.genome_live import list_all
        print(f"{'등급':3s} {'번호':5s} {'전략':24s} {'대상':10s} {'봉':4s} {'검증샤프':>7s} {'홀드아웃':>7s} {'연수익':>7s} {'MDD':>5s} 레버리지")
        for ref, name, uni, tf, oos, ho, cagr, mdd, lev, why, grade in list_all("."):
            print(f"{grade:3s} {ref:5s} {name[:24]:24s} {uni:10s} {tf:4s} {oos:7.2f} {ho:7.2f} {cagr * 100:6.1f}% "
                  f"{mdd * 100:4.0f}% {lev:g}x" + (f"  (실시간 미지원: {why})" if why else ""))
        return

    import json
    from lab.data import INTERVAL_MS, symbols
    from strategies.live import BinanceSource, LocalSource, Runner, builtin_spec, seconds_to_next_close
    if args.pick:
        from strategies.genome_live import genome_spec, grade_refs
        with open("research/config.json") as f:
            cfg = json.load(f)
        refs = []
        for r in (x.strip() for x in args.pick.split(",") if x.strip()):
            refs += grade_refs(".", r.upper()) if r.upper() in ("A", "B", "C") else [r]
        if not refs:
            raise SystemExit(f"--pick {args.pick}: 실행할 전략이 없습니다")
        print("실행 전략:", ", ".join(refs))
        specs = [genome_spec(".", r, cfg, symbols()) for r in refs]
    else:
        specs = [builtin_spec(n.strip()) for n in args.strategies.split(",") if n.strip()]
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
        runner.run_once(specs, now_ms)
        if not args.loop:
            break
        wait = seconds_to_next_close(min(INTERVAL_MS[s["tf"]] for s in specs))
        print(f"\n다음 확인까지 {wait / 60:.1f}분 대기 (Ctrl+C로 종료)")
        time.sleep(wait)


if __name__ == "__main__":
    main()
