"""The discovered strategies: parameters and entry/exit signals.

Each signal function takes candle arrays (o, h, l, c of CLOSED candles) and returns four
boolean arrays evaluated on each candle's close:
    long_entry, short_entry, long_exit, short_exit
Exits, stops and time limits are applied by simulator.CoinTrader.
"""

import math

import numpy as np

from . import indicators as ind


def momentum_signals(o, h, l, c, p):
    """#2 Volatility-scaled time-series momentum (Moskowitz, Ooi & Pedersen 2012).
    z = ln(c / c[L bars ago]) / (std of 1-bar log returns over W bars * sqrt(L))"""
    L = p["lookback"]
    W = max(100, min(2000, 2 * L))
    with np.errstate(invalid="ignore", divide="ignore"):
        z = ind.log_roc(c, L) / (ind.rolling_std(ind.log_returns(c), W) * math.sqrt(L))
    exit_z = min(p["exit_z"], p["entry_z"])
    return z > p["entry_z"], z < -p["entry_z"], z < exit_z, z > -exit_z


def rsi_signals(o, h, l, c, p):
    """#5 RSI oversold dip-buying (Wilder 1978)."""
    r = ind.rsi(c, p["n"])
    return r < p["low"], r > 100 - p["low"], r > p["exit"], r < 100 - p["exit"]


def squeeze_signals(o, h, l, c, p):
    """#8 Bollinger squeeze breakout: band-width compressed on the previous candle,
    then a close outside the band; exit on a close back across the middle line."""
    n = p["n"]
    m = ind.sma(c, n)
    sd = ind.rolling_std(c, n)
    with np.errstate(invalid="ignore", divide="ignore"):
        bw = np.log(np.maximum(sd, 1e-12) / m)
    if bw.size >= n:
        bw[: n - 1] = bw[n - 1]
    squeezed = ind.shift(ind.zscore(bw, p["w"]), 1) < p["squeeze"]
    k = p["k"]
    with np.errstate(invalid="ignore"):
        return (c > m + k * sd) & squeezed, (c < m - k * sd) & squeezed, c < m, c > m


STRATEGIES = {
    "momentum_30m": dict(
        id=2, name="시계열 모멘텀 롱", tf="30m", signals=momentum_signals,
        params={"lookback": 172, "entry_z": 2.3357, "exit_z": -0.7185},
        direction="long", sl_k=0.0, tp_k=0.0, max_hold=120, leverage=1.0,
    ),
    "rsi_dip_30m": dict(
        id=5, name="RSI 과매도 매수", tf="30m", signals=rsi_signals,
        params={"n": 26, "low": 22.9569, "exit": 60.7934},
        direction="long", sl_k=0.0, tp_k=1.0, max_hold=54, leverage=0.5,
    ),
    "squeeze_4h": dict(
        id=8, name="볼린저 스퀴즈 돌파", tf="4h", signals=squeeze_signals,
        params={"n": 50, "k": 1.3432, "w": 583, "squeeze": -0.9064},
        direction="both", sl_k=3.7053, tp_k=3.2374, max_hold=25, leverage=1.0,
    ),
}

# Assumptions used in the research backtests.
COST_PER_SIDE = 0.0007   # 0.05% taker fee + 0.02% slippage
FUNDING_8H = 0.0001      # average funding paid by longs per 8 hours
TF_MS = {"30m": 1_800_000, "4h": 14_400_000}


def build_signals(name, o, h, l, c):
    s = STRATEGIES[name]
    le, se, lx, sx = s["signals"](o, h, l, c, s["params"])
    if s["direction"] == "long":
        se = np.zeros_like(se)
    elif s["direction"] == "short":
        le = np.zeros_like(le)
    return le, se, lx, sx, ind.atr(h, l, c, 14)
