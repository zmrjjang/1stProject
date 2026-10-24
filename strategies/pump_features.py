"""Features of the pump radar (see PUMP_RADAR.md), shared by research_pump/train.py and pump_radar.py.

Every feature at hour i uses candles <= i only. Inputs are 1h USDT-M perpetual candles plus the
1h premium index (mark vs index price; strongly negative = shorts crowded, funding about to be negative).
"""

import numpy as np

H = 3_600_000
FEATS = ["r1d", "r3d", "r7d", "r30d", "dd90", "up30", "rng7", "rng_ratio", "vol_ratio", "lqv", "qv_r1", "qv_r3",
         "taker1", "taker3", "prem1", "prem3", "prem_min1", "prem_z", "age", "pumps90", "spike7", "btc_r1d", "btc_r7d"]
HISTORY_BARS = 2400  # enough history for every feature (90-day windows + past-pump count)

# perpetuals on stocks, ETFs, commodities, pre-IPO companies and stablecoins are not crypto pumps
NON_CRYPTO = set("""SPY QQQ IWM EWJ EWT EWZ EWY XBI XLE SMH URNM TMF TBT TZA UVXY BITO NATGAS CL BZ COPPER ANTHROPIC OPENAI
MINIMAX ZHIPU SAMSUNG SKHYNIX SKHY HYUNDAI TENCENT SONY POPMART NVDA NVO MSTR TSM AVGO JPM HD DIS V NOK BRKB TXN DRAM
CHIP STRC SPCX GEV XAU XAG XAUT XPD XPT AAPL TSLA COIN AMZN GOOGL META MSFT NFLX AMD INTC MU ORCL PLTR HOOD CRCL BILL
USDC FDUSD TUSD USDP USDE BUSD DAI XUSD RLUSD USD1""".split())


def non_crypto(symbol):
    base = symbol[:-4] if symbol.endswith("USDT") else symbol
    return base in NON_CRYPTO or any(k in symbol for k in ("CSOP", "SKHYNIX", "SAMSUNG", "2LUSDT", "3LUSDT"))


def _sw_max(x, n):
    from numpy.lib.stride_tricks import sliding_window_view
    out = np.full(x.size, np.nan)
    if x.size >= n:
        out[n - 1:] = sliding_window_view(x, n).max(axis=1)
    return out


def _sw_min(x, n):
    return -_sw_max(-x, n)


def _mean(x, n):
    cs = np.cumsum(np.insert(np.nan_to_num(x), 0, 0.0))
    out = np.full(x.size, np.nan)
    if x.size >= n:
        out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def _std(x, n):
    m, m2 = _mean(x, n), _mean(x * x, n)
    return np.sqrt(np.maximum(m2 - m * m, 0))


def _lag(x, n):
    out = np.full(x.size, np.nan)
    out[n:] = x[:-n]
    return out


def fwd_max(x, n):
    """max of x[i+1 .. i+n] (labels only, never a feature)."""
    out = np.full(x.size, np.nan)
    out[:-n] = _sw_max(x, n)[n:]
    return out


def fwd_min(x, n):
    out = np.full(x.size, np.nan)
    out[:-n] = _sw_min(x, n)[n:]
    return out


def features(t, h, l, c, qv, tbq, prem, listing_ms, btc_t, btc_c):
    """(n_bars, len(FEATS)) feature matrix; NaN where the history is too short."""
    with np.errstate(all="ignore"):
        lc = np.log(c)
        lr = np.diff(lc, prepend=lc[0])
        F = {"r1d": lc - _lag(lc, 24), "r3d": lc - _lag(lc, 72), "r7d": lc - _lag(lc, 168), "r30d": lc - _lag(lc, 720),
             "dd90": c / _sw_max(h, 2160) - 1, "up30": c / _sw_min(l, 720) - 1}
        r7 = (_sw_max(h, 168) - _sw_min(l, 168)) / c
        F["rng7"], F["rng_ratio"] = r7, r7 / ((_sw_max(h, 720) - _sw_min(l, 720)) / c)
        F["vol_ratio"] = _std(lr, 24) / _std(lr, 720)
        q30 = _mean(qv, 720) * 24
        F["lqv"] = np.log10(np.maximum(q30, 1))
        F["qv_r1"], F["qv_r3"] = _mean(qv, 24) * 24 / q30, _mean(qv, 72) * 24 / q30
        F["taker1"] = _mean(tbq, 24) / np.maximum(_mean(qv, 24), 1e-9)
        F["taker3"] = _mean(tbq, 72) / np.maximum(_mean(qv, 72), 1e-9)
        p = np.where(np.isfinite(prem), prem, 0.0)
        F["prem1"], F["prem3"], F["prem_min1"] = _mean(p, 24), _mean(p, 72), _sw_min(p, 24)
        F["prem_z"] = (F["prem1"] - _mean(p, 720)) / (_std(p, 720) + 1e-6)
        F["age"] = np.minimum((t - listing_ms) / 86_400_000, 2000)
        # completed +50%-within-72h moves that started 72 .. 2160 hours ago (pumps cluster)
        started = (fwd_max(h, 72) / c - 1 >= 0.5).astype(float)
        F["pumps90"] = _mean(np.nan_to_num(_lag(started, 72)), 2088) * 2088 / 72
        F["spike7"] = _sw_max(np.nan_to_num(F["r1d"]), 168)
        bi = np.minimum(np.searchsorted(btc_t, t), btc_t.size - 1)
        blc = np.log(btc_c)
        F["btc_r1d"] = blc[bi] - blc[np.maximum(bi - 24, 0)]
        F["btc_r7d"] = blc[bi] - blc[np.maximum(bi - 168, 0)]
        return np.column_stack([F[k] for k in FEATS])


class Model:
    """Gradient-boosted trees exported from scikit-learn to plain arrays (no sklearn needed)."""

    def __init__(self, path):
        z = np.load(path, allow_pickle=False)
        self.baseline = float(z["baseline"])
        self.feature, self.threshold = z["feature"], z["threshold"]
        self.left, self.right, self.value = z["left"], z["right"], z["value"]
        self.missing_left, self.leaf, self.roots = z["missing_left"].astype(bool), z["leaf"].astype(bool), z["roots"]
        self.calib_edges, self.calib_p50, self.calib_p30 = z["calib_edges"], z["calib_p50"], z["calib_p30"]

    def raw(self, X):
        out = np.full(X.shape[0], self.baseline)
        for r, x in enumerate(X):
            s = 0.0
            for root in self.roots:
                k = root
                while not self.leaf[k]:
                    v = x[self.feature[k]]
                    k = (self.left[k] if (self.missing_left[k] if v != v else v <= self.threshold[k]) else self.right[k])
                s += self.value[k]
            out[r] += s
        return out

    def score(self, X):
        """Model probability and the hit rates actually measured out of sample for that score level."""
        p = 1.0 / (1.0 + np.exp(-self.raw(X)))
        b = np.clip(np.searchsorted(self.calib_edges, p, side="right") - 1, 0, self.calib_p50.size - 1)
        return p, self.calib_p50[b], self.calib_p30[b]


def export(model, path, calib_edges, calib_p50, calib_p30):
    """Write a fitted sklearn HistGradientBoostingClassifier as arrays for Model."""
    feat, thr, left, right, val, miss, leaf, roots = [], [], [], [], [], [], [], []
    for (pred,) in model._predictors:
        nodes, off = pred.nodes, len(feat)
        roots.append(off)
        feat += nodes["feature_idx"].tolist()
        thr += nodes["num_threshold"].tolist()
        left += (nodes["left"] + off).tolist()
        right += (nodes["right"] + off).tolist()
        val += nodes["value"].tolist()
        miss += nodes["missing_go_to_left"].tolist()
        leaf += nodes["is_leaf"].tolist()
    np.savez_compressed(path, baseline=float(np.ravel(model._baseline_prediction)[0]), feature=np.array(feat, np.int32),
                        threshold=np.array(thr), left=np.array(left, np.int32), right=np.array(right, np.int32),
                        value=np.array(val), missing_left=np.array(miss, np.int8), leaf=np.array(leaf, np.int8),
                        roots=np.array(roots, np.int32), calib_edges=np.asarray(calib_edges, float),
                        calib_p50=np.asarray(calib_p50, float), calib_p30=np.asarray(calib_p30, float))
