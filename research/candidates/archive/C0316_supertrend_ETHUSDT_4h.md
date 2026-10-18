# 후보 C316 [C등급]: supertrend — ETHUSDT 4h

- 규칙: 슈퍼트렌드(ATR 7, ×5.63) 방향대로 롱/숏, 방향이 바뀌면 청산·전환. 추세장에서만: ADX(14) > 18. [롱만, 손절 ATR(14)×0.68]
- 권장 레버리지: 0.5x

| 구간 | 샤프 | 연수익 | 최대낙폭 |
|---|---|---|---|
| is | 1.24 | +63.9% | 33.9% |
| oos | 1.50 | +53.7% | 21.5% |
| ho | 1.46 | +52.4% | 31.8% |
| all | 1.29 | +59.4% | 33.9% |

`python run_strategy.py paper --pick C316`

```json
{
  "family": "supertrend",
  "tf": "4h",
  "p": {
    "n": 7,
    "mult": 5.6286,
    "filter": "adx_hi",
    "f_n": 44,
    "f_th": 0.1388,
    "htf": 2
  },
  "mod": {
    "direction": "long",
    "sl_k": 0.677,
    "tp_k": 0.0,
    "max_hold": 0
  },
  "universe": "ETHUSDT"
}
```
