#!/usr/bin/env python3
"""Train and evaluate the pump radar model on research_pump/cache/ (run fetch.py first).

Label: the high of the next 72 hours is >= +50% above the close. Snapshots every 4 hours.
Train on snapshots before 2025-07-01, evaluate after; then refit on everything and export
strategies/pump_model.npz for pump_radar.py. Needs scikit-learn (pip install scikit-learn)."""

import glob
import json
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.pump_features import FEATS, H, Model, export, features, fwd_max, fwd_min, non_crypto  # noqa: E402

warnings.filterwarnings("ignore")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
MODEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "strategies", "pump_model.npz")
SPLIT = np.datetime64("2025-07-01", "ms").astype(np.int64)
EDGES = [0, 0.02, 0.05, 0.1, 0.2, 0.3, 1.01]


def looks_tradfi(t, c):
    """Stock/commodity perps move mostly in US market hours, barely at weekends, or hardly at all."""
    r = np.abs(np.diff(np.log(c)))
    if r.size < 200:
        return False
    wd = ((t[1:] // 86_400_000) + 3) % 7
    hr = (t[1:] // H) % 24
    tot = r.sum() or 1
    ann = np.std(np.diff(np.log(c[-720:]))) * np.sqrt(24 * 365)
    return r[wd >= 5].sum() / tot < 0.12 or r[(wd < 5) & (hr >= 13) & (hr < 21)].sum() / tot > 0.45 or ann < 0.15


def build(step=4):
    lst = json.load(open(os.path.join(CACHE, "listing.json")))
    btc = np.load(os.path.join(CACHE, "npz", "BTCUSDT.npz"))
    rows, last = [], {}
    li = FEATS.index("lqv")
    for p in sorted(glob.glob(os.path.join(CACHE, "npz", "*.npz"))):
        sym = os.path.basename(p)[:-4]
        z = np.load(p)
        t, c = z["t"], z["c"]
        if t.size < 200 or non_crypto(sym) or looks_tradfi(t, c):
            continue
        first = (lst.get(sym) or [None])[0]
        lms = np.datetime64(first, "ms").astype(np.int64) if first else t[0]
        X = features(t, z["h"], z["l"], c, z["qv"], z["tbq"], z["prem"], lms, btc["t"], btc["c"])
        if np.isfinite(X[-1, li]) and X[-1, li] >= 6:  # >= $1M average daily volume
            last[sym] = (int(t[-1]), X[-1], float(c[-1]))
        up = fwd_max(z["h"], 72) / c - 1
        dn = fwd_min(z["l"], 72) / c - 1
        idx = np.arange(168, t.size - 72)
        idx = idx[(t[idx] % (step * H) == 0) & np.isfinite(X[idx, li]) & (X[idx, li] >= 6)]
        rows.append((t[idx], X[idx], up[idx], dn[idx]))
    T = np.concatenate([r[0] for r in rows])
    X = np.vstack([r[1] for r in rows])
    UP = np.concatenate([r[2] for r in rows])
    DN = np.concatenate([r[3] for r in rows])
    return T, X, UP, DN, last


def fit(X, y):
    from sklearn.ensemble import HistGradientBoostingClassifier
    m = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=200,
                                       l2_regularization=1.0, random_state=0)
    return m.fit(X, y)


def topk(T, p, y, k=10):
    hits = []
    for ts in np.unique(T):
        i = np.nonzero(T == ts)[0]
        if i.size >= 50:
            hits.append(y[i[np.argsort(-p[i])][:k]].mean())
    return float(np.mean(hits))


def main():
    from sklearn.metrics import roc_auc_score
    T, X, UP, DN, last = build()
    y50, y30 = UP >= 0.5, UP >= 0.3
    tr, te = T < SPLIT - 3 * 86_400_000, T >= SPLIT
    print(f"{len(T):,} snapshots, {len(last)} coins now; +50%/72h base rate train {y50[tr].mean():.2%} test {y50[te].mean():.2%}")
    m = fit(X[tr], y50[tr])
    p = m.predict_proba(X[te])[:, 1]
    print(f"test AUC {roc_auc_score(y50[te], p):.3f}")
    for a, b in (("2025-07-01", "2026-01-01"), ("2026-01-01", "2026-07-01"), ("2026-07-01", "2027-01-01")):
        lo, hi = (np.datetime64(x, "ms").astype(np.int64) for x in (a, b))
        s = (T[te] >= lo) & (T[te] < hi)
        if s.sum():
            print(f"  {a[:7]}~ top10 hit +50% {topk(T[te][s], p[s], y50[te][s]):.1%} (base {y50[te][s].mean():.2%}), "
                  f"+30% {topk(T[te][s], p[s], y30[te][s]):.1%} (base {y30[te][s].mean():.2%})")
    c50, c30 = [], []
    for a, b in zip(EDGES[:-1], EDGES[1:]):
        s = (p >= a) & (p < b)
        c50.append(float(y50[te][s].mean()) if s.sum() else 0.0)
        c30.append(float(y30[te][s].mean()) if s.sum() else 0.0)
        print(f"  score {a:.2f}-{b:.2f}: n {s.sum():7d}  measured +50% {c50[-1]:.1%}  +30% {c30[-1]:.1%}  "
              f"fell 30%+ {np.mean(DN[te][s] <= -0.3) if s.sum() else 0:.1%}")
    full = fit(X, y50)
    export(full, MODEL, EDGES[:-1], c50, c30)
    mm = Model(MODEL)
    sample = X[np.random.default_rng(0).choice(len(X), 2000, replace=False)]
    diff = np.abs(mm.raw(sample) - full._raw_predict(sample).ravel()).max()
    print(f"exported {MODEL} (max raw difference vs sklearn {diff:.2e})")
    syms = sorted(last)
    pr, h50, h30 = mm.score(np.vstack([last[s][1] for s in syms]))
    when = max(v[0] for v in last.values()) + H
    print(f"\nTop 25 at {np.datetime64(when, 'ms')} UTC")
    for i in np.argsort(-pr)[:25]:
        x = dict(zip(FEATS, last[syms[i]][1]))
        print(f"{syms[i]:14s} score {pr[i]:.2f} (measured +50% {h50[i]:.0%}, +30% {h30[i]:.0%}) 1d {x['r1d']:+.0%} 7d {x['r7d']:+.0%} "
              f"from 90d high {x['dd90']:+.0%} prem {x['prem1'] * 100:+.3f}% vol x{x['qv_r1']:.1f}")


if __name__ == "__main__":
    main()
