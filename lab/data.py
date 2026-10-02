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
        self.matrices = {iv: self._align(iv) for iv in self.intervals}

    def _align(self, iv):
        step = INTERVAL_MS[iv]
        starts = [self.series[(s, iv)]["t"][0] for s in self.symbols]
        ends = [self.series[(s, iv)]["t"][-1] for s in self.symbols]
        t0, t1 = min(starts), max(ends)
        n = int((t1 - t0) // step) + 1
        m = {"t": t0 + step * np.arange(n, dtype=np.int64)}
        for field in ("o", "c"):
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
