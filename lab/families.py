"""Strategy families: parameter spaces, signal builders and plain-language rules.

Each single-asset family returns four boolean arrays evaluated on bar closes:
(long_entry, short_entry, long_exit, short_exit). Portfolio families (cross-
sectional momentum, pairs) return a weight matrix instead.
"""

import math

import numpy as np
from numba import njit

from . import indicators as ind

ALL_TF = ["5m", "15m", "30m", "1h", "4h", "1d"]
INTRADAY_TF = ["5m", "15m", "30m", "1h"]
PORTFOLIO_TF = ["15m", "30m", "1h", "4h", "1d"]
DERIV_TF = ["30m", "1h", "4h", "1d"]  # open interest / ratios are 30-minute snapshots

# Common modifiers for single-asset families.
MODIFIERS = {
    "direction": ("choice", ["both", "long", "short"]),
    "sl_k": ("opt", 0.5, 8.0, 0.4, False),       # ATR stop-loss multiple (0 = off)
    "tp_k": ("opt", 1.0, 15.0, 0.6, False),      # ATR take-profit multiple (0 = off)
    "max_hold": ("optint", 2, 1000, 0.6, True),  # time stop in bars (0 = off)
}


def vol_scaled_momentum(F, L):
    sig = F("rolling_std", "logret", max(100, min(2000, 2 * L)))
    roc = F("log_roc", L)
    with np.errstate(invalid="ignore", divide="ignore"):
        return roc / (sig * math.sqrt(L))


def _trend_ok(F, c, trend):
    if trend <= 0:
        return np.ones(c.size, bool), np.ones(c.size, bool)
    e = F("ema", "c", int(trend))
    return c > e, c < e


# ---------------------------------------------------------------------------

def b_tsmom(d, p, F):
    z = vol_scaled_momentum(F, int(p["lookback"]))
    ez, xz = p["entry_z"], min(p["exit_z"], p["entry_z"])
    return z > ez, z < -ez, z < xz, z > -xz


def b_ma_cross(d, p, F):
    f = int(p["fast"])
    s = max(f + 1, int(round(f * p["ratio"])))
    dist = (F("ema", "c", f) - F("ema", "c", s)) / F("atr", 14)
    th, xth = p["entry"], min(p["exit"], p["entry"])
    return dist > th, dist < -th, dist < xth, dist > -xth


def b_donchian(d, p, F):
    n = int(p["n"])
    m = max(2, int(round(n * p["exit_frac"])))
    c = d["c"]
    return (c > F("shift_max", "h", n), c < F("shift_min", "l", n),
            c < F("shift_min", "l", m), c > F("shift_max", "h", m))


def b_zscore_mr(d, p, F):
    c = d["c"]
    z = F("zscore", "c", int(p["n"]))
    up, dn = _trend_ok(F, c, p["trend"])
    zin, zout = p["z_in"], p["z_out"]
    return (z < -zin) & up, (z > zin) & dn, z > -zout, z < zout


def b_rsi_mr(d, p, F):
    c = d["c"]
    r = F("rsi", int(p["n"]))
    up, dn = _trend_ok(F, c, p["trend"])
    lo, ex = p["low"], p["exit"]
    return (r < lo) & up, (r > 100 - lo) & dn, r > ex, r < 100 - ex


def b_squeeze(d, p, F):
    c = d["c"]
    n = int(p["n"])
    m = F("sma", "c", n)
    sd = F("rolling_std", "c", n)
    bwz = F("bw_z", n, int(p["w"]))
    squeezed = ind.shift(bwz, 1) < p["squeeze"]
    k = p["k"]
    return (c > m + k * sd) & squeezed, (c < m - k * sd) & squeezed, c < m, c > m


def b_flow(d, p, F):
    s = F("flow_z", int(p["n"]), int(p["w"])) * p["mode"]
    th, xth = p["th"], min(p["exit"], p["th"])
    return s > th, s < -th, s < xth, s > -xth


def b_regime(d, p, F):
    trend = F("er", int(p["er_n"])) > p["er_th"]
    tz = vol_scaled_momentum(F, int(p["lookback"]))
    mz = F("zscore", "c", int(p["mr_n"]))
    mzin = p["mr_z"]
    rng = ~trend
    return ((trend & (tz > 0.5)) | (rng & (mz < -mzin)),
            (trend & (tz < -0.5)) | (rng & (mz > mzin)),
            (trend & (tz < 0)) | (rng & (mz > 0)),
            (trend & (tz > 0)) | (rng & (mz < 0)))


def b_season(d, p, F):
    t = d["t"]
    step = int(t[1] - t[0])
    nxt = t + step  # decision at close i is for the bar opening at t[i] + step
    hour = (nxt // 3_600_000) % 24
    dow = (nxt // 86_400_000 + 3) % 7  # Monday = 0
    inside = ((hour - int(p["start"])) % 24) < int(p["length"])
    if p["days"] == "weekdays":
        inside &= dow < 5
    elif p["days"] == "weekend":
        inside &= dow >= 5
    off = ~inside
    if p["side"] > 0:
        return inside, np.zeros(t.size, bool), off, off
    return np.zeros(t.size, bool), inside, off, off


# ---------------------------------------------------------------------------
# Positioning families (funding, open interest, long/short ratios)

def _z_rule(z, p, up, dn):
    th, xth = p["th"], min(p["exit"], p["th"])
    return (z > th) & up, (z < -th) & dn, z < xth, z > -xth


def b_funding(d, p, F):
    """mode +1: follow the crowd (high funding -> long); -1: fade crowded funding."""
    z = F("deriv_z", "fr", int(p["smooth"]), int(p["w"])) * p["mode"]
    up, dn = _trend_ok(F, d["c"], p["trend"])
    return _z_rule(z, p, up, dn)


def b_positioning(d, p, F):
    """Long/short account or position ratios (log), z-scored; mode -1 fades the crowd."""
    z = F("deriv_z", p["which"], int(p["smooth"]), int(p["w"])) * p["mode"]
    up, dn = _trend_ok(F, d["c"], p["trend"])
    return _z_rule(z, p, up, dn)


def b_oi(d, p, F):
    """Price move vs open-interest change over the same lookback (both z-scored).
    confirm: price up + OI up -> long (new money), price down + OI up -> short.
    fade:    price down + OI down -> long (liquidation flush), price up + OI down -> short."""
    L, w = int(p["lookback"]), int(p["w"])
    pz = F("roc_z", L, w)
    oz = F("oi_roc_z", L, w)
    a, b, x = p["price_th"], p["oi_th"], p["exit"]
    if p["mode"] == "confirm":
        return (pz > a) & (oz > b), (pz < -a) & (oz > b), pz < x, pz > -x
    return (pz < -a) & (oz < -b), (pz > a) & (oz < -b), pz > -x, pz < x


# ---------------------------------------------------------------------------
# Portfolio families

def w_xsmom(m, p, cache):
    """Cross-sectional momentum / reversal weights on the aligned close matrix."""
    c = m["c"]
    L, R, k = int(p["lookback"]), int(p["rebalance"]), int(p["k"])
    key = ("xs_score", L, p["vol_adj"])
    score = cache.get(key)
    if score is None:
        with np.errstate(invalid="ignore", divide="ignore"):
            score = np.log(c / np.roll(c, L, axis=0))
            score[:L] = np.nan
            if p["vol_adj"]:
                lr = np.log(c / np.roll(c, 1, axis=0))
                lr[0] = np.nan
                vol = np.sqrt(_rolling_nanmean(lr * lr, max(L, 20)))
                score = score / vol
        cache[key] = score
    if p["mode"] == "rev":
        score = -score
    return _xs_weights(score, R, k, 1 if p["legs"] == "ls" else 0)


@njit(cache=True)
def _xs_weights(score, R, k, short_leg):
    n, s = score.shape
    w = np.zeros((n, s))
    cur = np.zeros(s)
    for i in range(n):
        if i % R == 0:
            cnt = 0
            for j in range(s):
                if score[i, j] == score[i, j]:
                    cnt += 1
            cur[:] = 0.0
            if cnt >= 2 * k:
                vals = np.empty(cnt)
                idx = np.empty(cnt, np.int64)
                q = 0
                for j in range(s):
                    if score[i, j] == score[i, j]:
                        vals[q] = score[i, j]
                        idx[q] = j
                        q += 1
                order = np.argsort(vals)
                gross = 2.0 * k if short_leg else 1.0 * k
                for r in range(k):
                    cur[idx[order[cnt - 1 - r]]] = 1.0 / gross
                    if short_leg:
                        cur[idx[order[r]]] = -1.0 / gross
        w[i] = cur
    return w


def _rolling_nanmean(x, n):
    out = np.full_like(x, np.nan)
    for j in range(x.shape[1]):
        col = x[:, j]
        ok = np.isfinite(col)
        cs = np.cumsum(np.where(ok, col, 0.0))
        cn = np.cumsum(ok)
        s = cs[n:] - cs[:-n]
        k = cn[n:] - cn[:-n]
        with np.errstate(invalid="ignore", divide="ignore"):
            out[n:, j] = np.where(k > n // 2, s / k, np.nan)
    return out


def w_xscarry(m, p, cache):
    """Cross-sectional funding carry: rank coins by smoothed funding rate."""
    L, R, k = int(p["lookback"]), int(p["rebalance"]), int(p["k"])
    key = ("carry", L)
    score = cache.get(key)
    if score is None:
        fr = m["fr"]
        score = np.empty_like(fr)
        for j in range(fr.shape[1]):
            score[:, j] = ind.ema_nan(np.ascontiguousarray(fr[:, j]), L)
        score[~np.isfinite(m["c"])] = np.nan
        cache[key] = score
    # carry: long the coins whose longs pay the least (crowd is short), short the most crowded
    signed = -score if p["mode"] == "carry" else score
    return _xs_weights(signed, R, k, 1 if p["legs"] == "ls" else 0)


def w_pairs(m, p, cache, symbols):
    """Engle-Granger style spread mean reversion between two coins with rolling hedge ratio."""
    a, b = symbols.index(p["a"]), symbols.index(p["b"])
    c = m["c"]
    x, y = np.log(c[:, a]), np.log(c[:, b])
    pos = _pair_positions(x, y, int(p["beta_n"]), int(p["z_n"]), p["z_in"], p["z_out"])
    beta = cache.get(("beta", a, b, int(p["beta_n"])))
    if beta is None:
        beta = _rolling_beta(x, y, int(p["beta_n"]))
        cache[("beta", a, b, int(p["beta_n"]))] = beta
    w = np.zeros(c.shape)
    gross = 1.0 + np.abs(beta)
    with np.errstate(invalid="ignore"):
        w[:, a] = np.where(np.isfinite(beta), pos / gross, 0.0)
        w[:, b] = np.where(np.isfinite(beta), -pos * beta / gross, 0.0)
    return w


@njit(cache=True)
def _rolling_beta(x, y, n):
    out = np.full(x.size, np.nan)
    sx = sy = sxy = syy = 0.0
    cnt = 0
    for i in range(x.size):
        if x[i] == x[i] and y[i] == y[i]:
            sx += x[i]
            sy += y[i]
            sxy += x[i] * y[i]
            syy += y[i] * y[i]
            cnt += 1
        j = i - n
        if j >= 0 and x[j] == x[j] and y[j] == y[j]:
            sx -= x[j]
            sy -= y[j]
            sxy -= x[j] * y[j]
            syy -= y[j] * y[j]
            cnt -= 1
        if cnt >= n:
            vy = syy - sy * sy / cnt
            if vy > 0:
                out[i] = (sxy - sx * sy / cnt) / vy
    return out


@njit(cache=True)
def _pair_positions(x, y, beta_n, z_n, z_in, z_out):
    beta = _rolling_beta(x, y, beta_n)
    spread = np.full(x.size, np.nan)
    for i in range(x.size):
        if beta[i] == beta[i]:
            spread[i] = x[i] - beta[i] * y[i]
    pos = np.zeros(x.size)
    s = s2 = 0.0
    cnt = 0
    cur = 0.0
    for i in range(x.size):
        v = spread[i]
        if v == v:
            s += v
            s2 += v * v
            cnt += 1
        j = i - z_n
        if j >= 0 and spread[j] == spread[j]:
            s -= spread[j]
            s2 -= spread[j] * spread[j]
            cnt -= 1
        if cnt >= z_n and v == v:
            mu = s / cnt
            var = s2 / cnt - mu * mu
            if var > 0:
                z = (v - mu) / np.sqrt(var)
                if cur == 0.0:
                    if z > z_in:
                        cur = -1.0
                    elif z < -z_in:
                        cur = 1.0
                elif cur > 0 and z > -z_out:
                    cur = 0.0
                elif cur < 0 and z < z_out:
                    cur = 0.0
        else:
            cur = 0.0
        pos[i] = cur
    return pos


# ---------------------------------------------------------------------------

FAMILIES = {
    "tsmom": dict(
        kind="single", tfs=ALL_TF, build=b_tsmom,
        params={"lookback": ("int", 3, 1000, True), "entry_z": ("float", 0.0, 2.5),
                "exit_z": ("float", -1.0, 2.0)},
        name="시계열 모멘텀 (변동성 정규화)",
        ref="Moskowitz, Ooi & Pedersen (2012) 'Time Series Momentum', J. Financial Economics",
        rule=lambda p: (f"최근 {int(p['lookback'])}봉 로그수익률을 변동성으로 나눈 z값이 "
                        f"+{p['entry_z']:.2f} 초과면 롱, -{p['entry_z']:.2f} 미만이면 숏. "
                        f"z가 {min(p['exit_z'], p['entry_z']):+.2f} 아래(롱)/위(숏)로 돌아오면 청산."),
    ),
    "ma_cross": dict(
        kind="single", tfs=ALL_TF, build=b_ma_cross,
        params={"fast": ("int", 2, 200, True), "ratio": ("float", 1.5, 10.0),
                "entry": ("float", 0.0, 1.5), "exit": ("float", -1.0, 1.0)},
        name="이동평균 교차 추세추종",
        ref="Brock, Lakonishok & LeBaron (1992) 'Simple Technical Trading Rules', J. Finance",
        rule=lambda p: (f"EMA({int(p['fast'])}) - EMA({max(int(p['fast']) + 1, int(round(p['fast'] * p['ratio'])))})"
                        f" 차이를 ATR(14)로 나눈 값이 +{p['entry']:.2f} 초과면 롱, 반대면 숏. "
                        f"{min(p['exit'], p['entry']):+.2f} 아래(롱)/위(숏)로 오면 청산."),
    ),
    "donchian": dict(
        kind="single", tfs=ALL_TF, build=b_donchian,
        params={"n": ("int", 5, 500, True), "exit_frac": ("float", 0.1, 1.0)},
        name="돈치안 채널 돌파 (터틀)",
        ref="Hurst, Ooi & Pedersen (2017) 'A Century of Evidence on Trend-Following Investing'",
        rule=lambda p: (f"종가가 직전 {int(p['n'])}봉 최고가 돌파 시 롱, 최저가 이탈 시 숏. "
                        f"직전 {max(2, int(round(p['n'] * p['exit_frac'])))}봉 반대편 극값 이탈 시 청산."),
    ),
    "zscore_mr": dict(
        kind="single", tfs=ALL_TF, build=b_zscore_mr,
        params={"n": ("int", 10, 1000, True), "z_in": ("float", 0.8, 3.5),
                "z_out": ("float", -0.5, 1.5), "trend": ("optint", 50, 2000, 0.5, True)},
        name="Ornstein-Uhlenbeck 평균회귀 (z-score)",
        ref="Avellaneda & Lee (2010) 'Statistical Arbitrage in the US Equities Market', Quant. Finance",
        rule=lambda p: (f"가격의 {int(p['n'])}봉 z-score가 -{p['z_in']:.2f} 미만이면 롱, +{p['z_in']:.2f} 초과면 숏. "
                        f"z가 ∓{p['z_out']:.2f}까지 회귀하면 청산."
                        + (f" 추세필터: EMA({int(p['trend'])}) 위에서만 롱, 아래에서만 숏." if p["trend"] > 0 else "")),
    ),
    "rsi_mr": dict(
        kind="single", tfs=ALL_TF, build=b_rsi_mr,
        params={"n": ("int", 2, 30, False), "low": ("float", 5.0, 40.0),
                "exit": ("float", 40.0, 75.0), "trend": ("optint", 50, 2000, 0.5, True)},
        name="RSI 과매도/과매수 역추세",
        ref="Wilder (1978) 'New Concepts in Technical Trading Systems'; Connors & Alvarez (2009)",
        rule=lambda p: (f"RSI({int(p['n'])}) < {p['low']:.1f} 이면 롱, > {100 - p['low']:.1f} 이면 숏. "
                        f"RSI가 {p['exit']:.1f} 초과(롱)/{100 - p['exit']:.1f} 미만(숏)이면 청산."
                        + (f" 추세필터: EMA({int(p['trend'])})." if p["trend"] > 0 else "")),
    ),
    "squeeze": dict(
        kind="single", tfs=ALL_TF, build=b_squeeze,
        params={"n": ("int", 10, 200, True), "k": ("float", 0.5, 3.0),
                "w": ("int", 50, 2000, True), "squeeze": ("float", -2.5, 0.5)},
        name="변동성 수축 후 돌파 (볼린저 스퀴즈)",
        ref="Bollerslev (1986) GARCH volatility clustering; Bollinger (2001) 'Bollinger on Bollinger Bands'",
        rule=lambda p: (f"볼린저밴드({int(p['n'])}, {p['k']:.2f}σ) 폭의 {int(p['w'])}봉 z-score가 "
                        f"{p['squeeze']:.2f} 미만(수축)인 상태에서 상단 돌파 시 롱, 하단 이탈 시 숏. 중심선 복귀 시 청산."),
    ),
    "flow": dict(
        kind="single", tfs=ALL_TF, build=b_flow,
        params={"n": ("int", 1, 200, True), "w": ("int", 50, 3000, True),
                "th": ("float", 0.5, 3.0), "exit": ("float", -0.5, 1.5), "mode": ("choice", [1, -1])},
        name="테이커 주문흐름 불균형",
        ref="Cont, Kukanov & Stoikov (2014) 'The Price Impact of Order Book Events'; "
            "Easley, Lopez de Prado & O'Hara (2012) VPIN",
        rule=lambda p: (f"시장가 매수-매도 불균형의 EMA({int(p['n'])})를 {int(p['w'])}봉 z-score로 만든 값이 "
                        f"+{p['th']:.2f} 초과면 {'롱' if p['mode'] > 0 else '숏'}, -{p['th']:.2f} 미만이면 "
                        f"{'숏' if p['mode'] > 0 else '롱'} ({'추종' if p['mode'] > 0 else '역추종'}). "
                        f"{min(p['exit'], p['th']):.2f} 이내로 돌아오면 청산."),
    ),
    "regime": dict(
        kind="single", tfs=ALL_TF, build=b_regime,
        params={"er_n": ("int", 10, 500, True), "er_th": ("float", 0.1, 0.6),
                "lookback": ("int", 5, 500, True), "mr_n": ("int", 10, 500, True),
                "mr_z": ("float", 1.0, 3.0)},
        name="국면 전환 (추세/횡보 판별 후 전략 선택)",
        ref="Kaufman (1995) efficiency ratio; Lo & MacKinlay (1988) variance ratio test",
        rule=lambda p: (f"효율비율 ER({int(p['er_n'])}) > {p['er_th']:.2f} 이면 추세장: {int(p['lookback'])}봉 모멘텀 방향 추종. "
                        f"아니면 횡보장: {int(p['mr_n'])}봉 z-score ±{p['mr_z']:.2f} 역추세."),
    ),
    "season": dict(
        kind="single", tfs=INTRADAY_TF, build=b_season,
        params={"start": ("int", 0, 23, False), "length": ("int", 1, 12, False),
                "side": ("choice", [1, -1]), "days": ("choice", ["all", "weekdays", "weekend"])},
        name="시간대 계절성",
        ref="Eross, McGroarty, Urquhart & Wolfe (2019) 'The intraday dynamics of bitcoin', Res. Int. Bus. Finance",
        rule=lambda p: (f"UTC {int(p['start']):02d}시부터 {int(p['length'])}시간 동안 "
                        f"{'롱' if p['side'] > 0 else '숏'} 보유 ({ {'all': '매일', 'weekdays': '평일만', 'weekend': '주말만'}[p['days']] })."),
    ),
    "funding": dict(
        kind="single", tfs=DERIV_TF, build=b_funding, weight=3.0, scale="w",
        params={"smooth": ("int", 1, 50, True), "w": ("int", 50, 3000, True),
                "th": ("float", 0.5, 3.0), "exit": ("float", -1.0, 1.5), "mode": ("choice", [1, -1]),
                "trend": ("optint", 50, 2000, 0.6, True)},
        name="펀딩비 쏠림",
        ref="He, Manela, Ross & von Wachter (2022) 'Fundamentals of Perpetual Futures'; "
            "Ackerer, Hugonnier & Jermann (2024) 'Perpetual Futures Pricing', Math. Finance",
        rule=lambda p: (f"펀딩비의 EMA({int(p['smooth'])})를 {int(p['w'])}봉 z-score로 만든 값이 "
                        f"+{p['th']:.2f} 초과면 {'롱' if p['mode'] > 0 else '숏'}, -{p['th']:.2f} 미만이면 "
                        f"{'숏' if p['mode'] > 0 else '롱'} ({'쏠림 추종' if p['mode'] > 0 else '쏠림 역행'}). "
                        f"{min(p['exit'], p['th']):.2f} 이내로 돌아오면 청산."
                        + (f" 추세필터 EMA({int(p['trend'])})." if p["trend"] > 0 else "")),
    ),
    "positioning": dict(
        kind="single", tfs=DERIV_TF, build=b_positioning, weight=3.0, scale="w",
        params={"which": ("choice", ["ls_glob", "ls_top_acc", "ls_top_pos", "smart_gap"]),
                "smooth": ("int", 1, 50, True), "w": ("int", 50, 3000, True),
                "th": ("float", 0.5, 3.0), "exit": ("float", -1.0, 1.5), "mode": ("choice", [1, -1]),
                "trend": ("optint", 50, 2000, 0.6, True)},
        name="롱/숏 비율 포지셔닝",
        ref="Kogan, Makarov, Niessner & Schoar (2024) 'Are Cryptocurrencies Different? Evidence from "
            "Retail Trading', J. Financial Economics; Wang (2003) J. Futures Markets",
        rule=lambda p: (f"{ {'ls_glob': '전체 계정 롱/숏 비율', 'ls_top_acc': '상위 트레이더 계정 롱/숏 비율', 'ls_top_pos': '상위 트레이더 포지션 롱/숏 비율', 'smart_gap': '상위 트레이더 포지션 비율 ÷ 전체 계정 비율'}[p['which']] }"
                        f"(로그)의 EMA({int(p['smooth'])})를 {int(p['w'])}봉 z-score로 만든 값이 +{p['th']:.2f} 초과면 "
                        f"{'롱' if p['mode'] > 0 else '숏'}, -{p['th']:.2f} 미만이면 {'숏' if p['mode'] > 0 else '롱'}. "
                        f"{min(p['exit'], p['th']):.2f} 이내로 돌아오면 청산."
                        + (f" 추세필터 EMA({int(p['trend'])})." if p["trend"] > 0 else "")),
    ),
    "oi_trend": dict(
        kind="single", tfs=DERIV_TF, build=b_oi, weight=3.0, scale="lookback",
        params={"lookback": ("int", 2, 500, True), "w": ("int", 100, 3000, True),
                "price_th": ("float", 0.0, 2.5), "oi_th": ("float", 0.0, 2.5),
                "exit": ("float", -1.0, 1.0), "mode": ("choice", ["confirm", "fade"])},
        name="미결제약정(OI) × 가격",
        ref="Hong & Yogo (2012) 'What does futures market interest tell us about the macroeconomy and "
            "asset prices?', J. Financial Economics; Bessembinder & Seguin (1993) JFQA",
        rule=lambda p: (f"{int(p['lookback'])}봉 가격 변화와 미결제약정 변화를 각각 {int(p['w'])}봉 z-score로 만들어, "
                        + (f"가격 z > {p['price_th']:.2f} 이고 OI z > {p['oi_th']:.2f}(신규 자금 유입)면 롱, "
                           f"가격 z < -{p['price_th']:.2f} 이고 OI z > {p['oi_th']:.2f}면 숏. "
                           f"가격 z가 {p['exit']:+.2f} 아래(롱)/위(숏)로 돌아오면 청산."
                           if p["mode"] == "confirm" else
                           f"가격 z < -{p['price_th']:.2f} 이고 OI z < -{p['oi_th']:.2f}(청산 물량 소진)면 롱, "
                           f"가격 z > {p['price_th']:.2f} 이고 OI z < -{p['oi_th']:.2f}(숏 커버링 소진)면 숏. "
                           f"가격 z가 {-p['exit']:+.2f} 위(롱)/아래(숏)로 돌아오면 청산.")),
    ),
    "xs_carry": dict(
        kind="xs", tfs=["1h", "4h", "1d"], weight=3.0, scale="lookback",
        params={"lookback": ("int", 3, 500, True), "rebalance": ("int", 1, 100, True),
                "k": ("int", 1, 4, False), "mode": ("choice", ["carry", "anti"]),
                "legs": ("choice", ["ls", "long"])},
        name="횡단면 펀딩 캐리 (10개 코인 순위)",
        ref="Schmeling, Schrimpf & Todorov (2023) 'Crypto Carry', BIS Working Paper; "
            "Koijen, Moskowitz, Pedersen & Vrugt (2018) 'Carry', J. Financial Economics",
        rule=lambda p: (f"{int(p['rebalance'])}봉마다 10개 코인을 펀딩비 EMA({int(p['lookback'])}) 순으로 정렬해 "
                        + (f"펀딩비가 가장 낮은 {int(p['k'])}개 롱" + (f", 가장 높은 {int(p['k'])}개 숏" if p["legs"] == "ls" else "")
                           if p["mode"] == "carry" else
                           f"펀딩비가 가장 높은 {int(p['k'])}개 롱" + (f", 가장 낮은 {int(p['k'])}개 숏" if p["legs"] == "ls" else ""))
                        + " (동일비중)."),
    ),
    "xsmom": dict(
        kind="xs", tfs=PORTFOLIO_TF,
        params={"lookback": ("int", 2, 2000, True), "rebalance": ("int", 1, 300, True),
                "k": ("int", 1, 4, False), "mode": ("choice", ["mom", "rev"]),
                "legs": ("choice", ["ls", "long"]), "vol_adj": ("choice", [0, 1])},
        name="횡단면 모멘텀/리버설 (10개 코인 순위)",
        ref="Jegadeesh & Titman (1993) J. Finance; Liu, Tsyvinski & Wu (2022) 'Common Risk Factors in Cryptocurrency', J. Finance",
        rule=lambda p: (f"{int(p['rebalance'])}봉마다 10개 코인을 최근 {int(p['lookback'])}봉 수익률"
                        f"{'(변동성 조정)' if p['vol_adj'] else ''}로 순위를 매겨 "
                        f"{'상위' if p['mode'] == 'mom' else '하위'} {int(p['k'])}개 롱"
                        + (f", {'하위' if p['mode'] == 'mom' else '상위'} {int(p['k'])}개 숏" if p["legs"] == "ls" else "")
                        + " (동일비중)."),
    ),
    "pairs": dict(
        kind="pair", tfs=PORTFOLIO_TF,
        params={"beta_n": ("int", 100, 3000, True), "z_n": ("int", 20, 1000, True),
                "z_in": ("float", 1.0, 3.5), "z_out": ("float", -0.5, 1.0)},
        name="페어 트레이딩 (공적분 스프레드 평균회귀)",
        ref="Engle & Granger (1987) Econometrica; Gatev, Goetzmann & Rouwenhorst (2006) 'Pairs Trading', RFS",
        rule=lambda p: (f"log({p['a']}) - β·log({p['b']}) 스프레드 (β는 {int(p['beta_n'])}봉 롤링 회귀)의 "
                        f"{int(p['z_n'])}봉 z-score가 ±{p['z_in']:.2f}를 넘으면 스프레드 역방향 진입, "
                        f"∓{p['z_out']:.2f}까지 회귀하면 청산 (달러중립)."),
    ),
}
