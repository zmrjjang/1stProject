"""Live signals and paper trading.

Fetches the latest closed candles from Binance USDT-M futures (public API, no key),
runs each strategy's state machine, and reports per coin: the current position, its
stop/take-profit levels and what to do at the next candle open. In paper mode the
state is kept in paper/state.json so every new closed candle is traded on paper.
"""

import csv
import json
import os
import time
from datetime import datetime, timezone

import numpy as np
import requests

from lab.data import load, symbols

from .rules import COST_PER_SIDE, FUNDING_8H, STRATEGIES, TF_MS, build_signals
from .simulator import CoinTrader

FAPI = "https://fapi.binance.com/fapi/v1/klines"
SIDE = {1: "롱", -1: "숏", 0: "없음"}
REASON = {"exit_signal": "청산 신호", "time_limit": "보유기간 만료", "reverse": "반대 신호", "stop": "손절",
          "take": "익절", "": ""}


def fmt_t(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%m-%d %H:%M")


def fmt_px(x):
    return f"{x:,.6g}"


class BinanceSource:
    def __init__(self, delay=0.25):
        self.s = requests.Session()
        self.delay = delay

    def candles(self, symbol, tf, now_ms):
        for attempt in range(5):
            try:
                r = self.s.get(FAPI, params={"symbol": symbol, "interval": tf, "limit": 1500}, timeout=20)
                if r.status_code == 451:
                    raise SystemExit("fapi.binance.com이 이 지역에서 차단되어 있습니다 (HTTP 451). "
                                     "바이낸스 접속이 되는 PC에서 실행하세요.")
                if r.status_code in (418, 429):
                    time.sleep(int(r.headers.get("Retry-After", 60)))
                    continue
                r.raise_for_status()
                rows = [k for k in r.json() if int(k[6]) < now_ms]  # closed candles only
                time.sleep(self.delay)
                a = np.array([[float(x) for x in k[:5]] for k in rows])
                return {"t": a[:, 0].astype(np.int64), "o": a[:, 1], "h": a[:, 2], "l": a[:, 3], "c": a[:, 4]}
            except requests.RequestException:
                time.sleep(2 ** attempt)
        raise RuntimeError(f"failed to fetch {symbol} {tf}")


class LocalSource:
    """Replays the collected data files as if `now` were the current time (for testing)."""

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def candles(self, symbol, tf, now_ms):
        d = load(symbol, tf, self.data_dir)
        end = int(np.searchsorted(d["t"] + TF_MS[tf], now_ms, side="right"))
        start = max(0, end - 1500)
        return {k: d[k][start:end] for k in ("t", "o", "h", "l", "c")}


def new_trader(s, state=None):
    return CoinTrader(s["sl_k"], s["tp_k"], s["max_hold"], COST_PER_SIDE,
                      FUNDING_8H * TF_MS[s["tf"]] / 28_800_000, state)


class Runner:
    def __init__(self, source, coins=None, capital=1000.0, paper_dir="paper", notify=False, persist=True):
        self.source = source
        self.persist = persist
        self.coins = coins or symbols()
        self.capital = capital
        self.paper_dir = paper_dir
        self.notify = notify
        self.state_path = os.path.join(paper_dir, "state.json")
        try:
            with open(self.state_path) as f:
                self.state = json.load(f)
        except FileNotFoundError:
            self.state = {}

    def save(self):
        if not self.persist:
            return
        os.makedirs(self.paper_dir, exist_ok=True)
        tmp = self.state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f, indent=1)
        os.replace(tmp, self.state_path)

    def log_trades(self, name, trades):
        if not trades or not self.persist:
            return
        path = os.path.join(self.paper_dir, "trades.csv")
        new = not os.path.exists(path)
        os.makedirs(self.paper_dir, exist_ok=True)
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["strategy", "symbol", "side", "entry_time_utc", "exit_time_utc", "entry", "exit",
                            "reason", "return_1x"])
            for tr in trades:
                w.writerow([name, tr["symbol"], SIDE[tr["side"]],
                            datetime.fromtimestamp(tr["entry_time"] / 1000, timezone.utc).isoformat(timespec="minutes"),
                            datetime.fromtimestamp(tr["exit_time"] / 1000, timezone.utc).isoformat(timespec="minutes"),
                            tr["entry"], tr["exit"], REASON.get(tr["reason"], tr["reason"]), round(tr["ret"], 6)])

    def run_strategy(self, name, now_ms):
        s = STRATEGIES[name]
        st = self.state.get(name)
        fresh = st is None
        if fresh:
            st = {"equity": 1.0, "start_time": None, "last_time": None, "coins": {}}
        lines, actions, paper_trades = [], [], []
        bar_returns = {}
        last_closed = None
        for sym in self.coins:
            d = self.source.candles(sym, s["tf"], now_ms)
            if d["c"].size < 700:
                lines.append(f"  {sym:10s} 데이터 부족 ({d['c'].size}봉) - 건너뜀")
                continue
            le, se, lx, sx, atr = build_signals(name, d["o"], d["h"], d["l"], d["c"])
            prev = st["coins"].get(sym)
            replay = prev is None or st["last_time"] is None or st["last_time"] < d["t"][0]
            trader = new_trader(s, None if replay else prev)
            start = 1 if replay else int(np.searchsorted(d["t"], st["last_time"], side="right"))
            trades = []
            for i in range(max(1, start), d["c"].size):
                r = trader.step(int(d["t"][i]), d["o"][i], d["h"][i], d["l"][i], d["c"][i],
                                bool(le[i]), bool(se[i]), bool(lx[i]), bool(sx[i]), atr[i - 1], trades)
                if not replay:
                    bar_returns.setdefault(int(d["t"][i]), []).append(r)
            if not replay:
                paper_trades += [dict(tr, symbol=sym) for tr in trades]
            st["coins"][sym] = trader.state()
            last_closed = int(d["t"][-1]) if last_closed is None else max(last_closed, int(d["t"][-1]))
            lines.append(self.describe(sym, s, trader, d, atr[-1]))
            if trader.pending is not None:
                actions.append(f"{sym} {self.action_text(trader)}")

        for t in sorted(bar_returns):  # paper equity: equal weight across coins, strategy leverage
            st["equity"] *= 1.0 + s["leverage"] * float(np.mean(bar_returns[t]))
        if st["start_time"] is None:
            st["start_time"] = last_closed
        st["last_time"] = last_closed
        self.state[name] = st
        self.log_trades(name, paper_trades)

        per_coin = self.capital * s["leverage"] / len(self.coins)
        head = (f"\n[{name}] #{s['id']} {s['name']} ({s['tf']}, 레버리지 {s['leverage']:g}x, "
                f"코인당 {per_coin:,.0f} USDT)\n"
                f"  마지막 마감: {fmt_t(last_closed + TF_MS[s['tf']])} UTC → 아래 신호는 지금 시작된 봉의 시가에 실행 | "
                f"페이퍼 수익 {(st['equity'] - 1) * 100:+.2f}% (시작 {fmt_t(st['start_time'])} UTC)")
        return head + "\n" + "\n".join(lines), actions

    @staticmethod
    def action_text(tr):
        if tr.pending == 0:
            return f"{SIDE[tr.pos]} 청산 ({REASON[tr.pending_reason]})"
        if tr.pos == 0:
            return f"{SIDE[tr.pending]} 진입"
        return f"{SIDE[tr.pos]} 청산 후 {SIDE[tr.pending]} 진입"

    @staticmethod
    def describe(sym, s, tr, d, atr_last):
        if tr.pos != 0:
            pnl = tr.pos * (d["c"][-1] / tr.entry - 1) * 100
            txt = (f"{SIDE[tr.pos]} 보유 (진입 {fmt_px(tr.entry)} @ {fmt_t(tr.entry_time)}, "
                   f"현재 {fmt_px(d['c'][-1])}, {pnl:+.2f}%, {tr.held}/{s['max_hold']}봉)")
            if s["sl_k"] > 0:
                txt += f" 손절 {fmt_px(tr.stop)}"
            if s["tp_k"] > 0:
                txt += f" 익절 {fmt_px(tr.take)}"
        else:
            txt = "포지션 없음"
        if tr.pending is not None:
            txt += f"  ▶ 다음 시가: {Runner.action_text(tr)}"
            if tr.pending != 0 and (s["sl_k"] > 0 or s["tp_k"] > 0):
                parts = []
                if s["sl_k"] > 0:
                    parts.append(f"손절 = 체결가 {'-' if tr.pending > 0 else '+'} {fmt_px(s['sl_k'] * atr_last)}")
                if s["tp_k"] > 0:
                    parts.append(f"익절 = 체결가 {'+' if tr.pending > 0 else '-'} {fmt_px(s['tp_k'] * atr_last)}")
                txt += " (" + ", ".join(parts) + ")"
        else:
            txt += "  ▷ 유지"
        return f"  {sym:10s} {txt}"

    def run_once(self, names, now_ms=None):
        now_ms = now_ms or int(time.time() * 1000)
        all_actions = []
        for name in names:
            text, actions = self.run_strategy(name, now_ms)
            print(text)
            all_actions += [f"[{name}] {a}" for a in actions]
        self.save()
        if all_actions:
            print("\n다음 봉 시가에 할 일:\n  " + "\n  ".join(all_actions))
            if self.notify:
                from lab.notify import notify
                notify("전략 신호", "\n".join(all_actions))
        else:
            print("\n다음 봉 시가에 할 일: 없음")
        return all_actions


def seconds_to_next_close(period_ms=1_800_000, lag_s=15):
    now = time.time() * 1000
    return (period_ms - now % period_ms) / 1000 + lag_s
