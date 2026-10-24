#!/usr/bin/env python3
"""Backtest of the new-listing short rule (strategies/listing_short.py) on research_lowcap/cache/
(run fetch.py first). Uses the same signal()/simulate() as the paper runner."""

import collections
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.listing_short import RULE, TRADFI, signal, simulate  # noqa: E402

H = 3_600_000
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")


def is_tradfi(sym, t, c):
    """Stock/commodity perps move mostly in US market hours or barely at weekends."""
    if sym[:-4] in TRADFI:
        return True
    r = np.abs(np.diff(np.log(c)))
    wd = ((t[1:] // 86_400_000) + 3) % 7
    hr = (t[1:] // H) % 24
    tot = r.sum() or 1
    return r[wd >= 5].sum() / tot < 0.12 or r[(wd < 5) & (hr >= 13) & (hr < 21)].sum() / tot > 0.45


def load(since="2024-01-01"):
    since_ms = int(np.datetime64(since, "ms").astype(np.int64))
    coins = {}
    for p in sorted(glob.glob(os.path.join(CACHE, "*.npz"))):
        sym = os.path.basename(p)[:-4]
        z = np.load(p)
        if z["t"].size > 48 and z["t"][0] >= since_ms and not is_tradfi(sym, z["t"], z["c"]):
            coins[sym] = {k: z[k] for k in z.files}
    return coins


def backtest(coins, rule=RULE, skip_day1_up=True):
    out = []
    for sym, d in coins.items():
        t, o, h, l, c = d["t"], d["o"], d["h"], d["l"], d["c"]
        i = rule["entry_after_h"]
        if c.size < i + rule["hold_h"] + 1:
            continue  # only listings whose whole holding period is in the data
        if skip_day1_up and not signal(o, c):
            continue
        res = simulate(t, o, h, l, c, i, o[i], list(zip(d["ft"].tolist(), d["fr"].tolist())), rule)
        out.append({"sym": sym, "listed": int(t[0]), "entry": int(t[i]), **res})
    return out


def half(ms):
    y = 1970 + ms / (365.25 * 86_400_000)
    return f"{int(y)}H{1 if y - int(y) < 0.5 else 2}"


def report(name, trades, size=0.02):
    r = np.array([x["ret"] for x in trades])
    by = collections.defaultdict(list)
    for x in trades:
        by[half(x["listed"])].append(x["ret"])
    eq = peak = 1.0
    mdd = 0.0
    for x in sorted(trades, key=lambda x: x["exit_ms"]):
        eq += size * x["ret"] * eq
        peak = max(peak, eq)
        mdd = max(mdd, 1 - eq / peak)
    t = r.mean() / (r.std() / np.sqrt(r.size))
    print(f"{name:34s} n{r.size:4d} mean {r.mean() * 100:+5.1f}% (t {t:.1f}) win {np.mean(r > 0) * 100:3.0f}% "
          f"worst {r.min() * 100:4.0f}% | " + " ".join(f"{k} {np.mean(v) * 100:+.0f}%" for k, v in sorted(by.items()))
          + f" | {size:.0%}/trade x{eq:.2f} DD {mdd * 100:.0f}%")


def main():
    coins = load()
    print(f"{len(coins)} crypto perpetuals in {CACHE}")
    report("RULE (day-1 down only)", backtest(coins))
    report("every listing (no day-1 filter)", backtest(coins, skip_day1_up=False))
    for k, vals in {"stop": [0.4, 0.75], "take": [0.4, 0.6], "hold_h": [504, 1080], "funding_cap": [0.0, 0.05],
                    "cost": [0.003]}.items():
        for v in vals:
            report(f"  {k}={v}", backtest(coins, {**RULE, k: v}))
    tr = backtest(coins)
    print("exit reasons:", dict(collections.Counter(x["reason"] for x in tr)))
    with open(os.path.join(CACHE, "trades.json"), "w") as f:
        json.dump(tr, f)


if __name__ == "__main__":
    main()
