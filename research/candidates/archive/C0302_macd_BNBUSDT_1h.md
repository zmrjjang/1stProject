# 후보 C302: macd — BNBUSDT 1h

- 규칙: MACD(13,65,16) 라인 ÷ ATR(14)가 +0.23 초과면 롱, -0.23 미만이면 숏, 0을 반대로 넘으면 청산. 고변동성에서만: ATR% z-score(172) > +1.25. [롱만, 익절 ATR(14)×5.58]
- 권장 레버리지: 1.0x

| 구간 | 샤프 | 연수익 | 최대낙폭 |
|---|---|---|---|
| is | 1.33 | +44.1% | 17.7% |
| oos | 1.49 | +36.9% | 12.3% |
| ho | 1.30 | +21.7% | 9.2% |
| all | 1.32 | +38.0% | 17.7% |

`python run_strategy.py paper --pick C302`

```json
{
  "family": "macd",
  "tf": "1h",
  "p": {
    "fast": 13,
    "ratio": 5.0,
    "sig": 16,
    "th": 0.2342,
    "mode": "line",
    "filter": "vol_hi",
    "f_n": 172,
    "f_th": 0.9154,
    "htf": 1
  },
  "mod": {
    "direction": "long",
    "sl_k": 0.0,
    "tp_k": 5.575,
    "max_hold": 0
  },
  "universe": "BNBUSDT"
}
```
