"""Indicators in plain numpy, matching the research engine (lab/indicators.py) exactly.

All values at index i use only candles 0..i (the candle that just closed and earlier).
"""

import numpy as np


def log_returns(c):
    out = np.zeros_like(c)
    out[1:] = np.log(c[1:] / c[:-1])
    return out


def log_roc(c, n):
    """ln(c[i] / c[i-n]); NaN for the first n candles."""
    out = np.full(c.size, np.nan)
    out[n:] = np.log(c[n:] / c[:-n])
    return out


def sma(x, n):
    out = np.full(x.size, np.nan)
    cs = np.cumsum(np.insert(x, 0, 0.0))
    out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def rolling_std(x, n):
    """Sample standard deviation (ddof=1) of x[i-n+1..i]; NaN for the first n-1 candles."""
    out = np.full(x.size, np.nan)
    if x.size < n:
        return out
    y = x - x[0]  # shift for numerical stability (same as the research engine)
    s = np.cumsum(np.insert(y, 0, 0.0))
    s2 = np.cumsum(np.insert(y * y, 0, 0.0))
    ws = s[n:] - s[:-n]
    ws2 = s2[n:] - s2[:-n]
    var = (ws2 - ws * ws / n) / (n - 1)
    out[n - 1:] = np.sqrt(np.maximum(var, 0.0))
    return out


def zscore(x, n):
    m, sd = sma(x, n), rolling_std(x, n)
    out = np.full(x.size, np.nan)
    ok = sd > 0
    out[ok] = (x[ok] - m[ok]) / sd[ok]
    return out


def atr(h, l, c, n=14):
    """Wilder's Average True Range, seeded with the first candle's range."""
    out = np.empty_like(c)
    acc = h[0] - l[0]
    out[0] = acc
    for i in range(1, c.size):
        tr = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
        acc += (tr - acc) / n
        out[i] = acc
    return out


def rsi(c, n):
    """Wilder's RSI: simple average of the first n moves, then Wilder smoothing."""
    out = np.full(c.size, 50.0)
    up = dn = 0.0
    for i in range(1, c.size):
        d = c[i] - c[i - 1]
        g, ls = max(d, 0.0), max(-d, 0.0)
        if i <= n:
            up += g / n
            dn += ls / n
        else:
            up += (g - up) / n
            dn += (ls - dn) / n
        if i >= n:
            out[i] = 100.0 if dn == 0 else 100.0 - 100.0 / (1.0 + up / dn)
    return out


def shift(x, k):
    out = np.full(x.size, np.nan)
    out[k:] = x[:-k]
    return out
