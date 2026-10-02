"""Performance statistics and multiple-testing-aware significance tests.

References
  * Sharpe (1966, 1994) - Sharpe ratio.
  * Bailey & Lopez de Prado (2012) "The Sharpe Ratio Efficient Frontier",
    J. of Risk - Probabilistic Sharpe Ratio (PSR), corrects for sample length,
    skewness and fat tails.
  * Bailey & Lopez de Prado (2014) "The Deflated Sharpe Ratio: Correcting for
    Selection Bias, Backtest Overfitting and Non-Normality", J. of Portfolio
    Management - DSR: PSR against the Sharpe ratio expected from the best of N
    unskilled trials (false strategy theorem).
  * Kelly (1956) - growth-optimal fraction f* = mu / sigma^2.
"""

import base64
import hashlib
import math
from statistics import NormalDist

import numpy as np

_N = NormalDist()
EULER_GAMMA = 0.5772156649015329


def moments(x):
    """mean, std (ddof=1), skewness, kurtosis (normal = 3)."""
    n = x.size
    if n < 3:
        return 0.0, 0.0, 0.0, 3.0
    m = float(x.mean())
    d = x - m
    s2 = float((d * d).mean())
    if s2 <= 0:
        return m, 0.0, 0.0, 3.0
    skew = float((d ** 3).mean() / s2 ** 1.5)
    kurt = float((d ** 4).mean() / s2 ** 2)
    return m, math.sqrt(s2 * n / (n - 1)), skew, kurt


def psr(sr, n, skew, kurt, sr_star=0.0):
    """Probability that the true (per-period) Sharpe exceeds sr_star."""
    if n < 3:
        return 0.0
    var = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr
    if var <= 0:
        var = 1e-9
    return _N.cdf((sr - sr_star) * math.sqrt(n - 1) / math.sqrt(var))


def expected_max_sharpe(n_trials, var_sr):
    """E[max SR] over n_trials unskilled strategies whose SRs have variance var_sr."""
    if n_trials < 2 or var_sr <= 0:
        return 0.0
    z1 = _N.inv_cdf(1.0 - 1.0 / n_trials)
    z2 = _N.inv_cdf(1.0 - 1.0 / (n_trials * math.e))
    return math.sqrt(var_sr) * ((1.0 - EULER_GAMMA) * z1 + EULER_GAMMA * z2)


def dsr(sr, n, skew, kurt, n_trials, var_sr):
    return psr(sr, n, skew, kurt, expected_max_sharpe(n_trials, var_sr))


def summarize(daily, trades, days_per_year=365.0):
    """daily: daily strategy returns (NaN = not active). trades: count in the window."""
    x = daily[np.isfinite(daily)]
    out = {"days": int(x.size), "trades": int(trades)}
    if x.size < 30:
        out.update(sharpe=0.0, sr_daily=0.0, psr0=0.0, skew=0.0, kurt=3.0, cagr=0.0,
                   total_return=0.0, max_dd=0.0, vol=0.0, kelly=0.0, exposure_days=0.0)
        return out
    m, sd, skew, kurt = moments(x)
    sr = m / sd if sd > 0 else 0.0
    eq = np.cumprod(1.0 + np.clip(x, -0.99, None))
    peak = np.maximum.accumulate(eq)
    years = x.size / days_per_year
    total = float(eq[-1] - 1.0)
    out.update(
        sharpe=sr * math.sqrt(days_per_year),
        sr_daily=sr,
        psr0=psr(sr, x.size, skew, kurt),
        skew=skew,
        kurt=kurt,
        total_return=total,
        cagr=float(eq[-1] ** (1.0 / years) - 1.0) if eq[-1] > 0 else -1.0,
        max_dd=float((1.0 - eq / peak).max()),
        vol=sd * math.sqrt(days_per_year),
        kelly=m / (sd * sd) if sd > 0 else 0.0,
        exposure_days=float((x != 0).mean()),
    )
    return out


class HyperLogLog:
    """Distinct-count sketch (Flajolet et al. 2007) - counts independent trials in 4 KB."""

    def __init__(self, data=None, p=12):
        self.p, self.m = p, 1 << p
        self.reg = bytearray(base64.b64decode(data)) if data else bytearray(self.m)

    def add(self, item):
        h = int.from_bytes(hashlib.sha1(item.encode()).digest()[:8], "big")
        idx = h >> (64 - self.p)
        w = h & ((1 << (64 - self.p)) - 1)
        rho = (64 - self.p) - w.bit_length() + 1
        if rho > self.reg[idx]:
            self.reg[idx] = rho

    def count(self):
        m = self.m
        est = 0.7213 / (1 + 1.079 / m) * m * m / sum(2.0 ** -r for r in self.reg)
        zeros = self.reg.count(0)
        if est <= 2.5 * m and zeros:
            est = m * math.log(m / zeros)
        return int(round(est))

    def dump(self):
        return base64.b64encode(bytes(self.reg)).decode()


class RunningVar:
    """Welford running mean/variance (persisted between runs) for trial Sharpe ratios."""

    def __init__(self, n=0, mean=0.0, m2=0.0):
        self.n, self.mean, self.m2 = n, mean, m2

    def add(self, x):
        self.n += 1
        d = x - self.mean
        self.mean += d / self.n
        self.m2 += d * (x - self.mean)

    @property
    def var(self):
        return self.m2 / (self.n - 1) if self.n > 1 else 0.0

    def to_dict(self):
        return {"n": self.n, "mean": self.mean, "m2": self.m2}
