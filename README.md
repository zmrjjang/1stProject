# Binance 선물 차트 데이터 수집기

바이낸스 USDT-M 무기한 선물에 상장된 코인 중 **시가총액 상위 10개**의
캔들(OHLCV) 데이터를 **5분 / 15분 / 30분 / 1시간 / 4시간 / 1일** 봉으로,
**상장 시점부터 가장 과거 데이터까지** 모두 받아 저장합니다. API 키는 필요 없습니다.

## 수집 대상 (2026-10-02 기준)

시가총액 순위(CoinGecko)에서 스테이블코인(USDT, USDC 등)과 래핑/스테이킹 토큰(stETH 등)을
제외하고, 바이낸스 USDT-M 무기한 선물이 있는 코인을 위에서부터 10개 고릅니다.

| 시총 순위 | 심볼 | 데이터 시작 |
|---|---|---|
| 1 | BTCUSDT | 2020-01 |
| 2 | ETHUSDT | 2020-01 |
| 4 | BNBUSDT | 2020-02 |
| 5 | XRPUSDT | 2020-01 |
| 7 | SOLUSDT | 2020-09 |
| 8 | TRXUSDT | 2020-01 |
| 10 | ZECUSDT | 2020-02 |
| 11 | HYPEUSDT | 2025-05 |
| 12 | DOGEUSDT | 2020-07 |
| 13 | LINKUSDT | 2020-01 |

실제 선택 결과와 시가총액은 실행할 때마다 `data/symbols.json`에 기록됩니다.

## 저장 형식

```
data/
  symbols.json                 # 선택된 코인 목록, 순위, 시총
  collector.log                # 실행 로그
  BTCUSDT/
    BTCUSDT_5m.csv.gz
    BTCUSDT_15m.csv.gz
    BTCUSDT_30m.csv.gz
    BTCUSDT_1h.csv.gz
    BTCUSDT_4h.csv.gz
    BTCUSDT_1d.csv.gz
  ETHUSDT/ ...
```

gzip 압축 CSV이며, 컬럼은 다음과 같습니다 (시간은 모두 UTC, `open_time`/`close_time`은 밀리초).

| 컬럼 | 설명 |
|---|---|
| datetime_utc | 캔들 시작 시각 (`YYYY-MM-DD HH:MM:SS`, UTC) |
| open_time | 캔들 시작 시각 (ms) |
| open, high, low, close | 시가, 고가, 저가, 종가 |
| volume | 거래량 (코인 수량) |
| close_time | 캔들 종료 시각 (ms) |
| quote_volume | 거래대금 (USDT) |
| trades | 체결 건수 |
| taker_buy_volume | 시장가 매수 거래량 |
| taker_buy_quote_volume | 시장가 매수 거래대금 (USDT) |

마감된 캔들만 저장합니다 (진행 중인 캔들은 저장하지 않음).

### pandas로 읽기

```python
import pandas as pd

df = pd.read_csv("data/BTCUSDT/BTCUSDT_1h.csv.gz", parse_dates=["datetime_utc"], index_col="datetime_utc")
print(df[["open", "high", "low", "close", "volume"]].tail())
```

## 실행 방법

```bash
pip install -r requirements.txt
python binance_futures_collector.py          # 상위 10개 코인 x 6개 봉 전부 수집/업데이트
python verify_data.py                        # 누락(갭)/중복 검사
```

다시 실행하면 **마지막으로 저장된 캔들 이후부터 이어서** 받습니다. 중간에 끊겨도
(네트워크 오류, Ctrl+C 등) 그냥 다시 실행하면 됩니다. 손상된 파일 끝부분은 자동 복구됩니다.

주요 옵션:

| 옵션 | 설명 |
|---|---|
| `--top 20` | 시총 상위 N개 (기본 10) |
| `--symbols BTCUSDT,ETHUSDT` | 코인을 직접 지정 |
| `--intervals 5m,1h` | 봉 지정 (기본 `5m,15m,30m,1h,4h,1d`) |
| `--source auto\|vision\|api` | 데이터 소스 (아래 참고, 기본 `auto`) |
| `--api-delay 0.5` | API 요청 간 대기 시간(초) |
| `--vision-delay 0.25` | 덤프 파일 요청 간 대기 시간(초) |
| `--verify-checksum` | 덤프 파일 SHA256 검증 (요청 수 2배) |

## 데이터 소스와 오류 방지

두 가지 바이낸스 공식 공개 소스를 사용합니다.

1. **data.binance.vision** – 바이낸스 공식 과거 데이터 덤프 (월별/일별 zip).
   과거 전체 기록을 빠르고 정확하게 받을 수 있습니다. 하루 정도 늦게 올라옵니다.
   일부 월별 파일이 잘려 있는 경우(예: 2022-02, 2022-03의 SOL/XRP/TRX/ZEC)가 있어,
   그 날짜는 일별 파일로 자동 보충합니다.
2. **fapi.binance.com** – 선물 REST API `/fapi/v1/klines`.
   `auto` 모드에서는 덤프 이후 ~ 현재까지의 최신 캔들을 채우고,
   덤프가 시작되는 2020-01 이전 데이터(BTC/ETH 등은 2019-09 상장)도 API로 채웁니다.

천천히, 오류 없이 받기 위해:

- 요청마다 최소 대기 시간을 둡니다 (API 0.5초, 덤프 0.25초).
- API 응답 헤더 `X-MBX-USED-WEIGHT-1M`을 확인해 한도(2400/분)의 절반인 1200에 도달하면 다음 분까지 쉽니다.
- HTTP 429/418(요청 제한)이면 `Retry-After`만큼 기다린 뒤 재시도합니다.
- 네트워크 오류·5xx 오류는 지수 백오프로 최대 8회 재시도합니다.
- 한 코인/봉이 실패해도 나머지는 계속 진행하고, 마지막에 실패 목록을 출력합니다.

> **참고:** 미국 등 일부 지역에서는 `fapi.binance.com`이 HTTP 451로 차단됩니다.
> 이 경우 자동으로 data.binance.vision만 사용하므로 데이터는 **전날까지**만 저장되고
> 2020-01 이전(BTC/ETH의 2019-09~12) 데이터는 빠집니다.
> 이 저장소에 포함된 데이터는 이 방식(차단된 환경)으로 2026-10-02에 수집되어 2026-09-30 ~ 10-01 캔들까지 들어 있습니다
> (코인마다 바이낸스의 일별 덤프 공개 시점이 달라 하루 차이가 있음).
> 바이낸스 API가 열리는 환경에서 다시 실행하면 최신 캔들까지 이어서 채웁니다.
