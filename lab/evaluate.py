"""Turn a strategy genome into daily returns and per-segment statistics."""

import warnings
from collections import OrderedDict

import numpy as np

from . import engine
from . import indicators as ind
from .data import INTERVAL_MS
from .families import FAMILIES, w_pairs, w_xscarry, w_xsmom
from .stats import summarize

SEGMENTS = ("is", "oos", "ho")


class Evaluator:
    def __init__(self, uni, cfg):
        self.uni = uni
        self.cost = cfg["cost_per_side"]
        self.funding_8h = cfg["funding_8h"]
        self.is_end = uni.day_of(cfg["split"]["is_end"])
        self.oos_end = uni.day_of(cfg["split"]["oos_end"])
        self.cache_max = cfg.get("feature_cache_size", 160)
        self._cache = OrderedDict()
        self._pcache = {}

    # -- features ----------------------------------------------------------
    def _arr(self, sym, tf, field):
        if field == "logret":
            return self.feature(sym, tf, "logret")
        return self.uni.series[(sym, tf)][field]

    def feature(self, sym, tf, name, *args):
        key = (sym, tf, name) + args
        v = self._cache.get(key)
        if v is not None:
            self._cache.move_to_end(key)
            return v
        d = self.uni.series[(sym, tf)]
        c = d["c"]
        if name == "logret":
            v = ind.log_returns(c)
        elif name == "rolling_std":
            v = ind.rolling_std(self._arr(sym, tf, args[0]), args[1])
        elif name == "log_roc":
            v = ind.log_roc(c, args[0])
        elif name == "ema":
            v = ind.ema(self._arr(sym, tf, args[0]), args[1])
        elif name == "sma":
            v = ind.sma(self._arr(sym, tf, args[0]), args[1])
        elif name == "zscore":
            v = ind.zscore(self._arr(sym, tf, args[0]), args[1])
        elif name == "atr":
            v = ind.atr(d["h"], d["l"], c, args[0])
        elif name == "shift_max":
            v = ind.shift(ind.rolling_max(d[args[0]], args[1]), 1)
        elif name == "shift_min":
            v = ind.shift(ind.rolling_min(d[args[0]], args[1]), 1)
        elif name == "rsi":
            v = ind.rsi(c, args[0])
        elif name == "er":
            v = ind.efficiency_ratio(c, args[0])
        elif name == "bw_z":
            n, w = args
            with np.errstate(divide="ignore", invalid="ignore"):
                bw = np.log(np.maximum(ind.rolling_std(c, n), 1e-12) / ind.sma(c, n))
            bw[: n - 1] = bw[n - 1] if bw.size >= n else 0.0
            v = ind.zscore(bw, w)
        elif name == "deriv_z":
            field, smooth, w = args
            with np.errstate(divide="ignore", invalid="ignore"):
                if field == "fr":
                    x = d["fr"]
                elif field == "smart_gap":
                    x = np.log(d["ls_top_pos"]) - np.log(d["ls_glob"])
                else:
                    x = np.log(d[field])
            x = np.where(np.isfinite(x), x, np.nan)
            v = ind.zscore_nan(ind.ema_nan(x, smooth) if smooth > 1 else x, w)
        elif name == "roc_z":
            v = ind.zscore_nan(ind.log_roc(c, args[0]), args[1])
        elif name == "oi_roc_z":
            oi = np.where(d["oi"] > 0, d["oi"], np.nan)  # zero/negative snapshots are bad data
            L = args[0]
            roc = np.full(oi.size, np.nan)
            roc[L:] = np.log(oi[L:] / oi[:-L])
            v = ind.zscore_nan(roc, args[1])
        elif name == "flow_z":
            n, w = args
            v = ind.zscore(ind.ema(ind.taker_imbalance(d["v"], d["tbv"]), n), w)
        else:
            raise KeyError(name)
        self._cache[key] = v
        while len(self._cache) > self.cache_max:
            self._cache.popitem(last=False)
        return v

    # -- runs --------------------------------------------------------------
    def _fund(self, tf):
        return self.funding_8h * INTERVAL_MS[tf] / 28_800_000

    def _single(self, g, sym, upto_day, cost):
        tf, p, mod = g["tf"], g["p"], g["mod"]
        d = self.uni.series[(sym, tf)]
        fam = FAMILIES[g["family"]]
        with np.errstate(all="ignore"):
            le, se, lx, sx = fam["build"](d, p, lambda name, *a: self.feature(sym, tf, name, *a))
        if mod["direction"] == "long":
            se = np.zeros_like(se)
        elif mod["direction"] == "short":
            le = np.zeros_like(le)
        n_end = d["c"].size if upto_day is None else int(np.searchsorted(d["day"], upto_day))
        ret, trades = engine.run_single(
            d["o"], d["h"], d["l"], d["c"], self.feature(sym, tf, "atr", 14),
            np.ascontiguousarray(le, bool), np.ascontiguousarray(se, bool),
            np.ascontiguousarray(lx, bool), np.ascontiguousarray(sx, bool),
            float(mod["sl_k"]), float(mod["tp_k"]), int(mod["max_hold"]),
            cost, self._fund(tf), n_end)
        day = d["day"][:n_end]
        daily = np.bincount(day, weights=ret[:n_end], minlength=self.uni.n_days).astype(float)
        daily[np.bincount(day, minlength=self.uni.n_days) == 0] = np.nan
        tday = np.bincount(d["day"][trades[:, 1].astype(np.int64)], minlength=self.uni.n_days)
        mae = float(trades[:, 4].min()) if len(trades) else 0.0
        return daily, tday.astype(float), mae

    def _portfolio(self, g, upto_day, cost):
        tf, p = g["tf"], g["p"]
        m = self.uni.matrices[tf]
        pc = self._pcache.setdefault(tf, {})
        if len(pc) > 40:
            pc.clear()
        if g["family"] == "xsmom":
            w = w_xsmom(m, p, pc)
            valid = np.isfinite(m["c"]).sum(axis=1) >= 2 * int(p["k"])
        elif g["family"] == "xs_carry":
            w = w_xscarry(m, p, pc)
            valid = np.isfinite(m["fr"]).sum(axis=1) >= 2 * int(p["k"])
        else:
            w = w_pairs(m, p, pc, self.uni.symbols)
            a, b = self.uni.symbols.index(p["a"]), self.uni.symbols.index(p["b"])
            valid = np.isfinite(m["c"][:, a]) & np.isfinite(m["c"][:, b])
        n_end = m["o"].shape[0] if upto_day is None else int(np.searchsorted(m["day"], upto_day))
        ret, changes = engine.run_weights(m["o"], np.ascontiguousarray(w), cost, self._fund(tf), n_end)
        day = m["day"][:n_end]
        daily = np.bincount(day, weights=ret[:n_end], minlength=self.uni.n_days).astype(float)
        daily[np.bincount(day[valid[:n_end]], minlength=self.uni.n_days) == 0] = np.nan
        tday = np.bincount(day, weights=changes[:n_end], minlength=self.uni.n_days)
        return daily, tday, 0.0

    def run(self, g, upto_day=None, cost_mult=1.0):
        """Daily returns over the whole calendar (NaN where inactive), trades per day,
        worst intra-trade adverse excursion."""
        cost = self.cost * cost_mult
        kind = FAMILIES[g["family"]]["kind"]
        if kind != "single":
            return self._portfolio(g, upto_day, cost)
        if g["universe"] != "ALL":
            return self._single(g, g["universe"], upto_day, cost)
        dailies, trades, maes = [], 0.0, []
        for sym in self.uni.symbols:
            d, t, m = self._single(g, sym, upto_day, cost)
            dailies.append(d)
            trades = trades + t
            maes.append(m)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            daily = np.nanmean(np.vstack(dailies), axis=0)  # equal weight across listed coins
        return daily, trades, min(maes)

    # -- statistics --------------------------------------------------------
    def bounds(self):
        return {"is": (0, self.is_end), "oos": (self.is_end, self.oos_end),
                "ho": (self.oos_end, self.uni.n_days)}

    def segment_stats(self, daily, tday, segments=SEGMENTS):
        b = self.bounds()
        return {s: summarize(daily[b[s][0]:b[s][1]], tday[b[s][0]:b[s][1]].sum()) for s in segments}

    def eval_is(self, g):
        daily, tday, _ = self.run(g, upto_day=self.is_end)
        return self.segment_stats(daily, tday, ("is",))["is"]

    def eval_full(self, g, cost_mult=1.0):
        daily, tday, mae = self.run(g, cost_mult=cost_mult)
        out = self.segment_stats(daily, tday)
        b = self.bounds()
        out["is_oos"] = summarize(daily[:b["oos"][1]], tday[:b["oos"][1]].sum())
        out["all"] = summarize(daily, tday.sum())
        out["worst_mae"] = mae
        fin = daily[np.isfinite(daily)]
        out["worst_day"] = float(fin.min()) if fin.size else 0.0
        return out, daily
