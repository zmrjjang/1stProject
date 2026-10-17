"""Chart/indicator strategy families (second generation).

Every family here produces (long_entry, short_entry, long_exit, short_exit) from price/volume
only, and can be combined with one shared filter:
  none    - no filter
  trend   - longs only above EMA(f_n), shorts only below
  htf     - only in the direction of the higher-timeframe trend (close vs EMA(f_n) on the
            timeframe 1 or 2 steps up, using that timeframe's last CLOSED candle)
  adx_hi  - only while ADX(14) > threshold (trending market)
  adx_lo  - only while ADX(14) < threshold (ranging market)
  vol_lo  - only while ATR% is low relative to its own f_n-bar history (z-score below threshold)
  vol_hi  - only while ATR% is high
"""

import numpy as np

ALL_TF = ["5m", "15m", "30m", "1h", "4h", "1d"]

FILTER_PARAMS = {
    "filter": ("choice", ["none", "trend", "htf", "adx_hi", "adx_lo", "vol_lo", "vol_hi"]),
    "f_n": ("int", 20, 500, True),
    "f_th": ("float", 0.0, 1.0),
    "htf": ("choice", [1, 2]),
}
FILTER_TEXT = {
    "none": "",
    "trend": "추세필터: EMA({n}) 위에서만 롱, 아래에서만 숏",
    "htf": "상위봉 필터: {htf}단계 위 봉의 종가가 EMA({n}) 위일 때만 롱, 아래일 때만 숏",
    "adx_hi": "추세장에서만: ADX(14) > {adx:.0f}",
    "adx_lo": "횡보장에서만: ADX(14) < {adx:.0f}",
    "vol_lo": "저변동성에서만: ATR% z-score({n}) < {vz:+.2f}",
    "vol_hi": "고변동성에서만: ATR% z-score({n}) > {vz:+.2f}",
}


def apply_filter(d, p, F, le, se):
    f = p["filter"]
    if f == "none":
        return le, se
    n, x = int(p["f_n"]), p["f_th"]
    with np.errstate(invalid="ignore"):
        if f == "trend":
            e = F("ema", "c", n)
            return le & (d["c"] > e), se & (d["c"] < e)
        if f == "htf":
            t = F("htf_trend", int(p["htf"]), n)
            return le & (t > 0), se & (t < 0)
        if f in ("adx_hi", "adx_lo"):
            a = F("dmi", 14)[2]
            ok = a > 15 + 25 * x if f == "adx_hi" else a < 15 + 25 * x
            return le & ok, se & ok
        z = F("atr_pct_z", n)
        ok = z < -1.5 + 3 * x if f == "vol_lo" else z > -1.5 + 3 * x
        return le & ok, se & ok


def filter_text(p):
    t = FILTER_TEXT[p["filter"]]
    return t.format(n=int(p["f_n"]), htf=p["htf"], adx=15 + 25 * p["f_th"], vz=-1.5 + 3 * p["f_th"])


def _sym(s, th, exit_level=0.0):
    """Trend-style rule on an oscillating signal: enter beyond +-th, exit back through exit_level."""
    return s > th, s < -th, s < exit_level, s > -exit_level


def _ema_exit(d, p, F):
    e = F("ema", "c", int(p["exit_n"]))
    with np.errstate(invalid="ignore"):
        return d["c"] < e, d["c"] > e


# ---------------------------------------------------------------------------

def b_macd(d, p, F):
    f = int(p["fast"])
    s = max(f + 1, int(round(f * p["ratio"])))
    line, hist = F("macd", f, s, int(p["sig"]))
    x = hist if p["mode"] == "hist" else line
    with np.errstate(invalid="ignore"):
        return _sym(x, p["th"])


def b_adx(d, p, F):
    pdi, mdi, adx = F("dmi", int(p["n"]))
    with np.errstate(invalid="ignore"):
        strong = adx > p["th"]
        return (pdi > mdi) & strong, (mdi > pdi) & strong, pdi < mdi, mdi < pdi


def b_ichimoku(d, p, F):
    tk, kj, top, bot = F("ichimoku", round(p["scale"], 2))
    c = d["c"]
    with np.errstate(invalid="ignore"):
        if p["mode"] == "cloud":
            return (c > top) & (tk > kj), (c < bot) & (tk < kj), c < kj, c > kj
        return (tk > kj) & (c > kj), (tk < kj) & (c < kj), tk < kj, tk > kj


def b_keltner(d, p, F):
    n, k = int(p["n"]), p["k"]
    e, a = F("ema", "c", n), F("atr", n)
    c = d["c"]
    with np.errstate(invalid="ignore"):
        if p["mode"] == "breakout":
            return c > e + k * a, c < e - k * a, c < e, c > e
        return c < e - k * a, c > e + k * a, c > e, c < e


def b_supertrend(d, p, F):
    s = F("supertrend", int(p["n"]), round(p["mult"], 2))
    return s > 0, s < 0, s < 0, s > 0


def b_stoch(d, p, F):
    k = F("stoch", int(p["n"]), int(p["smooth"]))
    lo, ex = p["low"], p["exit"]
    with np.errstate(invalid="ignore"):
        return k < lo, k > 100 - lo, k > ex, k < 100 - ex


def b_mfi(d, p, F):
    m = F("mfi", int(p["n"]))
    lo, ex = p["low"], p["exit"]
    with np.errstate(invalid="ignore"):
        return m < lo, m > 100 - lo, m > ex, m < 100 - ex


def b_obv(d, p, F):
    z = F("obv_z", int(p["n"]), int(p["w"])) * p["mode"]
    with np.errstate(invalid="ignore"):
        return _sym(z, p["th"])


def b_vwap(d, p, F):
    dev = F("vwap_dev", int(p["n"]))
    k = p["k"]
    with np.errstate(invalid="ignore"):
        if p["mode"] == "revert":
            return dev < -k, dev > k, dev > 0, dev < 0
        return dev > k, dev < -k, dev < 0, dev > 0


def b_aroon(d, p, F):
    up, dn = F("aroon", int(p["n"]))
    th = p["th"]
    with np.errstate(invalid="ignore"):
        return (up >= th) & (dn <= 100 - th), (dn >= th) & (up <= 100 - th), up < dn, dn < up


def b_psar(d, p, F):
    s = F("psar", round(p["step"], 4), round(p["max_step"], 3))
    return s > 0, s < 0, s < 0, s > 0


def b_linreg(d, p, F):
    t = F("linreg_t", int(p["n"]))
    with np.errstate(invalid="ignore"):
        return _sym(t, p["th"], min(p["exit"], p["th"]))


def b_heikin(d, p, F):
    r = F("ha_run")
    k, x = int(p["k"]), int(p["exit_k"])
    return r >= k, r <= -k, r <= -x, r >= x


def b_candle(d, p, F):
    bull, bear = F("candle", p["pattern"])
    lx, sx = _ema_exit(d, p, F)
    return bull, bear, lx, sx


def b_nr(d, p, F):
    nr = F("nr_prev", int(p["n"]))
    c, h, l = d["c"], d["h"], d["l"]
    ph, pl = np.roll(h, 1), np.roll(l, 1)
    lx, sx = _ema_exit(d, p, F)
    return nr & (c > ph), nr & (c < pl), lx, sx


def b_volbreak(d, p, F):
    vz = F("vol_z", int(p["w"]))
    c = d["c"]
    n = int(p["n"])
    lx, sx = _ema_exit(d, p, F)
    with np.errstate(invalid="ignore"):
        spike = vz > p["z"]
        return spike & (c > F("shift_max", "h", n)), spike & (c < F("shift_min", "l", n)), lx, sx


def _wrap(build):
    def built(d, p, F):
        le, se, lx, sx = build(d, p, F)
        le, se = apply_filter(d, p, F, np.asarray(le, bool), np.asarray(se, bool))
        return le, se, np.asarray(lx, bool), np.asarray(sx, bool)
    return built


def _fam(build, params, name, ref, rule, scale, tfs=ALL_TF):
    return dict(kind="single", tfs=tfs, build=_wrap(build), params={**params, **FILTER_PARAMS},
                weight=2.0, scale=scale, name=name, ref=ref,
                rule=lambda p: rule(p) + (" " + filter_text(p) + "." if p["filter"] != "none" else ""))


def _ex(p):
    return f"EMA({int(p['exit_n'])}) 반대편으로 종가가 넘어가면 청산."


CANDLE = {"engulf": "장악형(engulfing)", "pin": "망치형/유성형(pin bar)", "inside": "인사이드바 돌파",
          "three": "적삼병/흑삼병"}

CHART_FAMILIES = {
    "macd": _fam(b_macd, {"fast": ("int", 3, 50, True), "ratio": ("float", 1.5, 5.0),
                          "sig": ("int", 3, 30, True), "th": ("float", 0.0, 1.0),
                          "mode": ("choice", ["hist", "line"])},
                 "MACD", "Appel (1979) 'The Moving Average Convergence-Divergence Method'",
                 lambda p: (f"MACD({int(p['fast'])},{max(int(p['fast']) + 1, int(round(p['fast'] * p['ratio'])))},"
                            f"{int(p['sig'])}) {'히스토그램' if p['mode'] == 'hist' else '라인'} ÷ ATR(14)가 "
                            f"+{p['th']:.2f} 초과면 롱, -{p['th']:.2f} 미만이면 숏, 0을 반대로 넘으면 청산."),
                 "fast"),
    "adx_dmi": _fam(b_adx, {"n": ("int", 7, 50, True), "th": ("float", 15.0, 40.0)},
                    "ADX/DMI 추세", "Wilder (1978) 'New Concepts in Technical Trading Systems'",
                    lambda p: (f"ADX({int(p['n'])}) > {p['th']:.1f} 이고 +DI > -DI면 롱, -DI > +DI면 숏. "
                               f"DI가 교차하면 청산."), "n"),
    "ichimoku": _fam(b_ichimoku, {"scale": ("float", 0.5, 4.0), "mode": ("choice", ["cloud", "tk"])},
                     "일목균형표", "Hosoda (1969); Deng, Sakurai & Shimada (2020) 'Ichimoku Kinko Hyo', IEEE Access",
                     lambda p: (f"일목균형표 (전환/기준/선행 = {round(9 * p['scale'])}/{round(26 * p['scale'])}/"
                                f"{round(52 * p['scale'])}) "
                                + ("구름 위 + 전환선 > 기준선이면 롱, 구름 아래 + 전환선 < 기준선이면 숏, 기준선 이탈 시 청산."
                                   if p["mode"] == "cloud" else
                                   "전환선 > 기준선 + 종가 > 기준선이면 롱, 반대면 숏, 전환/기준선 교차 시 청산.")),
                     "scale"),
    "keltner": _fam(b_keltner, {"n": ("int", 10, 200, True), "k": ("float", 0.5, 4.0),
                                "mode": ("choice", ["breakout", "revert"])},
                    "켈트너 채널", "Keltner (1960) 'How to Make Money in Commodities'",
                    lambda p: (f"켈트너 채널 EMA({int(p['n'])}) ± {p['k']:.2f}×ATR({int(p['n'])}) "
                               + ("상단 돌파 롱 / 하단 이탈 숏, 중심선 복귀 시 청산." if p["mode"] == "breakout"
                                  else "하단 이탈 시 롱 / 상단 돌파 시 숏 (역추세), 중심선 복귀 시 청산.")), "n"),
    "supertrend": _fam(b_supertrend, {"n": ("int", 5, 50, True), "mult": ("float", 1.0, 6.0)},
                       "슈퍼트렌드", "Seban (2009); Wilder (1978) ATR",
                       lambda p: f"슈퍼트렌드(ATR {int(p['n'])}, ×{p['mult']:.2f}) 방향대로 롱/숏, 방향이 바뀌면 청산·전환.",
                       "n"),
    "stoch": _fam(b_stoch, {"n": ("int", 5, 100, True), "smooth": ("int", 1, 10, False),
                            "low": ("float", 5.0, 35.0), "exit": ("float", 40.0, 80.0)},
                  "스토캐스틱 역추세", "Lane (1984) 'Lane's Stochastics', Technical Analysis of Stocks & Commodities",
                  lambda p: (f"스토캐스틱 %K({int(p['n'])}, {int(p['smooth'])}) < {p['low']:.1f} 이면 롱, "
                             f"> {100 - p['low']:.1f} 이면 숏. {p['exit']:.1f} 초과(롱)/{100 - p['exit']:.1f} 미만(숏)이면 청산."),
                  "n"),
    "mfi": _fam(b_mfi, {"n": ("int", 5, 60, True), "low": ("float", 5.0, 35.0), "exit": ("float", 40.0, 80.0)},
                "MFI (거래량 가중 RSI) 역추세", "Quong & Soudack (1989) 'Volume-Weighted RSI: Money Flow'",
                lambda p: (f"MFI({int(p['n'])}) < {p['low']:.1f} 이면 롱, > {100 - p['low']:.1f} 이면 숏. "
                           f"{p['exit']:.1f} 초과(롱)/{100 - p['exit']:.1f} 미만(숏)이면 청산."), "n"),
    "obv": _fam(b_obv, {"n": ("int", 5, 300, True), "w": ("int", 50, 2000, True),
                        "th": ("float", 0.5, 3.0), "mode": ("choice", [1, -1])},
                "OBV 거래량 모멘텀", "Granville (1963) 'New Key to Stock Market Profits'",
                lambda p: (f"OBV의 {int(p['n'])}봉 변화량을 {int(p['w'])}봉 z-score로 만든 값이 +{p['th']:.2f} 초과면 "
                           f"{'롱' if p['mode'] > 0 else '숏'}, -{p['th']:.2f} 미만이면 {'숏' if p['mode'] > 0 else '롱'}, "
                           f"0을 반대로 넘으면 청산."), "n"),
    "vwap_dev": _fam(b_vwap, {"n": ("int", 10, 1000, True), "k": ("float", 0.5, 4.0),
                              "mode": ("choice", ["revert", "trend"])},
                     "롤링 VWAP 이격", "Berkowitz, Logue & Noser (1988) 'The total cost of transactions on the NYSE', J. Finance",
                     lambda p: (f"(종가 - {int(p['n'])}봉 VWAP) ÷ ATR(14)가 "
                                + (f"-{p['k']:.2f} 미만이면 롱, +{p['k']:.2f} 초과면 숏 (역추세)"
                                   if p["mode"] == "revert" else
                                   f"+{p['k']:.2f} 초과면 롱, -{p['k']:.2f} 미만이면 숏 (추세)")
                                + ", VWAP를 다시 넘으면 청산."), "n"),
    "aroon": _fam(b_aroon, {"n": ("int", 10, 300, True), "th": ("float", 50.0, 100.0)},
                  "아룬 추세", "Chande (1995) 'Aroon', Technical Analysis of Stocks & Commodities",
                  lambda p: (f"Aroon({int(p['n'])}) Up ≥ {p['th']:.0f} 이고 Down ≤ {100 - p['th']:.0f} 이면 롱, "
                             f"반대면 숏, Up/Down이 뒤집히면 청산."), "n"),
    "psar": _fam(b_psar, {"step": ("float", 0.005, 0.05), "max_step": ("float", 0.05, 0.5)},
                 "파라볼릭 SAR", "Wilder (1978) 'New Concepts in Technical Trading Systems'",
                 lambda p: f"파라볼릭 SAR(가속 {p['step']:.3f}, 최대 {p['max_step']:.2f}) 방향대로 롱/숏, 반전 시 청산·전환.",
                 "step"),
    "linreg": _fam(b_linreg, {"n": ("int", 10, 500, True), "th": ("float", 1.0, 10.0),
                              "exit": ("float", -2.0, 3.0)},
                   "선형회귀 추세 유의성", "Lempérière et al. (2014) 'Two Centuries of Trend Following', J. Investment Strategies",
                   lambda p: (f"최근 {int(p['n'])}봉 로그가격 회귀 기울기의 t값이 +{p['th']:.2f} 초과면 롱, "
                              f"-{p['th']:.2f} 미만이면 숏, {min(p['exit'], p['th']):+.2f} 아래(롱)/위(숏)로 오면 청산."), "n"),
    "heikin": _fam(b_heikin, {"k": ("int", 1, 10, False), "exit_k": ("int", 1, 5, False)},
                   "하이킨아시 연속봉", "Valcu (2004) 'Using the Heikin-Ashi Technique', Technical Analysis of Stocks & Commodities",
                   lambda p: (f"하이킨아시 양봉이 {int(p['k'])}개 연속이면 롱, 음봉이 {int(p['k'])}개 연속이면 숏. "
                              f"반대색이 {int(p['exit_k'])}개 연속이면 청산."), "k"),
    "candle": _fam(b_candle, {"pattern": ("choice", list(CANDLE)), "exit_n": ("int", 5, 200, True)},
                   "캔들 패턴", "Nison (1991); Marshall, Young & Rose (2006) 'Candlestick technical trading strategies', "
                   "J. Banking & Finance; Lu, Shiu & Liu (2012) Rev. Financial Economics",
                   lambda p: f"{CANDLE[p['pattern']]} 상승형이면 롱, 하락형이면 숏. " + _ex(p), "exit_n"),
    "nr_breakout": _fam(b_nr, {"n": ("int", 4, 20, False), "exit_n": ("int", 5, 200, True)},
                        "NR 협폭봉 돌파", "Crabel (1990) 'Day Trading with Short Term Price Patterns and Opening Range Breakout'",
                        lambda p: (f"직전 봉이 최근 {int(p['n'])}봉 중 가장 좁은 봉(NR{int(p['n'])})이고 종가가 그 고가를 "
                                   f"돌파하면 롱, 저가를 이탈하면 숏. " + _ex(p)), "n"),
    "vol_breakout": _fam(b_volbreak, {"w": ("int", 50, 2000, True), "z": ("float", 1.0, 4.0),
                                      "n": ("int", 5, 100, True), "exit_n": ("int", 5, 200, True)},
                         "거래량 급증 돌파", "Gervais, Kaniel & Mingelgrin (2001) 'The High-Volume Return Premium', J. Finance",
                         lambda p: (f"거래량(로그)의 {int(p['w'])}봉 z-score > {p['z']:.2f} 이면서 종가가 직전 "
                                    f"{int(p['n'])}봉 고가 돌파 시 롱, 저가 이탈 시 숏. " + _ex(p)), "w"),
}
