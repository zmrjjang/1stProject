# 후보 C345 [C등급]: psar — BTCUSDT 1d

- 규칙: 파라볼릭 SAR(가속 0.045, 최대 0.09) 방향대로 롱/숏, 반전 시 청산·전환. 횡보장에서만: ADX(14) < 29. [롱만, 최대 보유 59봉]
- 권장 레버리지: 1.0x

| 구간 | 샤프 | 연수익 | 최대낙폭 |
|---|---|---|---|
| is | 1.44 | +61.9% | 49.6% |
| oos | 1.08 | +36.6% | 28.3% |
| ho | 0.92 | +19.9% | 21.1% |
| all | 1.28 | +47.5% | 49.6% |

`python run_strategy.py paper --pick C345`

```json
{
  "family": "psar",
  "tf": "1d",
  "p": {
    "step": 0.0455,
    "max_step": 0.0854,
    "filter": "adx_lo",
    "f_n": 145,
    "f_th": 0.5648,
    "htf": 2
  },
  "mod": {
    "direction": "long",
    "sl_k": 0.0,
    "tp_k": 0.0,
    "max_hold": 59
  },
  "universe": "BTCUSDT"
}
```
