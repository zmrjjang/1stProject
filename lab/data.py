"""Load the collected klines into numpy arrays (cached as .npz for fast restarts)."""

import gzip
import json
import os

import numpy as np

DAY_MS = 86_400_000
INTERVAL_MS = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000,
               "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000}

# open_time, open, high, low, close, volume, trades, taker_buy_volume
_USECOLS = (1, 2, 3, 4, 5, 6, 9, 10)
_FIELDS = ("t", "o", "h", "l", "c", "v", "n", "tbv")


def symbols(data_dir="data"):
    with open(os.path.join(data_dir, "symbols.json")) as f:
        return [s["symbol"] for s in json.load(f)["symbols"]]


def load(symbol, interval, data_dir="data", cache_dir=".cache"):
    path = os.path.join(data_dir, symbol, f"{symbol}_{interval}.csv.gz")
    cache = os.path.join(cache_dir, f"{symbol}_{interval}.npz")
    if os.path.exists(cache) and os.path.getmtime(cache) >= os.path.getmtime(path):
        with np.load(cache) as z:
            return {k: z[k] for k in z.files}
    with gzip.open(path, "rt") as f:
        raw = np.loadtxt(f, delimiter=",", skiprows=1, usecols=_USECOLS)
    d = {name: raw[:, i].copy() for i, name in enumerate(_FIELDS)}
    d["t"] = d["t"].astype(np.int64)
    os.makedirs(cache_dir, exist_ok=True)
    np.savez(cache, **d)
    return d


# Derivative data alignment: a value may be used on a candle's close only if it was
# published at least `lag` before that close, and only while it is fresh.
_DERIV = {
    # field: (file, column, lag_ms, max_age_ms)
    "fr": ("funding", "funding_rate", 0, 12 * 3_600_000),
    "oi": ("metrics", "open_interest_value", 300_000, 2 * 3_600_000),
    "ls_glob": ("metrics", "global_account_ratio", 300_000, 2 * 3_600_000),
    "ls_top_acc": ("metrics", "top_account_ratio", 300_000, 2 * 3_600_000),
    "ls_top_pos": ("metrics", "top_position_ratio", 300_000, 2 * 3_600_000),
}


def load_derivatives(symbol, data_dir="data"):
    """{'funding': {...}, 'metrics': {...}} column arrays; a missing file is skipped."""
    out = {}
    for name in ("funding", "metrics"):
        path = os.path.join(data_dir, symbol, f"{symbol}_{name}.csv.gz")
        if not os.path.exists(path):
            continue
        with gzip.open(path, "rt") as f:
            header = f.readline().strip().split(",")
            raw = np.loadtxt(f, delimiter=",", ndmin=2)
        if raw.size == 0:
            continue
        cols = {h: raw[:, i] for i, h in enumerate(header)}
        cols["time"] = cols["time"].astype(np.int64)
        out[name] = cols
    return out


def asof(times, values, query, lag, max_age):
    """Last value published at or before query - lag (NaN if none or older than max_age)."""
    q = query - lag
    idx = np.searchsorted(times, q, side="right") - 1
    out = np.full(query.size, np.nan)
    ok = idx >= 0
    out[ok] = values[idx[ok]]
    stale = np.zeros(query.size, bool)
    stale[ok] = (q[ok] - times[idx[ok]]) > max_age
    out[stale] = np.nan
    return out


class Universe:
    """All symbols x intervals in memory, plus close/open matrices aligned on a common grid."""

    def __init__(self, intervals, data_dir="data", cache_dir=".cache"):
        self.symbols = symbols(data_dir)
        self.intervals = list(intervals)
        self.series = {(s, iv): load(s, iv, data_dir, cache_dir)
                       for s in self.symbols for iv in self.intervals}
        first = min(d["t"][0] for d in self.series.values())
        last = max(d["t"][-1] for d in self.series.values())
        self.day0 = int(first // DAY_MS)
        self.n_days = int(last // DAY_MS) - self.day0 + 1
        for d in self.series.values():
            d["day"] = (d["t"] // DAY_MS - self.day0).astype(np.int64)
        self.derivatives = {s: load_derivatives(s, data_dir) for s in self.symbols}
        for (s, iv), d in self.series.items():
            close = d["t"] + INTERVAL_MS[iv]
            for field, (src, col, lag, age) in _DERIV.items():
                data = self.derivatives[s].get(src)
                d[field] = (asof(data["time"], data[col], close, lag, age) if data is not None
                            else np.full(close.size, np.nan))
        self.matrices = {iv: self._align(iv) for iv in self.intervals}

    def _align(self, iv):
        step = INTERVAL_MS[iv]
        starts = [self.series[(s, iv)]["t"][0] for s in self.symbols]
        ends = [self.series[(s, iv)]["t"][-1] for s in self.symbols]
        t0, t1 = min(starts), max(ends)
        n = int((t1 - t0) // step) + 1
        m = {"t": t0 + step * np.arange(n, dtype=np.int64)}
        for field in ("o", "c", "fr"):
            arr = np.full((n, len(self.symbols)), np.nan)
            for j, s in enumerate(self.symbols):
                d = self.series[(s, iv)]
                idx = ((d["t"] - t0) // step).astype(np.int64)
                arr[idx, j] = d[field]
            m[field] = arr
        m["day"] = (m["t"] // DAY_MS - self.day0).astype(np.int64)
        return m

    def day_of(self, iso_date):
        y, mth, d = map(int, iso_date.split("-"))
        import datetime as _dt
        ms = int(_dt.datetime(y, mth, d, tzinfo=_dt.timezone.utc).timestamp() * 1000)
        return ms // DAY_MS - self.day0
