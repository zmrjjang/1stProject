"""Run any strategy found by the research lab (discovery #N or candidate CN) live/paper,
using exactly the same signal code (lab/families*.py) that the search evaluated."""

import json
import os

import numpy as np

from lab.evaluate import Evaluator
from lab.families import FAMILIES

TF_ORDER = ["5m", "15m", "30m", "1h", "4h", "1d"]
DERIV_FAMILIES = {"funding", "positioning", "oi_trend", "xs_carry"}
DERIV_FIELDS = ("fr", "oi", "ls_glob", "ls_top_acc", "ls_top_pos")


class _LiveUniverse:
    """Just enough of lab.data.Universe for Evaluator.feature()."""

    def __init__(self, series, symbols):
        self.series = series
        self.symbols = symbols
        self.matrices = {}
        self.n_days = 1

    def day_of(self, iso_date):
        return 0


def find(root, ref):
    """'C12' -> research/candidates/C0012_*.json, '9' or '#9' -> research/discoveries/0009_*.json."""
    ref = ref.strip().lstrip("#")
    cand = ref.upper().startswith("C")
    num = int(ref[1:] if cand else ref)
    folder = os.path.join(root, "research", "candidates" if cand else "discoveries")
    prefix = f"{'C' if cand else ''}{num:04d}_"
    for sub in (folder, os.path.join(folder, "archive")):
        if not os.path.isdir(sub):
            continue
        for name in sorted(os.listdir(sub)):
            if name.startswith(prefix) and name.endswith(".json"):
                with open(os.path.join(sub, name)) as f:
                    return name[:-5], json.load(f)
    raise SystemExit(f"{ref}: research/{'candidates' if cand else 'discoveries'}/ 에 없습니다")


def unsupported_reason(g):
    fam = FAMILIES[g["family"]]
    if fam["kind"] != "single":
        return "포트폴리오형(여러 코인 순위/페어) 전략은 아직 실시간 실행을 지원하지 않습니다"
    if g["family"] in DERIV_FAMILIES:
        return "펀딩비/미결제약정 데이터를 쓰는 전략은 아직 실시간 실행을 지원하지 않습니다"
    return None


def genome_spec(root, ref, cfg, all_symbols):
    slug, info = find(root, ref)
    g = info["genome"]
    why = unsupported_reason(g)
    if why:
        raise SystemExit(f"{ref} ({slug}): {why}")
    fam = FAMILIES[g["family"]]
    p, mod, tf = g["p"], g["mod"], g["tf"]
    htf = None
    if p.get("filter") == "htf":
        i = TF_ORDER.index(tf) + int(p["htf"])
        htf = TF_ORDER[i] if i < len(TF_ORDER) else None

    def signals(sym, d, fetch):
        series = {(sym, tf): dict(d)}
        if htf:
            series[(sym, htf)] = dict(fetch(sym, htf))
        for dd in series.values():
            for f in DERIV_FIELDS:
                dd.setdefault(f, np.full(dd["c"].size, np.nan))
        ev = Evaluator(_LiveUniverse(series, all_symbols), cfg)
        F = lambda name, *a: ev.feature(sym, tf, name, *a)  # noqa: E731
        with np.errstate(all="ignore"):
            le, se, lx, sx = fam["build"](series[(sym, tf)], p, F)
        le, se = np.asarray(le, bool), np.asarray(se, bool)
        if mod["direction"] == "long":
            se = np.zeros_like(se)
        elif mod["direction"] == "short":
            le = np.zeros_like(le)
        return le, se, np.asarray(lx, bool), np.asarray(sx, bool), F("atr", 14)

    label = f"{'후보 C' if slug.startswith('C') else '#'}{info['id']} {fam['name']}"
    return dict(key=slug, label=label, tf=tf, coins=None if g["universe"] == "ALL" else [g["universe"]],
                direction=mod["direction"], sl_k=float(mod["sl_k"]), tp_k=float(mod["tp_k"]),
                max_hold=int(mod["max_hold"]), leverage=float(info.get("leverage", 1.0)),
                bars=4000, signals=signals)


def list_all(root):
    rows = []
    for folder, cand in (("discoveries", False), ("candidates", True)):
        path = os.path.join(root, "research", folder)
        if not os.path.isdir(path):
            continue
        for name in sorted(os.listdir(path)):
            if name.endswith(".json"):
                with open(os.path.join(path, name)) as f:
                    info = json.load(f)
                g, s = info["genome"], info["stats"]
                ref = f"C{info['id']}" if cand else f"#{info['id']}"
                rows.append((ref, FAMILIES[g["family"]]["name"], g["universe"], g["tf"], s["oos"]["sharpe"],
                             s["ho"]["sharpe"], s["all"]["cagr"], s["all"]["max_dd"], info.get("leverage", 1),
                             unsupported_reason(g)))
    return rows
