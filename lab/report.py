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


def write_discovery(out_dir, disc_id, g, stats, extra, daily, uni, cfg, link_base=None, kind="discovery",
                    grade=None):
    fam = FAMILIES[g["family"]]
    lev = recommended_leverage(stats, cfg)
    grade = grade or ("A" if kind == "discovery" else "C")
    tag = (f"C{disc_id}" if kind == "candidate" else f"#{disc_id}") + f" [{grade}등급]"
    slug = (f"{'C' if kind == 'candidate' else ''}{disc_id:04d}_{g['family']}_"
            f"{g['universe'].replace('/', '-')}_{g['tf']}")
    years = yearly(daily, uni.day0)
    split = cfg["split"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rule = describe(g)
    md = [
        f"# {'후보' if kind == 'candidate' else '전략'} {tag}: {fam['name']} — {g['universe']} {g['tf']}",
        "",
        *(["> 페이퍼 트레이딩 후보: 엄격한 과최적화 검정(Deflated Sharpe Ratio)을 통과하지 않았을 수 있습니다. "
           f"`python run_strategy.py paper --pick C{disc_id}` 로 모의매매해 보세요.", ""]
          if kind == "candidate" else []),
        f"- 발견 시각: {now}",
        f"- 근거 논문/이론: {fam['ref']}",
        f"- 규칙: {rule}",
        "- 체결 가정: 봉 마감에 신호 → 다음 봉 시가 체결, 손절/익절은 봉 내 고가/저가로 판정",
        f"- 비용 가정: 편도 {cfg['cost_per_side'] * 100:.3f}% (수수료+슬리피지), 실제 펀딩비 (롱 지불, 숏 수령)",
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
        json.dump({"id": disc_id, "grade": grade, "genome": g, "stats": stats, "checks": extra, "leverage": lev,
                   "yearly": years, "found_at": now}, f, indent=2, ensure_ascii=False)
    np.save(os.path.join(out_dir, slug + ".npy"), daily.astype(np.float32))

    s_oos, s_ho = stats["oos"], stats["ho"]
    title = f"{'후보' if kind == 'candidate' else '전략 발견'} {tag}: {fam['name']} {g['universe']} {g['tf']}"
    message = (f"검증 샤프 {s_oos['sharpe']:.2f} / 홀드아웃 샤프 {s_ho['sharpe']:.2f} / "
               f"전체 연수익 {_pct(stats['all']['cagr'])} / MDD {stats['all']['max_dd'] * 100:.0f}% (1x) / "
               f"권장 {lev:g}x\n{rule}")
    link = f"{link_base}/{slug}.md" if link_base else None
    return slug, title, message, "\n".join(md), link, lev


def write_index(out_dir, entries, kind="discovery"):
    cand = kind == "candidate"
    lines = ["# 페이퍼 트레이딩 후보 목록" if cand else "# 발견된 전략 목록", "",
             *(["엄격한 과최적화 검정 없이 검증·홀드아웃 구간 수익, 비용 스트레스, 파라미터 안정성만 통과한 후보입니다. "
                "같은 아이디어의 변형은 더 좋은 것이 나오면 교체되고, 목록은 min(검증, 홀드아웃 샤프) 상위 "
                "최대 50개만 유지합니다 (밀려난 후보는 [archive](archive/)에 보관되며 번호로 계속 실행 가능). "
                "`python run_strategy.py paper --pick C번호` 로 모의매매할 수 있습니다.", ""] if cand else []),
             "| # | 등급 | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 거래/년 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    order = (lambda e: (e.get("grade", "C") != "B", e["id"])) if cand else (lambda e: e["id"])
    for e in sorted(entries, key=order):
        lines.append(f"| {'C' if cand else ''}{e['id']} | {e.get('grade', 'C' if cand else 'A')} | {e['name']} | {e['universe']} | {e['tf']} | {e['oos_sharpe']:.2f} | "
                     f"{e['ho_sharpe']:.2f} | {e.get('tpy', 0):.0f} | {_pct(e['cagr'])} | {e['mdd'] * 100:.0f}% | {e['lev']:g}x | "
                     f"[보기]({e['slug']}.md) |")
    if not cand:
        lines += ["", "같은 전략의 변형(같은 계열·대상·방향이거나 일간수익률 상관 > 0.4)은 "
                      "알리지 않으며, 예전에 정리된 변형은 [variants](variants/) 폴더에 있습니다."]
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write("\n".join(lines) + "\n")


_LIVE_UNSUPPORTED = {"funding", "positioning", "oi_trend", "xs_carry"}
_TF_KO = {"5m": "5분봉", "15m": "15분봉", "30m": "30분봉", "1h": "1시간봉", "4h": "4시간봉", "1d": "일봉"}


def _short_section(rd):
    """Every active short-only strategy (any grade): they have their own candidate slots."""
    rows = []
    for folder, prefix in (("discoveries", "#"), ("candidates", "C")):
        path = os.path.join(rd, folder)
        if not os.path.isdir(path):
            continue
        for name in sorted(os.listdir(path)):
            if not name.endswith(".json"):
                continue
            with open(os.path.join(path, name)) as f:
                info = json.load(f)
            g = info["genome"]
            if (g.get("mod") or {}).get("direction") == "short":
                rows.append((prefix + str(info["id"]), f"research/{folder}/{name[:-5]}.md", info,
                             "A" if prefix == "#" else info.get("grade", "C")))
    L = ["", "## 숏 전용 전략", "",
         "하락에 베팅하는 전략만 따로 모았습니다 (C등급 포함). 숏 전용 후보는 롱 전략과 순위 경쟁 없이 별도 자리를 가집니다. "
         "`python run_strategy.py paper --pick S --paper-dir paper_S --loop` 로 한꺼번에 모의매매할 수 있습니다.", ""]
    if not rows:
        return L + ["(아직 없음)"]
    L += ["| 등급 | 번호 | 전략 | 대상 | 봉 | 학습 샤프 | 검증 샤프 | 최근 샤프 | 연수익 | 최대낙폭 | 상세 |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    rows.sort(key=lambda r: -min(r[2]["stats"]["oos"]["sharpe"], r[2]["stats"]["ho"]["sharpe"]))
    for ref, md, info, grade in rows:
        g, st = info["genome"], info["stats"]
        L.append(f"| {grade} | {ref} | {FAMILIES[g['family']]['name']} | {g['universe']} | {g['tf']} | "
                 f"{st['is']['sharpe']:.2f} | {st['oos']['sharpe']:.2f} | {st['ho']['sharpe']:.2f} | "
                 f"{_pct(st['all']['cagr'])} | {st['all']['max_dd'] * 100:.0f}% | [보기]({md}) |")
    return L


def write_grades(root, cfg):
    """GRADES.md: every A and B strategy with rules, performance and settings on one page."""
    rd = os.path.join(root, "research")
    items = []
    for folder, kind in (("discoveries", "A"), ("candidates", None)):
        path = os.path.join(rd, folder)
        if not os.path.isdir(path):
            continue
        for name in sorted(os.listdir(path)):
            if not name.endswith(".json"):
                continue
            with open(os.path.join(path, name)) as f:
                info = json.load(f)
            grade = kind or info.get("grade", "C")
            if grade in ("A", "B"):
                items.append((grade, ("#" if kind else "C") + str(info["id"]), f"research/{folder}/{name[:-5]}.md", info))
    items.sort(key=lambda x: (x[0], int(x[1].lstrip("#C"))))
    b = cfg["b_grade"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    split = cfg["split"]
    L = [
        "# A·B 등급 전략 모음",
        "",
        f"자동 탐색기가 갱신합니다 (마지막 갱신: {now}). 백테스트 기간: 학습 ~{split['is_end']} / "
        f"검증 ~{split['oos_end']} / 홀드아웃(최근) {split['oos_end']}~. 모든 수치는 레버리지 1x, 비용 반영 기준.",
        "",
        "- **A등급**: 엄격한 과최적화 검정(Deflated Sharpe Ratio)까지 통과",
        f"- **B등급**: 학습·검증·홀드아웃 샤프 모두 ≥ {b['min_sharpe_every_period']}, 최대낙폭 ≤ {b['max_dd'] * 100:.0f}%, "
        f"거래 ≥ {b['min_trades']}회, 비용 2배 샤프 ≥ {b['min_stress_sharpe']}, "
        f"파라미터 근방 {b['min_neighbors_positive'] * 100:.0f}% 이상 수익 (DSR 검정 없음)",
        "- 'ALL'은 10개 코인 각각에 같은 규칙을 적용하고 자금을 1/10씩 배분한다는 뜻입니다.",
        "",
        "## 모의매매 실행",
        "",
        "```bash",
        "git pull && pip install -r requirements.txt",
        "python run_strategy.py paper --pick A --paper-dir paper_A --loop   # A등급 전체",
        "python run_strategy.py paper --pick B --paper-dir paper_B --loop   # B등급 전체",
        "python run_strategy.py paper --pick C1,C20 --loop                  # 원하는 번호만",
        "```",
        "",
        *_recent_ab_changes(root),
        "## 요약",
        "",
        "| 등급 | 번호 | 전략 | 대상 | 봉 | 방향 | 학습 샤프 | 검증 샤프 | 최근 샤프 | 거래/년 | 연수익 | 최대낙폭 | 권장 레버리지 |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for grade, ref, md, info in items:
        g, s = info["genome"], info["stats"]
        fam = FAMILIES[g["family"]]
        direction = DIR_LABEL.get((g.get("mod") or {}).get("direction", ""), "포트폴리오")
        L.append(f"| {grade} | [{ref}](#{ref.lower().lstrip('#')}) | {fam['name']} | {g['universe']} | {g['tf']} | {direction} | "
                 f"{s['is']['sharpe']:.2f} | {s['oos']['sharpe']:.2f} | {s['ho']['sharpe']:.2f} | "
                 f"{s['all']['trades'] / max(s['all']['days'], 1) * 365.25:.0f} | "
                 f"{_pct(s['all']['cagr'])} | {s['all']['max_dd'] * 100:.0f}% | {info.get('leverage', 1):g}x |")
    L += _short_section(rd)
    L += ["", "## 전략별 상세", ""]
    for grade, ref, md, info in items:
        g, s, c = info["genome"], info["stats"], info.get("checks", {})
        fam = FAMILIES[g["family"]]
        live = fam["kind"] == "single" and g["family"] not in _LIVE_UNSUPPORTED
        uni = "10개 코인 전체 (코인당 자금 1/10)" if g["universe"] == "ALL" else g["universe"]
        years = " · ".join(f"{y} {_pct(r)}" for y, r in (info.get("yearly") or {}).items())
        L += [
            f'<a id="{ref.lower().lstrip("#")}"></a>',
            f"### {grade}등급 {ref} — {fam['name']} ({uni}, {_TF_KO.get(g['tf'], g['tf'])})",
            "",
            f"- **규칙**: {describe(g)}",
            "- **체결**: 봉 마감에 신호 확인 → 다음 봉 시가에 시장가. 손절/익절은 진입가 기준 ATR(14) 배수로 미리 걸어둠",
            f"- **권장 레버리지**: {info.get('leverage', 1):g}x"
            + ("" if live else "  ·  ⚠️ 아직 실시간 모의매매 미지원 (포트폴리오형/파생데이터 전략)"),
            f"- **모의매매**: `python run_strategy.py paper --pick {ref.lstrip('#')} --loop`" if live else "",
            "",
            "| 구간 | 샤프 | 연수익 | 최대낙폭 | 거래수 |",
            "|---|---|---|---|---|",
            *[f"| {label} | {s[k]['sharpe']:.2f} | {_pct(s[k]['cagr'])} | {s[k]['max_dd'] * 100:.1f}% | {s[k]['trades']} |"
              for k, label in (("is", "학습"), ("oos", "검증"), ("ho", "홀드아웃(최근)"), ("all", "전체"))],
            "",
            f"- **연도별 수익률**: {years}" if years else "",
            f"- **강건성**: 비용 2배 샤프 {c.get('stress_sharpe', 0):.2f} · 파라미터 근방 수익 비율 "
            f"{c.get('nb_pos', 0) * 100:.0f}% · 근거: {fam['ref']}",
            f"- **상세 보고서**: [{os.path.basename(md)}]({md})",
            "",
            "<details><summary>파라미터 (JSON)</summary>",
            "",
            "```json",
            json.dumps(g, indent=2, ensure_ascii=False),
            "```",
            "</details>",
            "",
        ]
    L.append("> 모든 성과는 과거 백테스트입니다. 실거래 전 모의매매로 확인하세요.")
    with open(os.path.join(root, "GRADES.md"), "w") as f:
        f.write("\n".join(x for x in L if x is not None) + "\n")
    return len(items)



def change_summary(ref, info, grade):
    """Compact description of one strategy version for the change log."""
    g, st = info["genome"], info["stats"]
    return {"ref": ref, "grade": grade, "name": FAMILIES[g["family"]]["name"], "universe": g["universe"],
            "tf": g["tf"], "rule": describe(g), "oos": round(st["oos"]["sharpe"], 2), "ho": round(st["ho"]["sharpe"], 2),
            "cagr": round(st["all"]["cagr"], 4), "mdd": round(st["all"]["max_dd"], 4),
            "lev": info.get("leverage", 1), "genome": g}


def _short(x):
    return (f"{x['name']} {x['universe']} {x['tf']} · 검증 {x['oos']:.2f} / 최근 {x['ho']:.2f} · "
            f"연 {_pct(x['cagr'])} · MDD {x['mdd'] * 100:.0f}%") if x else "-"


KIND_KO = {"new": "신규", "replaced": "교체(개선)", "archived": "밀려남", "restored": "복원", "discovery": "A 신규"}


def write_changelog(root, limit=400):
    """research/CHANGELOG.md from research/changes.jsonl (newest first)."""
    path = os.path.join(root, "research", "changes.jsonl")
    events = []
    if os.path.exists(path):
        with open(path) as f:
            events = [json.loads(x) for x in f if x.strip()]
    events = events[::-1][:limit]
    L = ["# 전략 변경 기록", "",
         "탐색기가 전략을 새로 추가·교체(같은 번호로 더 좋은 변형)·밀어낼 때마다 자동으로 기록합니다 (최신이 위). "
         "등급 현황은 [GRADES.md](../GRADES.md).", "",
         "| 시각 (UTC) | 종류 | 번호 | 등급 | 이전 | 이후 |", "|---|---|---|---|---|---|"]
    for e in events:
        old, new = e.get("old"), e.get("new")
        grade = (f"{old['grade']}→{new['grade']}" if old and new and old["grade"] != new["grade"]
                 else (new or old)["grade"])
        L.append(f"| {e['time'][:16].replace('T', ' ')} | {KIND_KO.get(e['kind'], e['kind'])} | {e['ref']} | {grade} | "
                 f"{_short(old)} | {_short(new)} |")
    L += ["", "## 교체·신규 상세 (A·B 등급, 최근 50건)", ""]
    n = 0
    for e in events:
        new, old = e.get("new"), e.get("old")
        if not new or new["grade"] not in ("A", "B") or e["kind"] == "archived":
            continue
        L += [f"### {e['time'][:16].replace('T', ' ')} · {e['ref']} {KIND_KO.get(e['kind'], e['kind'])}", ""]
        if old:
            L += [f"- **이전** ({old['grade']}): {old['rule']}", f"  - {_short(old)}"]
        L += [f"- **이후** ({new['grade']}): {new['rule']}", f"  - {_short(new)} · 권장 레버리지 {new['lev']:g}x", ""]
        n += 1
        if n >= 50:
            break
    with open(os.path.join(root, "research", "CHANGELOG.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    return events



def _recent_ab_changes(root, n=15):
    path = os.path.join(root, "research", "changes.jsonl")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        events = [json.loads(x) for x in f if x.strip()]
    rows = []
    for e in reversed(events):
        old, new = e.get("old"), e.get("new")
        if not any(x and x["grade"] in ("A", "B") for x in (old, new)):
            continue
        what = {"new": "B 편입" if new and new["grade"] == "B" else "신규", "discovery": "A 신규",
                "archived": "밀려남", "replaced": "교체"}.get(e["kind"], e["kind"])
        if e["kind"] == "replaced" and old and new and old["grade"] != new["grade"]:
            what = f"교체 ({old['grade']}→{new['grade']})"
        rows.append(f"| {e['time'][:16].replace('T', ' ')} | {e['ref']} | {what} | {_short(new or old)} |")
        if len(rows) >= n:
            break
    if not rows:
        return []
    return ["## 최근 변경 (A·B 관련)", "", "같은 번호로 내용이 바뀐 전략은 모의매매를 다시 시작하세요. "
            "전체 기록: [research/CHANGELOG.md](research/CHANGELOG.md)", "",
            "| 시각 (UTC) | 번호 | 변경 | 현재 내용 |", "|---|---|---|---|", *rows, ""]
