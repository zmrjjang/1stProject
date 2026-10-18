"""Strategy grades.

  A - discoveries (#N): passed every strict gate including the Deflated Sharpe Ratio tests
  B - candidates that are strong in every period and robust (config "b_grade"), no DSR gates
  C - other paper-trading candidates
"""


def is_b(stats, checks, cfg):
    b = cfg["b_grade"]
    return (min(stats["is"]["sharpe"], stats["oos"]["sharpe"], stats["ho"]["sharpe"]) >= b["min_sharpe_every_period"]
            and stats["all"]["max_dd"] <= b["max_dd"] and stats["all"]["trades"] >= b["min_trades"]
            and checks.get("stress_sharpe", 0) >= b["min_stress_sharpe"]
            and checks.get("nb_pos", 0) >= b["min_neighbors_positive"])


def candidate_grade(info, cfg):
    return "B" if is_b(info["stats"], info.get("checks", {}), cfg) else "C"
