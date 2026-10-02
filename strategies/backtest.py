"""Backtest the strategies on the local candle files and compare with the research results."""

import json
import os
import warnings

import numpy as np

from lab.data import DAY_MS, load, symbols
from lab.stats import summarize

from .rules import COST_PER_SIDE, FUNDING_8H, STRATEGIES, TF_MS, build_signals
from .simulator import CoinTrader


def run_coin(name, d):
    s = STRATEGIES[name]
    o, h, l, c, t = d["o"], d["h"], d["l"], d["c"], d["t"]
    le, se, lx, sx, atr = build_signals(name, o, h, l, c)
    trader = CoinTrader(s["sl_k"], s["tp_k"], s["max_hold"], COST_PER_SIDE,
                        FUNDING_8H * TF_MS[s["tf"]] / 28_800_000)
    trades = []
    ret = np.zeros(c.size)
    # plain lists are much faster to index than numpy arrays in a Python loop
    cols = [x.tolist() for x in (t, o, h, l, c, le, se, lx, sx, atr)]
    t_, o_, h_, l_, c_, le_, se_, lx_, sx_, a_ = cols
    for i in range(1, c.size):
        ret[i] = trader.step(t_[i], o_[i], h_[i], l_[i], c_[i], le_[i], se_[i], lx_[i], sx_[i], a_[i - 1], trades)
    return ret, trades, trader


def run(name, data_dir="data", day0=None):
    """Equal-weight portfolio across all coins: daily returns (NaN before any coin is listed)."""
    tf = STRATEGIES[name]["tf"]
    series = {sym: load(sym, tf, data_dir) for sym in symbols(data_dir)}
    if day0 is None:
        day0 = min(int(d["t"][0] // DAY_MS) for d in series.values())
    last = max(int(d["t"][-1] // DAY_MS) for d in series.values())
    n_days = last - day0 + 1
    dailies, all_trades = [], []
    for sym, d in series.items():
        ret, trades, _ = run_coin(name, d)
        day = d["t"] // DAY_MS - day0
        daily = np.bincount(day, weights=ret, minlength=n_days).astype(float)
        daily[np.bincount(day, minlength=n_days) == 0] = np.nan
        dailies.append(daily)
        all_trades += [dict(tr, symbol=sym) for tr in trades]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return np.nanmean(np.vstack(dailies), axis=0), all_trades, day0


def report(root="."):
    with open(os.path.join(root, "research", "config.json")) as f:
        split = json.load(f)["split"]
    day0_all = 18262  # 2020-01-01, the first day in the collected data (research day index 0)
    seg_days = {k: (np.datetime64(v) - np.datetime64("1970-01-01")).astype(int) - day0_all
                for k, v in split.items()}
    for name, s in STRATEGIES.items():
        daily, trades, _ = run(name, os.path.join(root, "data"), day0_all)
        ddir = os.path.join(root, "research", "discoveries")
        ref = next((f for f in os.listdir(ddir) if f.startswith(f"{s['id']:04d}_") and f.endswith(".npy")), None)
        n_tr = np.zeros(daily.size)
        for tr in trades:
            n_tr[int(tr["exit_time"] // DAY_MS) - day0_all] += 1
        segs = {"학습 IS": (0, seg_days["is_end"]), "검증 OOS": (seg_days["is_end"], seg_days["oos_end"]),
                "홀드아웃": (seg_days["oos_end"], daily.size), "전체": (0, daily.size)}
        print(f"\n[{name}] #{s['id']} {s['name']} ({s['tf']}, 레버리지 1x 기준)")
        print(f"  {'구간':8s} {'샤프':>6s} {'연수익':>8s} {'최대낙폭':>8s} {'거래수':>6s}")
        for label, (a, b) in segs.items():
            st = summarize(daily[a:b], n_tr[a:b].sum())
            print(f"  {label:8s} {st['sharpe']:6.2f} {st['cagr'] * 100:7.1f}% {st['max_dd'] * 100:7.1f}% {st['trades']:6d}")
        if ref:
            r = np.load(os.path.join(ddir, ref)).astype(float)
            n = min(r.size, daily.size)
            both = np.isfinite(r[:n]) & np.isfinite(daily[:n])
            diff = np.abs(r[:n][both] - daily[:n][both]).max() if both.any() else float("nan")
            print(f"  연구 결과와의 일간수익률 최대 차이: {diff:.2e} ({'일치' if diff < 1e-5 else '불일치 - 확인 필요'})")
