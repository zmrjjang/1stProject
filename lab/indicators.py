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


# ---------------------------------------------------------------------------
# Additional chart indicators (all causal)

@njit(cache=True)
def wilder(x, n):
    """Wilder smoothing (RMA) seeded with x[0]."""
    out = np.empty_like(x)
    acc = x[0]
    for i in range(x.size):
        acc = acc + (x[i] - acc) / n if i else x[0]
        out[i] = acc
    return out


@njit(cache=True)
def dmi(h, l, c, n):
    """Wilder's +DI, -DI and ADX."""
    size = c.size
    pdm = np.zeros(size)
    mdm = np.zeros(size)
    tr = np.zeros(size)
    tr[0] = h[0] - l[0]
    for i in range(1, size):
        up = h[i] - h[i - 1]
        dn = l[i - 1] - l[i]
        pdm[i] = up if (up > dn and up > 0) else 0.0
        mdm[i] = dn if (dn > up and dn > 0) else 0.0
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    atr_ = wilder(tr, n)
    pdi = np.zeros(size)
    mdi = np.zeros(size)
    dx = np.zeros(size)
    sp = wilder(pdm, n)
    sm = wilder(mdm, n)
    for i in range(size):
        if atr_[i] > 0:
            pdi[i] = 100.0 * sp[i] / atr_[i]
            mdi[i] = 100.0 * sm[i] / atr_[i]
        s = pdi[i] + mdi[i]
        dx[i] = 100.0 * abs(pdi[i] - mdi[i]) / s if s > 0 else 0.0
    return pdi, mdi, wilder(dx, n)


@njit(cache=True)
def supertrend(h, l, c, atr_, mult):
    """Supertrend direction (+1 up / -1 down)."""
    size = c.size
    d = np.ones(size)
    upper = 0.0
    lower = 0.0
    for i in range(size):
        mid = (h[i] + l[i]) / 2.0
        bu = mid + mult * atr_[i]
        bl = mid - mult * atr_[i]
        if i == 0:
            upper, lower = bu, bl
            continue
        upper = bu if (bu < upper or c[i - 1] > upper) else upper
        lower = bl if (bl > lower or c[i - 1] < lower) else lower
        if d[i - 1] > 0:
            d[i] = -1.0 if c[i] < lower else 1.0
        else:
            d[i] = 1.0 if c[i] > upper else -1.0
    return d


@njit(cache=True)
def psar(h, l, step, max_step):
    """Wilder's Parabolic SAR direction (+1 long / -1 short)."""
    size = h.size
    d = np.ones(size)
    if size < 2:
        return d
    up = True
    sar = l[0]
    ep = h[0]
    af = step
    for i in range(1, size):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, l[i - 1], l[i - 2] if i > 1 else l[i - 1])
            if l[i] < sar:
                up, sar, ep, af = False, ep, l[i], step
            elif h[i] > ep:
                ep = h[i]
                af = min(af + step, max_step)
        else:
            sar = max(sar, h[i - 1], h[i - 2] if i > 1 else h[i - 1])
            if h[i] > sar:
                up, sar, ep, af = True, ep, h[i], step
            elif l[i] < ep:
                ep = l[i]
                af = min(af + step, max_step)
        d[i] = 1.0 if up else -1.0
    return d


@njit(cache=True)
def aroon(h, l, n):
    """Aroon up/down: 100 * (n - bars since the n-bar high/low) / n."""
    size = h.size
    up = np.full(size, np.nan)
    dn = np.full(size, np.nan)
    qh = np.empty(size, np.int64)
    ql = np.empty(size, np.int64)
    hh = th = hl = tl = 0
    for i in range(size):
        while th > hh and h[qh[th - 1]] <= h[i]:
            th -= 1
        qh[th] = i
        th += 1
        if qh[hh] <= i - n - 1:
            hh += 1
        while tl > hl and l[ql[tl - 1]] >= l[i]:
            tl -= 1
        ql[tl] = i
        tl += 1
        if ql[hl] <= i - n - 1:
            hl += 1
        if i >= n:
            up[i] = 100.0 * (n - (i - qh[hh])) / n
            dn[i] = 100.0 * (n - (i - ql[hl])) / n
    return up, dn


@njit(cache=True)
def linreg_t(c, n):
    """t-statistic of the OLS slope of log price over the last n candles (trend significance)."""
    size = c.size
    out = np.full(size, np.nan)
    if size == 0:
        return out
    y0 = np.log(c[0])
    sy = 0.0
    sjy = 0.0
    syy = 0.0
    sk = n * (n - 1) / 2.0
    skk = (n - 1) * n * (2 * n - 1) / 6.0
    sxx = skk - sk * sk / n
    for i in range(size):
        y = np.log(c[i]) - y0
        sy += y
        sjy += i * y
        syy += y * y
        if i >= n:
            yo = np.log(c[i - n]) - y0
            sy -= yo
            sjy -= (i - n) * yo
            syy -= yo * yo
        if i >= n - 1:
            start = i - n + 1
            sky = sjy - start * sy
            sxy = sky - sk * sy / n
            slope = sxy / sxx
            rss = syy - sy * sy / n - slope * sxy
            if rss > 0:
                se = np.sqrt(rss / (n - 2) / sxx)
                out[i] = slope / se
    return out


@njit(cache=True)
def heikin_run(o, h, l, c):
    """Signed run length of Heikin-Ashi candle colour (+k: k green in a row, -k: k red)."""
    size = c.size
    run = np.zeros(size)
    ho = (o[0] + c[0]) / 2.0
    prev_hc = 0.0
    for i in range(size):
        hc = (o[i] + h[i] + l[i] + c[i]) / 4.0
        if i > 0:
            ho = (ho + prev_hc) / 2.0
        prev_hc = hc
        green = hc >= ho
        if i == 0:
            run[i] = 1.0 if green else -1.0
        elif green:
            run[i] = run[i - 1] + 1.0 if run[i - 1] > 0 else 1.0
        else:
            run[i] = run[i - 1] - 1.0 if run[i - 1] < 0 else -1.0
    return run
