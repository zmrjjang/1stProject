"""Random generation, mutation and crossover of strategy genomes."""

import json
import math

from .families import FAMILIES, MODIFIERS


def _py(v):
    return v.item() if hasattr(v, "item") else v


def sample(spec, rng):
    kind = spec[0]
    if kind == "int":
        lo, hi, log = spec[1], spec[2], spec[3]
        if log:
            return int(round(math.exp(rng.uniform(math.log(lo), math.log(hi)))))
        return int(rng.integers(lo, hi + 1))
    if kind == "float":
        return round(float(rng.uniform(spec[1], spec[2])), 4)
    if kind == "choice":
        return _py(spec[1][int(rng.integers(len(spec[1])))])
    if kind == "opt":
        lo, hi, p_off = spec[1], spec[2], spec[3]
        return 0.0 if rng.random() < p_off else round(float(rng.uniform(lo, hi)), 3)
    if kind == "optint":
        lo, hi, p_off, log = spec[1], spec[2], spec[3], spec[4]
        if rng.random() < p_off:
            return 0
        return sample(("int", lo, hi, log), rng)
    raise ValueError(kind)


def perturb(spec, v, rng, scale):
    kind = spec[0]
    if kind == "int":
        lo, hi, log = spec[1], spec[2], spec[3]
        if log:
            nv = int(round(v * math.exp(rng.normal(0, scale))))
        else:
            nv = int(round(v + rng.normal(0, scale * (hi - lo))))
        if nv == v:
            nv = v + (1 if rng.random() < 0.5 else -1)
        return int(min(hi, max(lo, nv)))
    if kind == "float":
        lo, hi = spec[1], spec[2]
        return round(float(min(hi, max(lo, v + rng.normal(0, scale * (hi - lo))))), 4)
    if kind == "choice":
        return sample(spec, rng)
    if kind in ("opt", "optint"):
        on_spec = ("float", spec[1], spec[2]) if kind == "opt" else ("int", spec[1], spec[2], spec[4])
        if not v:
            return sample(on_spec, rng) if rng.random() < 0.5 else v
        if rng.random() < 0.15:
            return 0.0 if kind == "opt" else 0
        return perturb(on_spec, v, rng, scale)
    raise ValueError(kind)


def random_genome(rng, symbols, family=None):
    fam = family or list(FAMILIES)[int(rng.integers(len(FAMILIES)))]
    spec = FAMILIES[fam]
    g = {"family": fam, "tf": _py(spec["tfs"][int(rng.integers(len(spec["tfs"])))]),
         "p": {k: sample(s, rng) for k, s in spec["params"].items()}, "mod": {}}
    if spec["kind"] == "single":
        g["universe"] = "ALL" if rng.random() < 0.4 else symbols[int(rng.integers(len(symbols)))]
        g["mod"] = {k: sample(s, rng) for k, s in MODIFIERS.items()}
        if fam == "season":
            g["mod"]["direction"] = "both"
    elif spec["kind"] == "xs":
        g["universe"] = "ALL"
    else:
        a, b = rng.choice(len(symbols), 2, replace=False)
        g["p"]["a"], g["p"]["b"] = symbols[int(a)], symbols[int(b)]
        g["universe"] = f"{g['p']['a']}/{g['p']['b']}"
    return g


def mutate(g, rng, symbols, rate=0.35, scale=0.3):
    spec = FAMILIES[g["family"]]
    n = json.loads(json.dumps(g))
    changed = False
    for k, s in spec["params"].items():
        if rng.random() < rate:
            n["p"][k] = perturb(s, n["p"][k], rng, scale)
            changed = True
    if spec["kind"] == "single":
        for k, s in MODIFIERS.items():
            if rng.random() < rate * 0.5 and not (g["family"] == "season" and k == "direction"):
                n["mod"][k] = perturb(s, n["mod"][k], rng, scale)
                changed = True
        if rng.random() < 0.08:
            n["universe"] = "ALL" if rng.random() < 0.4 else symbols[int(rng.integers(len(symbols)))]
            changed = True
    elif spec["kind"] == "pair" and rng.random() < 0.08:
        a, b = rng.choice(len(symbols), 2, replace=False)
        n["p"]["a"], n["p"]["b"] = symbols[int(a)], symbols[int(b)]
        n["universe"] = f"{n['p']['a']}/{n['p']['b']}"
        changed = True
    if rng.random() < 0.08:
        n["tf"] = _py(spec["tfs"][int(rng.integers(len(spec["tfs"])))])
        changed = True
    if not changed:
        k = list(spec["params"])[int(rng.integers(len(spec["params"])))]
        n["p"][k] = perturb(spec["params"][k], n["p"][k], rng, scale)
    return n


def crossover(a, b, rng):
    if a["family"] != b["family"]:
        return json.loads(json.dumps(a))
    c = json.loads(json.dumps(a))
    for k in FAMILIES[a["family"]]["params"]:
        if rng.random() < 0.5:
            c["p"][k] = b["p"][k]
    for k in c["mod"]:
        if rng.random() < 0.5:
            c["mod"][k] = b["mod"][k]
    if rng.random() < 0.5:
        c["tf"], c["universe"] = b["tf"], b["universe"]
        if FAMILIES[a["family"]]["kind"] == "pair":
            c["p"]["a"], c["p"]["b"] = b["p"]["a"], b["p"]["b"]
    return c


def _numeric(spec, v):
    """Spec to perturb a value in place, or None if it is categorical / switched off."""
    if spec[0] in ("int", "float"):
        return spec
    if spec[0] == "opt" and v:
        return ("float", spec[1], spec[2])
    if spec[0] == "optint" and v:
        return ("int", spec[1], spec[2], spec[4])
    return None


def neighbors(g, rng, n, scale=0.12):
    """Small perturbations of numeric parameters only (same tf/universe/choices/switches)."""
    spec = FAMILIES[g["family"]]
    out = []
    for _ in range(n):
        x = json.loads(json.dumps(g))
        for k, s in spec["params"].items():
            ns = _numeric(s, x["p"][k])
            if ns:
                x["p"][k] = perturb(ns, x["p"][k], rng, scale)
        for k, s in MODIFIERS.items():
            ns = _numeric(s, x["mod"].get(k))
            if ns:
                x["mod"][k] = perturb(ns, x["mod"][k], rng, scale)
        out.append(x)
    return out


def structure_key(g):
    """The trading idea without its tuning: family + coin set + direction (or portfolio mode).
    Two discoveries with the same structure are treated as variants of one strategy."""
    fam = FAMILIES[g["family"]]
    if fam["kind"] == "single":
        side = g["p"]["side"] if g["family"] == "season" else g["mod"]["direction"]
        return f"{g['family']}|{g['universe']}|{side}"
    if fam["kind"] == "xs":
        return f"xsmom|{g['p']['mode']}|{g['p']['legs']}"
    return f"pairs|{'/'.join(sorted([g['p']['a'], g['p']['b']]))}"


def cluster_key(g):
    """Coarse identity used to count *independent* trials for the Deflated Sharpe Ratio:
    numeric parameters are bucketed on a log2 grid, so GA siblings that differ by a few
    percent count once (Bailey & Lopez de Prado 2014, section on effective trials)."""
    def bucket(v):
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return round(math.copysign(math.log2(1 + abs(v)), v) * 2) / 2
        return v
    parts = [g["family"], g["tf"], g["universe"]]
    parts += [f"{k}={bucket(v)}" for k, v in sorted(g["p"].items())]
    parts += [f"{k}={bucket(v)}" for k, v in sorted((g.get("mod") or {}).items())]
    return "|".join(map(str, parts))


def key(g):
    return json.dumps(g, sort_keys=True, separators=(",", ":"))
