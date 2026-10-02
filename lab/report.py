"""Discovery reports (Korean markdown + json) and the discoveries index."""

import json
import math
import os
from datetime import datetime, timezone

import numpy as np

from .data import DAY_MS
from .families import FAMILIES

DIR_LABEL = {"both": "롱/숏 양방향", "long": "롱만", "short": "숏만"}


def recommended_leverage(stats, cfg):
    lv = cfg["leverage"]
    vol = stats["all"]["vol"]
    caps = [lv["max"]]
    if vol > 0:
        caps.append(lv["target_vol"] / vol)
    if stats["worst_mae"] < 0:
        caps.append(lv["liq_buffer"] / abs(stats["worst_mae"]))
    if stats["worst_day"] < 0:
        caps.append(lv["liq_buffer"] / abs(stats["worst_day"]))
    return max(0.5, math.floor(min(caps) * 2) / 2)


def yearly(daily, day0):
    out = {}
    years = ((np.arange(daily.size) + day0) * DAY_MS).astype("datetime64[ms]").astype("datetime64[Y]")
    for y in np.unique(years):
        seg = daily[(years == y) & np.isfinite(daily)]
        if seg.size:
            out[str(y)] = float(np.prod(1.0 + seg) - 1.0)
    return out


def describe(g):
    fam = FAMILIES[g["family"]]
    text = fam["rule"](g["p"])
    mod = g.get("mod") or {}
    extra = []
    if mod and g["family"] != "season":
        extra.append(DIR_LABEL[mod["direction"]])
    if mod.get("sl_k"):
        extra.append(f"손절 ATR(14)×{mod['sl_k']:.2f}")
    if mod.get("tp_k"):
        extra.append(f"익절 ATR(14)×{mod['tp_k']:.2f}")
    if mod.get("max_hold"):
        extra.append(f"최대 보유 {int(mod['max_hold'])}봉")
    return text + (" [" + ", ".join(extra) + "]" if extra else "")


def _pct(x):
    return f"{x * 100:+.1f}%"


def _row(label, s):
    return (f"| {label} | {s['days']} | {s['trades']} | {s['sharpe']:.2f} | {s['psr0']:.3f} | "
            f"{_pct(s['cagr'])} | {_pct(s['total_return'])} | {s['max_dd'] * 100:.1f}% |")


def write_discovery(out_dir, disc_id, g, stats, extra, daily, uni, cfg, link_base=None):
    fam = FAMILIES[g["family"]]
    lev = recommended_leverage(stats, cfg)
    slug = f"{disc_id:04d}_{g['family']}_{g['universe'].replace('/', '-')}_{g['tf']}"
    years = yearly(daily, uni.day0)
    split = cfg["split"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rule = describe(g)
    md = [
        f"# 전략 #{disc_id}: {fam['name']} — {g['universe']} {g['tf']}",
        "",
        f"- 발견 시각: {now}",
        f"- 근거 논문/이론: {fam['ref']}",
        f"- 규칙: {rule}",
        "- 체결 가정: 봉 마감에 신호 → 다음 봉 시가 체결, 손절/익절은 봉 내 고가/저가로 판정",
        f"- 비용 가정: 편도 {cfg['cost_per_side'] * 100:.3f}% (수수료+슬리피지), 롱 펀딩 {cfg['funding_8h'] * 100:.3f}%/8h",
        f"- 권장 레버리지: **{lev:g}x** (목표 연변동성 {cfg['leverage']['target_vol'] * 100:.0f}%, "
        f"과거 최악 역행폭이 증거금의 {cfg['leverage']['liq_buffer'] * 100:.0f}% 이내가 되도록 제한)",
        "",
        "## 성과 (레버리지 1x 기준)",
        "",
        "| 구간 | 일수 | 거래수 | 샤프 | PSR(>0) | 연수익 | 누적수익 | 최대낙폭 |",
        "|---|---|---|---|---|---|---|---|",
        _row(f"학습 IS (~{split['is_end']})", stats["is"]),
        _row(f"검증 OOS (~{split['oos_end']})", stats["oos"]),
        _row(f"홀드아웃 ({split['oos_end']}~)", stats["ho"]),
        _row("전체", stats["all"]),
        "",
        "## 과최적화 검정",
        "",
        f"- 학습구간 Deflated Sharpe Ratio: {extra['is_dsr']:.3f} (지금까지 시도한 전략 수 {extra['n_trials']:,}개 반영)",
        f"- 검증구간 Deflated Sharpe Ratio: {extra['oos_dsr']:.3f} (독립 검증 시도 {extra['n_oos']:,}개 반영)",
        f"- 홀드아웃 Deflated Sharpe Ratio: {extra['ho_dsr']:.3f} (홀드아웃 확인 {extra['n_ho']:,}회 반영)",
        f"- 비용 {cfg['gates']['stress_cost_mult']:g}배 스트레스 샤프 (IS+OOS): {extra['stress_sharpe']:.2f}",
        f"- 파라미터 근방 {extra['nb_n']}개 샤프 중앙값 (IS+OOS): {extra['nb_median']:.2f}, 양수 비율 {extra['nb_pos'] * 100:.0f}%",
        "",
        "## 연도별 수익률 (1x)",
        "",
        "| 연도 | 수익률 |",
        "|---|---|",
        *[f"| {y} | {_pct(r)} |" for y, r in years.items()],
        "",
        "## 파라미터",
        "",
        "```json",
        json.dumps(g, indent=2, ensure_ascii=False),
        "```",
        "",
        "> 과거 백테스트 결과이며 미래 수익을 보장하지 않습니다. 실거래 전 소액/모의 거래로 먼저 검증하세요.",
        "",
    ]
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, slug + ".md"), "w") as f:
        f.write("\n".join(md))
    with open(os.path.join(out_dir, slug + ".json"), "w") as f:
        json.dump({"id": disc_id, "genome": g, "stats": stats, "checks": extra, "leverage": lev,
                   "yearly": years, "found_at": now}, f, indent=2, ensure_ascii=False)
    np.save(os.path.join(out_dir, slug + ".npy"), daily.astype(np.float32))

    s_oos, s_ho = stats["oos"], stats["ho"]
    title = f"전략 발견 #{disc_id}: {fam['name']} {g['universe']} {g['tf']}"
    message = (f"검증 샤프 {s_oos['sharpe']:.2f} / 홀드아웃 샤프 {s_ho['sharpe']:.2f} / "
               f"전체 연수익 {_pct(stats['all']['cagr'])} / MDD {stats['all']['max_dd'] * 100:.0f}% (1x) / "
               f"권장 {lev:g}x\n{rule}")
    link = f"{link_base}/{slug}.md" if link_base else None
    return slug, title, message, "\n".join(md), link, lev


def write_index(out_dir, entries):
    lines = ["# 발견된 전략 목록", "",
             "| # | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for e in entries:
        lines.append(f"| {e['id']} | {e['name']} | {e['universe']} | {e['tf']} | {e['oos_sharpe']:.2f} | "
                     f"{e['ho_sharpe']:.2f} | {_pct(e['cagr'])} | {e['mdd'] * 100:.0f}% | {e['lev']:g}x | "
                     f"[보기]({e['slug']}.md) |")
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
