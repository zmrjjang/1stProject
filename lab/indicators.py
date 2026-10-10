"""Causal technical indicators (value at i uses bars <= i only), compiled with numba."""

import numpy as np
from numba import njit


@njit(cache=True)
def ema(x, n):
    out = np.empty_like(x)
    a = 2.0 / (n + 1.0)
    acc = x[0]
    for i in range(x.size):
        v = x[i]
        if v == v:  # skip NaN
            acc = a * v + (1.0 - a) * acc
        out[i] = acc
    return out


@njit(cache=True)
def sma(x, n):
    out = np.full(x.size, np.nan)
    s = 0.0
    for i in range(x.size):
        s += x[i]
        if i >= n:
            s -= x[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


@njit(cache=True)
def rolling_std(x, n):
    out = np.full(x.size, np.nan)
    if x.size == 0:
        return out
    base = x[0]
    s = 0.0
    s2 = 0.0
    for i in range(x.size):
        v = x[i] - base
        s += v
        s2 += v * v
        if i >= n:
            w = x[i - n] - base
            s -= w
            s2 -= w * w
        if i >= n - 1:
            var = (s2 - s * s / n) / (n - 1)
            out[i] = np.sqrt(var) if var > 0 else 0.0
    return out


@njit(cache=True)
def zscore(x, n):
    m = sma(x, n)
    sd = rolling_std(x, n)
    out = np.full(x.size, np.nan)
    for i in range(x.size):
        if sd[i] > 0:
            out[i] = (x[i] - m[i]) / sd[i]
    return out


@njit(cache=True)
def rolling_max(x, n):
    """Max of x[i-n+1..i] using a monotonic deque, O(n)."""
    out = np.empty_like(x)
    dq = np.empty(x.size, np.int64)
    head = 0
    tail = 0
    for i in range(x.size):
        while tail > head and x[dq[tail - 1]] <= x[i]:
            tail -= 1
        dq[tail] = i
        tail += 1
        if dq[head] <= i - n:
            head += 1
        out[i] = x[dq[head]]
    return out


@njit(cache=True)
def rolling_min(x, n):
    out = np.empty_like(x)
    dq = np.empty(x.size, np.int64)
    head = 0
    tail = 0
    for i in range(x.size):
        while tail > head and x[dq[tail - 1]] >= x[i]:
            tail -= 1
        dq[tail] = i
        tail += 1
        if dq[head] <= i - n:
            head += 1
        out[i] = x[dq[head]]
    return out


@njit(cache=True)
def log_returns(c):
    out = np.zeros_like(c)
    for i in range(1, c.size):
        out[i] = np.log(c[i] / c[i - 1])
    return out


@njit(cache=True)
def log_roc(c, n):
    out = np.full(c.size, np.nan)
    for i in range(n, c.size):
        out[i] = np.log(c[i] / c[i - n])
    return out


@njit(cache=True)
def atr(h, l, c, n):
    """Wilder's Average True Range."""
    out = np.empty_like(c)
    acc = h[0] - l[0]
    out[0] = acc
    for i in range(1, c.size):
        tr = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
        acc = acc + (tr - acc) / n
        out[i] = acc
    return out


@njit(cache=True)
def rsi(c, n):
    """Wilder's Relative Strength Index (1978)."""
    out = np.full(c.size, 50.0)
    up = 0.0
    dn = 0.0
    for i in range(1, c.size):
        d = c[i] - c[i - 1]
        g = d if d > 0 else 0.0
        ls = -d if d < 0 else 0.0
        if i <= n:
            up += g / n
            dn += ls / n
        else:
            up = up + (g - up) / n
            dn = dn + (ls - dn) / n
        if i >= n:
            out[i] = 100.0 if dn == 0 else 100.0 - 100.0 / (1.0 + up / dn)
    return out


@njit(cache=True)
def efficiency_ratio(c, n):
    """Kaufman efficiency ratio: |net move| / path length over n bars (1 = pure trend)."""
    out = np.full(c.size, np.nan)
    path = np.zeros(c.size)
    for i in range(1, c.size):
        path[i] = path[i - 1] + abs(c[i] - c[i - 1])
    for i in range(n, c.size):
        p = path[i] - path[i - n]
        out[i] = abs(c[i] - c[i - n]) / p if p > 0 else 0.0
    return out


@njit(cache=True)
def taker_imbalance(v, tbv):
    """(buy - sell) / total taker volume in [-1, 1]."""
    out = np.zeros_like(v)
    for i in range(v.size):
        if v[i] > 0:
            out[i] = (2.0 * tbv[i] - v[i]) / v[i]
    return out


@njit(cache=True)
def shift(x, k):
    """Value from k bars ago (NaN-padded)."""
    out = np.full(x.size, np.nan)
    for i in range(k, x.size):
        out[i] = x[i - k]
    return out


@njit(cache=True)
def ema_nan(x, n):
    """EMA that starts at the first finite value and carries over NaN gaps (NaN before start)."""
    out = np.full(x.size, np.nan)
    a = 2.0 / (n + 1.0)
    acc = np.nan
    for i in range(x.size):
        v = x[i]
        if v == v:
            acc = v if acc != acc else a * v + (1.0 - a) * acc
        out[i] = acc
    return out


@njit(cache=True)
def zscore_nan(x, n):
    """Rolling z-score over the finite values among the last n candles; NaN when fewer than
    80% of them are finite or the current value is missing."""
    out = np.full(x.size, np.nan)
    s = 0.0
    s2 = 0.0
    cnt = 0
    base = np.nan
    for i in range(x.size):
        v = x[i]
        if v == v:
            if base != base:
                base = v
            d = v - base
            s += d
            s2 += d * d
            cnt += 1
        j = i - n
        if j >= 0:
            w = x[j]
            if w == w:
                d = w - base
                s -= d
                s2 -= d * d
                cnt -= 1
        if v == v and cnt >= 0.8 * n and cnt > 2:
            m = s / cnt
            var = (s2 - s * m) / (cnt - 1)
            if var > 0:
                out[i] = (v - base - m) / np.sqrt(var)
    return out
