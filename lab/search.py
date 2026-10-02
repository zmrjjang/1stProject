"""Endless strategy search: genetic algorithm + multi-stage anti-overfitting gates.

Pipeline for every candidate strategy
  1. In-sample (IS) fitness drives a genetic algorithm (selection, crossover, mutation,
     random immigrants, periodic restarts). Every distinct evaluation is counted as a
     trial so the selection bias can be corrected later.
  2. IS pre-gate: Sharpe, PSR, trade count, drawdown.
  3. Out-of-sample (OOS) gate: Sharpe, Deflated Sharpe Ratio using the number of OOS
     checks so far, trade count, drawdown, positive return.
  4. Robustness: cost stress test and parameter-neighbourhood stability (a real edge is
     a plateau, not a spike).
  5. Holdout (most recent data, never used for selection before this point): must
     stay profitable. Only then is the strategy reported, if it is not a near-duplicate
     of an earlier discovery (daily return correlation).
"""

import json
import logging
import multiprocessing as mp
import os
import signal
import subprocess
import time
from datetime import datetime, timezone

import numpy as np

from .data import Universe
from .evaluate import Evaluator
from .families import FAMILIES
from .genome import cluster_key, crossover, key, mutate, neighbors, random_genome
from .notify import notify
from .report import write_discovery, write_index
from .stats import HyperLogLog, RunningVar, dsr

log = logging.getLogger("lab")

_UNI = None
_CFG = None
_EV = None


def _ev():
    global _EV
    if _EV is None:
        _EV = Evaluator(_UNI, _CFG)
    return _EV


def _w_is(g):
    try:
        return g, _ev().eval_is(g)
    except Exception as e:  # noqa: BLE001 - a broken genome only loses itself
        return g, {"error": repr(e)}


def _w_full(g):
    try:
        st, daily = _ev().eval_full(g)
        return g, st, daily
    except Exception as e:  # noqa: BLE001
        return g, {"error": repr(e)}, None


def _w_robust(args):
    g, n_nb, seed, stress_mult = args
    ev = _ev()
    rng = np.random.default_rng(seed)
    stress = ev.eval_full(g, cost_mult=stress_mult)[0]["is_oos"]["sharpe"]
    nb = []
    for x in neighbors(g, rng, n_nb):
        try:
            nb.append(ev.eval_full(x)[0]["is_oos"]["sharpe"])
        except Exception:  # noqa: BLE001
            nb.append(-10.0)
    return stress, nb


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Search:
    def __init__(self, root, workers, hours, push, seed=None):
        self.root = root
        self.rdir = os.path.join(root, "research")
        self.ddir = os.path.join(self.rdir, "discoveries")
        with open(os.path.join(self.rdir, "config.json")) as f:
            self.cfg = json.load(f)
        self.G = self.cfg["gates"]
        self.workers = workers or os.cpu_count() or 1
        self.deadline = time.time() + hours * 3600 if hours else None
        self.push = push
        self.rng = np.random.default_rng(seed)
        self.stop = False
        self.state = self._load_state()
        self.is_sr = RunningVar(**self.state["is_sr"])
        self.oos_sr = RunningVar(**self.state["oos_sr"])
        self.ho_sr = RunningVar(**self.state["ho_sr"])
        self.oos_clusters = HyperLogLog(self.state.get("oos_clusters_hll"))
        self.memo = {}
        self.validated = set()
        self.known = []  # daily returns of earlier discoveries (for de-duplication)
        for name in sorted(os.listdir(self.ddir)) if os.path.isdir(self.ddir) else []:
            if name.endswith(".npy"):
                self.known.append(np.load(os.path.join(self.ddir, name)).astype(float))

    # -- persistence --------------------------------------------------------
    def _state_path(self):
        return os.path.join(self.rdir, "state.json")

    def _load_state(self):
        try:
            with open(self._state_path()) as f:
                st = json.load(f)
        except FileNotFoundError:
            st = {"created_at": _now(), "runs": 0, "runtime_hours": 0.0, "evaluations": 0,
                  "is_sr": {}, "oos_sr": {}, "ho_sr": {}, "oos_checks": 0, "robust_checks": 0,
                  "holdout_checks": 0, "holdout_rejects": 0, "duplicates": 0,
                  "families": {}, "best_near_miss": None, "discoveries": []}
        st.setdefault("ho_sr", {})
        for f in FAMILIES:
            st["families"].setdefault(f, {"evals": 0, "oos": 0, "robust": 0, "holdout": 0, "found": 0})
        return st

    def save_state(self):
        st = self.state
        st["is_sr"], st["oos_sr"], st["ho_sr"] = self.is_sr.to_dict(), self.oos_sr.to_dict(), self.ho_sr.to_dict()
        st["oos_independent_trials"] = self.oos_clusters.count()
        st["oos_clusters_hll"] = self.oos_clusters.dump()
        st["updated_at"] = _now()
        tmp = self._state_path() + ".tmp"
        with open(tmp, "w") as f:
            json.dump(st, f, indent=1, ensure_ascii=False)
        os.replace(tmp, self._state_path())

    def git_sync(self, message):
        if not self.push:
            return
        branch = os.environ.get("GITHUB_REF_NAME") or subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.root, capture_output=True,
            text=True).stdout.strip()
        run = lambda *a: subprocess.run(["git", *a], cwd=self.root, capture_output=True, text=True)  # noqa: E731
        run("add", "research")
        if run("diff", "--cached", "--quiet").returncode == 0:
            return
        run("commit", "-m", message)
        for attempt in range(5):
            if run("push", "origin", f"HEAD:{branch}").returncode == 0:
                return
            run("pull", "--rebase", "-X", "theirs", "origin", branch)
            time.sleep(2 ** attempt)
        log.warning("git push failed; results stay committed locally")

    # -- gates --------------------------------------------------------------
    def min_trades(self, g):
        kind = FAMILIES[g["family"]]["kind"]
        if kind == "single":
            return self.G["min_trades"]["all" if g["universe"] == "ALL" else "single"]
        return self.G["min_trades"][kind]

    def fitness(self, g, s):
        if "error" in s:
            return -10.0
        f = s["sharpe"]
        mt = self.min_trades(g)
        if s["trades"] < mt:
            f = f * s["trades"] / mt - 1.0
        if s["days"] < 365:
            f -= 2.0
        if s["max_dd"] > 0.6:
            f -= 2.0 * (s["max_dd"] - 0.6)
        return f

    def pre_gate(self, g, s):
        G = self.G
        return ("error" not in s and s["sharpe"] >= G["is_min_sharpe"] and s["psr0"] >= G["is_min_psr"]
                and s["trades"] >= self.min_trades(g) and s["days"] >= 365 and s["max_dd"] <= G["is_max_dd"])

    # -- GA -----------------------------------------------------------------
    def evaluate_population(self, pool, pop):
        todo, seen_now = [], set()
        for g in pop:
            k = key(g)
            if k not in self.memo and k not in seen_now:
                todo.append(g)
                seen_now.add(k)
        for g, s in pool.imap_unordered(_w_is, todo, chunksize=2):
            self.memo[key(g)] = s
            fam = self.state["families"][g["family"]]
            fam["evals"] += 1
            self.state["evaluations"] += 1
            if "error" not in s and s["days"] >= 30:
                self.is_sr.add(s["sr_daily"])
        scored = [(g, self.memo.get(key(g), {"error": "missing"})) for g in pop]
        if len(self.memo) > 300_000:  # bound memory; re-evaluating an old genome is harmless
            self.memo.clear()
        return scored

    def next_generation(self, scored):
        C = self.cfg["search"]
        P = C["population"]
        ranked = sorted(scored, key=lambda x: x[2], reverse=True)
        new = [r[0] for r in ranked[:C["elite"]]]
        n_imm = int(P * C["immigrants"])

        def tournament():
            idx = self.rng.integers(len(ranked), size=3)
            return ranked[int(min(idx))][0]

        while len(new) < P - n_imm:
            a = tournament()
            child = crossover(a, tournament(), self.rng) if self.rng.random() < 0.5 else a
            new.append(mutate(child, self.rng, _UNI.symbols, C["mutation_rate"]))
        new += [random_genome(self.rng, _UNI.symbols) for _ in range(P - len(new))]
        return new

    # -- validation ---------------------------------------------------------
    def validate(self, pool, cands):
        G = self.G
        passed = []
        for g, st, daily in pool.imap_unordered(_w_full, cands):
            if "error" in st:
                continue
            fam = self.state["families"][g["family"]]
            fam["oos"] += 1
            self.state["oos_checks"] += 1
            o = st["oos"]
            if o["days"] >= 30:
                self.oos_sr.add(o["sr_daily"])
            self.oos_clusters.add(cluster_key(g))
            oos_dsr = dsr(o["sr_daily"], o["days"], o["skew"], o["kurt"],
                          max(2, self.oos_clusters.count()), self.oos_sr.var)
            score = min(st["is"]["sharpe"], o["sharpe"])
            best = self.state["best_near_miss"]
            if best is None or score > best["score"]:
                self.state["best_near_miss"] = {
                    "score": round(score, 3), "family": g["family"], "universe": g["universe"], "tf": g["tf"],
                    "is_sharpe": round(st["is"]["sharpe"], 2), "oos_sharpe": round(o["sharpe"], 2),
                    "oos_dsr": round(oos_dsr, 3), "at": _now()}
            if (o["sharpe"] >= G["oos_min_sharpe"] and oos_dsr >= G["oos_min_dsr"]
                    and o["trades"] >= self.min_trades(g) * G["oos_trade_frac"]
                    and o["total_return"] > 0 and o["max_dd"] <= G["oos_max_dd"]):
                passed.append((g, st, daily, oos_dsr))
        if not passed:
            return
        jobs = [(g, G["neighbors"], int(self.rng.integers(1 << 31)), G["stress_cost_mult"]) for g, *_ in passed]
        for (g, st, daily, oos_dsr), (stress, nb) in zip(passed, pool.map(_w_robust, jobs)):
            self.state["robust_checks"] += 1
            self.state["families"][g["family"]]["robust"] += 1
            base = st["is_oos"]["sharpe"]
            nb = np.asarray(nb)
            med, pos = float(np.median(nb)), float((nb > 0).mean())
            if not (stress >= G["stress_min_sharpe"] and med >= G["nb_min_ratio"] * base
                    and pos >= G["nb_min_positive"]):
                continue
            # Variants of an earlier discovery are dropped before they can use up a holdout look.
            if self.is_duplicate(daily):
                self.state["duplicates"] += 1
                continue
            # Holdout is looked at only now, once per robust, novel candidate.
            self.state["holdout_checks"] += 1
            self.state["families"][g["family"]]["holdout"] += 1
            h = st["ho"]
            if h["days"] >= 30:
                self.ho_sr.add(h["sr_daily"])
            ho_dsr = dsr(h["sr_daily"], h["days"], h["skew"], h["kurt"],
                         max(2, self.state["holdout_checks"]), self.ho_sr.var)
            if not (h["sharpe"] >= G["ho_min_sharpe"] and h["total_return"] > 0 and ho_dsr >= G["ho_min_dsr"]
                    and h["trades"] >= self.min_trades(g) * G["ho_trade_frac"]):
                self.state["holdout_rejects"] += 1
                continue
            i = st["is"]
            extra = {
                "is_dsr": dsr(i["sr_daily"], i["days"], i["skew"], i["kurt"],
                              max(2, self.state["evaluations"]), self.is_sr.var),
                "n_trials": self.state["evaluations"], "oos_dsr": oos_dsr, "n_oos": self.oos_clusters.count(),
                "ho_dsr": ho_dsr,
                "stress_sharpe": stress, "nb_n": int(nb.size), "nb_median": med, "nb_pos": pos,
                "n_ho": self.state["holdout_checks"],
            }
            self.record(g, st, daily, extra)

    def is_duplicate(self, daily):
        """Correlation with earlier discoveries, measured on pre-holdout days only."""
        end = _UNI.day_of(self.cfg["split"]["oos_end"])
        for other in self.known:
            ok = np.isfinite(daily[:end]) & np.isfinite(other[:end])
            ok = np.concatenate([ok, np.zeros(daily.size - end, bool)])
            if ok.sum() > 100:
                a, b = daily[ok], other[ok]
                if a.std() > 0 and b.std() > 0 and np.corrcoef(a, b)[0, 1] > self.G["max_corr"]:
                    return True
        return False

    def record(self, g, st, daily, extra):
        disc_id = len(self.state["discoveries"]) + 1
        repo, ref = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_REF_NAME")
        link_base = f"https://github.com/{repo}/blob/{ref}/research/discoveries" if repo and ref else None
        slug, title, message, body, link, lev = write_discovery(
            self.ddir, disc_id, g, st, extra, daily, _UNI, self.cfg, link_base)
        self.known.append(daily.astype(float))
        self.state["families"][g["family"]]["found"] += 1
        self.state["discoveries"].append({
            "id": disc_id, "slug": slug, "name": FAMILIES[g["family"]]["name"], "universe": g["universe"],
            "tf": g["tf"], "oos_sharpe": st["oos"]["sharpe"], "ho_sharpe": st["ho"]["sharpe"],
            "cagr": st["all"]["cagr"], "mdd": st["all"]["max_dd"], "lev": lev, "found_at": _now()})
        write_index(self.ddir, self.state["discoveries"])
        self.save_state()
        log.info("DISCOVERY #%d %s | %s", disc_id, title, message.replace("\n", " | "))
        self.git_sync(f"Strategy discovery #{disc_id}: {g['family']} {g['universe']} {g['tf']}")
        sent = notify(title, message, body, link)
        log.info("notified via: %s", ", ".join(sent) or "(no channel configured)")

    # -- main loop ----------------------------------------------------------
    def progress(self, t0, evals0):
        st = self.state
        rate = (st["evaluations"] - evals0) / max(1e-9, time.time() - t0)
        nm = st["best_near_miss"]
        log.info("evals %d (%.0f/s) | OOS checks %d | robust %d | holdout %d (rejected %d) | dup %d | found %d | "
                 "best near-miss: %s", st["evaluations"], rate, st["oos_checks"], st["robust_checks"],
                 st["holdout_checks"], st["holdout_rejects"], st["duplicates"], len(st["discoveries"]),
                 f"{nm['family']} {nm['universe']} {nm['tf']} IS {nm['is_sharpe']} OOS {nm['oos_sharpe']}" if nm else "-")

    def _warmup(self, ev):
        """Compile all numba kernels once in the parent so forked workers inherit them."""
        for fam in FAMILIES:
            g = random_genome(self.rng, _UNI.symbols, fam)
            g["tf"] = "1d" if "1d" in FAMILIES[fam]["tfs"] else FAMILIES[fam]["tfs"][-1]
            if g["universe"] == "ALL" and FAMILIES[fam]["kind"] == "single":
                g["universe"] = _UNI.symbols[0]
            ev.eval_full(g)

    def run(self):
        global _UNI, _CFG, _EV
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, "stop", True))
        signal.signal(signal.SIGINT, lambda *_: setattr(self, "stop", True))
        log.info("loading data ...")
        _UNI = Universe(["5m", "15m", "30m", "1h", "4h", "1d"], os.path.join(self.root, "data"),
                        os.path.join(self.root, ".cache"))
        _CFG = self.cfg
        _EV = None
        self._warmup(Evaluator(_UNI, _CFG))
        self.state["runs"] += 1
        C = self.cfg["search"]
        t0, evals0, last_ck = time.time(), self.state["evaluations"], time.time()
        log.info("search started with %d workers (%s)", self.workers,
                 f"until {datetime.fromtimestamp(self.deadline, timezone.utc):%Y-%m-%d %H:%M} UTC"
                 if self.deadline else "no time limit")
        ctx = mp.get_context("fork")
        with ctx.Pool(self.workers) as pool:
            while not self._done():
                pop = [random_genome(self.rng, _UNI.symbols) for _ in range(C["population"])]
                best, stale = -1e9, 0
                for _ in range(C["generations_per_epoch"]):
                    scored = [(g, s, self.fitness(g, s)) for g, s in self.evaluate_population(pool, pop)]
                    cands = []
                    for g, s, _f in scored:
                        k = key(g)
                        if k not in self.validated and self.pre_gate(g, s):
                            self.validated.add(k)
                            cands.append(g)
                    if cands:
                        self.validate(pool, cands)
                    top = max(f for *_, f in scored)
                    best, stale = (top, 0) if top > best + 1e-6 else (best, stale + 1)
                    if time.time() - last_ck > float(os.environ.get("LAB_CHECKPOINT_SEC", 300)):
                        self.state["runtime_hours"] += (time.time() - last_ck) / 3600
                        last_ck = time.time()
                        self.save_state()
                        self.progress(t0, evals0)
                    if self._done() or stale >= C["stale_generations"]:
                        break
                    pop = self.next_generation(scored)
            pool.terminate()
        self.state["runtime_hours"] += (time.time() - last_ck) / 3600
        self.save_state()
        self.progress(t0, evals0)

    def _done(self):
        return self.stop or (self.deadline is not None and time.time() >= self.deadline)
