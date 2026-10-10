# 선물 전략 자동 탐색기 (Strategy Lab)

수집한 차트 데이터(10개 코인 × 6개 봉)로 **선물 매매전략을 끝없이 생성·검증**하고,
통계 검정을 모두 통과한 전략만 골라 **발견될 때마다 알림**을 보냅니다.
탐색은 GitHub Actions(무료)에서 6시간마다 5.5시간씩 자동으로 돌아가므로 사실상 24시간 쉬지 않고 동작하며,
**Claude 토큰을 전혀 쓰지 않습니다.**

## 알림 받는 법

| 방법 | 설정 |
|---|---|
| **GitHub 이슈** (기본) | 설정 불필요. 발견 시 이 저장소에 이슈가 생성되고 GitHub 이메일/앱 알림이 옵니다. |
| **휴대폰 푸시 (ntfy)** | [ntfy 앱](https://ntfy.sh) 설치 → 구독(Subscribe) → 토픽 `zmr-strategy-32bdb26924` 입력. 공개 토픽이므로 비공개로 쓰려면 저장소 Settings → Secrets → Actions에 `NTFY_TOPIC`을 다른 이름으로 등록하세요. |
| 텔레그램 (선택) | Secrets에 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` 등록 |
| 디스코드 (선택) | Secrets에 `DISCORD_WEBHOOK_URL` 등록 |

발견된 전략은 [`research/discoveries/`](research/discoveries/)에 한국어 보고서로 저장됩니다
(규칙, 구간별 성과, 연도별 수익률, 과최적화 검정 결과, 권장 레버리지, 파라미터).
누적 진행 상황(시도 횟수, 검증 통과 수 등)은 `research/state.json`에 있습니다.

## 어떻게 찾나

### 1. 전략 공간 — 학술적 근거가 있는 15개 계열

| 계열 | 근거 |
|---|---|
| 시계열 모멘텀 (변동성 정규화) | Moskowitz, Ooi & Pedersen (2012) *J. Financial Economics* |
| 이동평균 교차 | Brock, Lakonishok & LeBaron (1992) *J. Finance* |
| 돈치안 채널 돌파 (터틀) | Hurst, Ooi & Pedersen (2017) *A Century of Evidence on Trend-Following* |
| Ornstein-Uhlenbeck 평균회귀 | Avellaneda & Lee (2010) *Quantitative Finance* |
| RSI 역추세 | Wilder (1978); Connors & Alvarez (2009) |
| 변동성 수축 후 돌파 | Bollerslev (1986) GARCH; Bollinger (2001) |
| 테이커 주문흐름 불균형 | Cont, Kukanov & Stoikov (2014); Easley, López de Prado & O'Hara (2012) VPIN |
| 국면 전환 (추세/횡보) | Kaufman (1995) 효율비율; Lo & MacKinlay (1988) 분산비율 |
| 시간대 계절성 | Eross et al. (2019) *The intraday dynamics of bitcoin* |
| 횡단면 모멘텀/리버설 | Jegadeesh & Titman (1993); Liu, Tsyvinski & Wu (2022) *J. Finance* |
| 페어 트레이딩 (공적분) | Engle & Granger (1987); Gatev, Goetzmann & Rouwenhorst (2006) *RFS* |
| **펀딩비 쏠림** (추종/역행) | He, Manela, Ross & von Wachter (2022); Ackerer, Hugonnier & Jermann (2024) *Math. Finance* |
| **롱/숏 비율 포지셔닝** (전체 계정, 상위 트레이더, 둘의 차이) | Kogan, Makarov, Niessner & Schoar (2024) *JFE*; Wang (2003) *J. Futures Markets* |
| **미결제약정(OI) × 가격** (신규자금 추종 / 청산 소진 역행) | Hong & Yogo (2012) *JFE*; Bessembinder & Seguin (1993) *JFQA* |
| **횡단면 펀딩 캐리** | Schmeling, Schrimpf & Todorov (2023) *Crypto Carry*; Koijen et al. (2018) *Carry*, *JFE* |

굵게 표시한 4개는 가격 외 정보(펀딩비, 미결제약정, 롱/숏 비율 — `collect_derivatives.py`로 수집)를 쓰며,
탐색 시 다른 계열보다 3배 자주 시도됩니다. 이 데이터는 해당 봉이 마감되기 **최소 5분 전에 공개된 값만** 사용합니다
(펀딩비는 정산 시점 이후). 미결제약정·비율 데이터는 BTC 2020-09, 나머지 대부분 2021-12부터 있습니다.

여기에 공통 옵션(롱/숏/양방향, ATR 손절·익절, 최대 보유기간)과 대상(코인 1개 또는 10개 전체 동일비중)을 조합합니다.

### 2. 탐색 — 유전 알고리즘

선택(토너먼트) · 교차 · 돌연변이 · 무작위 이민자 · 정체 시 재시작을 반복하며 학습구간 성과가 좋은 전략을 진화시킵니다.

### 3. 백테스트 가정 (보수적)

- 봉 마감에 신호 → **다음 봉 시가**에 체결 (미래 데이터 사용 없음)
- 손절/익절은 봉 내 고가/저가로 판정, 같은 봉에서 둘 다 닿으면 **손절 먼저**
- 편도 비용 **0.07%** (테이커 수수료 0.05% + 슬리피지 0.02%), 롱 포지션 펀딩비 0.01%/8시간
- 성과는 레버리지 1x 기준, 권장 레버리지는 별도 계산

### 4. 과최적화 방지 — 5단계 관문

수많은 전략을 시도하면 우연히 좋아 보이는 전략이 반드시 나옵니다. 그래서 다음을 **모두** 통과해야만 알림을 보냅니다.

| 단계 | 데이터 | 조건 |
|---|---|---|
| ① 학습 (IS) | ~2023-12 | 샤프 ≥ 1.0, PSR ≥ 0.95, 최소 거래수, 낙폭 ≤ 60% |
| ② 검증 (OOS) | 2024-01 ~ 2025-06 | 샤프 ≥ 0.8, **Deflated Sharpe Ratio ≥ 0.9**, 수익 > 0, 낙폭 ≤ 50% |
| ③ 강건성 | IS+OOS | 비용 2배에서도 샤프 ≥ 0.4, 파라미터를 조금씩 바꾼 8개 중 75% 이상 수익 (뾰족한 봉우리가 아닌 고원) |
| ④ 중복 제거 | IS+OOS | 이미 발견한 전략과 **같은 계열·대상·방향**(예: 모멘텀/10코인/롱만)이거나 일간수익률 상관 > 0.4이면 같은 전략의 변형으로 보고 제외 |
| ⑤ 홀드아웃 | 2025-07 ~ | 샤프 ≥ 0.5, 수익 > 0, **홀드아웃 DSR ≥ 0.5** |

- **PSR** (Bailey & López de Prado 2012): 표본 길이·왜도·첨도를 반영해 "진짜 샤프 > 0"일 확률
- **DSR** (Bailey & López de Prado 2014): 지금까지 시도한 독립 전략 수 N을 반영해, 실력 없는 N개 중 최고값보다 나을 확률.
  시도가 늘수록 기준이 자동으로 엄격해집니다. 독립 시도 수 N은 "계열 × 봉 × 대상 × 방향 × 선택옵션 × 주 기간의 2배수 구간"으로
  묶은 클러스터 중 실제 시도된 수이며(HyperLogLog로 집계), 탐색 공간 전체의 클러스터 수(약 2.7만 개)를 넘을 수 없습니다.
  같은 클러스터 안의 전략들은 진입·청산 문턱만 달라 서로 강하게 상관되므로 독립 시도로 보지 않습니다 (López de Prado 2019).
- 홀드아웃은 앞 단계를 모두 통과한 전략에만 공개되며, 몇 번 들여다봤는지도 DSR에 반영합니다.

`python strategy_search.py --prune`을 실행하면 기존 발견 목록에도 같은 규칙을 다시 적용합니다
(그룹마다 min(검증 샤프, 홀드아웃 샤프)가 가장 높은 것만 남기고 나머지는 `variants/`로 이동).

## 직접 실행 (선택)

```bash
pip install -r requirements-lab.txt
python strategy_search.py              # 무한 실행 (Ctrl+C로 중지, 다시 실행하면 이어서)
python strategy_search.py --hours 2    # 2시간만
```

설정(구간 분할, 비용, 관문 기준, 유전 알고리즘 크기)은 `research/config.json`에서 바꿀 수 있습니다.

## 주의

- 백테스트 성과는 미래 수익을 보장하지 않습니다. 발견된 전략도 **소액 또는 모의 거래로 먼저 검증**하세요.
- 같은 과거 데이터로 무한히 탐색할수록 우연히 맞는 전략이 섞일 위험이 커집니다. 위 관문들이 그 위험을 줄이지만 0으로 만들지는 못합니다.
- 데이터는 2026-10-01까지 고정되어 있습니다. 시간이 지나 새 데이터가 쌓이면 `binance_futures_collector.py`로 갱신해 홀드아웃 이후 실제 성과를 다시 확인하는 것이 가장 강력한 검증입니다.
- 공개 저장소에서는 60일간 저장소 활동이 없으면 GitHub가 예약 실행을 멈출 수 있습니다. 탐색기가 매 실행마다 결과를 커밋하므로 보통은 유지되지만, 멈췄다면 Actions 탭에서 다시 켜면 됩니다.
