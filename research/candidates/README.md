# 페이퍼 트레이딩 후보 목록

엄격한 과최적화 검정 없이 검증·홀드아웃 구간 수익, 비용 스트레스, 파라미터 안정성만 통과한 후보입니다. 같은 아이디어의 변형은 더 좋은 것이 나오면 교체됩니다. `python run_strategy.py paper --pick C번호` 로 모의매매할 수 있습니다.

| # | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |
|---|---|---|---|---|---|---|---|---|---|
| C1 | 선형회귀 추세 유의성 | ALL | 30m | 2.40 | 2.30 | +35.4% | 16% | 1x | [보기](C0001_linreg_ALL_30m.md) |
| C2 | MACD | ALL | 1d | 2.06 | 2.70 | +43.9% | 18% | 0.5x | [보기](C0002_macd_ALL_1d.md) |
| C3 | 거래량 급증 돌파 | ALL | 30m | 2.37 | 2.19 | +21.0% | 8% | 1x | [보기](C0003_vol_breakout_ALL_30m.md) |
| C4 | 켈트너 채널 | ALL | 30m | 2.45 | 2.26 | +6.2% | 5% | 1x | [보기](C0004_keltner_ALL_30m.md) |
| C5 | 켈트너 채널 | ETHUSDT | 30m | 1.93 | 2.29 | +17.0% | 7% | 3.5x | [보기](C0005_keltner_ETHUSDT_30m.md) |
| C6 | 선형회귀 추세 유의성 | ALL | 1h | 1.65 | 1.79 | +22.6% | 31% | 1x | [보기](C0006_linreg_ALL_1h.md) |
| C7 | 돈치안 채널 돌파 (터틀) | XRPUSDT | 1h | 1.65 | 1.74 | +63.8% | 52% | 0.5x | [보기](C0007_donchian_XRPUSDT_1h.md) |
| C8 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 1h | 2.07 | 2.03 | +29.2% | 17% | 2x | [보기](C0008_squeeze_ALL_1h.md) |
| C9 | 캔들 패턴 | ALL | 4h | 2.08 | 1.98 | +37.8% | 19% | 0.5x | [보기](C0009_candle_ALL_4h.md) |
| C10 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 4h | 1.52 | 1.65 | +53.9% | 34% | 0.5x | [보기](C0010_squeeze_SOLUSDT_4h.md) |
| C11 | 켈트너 채널 | ALL | 15m | 2.57 | 2.61 | +5.2% | 4% | 2.5x | [보기](C0011_keltner_ALL_15m.md) |
| C12 | 거래량 급증 돌파 | ALL | 4h | 1.47 | 1.58 | +23.8% | 24% | 0.5x | [보기](C0012_vol_breakout_ALL_4h.md) |
| C13 | Ornstein-Uhlenbeck 평균회귀 (z-score) | ALL | 1h | 1.86 | 1.72 | +6.7% | 4% | 1x | [보기](C0013_zscore_mr_ALL_1h.md) |
| C14 | 거래량 급증 돌파 | ALL | 30m | 2.31 | 2.07 | +19.5% | 8% | 1x | [보기](C0014_vol_breakout_ALL_30m.md) |
| C15 | 시계열 모멘텀 (변동성 정규화) | XRPUSDT | 4h | 1.74 | 0.61 | +55.0% | 51% | 0.5x | [보기](C0015_tsmom_XRPUSDT_4h.md) |
| C16 | RSI 과매도/과매수 역추세 | DOGEUSDT | 30m | 1.18 | 1.08 | +18.8% | 8% | 2.5x | [보기](C0016_rsi_mr_DOGEUSDT_30m.md) |
| C17 | Ornstein-Uhlenbeck 평균회귀 (z-score) | XRPUSDT | 15m | 1.50 | 2.15 | +25.5% | 42% | 1x | [보기](C0017_zscore_mr_XRPUSDT_15m.md) |
| C18 | Ornstein-Uhlenbeck 평균회귀 (z-score) | DOGEUSDT | 5m | 1.16 | 1.72 | +31.8% | 17% | 1.5x | [보기](C0018_zscore_mr_DOGEUSDT_5m.md) |
| C19 | 캔들 패턴 | ALL | 1d | 1.92 | 2.04 | +43.1% | 31% | 1.5x | [보기](C0019_candle_ALL_1d.md) |
| C20 | 아룬 추세 | ALL | 4h | 2.49 | 2.28 | +34.4% | 12% | 0.5x | [보기](C0020_aroon_ALL_4h.md) |
| C21 | MACD | ALL | 1d | 2.01 | 2.09 | +54.3% | 27% | 1x | [보기](C0021_macd_ALL_1d.md) |
| C22 | 선형회귀 추세 유의성 | DOGEUSDT | 1h | 1.64 | 1.57 | +99.7% | 55% | 0.5x | [보기](C0022_linreg_DOGEUSDT_1h.md) |
| C23 | 일목균형표 | ALL | 4h | 1.72 | 1.72 | +12.5% | 11% | 0.5x | [보기](C0023_ichimoku_ALL_4h.md) |
| C24 | 거래량 급증 돌파 | ALL | 30m | 1.37 | 2.13 | +12.0% | 11% | 1x | [보기](C0024_vol_breakout_ALL_30m.md) |
| C25 | MACD | SOLUSDT | 4h | 2.12 | 1.56 | +42.2% | 33% | 1x | [보기](C0025_macd_SOLUSDT_4h.md) |
| C26 | 거래량 급증 돌파 | ETHUSDT | 15m | 2.18 | 2.10 | +5.9% | 5% | 5x | [보기](C0026_vol_breakout_ETHUSDT_15m.md) |
| C27 | 테이커 주문흐름 불균형 | ALL | 4h | 1.99 | 1.96 | +30.1% | 34% | 0.5x | [보기](C0027_flow_ALL_4h.md) |
| C28 | OBV 거래량 모멘텀 | ALL | 4h | 2.17 | 2.22 | +13.1% | 11% | 1.5x | [보기](C0028_obv_ALL_4h.md) |
| C29 | 선형회귀 추세 유의성 | SOLUSDT | 4h | 2.21 | 1.54 | +149.6% | 52% | 0.5x | [보기](C0029_linreg_SOLUSDT_4h.md) |
| C30 | 시계열 모멘텀 (변동성 정규화) | ETHUSDT | 30m | 1.33 | 1.76 | +31.6% | 22% | 1.5x | [보기](C0030_tsmom_ETHUSDT_30m.md) |
| C31 | MACD | BTCUSDT | 4h | 1.28 | 1.29 | +34.3% | 32% | 1x | [보기](C0031_macd_BTCUSDT_4h.md) |
| C32 | 아룬 추세 | ALL | 4h | 1.38 | 1.69 | +43.2% | 19% | 0.5x | [보기](C0032_aroon_ALL_4h.md) |
| C33 | 켈트너 채널 | ALL | 1h | 2.14 | 1.81 | +12.6% | 10% | 1x | [보기](C0033_keltner_ALL_1h.md) |
| C34 | 미결제약정(OI) × 가격 | ALL | 30m | 1.79 | 1.58 | +9.2% | 9% | 0.5x | [보기](C0034_oi_trend_ALL_30m.md) |
| C35 | 미결제약정(OI) × 가격 | ALL | 30m | 1.83 | 1.40 | +8.9% | 4% | 0.5x | [보기](C0035_oi_trend_ALL_30m.md) |
| C36 | 롤링 VWAP 이격 | ALL | 1h | 1.30 | 1.42 | +30.6% | 22% | 0.5x | [보기](C0036_vwap_dev_ALL_1h.md) |
| C37 | ADX/DMI 추세 | ALL | 4h | 1.63 | 1.57 | +24.5% | 15% | 0.5x | [보기](C0037_adx_dmi_ALL_4h.md) |
| C38 | 돈치안 채널 돌파 (터틀) | BTCUSDT | 30m | 1.39 | 1.22 | +27.8% | 30% | 1.5x | [보기](C0038_donchian_BTCUSDT_30m.md) |
| C39 | 파라볼릭 SAR | ALL | 1d | 1.71 | 2.39 | +16.6% | 13% | 1x | [보기](C0039_psar_ALL_1d.md) |
| C40 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 2.19 | 2.09 | +19.7% | 11% | 1x | [보기](C0040_regime_ALL_4h.md) |
| C41 | 이동평균 교차 추세추종 | ALL | 4h | 1.94 | 1.74 | +14.4% | 11% | 2x | [보기](C0041_ma_cross_ALL_4h.md) |
| C42 | 캔들 패턴 | SOLUSDT | 4h | 1.87 | 2.81 | +67.3% | 48% | 0.5x | [보기](C0042_candle_SOLUSDT_4h.md) |
| C43 | 아룬 추세 | ALL | 4h | 1.42 | 1.75 | +18.4% | 14% | 0.5x | [보기](C0043_aroon_ALL_4h.md) |
| C44 | 시계열 모멘텀 (변동성 정규화) | ALL | 4h | 1.63 | 1.60 | +36.8% | 33% | 0.5x | [보기](C0044_tsmom_ALL_4h.md) |
| C45 | 아룬 추세 | ETHUSDT | 4h | 1.41 | 1.21 | +53.5% | 37% | 0.5x | [보기](C0045_aroon_ETHUSDT_4h.md) |
| C46 | 켈트너 채널 | ETHUSDT | 30m | 1.75 | 1.76 | +22.2% | 10% | 2x | [보기](C0046_keltner_ETHUSDT_30m.md) |
| C47 | 페어 트레이딩 (공적분 스프레드 평균회귀) | SOLUSDT/BNBUSDT | 1h | 1.03 | 1.15 | +30.4% | 30% | 1x | [보기](C0047_pairs_SOLUSDT-BNBUSDT_1h.md) |
| C48 | OBV 거래량 모멘텀 | LINKUSDT | 30m | 1.16 | 1.15 | +20.3% | 23% | 2x | [보기](C0048_obv_LINKUSDT_30m.md) |
| C49 | 캔들 패턴 | ALL | 4h | 1.80 | 1.62 | +17.4% | 11% | 1.5x | [보기](C0049_candle_ALL_4h.md) |
| C50 | 켈트너 채널 | ETHUSDT | 1h | 1.87 | 1.40 | +42.9% | 33% | 1x | [보기](C0050_keltner_ETHUSDT_1h.md) |
| C51 | 롤링 VWAP 이격 | SOLUSDT | 1h | 1.37 | 1.41 | +26.7% | 12% | 2x | [보기](C0051_vwap_dev_SOLUSDT_1h.md) |
| C52 | OBV 거래량 모멘텀 | TRXUSDT | 4h | 1.22 | 0.55 | +23.2% | 38% | 1.5x | [보기](C0052_obv_TRXUSDT_4h.md) |
| C53 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 1d | 1.63 | 1.76 | +22.3% | 14% | 1x | [보기](C0053_regime_ALL_1d.md) |
| C54 | 켈트너 채널 | SOLUSDT | 30m | 1.96 | 1.86 | +23.1% | 9% | 2x | [보기](C0054_keltner_SOLUSDT_30m.md) |
| C55 | 선형회귀 추세 유의성 | DOGEUSDT | 5m | 1.15 | 1.18 | +89.4% | 41% | 0.5x | [보기](C0055_linreg_DOGEUSDT_5m.md) |
| C56 | 켈트너 채널 | SOLUSDT | 4h | 1.35 | 1.11 | +39.6% | 51% | 1x | [보기](C0056_keltner_SOLUSDT_4h.md) |
| C57 | 돈치안 채널 돌파 (터틀) | BNBUSDT | 4h | 1.59 | 1.44 | +30.1% | 18% | 1.5x | [보기](C0057_donchian_BNBUSDT_4h.md) |
| C58 | 롱/숏 비율 포지셔닝 | ALL | 4h | 2.05 | 1.99 | +19.3% | 9% | 1x | [보기](C0058_positioning_ALL_4h.md) |
| C59 | 롤링 VWAP 이격 | XRPUSDT | 5m | 2.20 | 2.34 | +48.7% | 16% | 1x | [보기](C0059_vwap_dev_XRPUSDT_5m.md) |
| C60 | 롤링 VWAP 이격 | ALL | 1h | 1.90 | 2.03 | +29.2% | 15% | 0.5x | [보기](C0060_vwap_dev_ALL_1h.md) |
| C61 | 슈퍼트렌드 | SOLUSDT | 1d | 1.67 | 1.82 | +119.6% | 56% | 0.5x | [보기](C0061_supertrend_SOLUSDT_1d.md) |
| C62 | 롱/숏 비율 포지셔닝 | ETHUSDT | 1h | 1.58 | 0.89 | +48.2% | 30% | 1x | [보기](C0062_positioning_ETHUSDT_1h.md) |
| C63 | 롱/숏 비율 포지셔닝 | BTCUSDT | 4h | 1.61 | 1.61 | +30.6% | 8% | 2x | [보기](C0063_positioning_BTCUSDT_4h.md) |
| C64 | 롱/숏 비율 포지셔닝 | BTCUSDT | 4h | 1.75 | 1.67 | +59.2% | 24% | 1.5x | [보기](C0064_positioning_BTCUSDT_4h.md) |
| C65 | 선형회귀 추세 유의성 | DOGEUSDT | 1h | 1.45 | 0.95 | +90.9% | 49% | 0.5x | [보기](C0065_linreg_DOGEUSDT_1h.md) |
| C66 | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/BNBUSDT | 15m | 2.00 | 1.59 | +43.3% | 31% | 1x | [보기](C0066_pairs_DOGEUSDT-BNBUSDT_15m.md) |
| C67 | 거래량 급증 돌파 | ETHUSDT | 1h | 2.12 | 1.96 | +66.8% | 36% | 0.5x | [보기](C0067_vol_breakout_ETHUSDT_1h.md) |
| C68 | MACD | ALL | 1d | 1.69 | 2.19 | +24.6% | 21% | 0.5x | [보기](C0068_macd_ALL_1d.md) |
| C69 | 롱/숏 비율 포지셔닝 | ALL | 30m | 2.55 | 2.22 | +32.1% | 16% | 1x | [보기](C0069_positioning_ALL_30m.md) |
| C70 | 일목균형표 | BNBUSDT | 1h | 1.74 | 1.39 | +44.6% | 32% | 1x | [보기](C0070_ichimoku_BNBUSDT_1h.md) |
| C71 | 하이킨아시 연속봉 | ALL | 1d | 1.64 | 1.64 | +36.6% | 28% | 0.5x | [보기](C0071_heikin_ALL_1d.md) |
| C72 | 일목균형표 | ZECUSDT | 1h | 2.29 | 2.31 | +124.4% | 47% | 0.5x | [보기](C0072_ichimoku_ZECUSDT_1h.md) |
| C73 | 켈트너 채널 | ZECUSDT | 15m | 2.08 | 1.36 | +37.6% | 30% | 1x | [보기](C0073_keltner_ZECUSDT_15m.md) |
| C74 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | XRPUSDT | 30m | 1.16 | 2.10 | +24.7% | 17% | 2.5x | [보기](C0074_squeeze_XRPUSDT_30m.md) |
| C75 | 횡단면 모멘텀/리버설 (10개 코인 순위) | ALL | 30m | 1.65 | 1.97 | +41.0% | 41% | 1x | [보기](C0075_xsmom_ALL_30m.md) |
| C76 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 30m | 1.18 | 1.14 | +6.4% | 6% | 3.5x | [보기](C0076_squeeze_ALL_30m.md) |
| C77 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 4h | 1.51 | 1.35 | +107.3% | 57% | 0.5x | [보기](C0077_squeeze_SOLUSDT_4h.md) |
| C78 | NR 협폭봉 돌파 | ALL | 1d | 1.20 | 2.21 | +30.0% | 39% | 1x | [보기](C0078_nr_breakout_ALL_1d.md) |
| C79 | RSI 과매도/과매수 역추세 | DOGEUSDT | 30m | 1.14 | 0.72 | +52.4% | 50% | 0.5x | [보기](C0079_rsi_mr_DOGEUSDT_30m.md) |
| C80 | MACD | ALL | 1d | 1.68 | 1.87 | +44.9% | 35% | 1x | [보기](C0080_macd_ALL_1d.md) |
| C81 | OBV 거래량 모멘텀 | ETHUSDT | 30m | 1.24 | 1.54 | +32.2% | 18% | 1.5x | [보기](C0081_obv_ETHUSDT_30m.md) |
| C82 | 아룬 추세 | DOGEUSDT | 1h | 1.55 | 1.41 | +59.3% | 36% | 0.5x | [보기](C0082_aroon_DOGEUSDT_1h.md) |
| C83 | ADX/DMI 추세 | SOLUSDT | 4h | 1.56 | 0.52 | +57.8% | 44% | 0.5x | [보기](C0083_adx_dmi_SOLUSDT_4h.md) |
| C84 | 선형회귀 추세 유의성 | BTCUSDT | 4h | 1.63 | 1.42 | +21.2% | 13% | 2.5x | [보기](C0084_linreg_BTCUSDT_4h.md) |
| C85 | 아룬 추세 | SOLUSDT | 4h | 1.42 | 1.49 | +61.3% | 39% | 0.5x | [보기](C0085_aroon_SOLUSDT_4h.md) |
| C86 | 시계열 모멘텀 (변동성 정규화) | ETHUSDT | 4h | 1.38 | 2.58 | +18.9% | 20% | 3x | [보기](C0086_tsmom_ETHUSDT_4h.md) |
| C87 | OBV 거래량 모멘텀 | SOLUSDT | 30m | 1.40 | 1.52 | +41.2% | 25% | 1x | [보기](C0087_obv_SOLUSDT_30m.md) |
| C88 | 파라볼릭 SAR | SOLUSDT | 1d | 1.62 | 2.14 | +60.6% | 52% | 0.5x | [보기](C0088_psar_SOLUSDT_1d.md) |
| C89 | 아룬 추세 | SOLUSDT | 4h | 1.00 | 1.35 | +88.0% | 36% | 0.5x | [보기](C0089_aroon_SOLUSDT_4h.md) |
| C90 | 일목균형표 | SOLUSDT | 4h | 1.18 | 1.64 | +67.2% | 59% | 0.5x | [보기](C0090_ichimoku_SOLUSDT_4h.md) |
| C91 | 일목균형표 | BNBUSDT | 1d | 1.33 | 1.37 | +69.5% | 55% | 0.5x | [보기](C0091_ichimoku_BNBUSDT_1d.md) |
| C92 | ADX/DMI 추세 | ALL | 1h | 1.86 | 1.32 | +8.9% | 10% | 1.5x | [보기](C0092_adx_dmi_ALL_1h.md) |
| C93 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 30m | 1.16 | 0.76 | +31.8% | 30% | 1x | [보기](C0093_squeeze_ZECUSDT_30m.md) |
| C94 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 30m | 1.63 | 1.62 | +33.8% | 17% | 1.5x | [보기](C0094_squeeze_ZECUSDT_30m.md) |
| C95 | 시계열 모멘텀 (변동성 정규화) | SOLUSDT | 4h | 1.38 | 1.15 | +51.0% | 55% | 0.5x | [보기](C0095_tsmom_SOLUSDT_4h.md) |
| C96 | RSI 과매도/과매수 역추세 | LINKUSDT | 15m | 1.45 | 1.20 | +10.4% | 9% | 3.5x | [보기](C0096_rsi_mr_LINKUSDT_15m.md) |
| C97 | 일목균형표 | ETHUSDT | 30m | 1.02 | 1.11 | +33.7% | 33% | 1x | [보기](C0097_ichimoku_ETHUSDT_30m.md) |
| C98 | 캔들 패턴 | ALL | 4h | 1.13 | 1.36 | +13.3% | 22% | 1x | [보기](C0098_candle_ALL_4h.md) |
| C99 | 국면 전환 (추세/횡보 판별 후 전략 선택) | XRPUSDT | 4h | 1.29 | 1.34 | +87.2% | 56% | 0.5x | [보기](C0099_regime_XRPUSDT_4h.md) |
| C100 | OBV 거래량 모멘텀 | XRPUSDT | 5m | 2.06 | 1.33 | +24.7% | 10% | 0.5x | [보기](C0100_obv_XRPUSDT_5m.md) |
| C101 | 롤링 VWAP 이격 | ETHUSDT | 4h | 1.18 | 1.12 | +38.8% | 33% | 1x | [보기](C0101_vwap_dev_ETHUSDT_4h.md) |
| C102 | 아룬 추세 | ETHUSDT | 4h | 1.96 | 1.73 | +50.6% | 23% | 1x | [보기](C0102_aroon_ETHUSDT_4h.md) |
| C103 | 거래량 급증 돌파 | SOLUSDT | 4h | 2.04 | 1.44 | +92.0% | 48% | 0.5x | [보기](C0103_vol_breakout_SOLUSDT_4h.md) |
| C104 | RSI 과매도/과매수 역추세 | XRPUSDT | 5m | 1.47 | 0.91 | +7.8% | 7% | 2x | [보기](C0104_rsi_mr_XRPUSDT_5m.md) |
| C105 | 거래량 급증 돌파 | SOLUSDT | 4h | 1.12 | 1.12 | +120.4% | 54% | 0.5x | [보기](C0105_vol_breakout_SOLUSDT_4h.md) |
| C106 | 파라볼릭 SAR | TRXUSDT | 1d | 1.23 | 1.89 | +56.5% | 54% | 0.5x | [보기](C0106_psar_TRXUSDT_1d.md) |
| C107 | ADX/DMI 추세 | BTCUSDT | 1h | 1.14 | 1.22 | +19.5% | 23% | 2x | [보기](C0107_adx_dmi_BTCUSDT_1h.md) |
| C108 | 롤링 VWAP 이격 | DOGEUSDT | 5m | 1.97 | 2.09 | +56.0% | 11% | 0.5x | [보기](C0108_vwap_dev_DOGEUSDT_5m.md) |
| C109 | 거래량 급증 돌파 | ETHUSDT | 1h | 1.99 | 2.38 | +16.0% | 8% | 3.5x | [보기](C0109_vol_breakout_ETHUSDT_1h.md) |
| C110 | 슈퍼트렌드 | LINKUSDT | 4h | 1.01 | 0.71 | +53.2% | 44% | 0.5x | [보기](C0110_supertrend_LINKUSDT_4h.md) |
| C111 | 거래량 급증 돌파 | XRPUSDT | 1h | 1.32 | 1.36 | +66.3% | 47% | 0.5x | [보기](C0111_vol_breakout_XRPUSDT_1h.md) |
| C112 | 이동평균 교차 추세추종 | SOLUSDT | 1d | 1.36 | 1.15 | +63.2% | 24% | 1x | [보기](C0112_ma_cross_SOLUSDT_1d.md) |
| C113 | 펀딩비 쏠림 | SOLUSDT | 4h | 1.52 | 1.43 | +53.7% | 27% | 1x | [보기](C0113_funding_SOLUSDT_4h.md) |
| C114 | MACD | ALL | 1h | 1.75 | 2.03 | +29.9% | 26% | 1x | [보기](C0114_macd_ALL_1h.md) |
| C115 | Ornstein-Uhlenbeck 평균회귀 (z-score) | SOLUSDT | 1h | 1.61 | 2.02 | +44.0% | 28% | 1x | [보기](C0115_zscore_mr_SOLUSDT_1h.md) |
| C116 | 슈퍼트렌드 | BNBUSDT | 4h | 1.16 | 0.86 | +41.8% | 32% | 1x | [보기](C0116_supertrend_BNBUSDT_4h.md) |
| C117 | 슈퍼트렌드 | ZECUSDT | 1h | 1.39 | 2.23 | +78.4% | 38% | 0.5x | [보기](C0117_supertrend_ZECUSDT_1h.md) |
| C118 | 돈치안 채널 돌파 (터틀) | XRPUSDT | 4h | 1.37 | 2.06 | +34.4% | 18% | 1.5x | [보기](C0118_donchian_XRPUSDT_4h.md) |
| C119 | 돈치안 채널 돌파 (터틀) | ALL | 4h | 1.11 | 1.21 | +16.3% | 12% | 0.5x | [보기](C0119_donchian_ALL_4h.md) |
| C120 | 거래량 급증 돌파 | LINKUSDT | 1h | 1.34 | 1.13 | +44.1% | 35% | 1x | [보기](C0120_vol_breakout_LINKUSDT_1h.md) |
| C121 | RSI 과매도/과매수 역추세 | ALL | 5m | 1.07 | 0.87 | +9.0% | 3% | 1.5x | [보기](C0121_rsi_mr_ALL_5m.md) |
| C122 | 미결제약정(OI) × 가격 | ZECUSDT | 30m | 1.20 | 0.59 | +13.7% | 28% | 2x | [보기](C0122_oi_trend_ZECUSDT_30m.md) |
| C123 | ADX/DMI 추세 | ETHUSDT | 30m | 1.17 | 1.19 | +9.2% | 11% | 5x | [보기](C0123_adx_dmi_ETHUSDT_30m.md) |
| C124 | 롤링 VWAP 이격 | SOLUSDT | 30m | 1.17 | 1.36 | +44.6% | 32% | 1x | [보기](C0124_vwap_dev_SOLUSDT_30m.md) |
| C125 | 국면 전환 (추세/횡보 판별 후 전략 선택) | BTCUSDT | 1d | 1.51 | 0.82 | +43.6% | 39% | 1x | [보기](C0125_regime_BTCUSDT_1d.md) |
| C126 | 일목균형표 | ZECUSDT | 1h | 1.17 | 2.42 | +94.9% | 43% | 0.5x | [보기](C0126_ichimoku_ZECUSDT_1h.md) |
| C127 | 파라볼릭 SAR | SOLUSDT | 1d | 1.29 | 1.94 | +79.3% | 55% | 0.5x | [보기](C0127_psar_SOLUSDT_1d.md) |
| C128 | 아룬 추세 | ETHUSDT | 4h | 1.56 | 1.45 | +40.9% | 15% | 1.5x | [보기](C0128_aroon_ETHUSDT_4h.md) |
| C129 | 시계열 모멘텀 (변동성 정규화) | ETHUSDT | 1d | 1.00 | 1.16 | +59.3% | 49% | 0.5x | [보기](C0129_tsmom_ETHUSDT_1d.md) |
| C130 | ADX/DMI 추세 | ALL | 4h | 1.48 | 1.48 | +21.3% | 19% | 0.5x | [보기](C0130_adx_dmi_ALL_4h.md) |
| C131 | 거래량 급증 돌파 | XRPUSDT | 1h | 1.23 | 1.67 | +31.7% | 32% | 1x | [보기](C0131_vol_breakout_XRPUSDT_1h.md) |
| C132 | OBV 거래량 모멘텀 | BNBUSDT | 30m | 1.17 | 1.50 | +23.1% | 14% | 2.5x | [보기](C0132_obv_BNBUSDT_30m.md) |
| C133 | 펀딩비 쏠림 | ALL | 1h | 1.89 | 1.69 | +24.1% | 28% | 0.5x | [보기](C0133_funding_ALL_1h.md) |
| C134 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 1.68 | 1.88 | +24.4% | 32% | 1x | [보기](C0134_regime_ALL_4h.md) |
| C135 | 롱/숏 비율 포지셔닝 | SOLUSDT | 30m | 1.30 | 1.36 | +60.9% | 34% | 1x | [보기](C0135_positioning_SOLUSDT_30m.md) |
| C136 | 켈트너 채널 | BNBUSDT | 30m | 1.84 | 1.61 | +15.2% | 8% | 3.5x | [보기](C0136_keltner_BNBUSDT_30m.md) |
| C137 | OBV 거래량 모멘텀 | DOGEUSDT | 5m | 1.34 | 1.24 | +15.3% | 13% | 2.5x | [보기](C0137_obv_DOGEUSDT_5m.md) |
| C138 | 거래량 급증 돌파 | SOLUSDT | 4h | 1.91 | 1.32 | +91.2% | 46% | 0.5x | [보기](C0138_vol_breakout_SOLUSDT_4h.md) |
| C139 | RSI 과매도/과매수 역추세 | SOLUSDT | 30m | 1.04 | 1.23 | +33.4% | 13% | 1x | [보기](C0139_rsi_mr_SOLUSDT_30m.md) |
| C140 | 롤링 VWAP 이격 | ZECUSDT | 15m | 1.55 | 1.76 | +20.8% | 19% | 1.5x | [보기](C0140_vwap_dev_ZECUSDT_15m.md) |
| C141 | 돈치안 채널 돌파 (터틀) | BNBUSDT | 4h | 1.06 | 1.56 | +23.5% | 16% | 1.5x | [보기](C0141_donchian_BNBUSDT_4h.md) |
| C142 | MFI (거래량 가중 RSI) 역추세 | BNBUSDT | 1h | 1.12 | 0.97 | +49.3% | 25% | 1x | [보기](C0142_mfi_BNBUSDT_1h.md) |
| C143 | RSI 과매도/과매수 역추세 | ZECUSDT | 5m | 1.51 | 2.29 | +14.9% | 8% | 5x | [보기](C0143_rsi_mr_ZECUSDT_5m.md) |
| C144 | NR 협폭봉 돌파 | BTCUSDT | 4h | 1.08 | 0.88 | +36.6% | 44% | 1x | [보기](C0144_nr_breakout_BTCUSDT_4h.md) |
| C145 | 롤링 VWAP 이격 | TRXUSDT | 4h | 1.63 | 1.03 | +35.8% | 39% | 1x | [보기](C0145_vwap_dev_TRXUSDT_4h.md) |
| C146 | 슈퍼트렌드 | ETHUSDT | 4h | 1.53 | 1.31 | +86.4% | 48% | 0.5x | [보기](C0146_supertrend_ETHUSDT_4h.md) |
| C147 | NR 협폭봉 돌파 | ETHUSDT | 4h | 1.01 | 0.77 | +48.8% | 40% | 1x | [보기](C0147_nr_breakout_ETHUSDT_4h.md) |
| C148 | 페어 트레이딩 (공적분 스프레드 평균회귀) | LINKUSDT/SOLUSDT | 15m | 1.22 | 0.97 | +14.2% | 12% | 3x | [보기](C0148_pairs_LINKUSDT-SOLUSDT_15m.md) |
| C149 | 슈퍼트렌드 | ALL | 4h | 1.98 | 1.52 | +35.7% | 22% | 0.5x | [보기](C0149_supertrend_ALL_4h.md) |
| C150 | 슈퍼트렌드 | ALL | 1d | 1.08 | 1.72 | +16.6% | 12% | 0.5x | [보기](C0150_supertrend_ALL_1d.md) |
| C151 | 아룬 추세 | DOGEUSDT | 1h | 1.37 | 1.44 | +58.8% | 47% | 0.5x | [보기](C0151_aroon_DOGEUSDT_1h.md) |
| C152 | 슈퍼트렌드 | XRPUSDT | 4h | 1.27 | 1.08 | +57.9% | 38% | 0.5x | [보기](C0152_supertrend_XRPUSDT_4h.md) |
| C153 | 켈트너 채널 | DOGEUSDT | 5m | 1.17 | 1.24 | +34.2% | 14% | 0.5x | [보기](C0153_keltner_DOGEUSDT_5m.md) |
| C154 | OBV 거래량 모멘텀 | ALL | 4h | 1.35 | 1.31 | +57.2% | 36% | 0.5x | [보기](C0154_obv_ALL_4h.md) |
| C155 | 선형회귀 추세 유의성 | TRXUSDT | 1h | 1.32 | 0.77 | +33.6% | 32% | 1x | [보기](C0155_linreg_TRXUSDT_1h.md) |
| C156 | 미결제약정(OI) × 가격 | DOGEUSDT | 30m | 1.67 | 0.97 | +16.5% | 13% | 0.5x | [보기](C0156_oi_trend_DOGEUSDT_30m.md) |
| C157 | 미결제약정(OI) × 가격 | DOGEUSDT | 30m | 1.66 | 0.70 | +20.1% | 16% | 0.5x | [보기](C0157_oi_trend_DOGEUSDT_30m.md) |
| C158 | 거래량 급증 돌파 | DOGEUSDT | 4h | 1.38 | 0.57 | +29.1% | 27% | 1x | [보기](C0158_vol_breakout_DOGEUSDT_4h.md) |
| C159 | 일목균형표 | ETHUSDT | 1d | 1.35 | 1.18 | +34.9% | 30% | 1x | [보기](C0159_ichimoku_ETHUSDT_1d.md) |
| C160 | 거래량 급증 돌파 | BNBUSDT | 4h | 1.11 | 0.99 | +39.5% | 40% | 1x | [보기](C0160_vol_breakout_BNBUSDT_4h.md) |
| C161 | 선형회귀 추세 유의성 | ALL | 4h | 1.12 | 1.35 | +15.2% | 16% | 0.5x | [보기](C0161_linreg_ALL_4h.md) |
| C162 | 롱/숏 비율 포지셔닝 | BTCUSDT | 1h | 1.35 | 0.81 | +15.6% | 14% | 2.5x | [보기](C0162_positioning_BTCUSDT_1h.md) |
| C163 | ADX/DMI 추세 | ETHUSDT | 1d | 1.18 | 1.23 | +69.9% | 51% | 0.5x | [보기](C0163_adx_dmi_ETHUSDT_1d.md) |
| C164 | 일목균형표 | SOLUSDT | 1d | 1.15 | 1.26 | +74.0% | 53% | 0.5x | [보기](C0164_ichimoku_SOLUSDT_1d.md) |
| C165 | Ornstein-Uhlenbeck 평균회귀 (z-score) | ZECUSDT | 15m | 2.33 | 1.22 | +27.9% | 25% | 1x | [보기](C0165_zscore_mr_ZECUSDT_15m.md) |
| C166 | RSI 과매도/과매수 역추세 | BNBUSDT | 15m | 1.43 | 1.11 | +15.9% | 9% | 2.5x | [보기](C0166_rsi_mr_BNBUSDT_15m.md) |
| C167 | 캔들 패턴 | XRPUSDT | 1d | 1.15 | 1.04 | +40.8% | 38% | 0.5x | [보기](C0167_candle_XRPUSDT_1d.md) |
| C168 | 선형회귀 추세 유의성 | ETHUSDT | 4h | 1.86 | 1.27 | +32.0% | 18% | 1.5x | [보기](C0168_linreg_ETHUSDT_4h.md) |
| C169 | 페어 트레이딩 (공적분 스프레드 평균회귀) | XRPUSDT/BNBUSDT | 30m | 1.53 | 0.72 | +22.0% | 29% | 1.5x | [보기](C0169_pairs_XRPUSDT-BNBUSDT_30m.md) |
| C170 | 페어 트레이딩 (공적분 스프레드 평균회귀) | BNBUSDT/ETHUSDT | 1h | 1.15 | 0.95 | +35.3% | 37% | 1x | [보기](C0170_pairs_BNBUSDT-ETHUSDT_1h.md) |
| C171 | 켈트너 채널 | LINKUSDT | 15m | 2.01 | 1.27 | +23.0% | 34% | 1x | [보기](C0171_keltner_LINKUSDT_15m.md) |
| C172 | 하이킨아시 연속봉 | DOGEUSDT | 4h | 1.27 | 1.13 | +82.8% | 51% | 0.5x | [보기](C0172_heikin_DOGEUSDT_4h.md) |
| C173 | Ornstein-Uhlenbeck 평균회귀 (z-score) | LINKUSDT | 15m | 1.57 | 1.00 | +28.7% | 12% | 1.5x | [보기](C0173_zscore_mr_LINKUSDT_15m.md) |
| C174 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ETHUSDT | 4h | 1.43 | 1.31 | +39.6% | 31% | 1x | [보기](C0174_squeeze_ETHUSDT_4h.md) |
| C175 | 페어 트레이딩 (공적분 스프레드 평균회귀) | ETHUSDT/TRXUSDT | 4h | 1.43 | 0.95 | +35.4% | 22% | 1.5x | [보기](C0175_pairs_ETHUSDT-TRXUSDT_4h.md) |
| C176 | 이동평균 교차 추세추종 | ETHUSDT | 30m | 1.74 | 1.01 | +51.3% | 30% | 1x | [보기](C0176_ma_cross_ETHUSDT_30m.md) |
| C177 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ETHUSDT | 1h | 1.62 | 1.27 | +45.1% | 40% | 1x | [보기](C0177_squeeze_ETHUSDT_1h.md) |
| C178 | MACD | TRXUSDT | 4h | 1.20 | 1.34 | +54.2% | 50% | 0.5x | [보기](C0178_macd_TRXUSDT_4h.md) |
| C179 | MACD | ETHUSDT | 4h | 1.42 | 1.27 | +25.7% | 24% | 1.5x | [보기](C0179_macd_ETHUSDT_4h.md) |
| C180 | 아룬 추세 | BNBUSDT | 30m | 1.04 | 0.60 | +37.2% | 23% | 1x | [보기](C0180_aroon_BNBUSDT_30m.md) |
| C181 | OBV 거래량 모멘텀 | ALL | 4h | 1.16 | 1.35 | +45.4% | 35% | 0.5x | [보기](C0181_obv_ALL_4h.md) |
| C182 | 국면 전환 (추세/횡보 판별 후 전략 선택) | SOLUSDT | 4h | 1.32 | 1.13 | +186.9% | 46% | 0.5x | [보기](C0182_regime_SOLUSDT_4h.md) |
| C183 | 시계열 모멘텀 (변동성 정규화) | BTCUSDT | 30m | 1.30 | 0.94 | +21.8% | 22% | 2x | [보기](C0183_tsmom_BTCUSDT_30m.md) |
| C184 | 슈퍼트렌드 | SOLUSDT | 1d | 1.24 | 1.94 | +123.2% | 48% | 0.5x | [보기](C0184_supertrend_SOLUSDT_1d.md) |
| C185 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 1.18 | 1.16 | +55.2% | 25% | 0.5x | [보기](C0185_regime_ALL_4h.md) |
| C186 | 선형회귀 추세 유의성 | ETHUSDT | 1d | 1.02 | 1.02 | +54.9% | 35% | 0.5x | [보기](C0186_linreg_ETHUSDT_1d.md) |
| C187 | 켈트너 채널 | XRPUSDT | 5m | 1.29 | 1.59 | +47.2% | 27% | 0.5x | [보기](C0187_keltner_XRPUSDT_5m.md) |
| C188 | OBV 거래량 모멘텀 | SOLUSDT | 4h | 1.38 | 3.70 | +44.0% | 38% | 1x | [보기](C0188_obv_SOLUSDT_4h.md) |
| C189 | 이동평균 교차 추세추종 | BTCUSDT | 1d | 1.29 | 0.65 | +24.9% | 24% | 1.5x | [보기](C0189_ma_cross_BTCUSDT_1d.md) |
| C190 | 선형회귀 추세 유의성 | SOLUSDT | 1d | 1.32 | 1.51 | +140.7% | 56% | 0.5x | [보기](C0190_linreg_SOLUSDT_1d.md) |
| C191 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | XRPUSDT | 30m | 1.02 | 0.89 | +19.6% | 21% | 1.5x | [보기](C0191_squeeze_XRPUSDT_30m.md) |
| C192 | 펀딩비 쏠림 | DOGEUSDT | 4h | 1.82 | 1.01 | +74.5% | 45% | 0.5x | [보기](C0192_funding_DOGEUSDT_4h.md) |
| C193 | 미결제약정(OI) × 가격 | SOLUSDT | 30m | 1.40 | 0.62 | +29.8% | 26% | 1x | [보기](C0193_oi_trend_SOLUSDT_30m.md) |
| C194 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | BTCUSDT | 1h | 1.01 | 0.78 | +13.6% | 16% | 2.5x | [보기](C0194_squeeze_BTCUSDT_1h.md) |
| C195 | 국면 전환 (추세/횡보 판별 후 전략 선택) | SOLUSDT | 4h | 1.04 | 0.90 | +155.7% | 52% | 0.5x | [보기](C0195_regime_SOLUSDT_4h.md) |
| C196 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ETHUSDT | 1d | 1.01 | 0.64 | +40.6% | 43% | 0.5x | [보기](C0196_regime_ETHUSDT_1d.md) |
| C197 | 선형회귀 추세 유의성 | LINKUSDT | 30m | 1.21 | 1.18 | +39.3% | 36% | 1x | [보기](C0197_linreg_LINKUSDT_30m.md) |
| C198 | 일목균형표 | ZECUSDT | 1h | 1.40 | 1.08 | +74.4% | 50% | 0.5x | [보기](C0198_ichimoku_ZECUSDT_1h.md) |
| C199 | MACD | XRPUSDT | 1d | 1.77 | 1.06 | +56.6% | 42% | 0.5x | [보기](C0199_macd_XRPUSDT_1d.md) |
| C200 | 페어 트레이딩 (공적분 스프레드 평균회귀) | LINKUSDT/ETHUSDT | 1h | 1.20 | 0.77 | +36.4% | 35% | 1x | [보기](C0200_pairs_LINKUSDT-ETHUSDT_1h.md) |
| C201 | 일목균형표 | TRXUSDT | 4h | 1.24 | 1.35 | +33.1% | 20% | 1x | [보기](C0201_ichimoku_TRXUSDT_4h.md) |
| C202 | 미결제약정(OI) × 가격 | XRPUSDT | 30m | 2.30 | 1.30 | +22.1% | 12% | 0.5x | [보기](C0202_oi_trend_XRPUSDT_30m.md) |
| C203 | 국면 전환 (추세/횡보 판별 후 전략 선택) | DOGEUSDT | 4h | 1.02 | 0.89 | +61.9% | 60% | 0.5x | [보기](C0203_regime_DOGEUSDT_4h.md) |
| C204 | 하이킨아시 연속봉 | ALL | 1d | 1.57 | 2.61 | +29.3% | 11% | 0.5x | [보기](C0204_heikin_ALL_1d.md) |
| C205 | Ornstein-Uhlenbeck 평균회귀 (z-score) | BNBUSDT | 1h | 1.28 | 1.42 | +17.5% | 17% | 1.5x | [보기](C0205_zscore_mr_BNBUSDT_1h.md) |
| C206 | 페어 트레이딩 (공적분 스프레드 평균회귀) | ZECUSDT/DOGEUSDT | 1h | 1.43 | 1.24 | +54.9% | 40% | 0.5x | [보기](C0206_pairs_ZECUSDT-DOGEUSDT_1h.md) |
| C207 | 하이킨아시 연속봉 | SOLUSDT | 4h | 1.11 | 1.43 | +50.1% | 42% | 0.5x | [보기](C0207_heikin_SOLUSDT_4h.md) |
| C208 | 롤링 VWAP 이격 | LINKUSDT | 5m | 1.08 | 0.99 | +22.8% | 6% | 0.5x | [보기](C0208_vwap_dev_LINKUSDT_5m.md) |
| C209 | 미결제약정(OI) × 가격 | BNBUSDT | 30m | 2.27 | 0.59 | +22.5% | 17% | 1.5x | [보기](C0209_oi_trend_BNBUSDT_30m.md) |
| C210 | 캔들 패턴 | ETHUSDT | 1d | 1.50 | 1.44 | +49.3% | 35% | 1x | [보기](C0210_candle_ETHUSDT_1d.md) |
| C211 | Ornstein-Uhlenbeck 평균회귀 (z-score) | SOLUSDT | 30m | 1.16 | 0.63 | +36.8% | 35% | 0.5x | [보기](C0211_zscore_mr_SOLUSDT_30m.md) |
| C212 | 파라볼릭 SAR | BTCUSDT | 1d | 1.18 | 1.00 | +32.5% | 39% | 1x | [보기](C0212_psar_BTCUSDT_1d.md) |
| C213 | 롤링 VWAP 이격 | SOLUSDT | 1h | 1.16 | 0.71 | +103.0% | 50% | 0.5x | [보기](C0213_vwap_dev_SOLUSDT_1h.md) |
| C214 | MFI (거래량 가중 RSI) 역추세 | SOLUSDT | 30m | 1.31 | 1.58 | +49.6% | 21% | 1x | [보기](C0214_mfi_SOLUSDT_30m.md) |
| C215 | 미결제약정(OI) × 가격 | BNBUSDT | 1h | 2.36 | 0.69 | +15.5% | 15% | 3.5x | [보기](C0215_oi_trend_BNBUSDT_1h.md) |
| C216 | Ornstein-Uhlenbeck 평균회귀 (z-score) | SOLUSDT | 1h | 1.01 | 1.40 | +38.9% | 25% | 1.5x | [보기](C0216_zscore_mr_SOLUSDT_1h.md) |
| C217 | 거래량 급증 돌파 | ETHUSDT | 4h | 1.06 | 0.77 | +15.6% | 13% | 2.5x | [보기](C0217_vol_breakout_ETHUSDT_4h.md) |
| C218 | 일목균형표 | ALL | 1d | 1.31 | 1.10 | +32.9% | 32% | 0.5x | [보기](C0218_ichimoku_ALL_1d.md) |
| C219 | 일목균형표 | DOGEUSDT | 1h | 1.45 | 1.26 | +78.0% | 48% | 0.5x | [보기](C0219_ichimoku_DOGEUSDT_1h.md) |
| C220 | OBV 거래량 모멘텀 | ZECUSDT | 30m | 1.93 | 1.42 | +27.9% | 16% | 2x | [보기](C0220_obv_ZECUSDT_30m.md) |
| C221 | 선형회귀 추세 유의성 | BNBUSDT | 1h | 1.13 | 1.15 | +35.0% | 36% | 1x | [보기](C0221_linreg_BNBUSDT_1h.md) |
| C222 | 선형회귀 추세 유의성 | XRPUSDT | 30m | 1.05 | 1.08 | +46.8% | 49% | 0.5x | [보기](C0222_linreg_XRPUSDT_30m.md) |
| C223 | ADX/DMI 추세 | SOLUSDT | 4h | 1.06 | 0.70 | +36.5% | 58% | 0.5x | [보기](C0223_adx_dmi_SOLUSDT_4h.md) |
| C224 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 30m | 1.58 | 1.09 | +47.0% | 27% | 1x | [보기](C0224_squeeze_SOLUSDT_30m.md) |
| C225 | 페어 트레이딩 (공적분 스프레드 평균회귀) | TRXUSDT/SOLUSDT | 1h | 1.09 | 0.80 | +10.1% | 9% | 3.5x | [보기](C0225_pairs_TRXUSDT-SOLUSDT_1h.md) |
| C226 | 롤링 VWAP 이격 | BNBUSDT | 5m | 1.35 | 0.80 | +17.5% | 10% | 2x | [보기](C0226_vwap_dev_BNBUSDT_5m.md) |
| C227 | NR 협폭봉 돌파 | BTCUSDT | 4h | 1.48 | 1.11 | +37.9% | 31% | 1.5x | [보기](C0227_nr_breakout_BTCUSDT_4h.md) |
| C228 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | DOGEUSDT | 4h | 1.19 | 1.36 | +55.3% | 33% | 0.5x | [보기](C0228_squeeze_DOGEUSDT_4h.md) |
| C229 | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/LINKUSDT | 30m | 1.23 | 1.38 | +28.7% | 11% | 2x | [보기](C0229_pairs_DOGEUSDT-LINKUSDT_30m.md) |
| C230 | 페어 트레이딩 (공적분 스프레드 평균회귀) | XRPUSDT/ETHUSDT | 15m | 1.33 | 1.00 | +31.1% | 17% | 1.5x | [보기](C0230_pairs_XRPUSDT-ETHUSDT_15m.md) |
| C231 | 시계열 모멘텀 (변동성 정규화) | TRXUSDT | 4h | 1.33 | 1.02 | +34.1% | 46% | 1x | [보기](C0231_tsmom_TRXUSDT_4h.md) |
| C232 | 롱/숏 비율 포지셔닝 | SOLUSDT | 30m | 1.88 | 1.25 | +24.2% | 21% | 2.5x | [보기](C0232_positioning_SOLUSDT_30m.md) |
| C233 | 거래량 급증 돌파 | ALL | 1h | 1.11 | 0.58 | +2.4% | 2% | 5x | [보기](C0233_vol_breakout_ALL_1h.md) |
| C234 | 돈치안 채널 돌파 (터틀) | ALL | 1d | 1.75 | 2.01 | +17.6% | 13% | 0.5x | [보기](C0234_donchian_ALL_1d.md) |
| C235 | MACD | XRPUSDT | 1d | 1.16 | 1.19 | +80.3% | 53% | 0.5x | [보기](C0235_macd_XRPUSDT_1d.md) |
| C236 | 일목균형표 | BTCUSDT | 4h | 1.35 | 0.55 | +24.2% | 27% | 1.5x | [보기](C0236_ichimoku_BTCUSDT_4h.md) |
| C237 | 롤링 VWAP 이격 | DOGEUSDT | 4h | 1.92 | 1.46 | +67.5% | 28% | 0.5x | [보기](C0237_vwap_dev_DOGEUSDT_4h.md) |
| C238 | 돈치안 채널 돌파 (터틀) | ETHUSDT | 4h | 1.37 | 1.01 | +38.0% | 38% | 1x | [보기](C0238_donchian_ETHUSDT_4h.md) |
| C239 | OBV 거래량 모멘텀 | ETHUSDT | 4h | 1.33 | 0.50 | +107.4% | 47% | 0.5x | [보기](C0239_obv_ETHUSDT_4h.md) |
| C240 | 돈치안 채널 돌파 (터틀) | SOLUSDT | 30m | 1.16 | 0.57 | +135.3% | 47% | 0.5x | [보기](C0240_donchian_SOLUSDT_30m.md) |
| C241 | OBV 거래량 모멘텀 | XRPUSDT | 15m | 1.36 | 0.55 | +11.1% | 6% | 3.5x | [보기](C0241_obv_XRPUSDT_15m.md) |
| C242 | 돈치안 채널 돌파 (터틀) | DOGEUSDT | 4h | 2.07 | 1.95 | +41.5% | 17% | 1.5x | [보기](C0242_donchian_DOGEUSDT_4h.md) |
| C243 | 이동평균 교차 추세추종 | SOLUSDT | 4h | 1.06 | 1.40 | +41.8% | 41% | 1x | [보기](C0243_ma_cross_SOLUSDT_4h.md) |
| C244 | 미결제약정(OI) × 가격 | ALL | 30m | 2.02 | 0.55 | +6.0% | 7% | 3x | [보기](C0244_oi_trend_ALL_30m.md) |
| C245 | 거래량 급증 돌파 | ZECUSDT | 1h | 1.03 | 2.10 | +71.3% | 33% | 0.5x | [보기](C0245_vol_breakout_ZECUSDT_1h.md) |
| C246 | NR 협폭봉 돌파 | XRPUSDT | 30m | 1.14 | 1.49 | +31.2% | 28% | 1x | [보기](C0246_nr_breakout_XRPUSDT_30m.md) |
| C247 | 거래량 급증 돌파 | BTCUSDT | 1h | 1.28 | 1.26 | +14.8% | 11% | 2.5x | [보기](C0247_vol_breakout_BTCUSDT_1h.md) |
| C248 | 페어 트레이딩 (공적분 스프레드 평균회귀) | ZECUSDT/SOLUSDT | 1d | 1.58 | 1.85 | +59.8% | 33% | 0.5x | [보기](C0248_pairs_ZECUSDT-SOLUSDT_1d.md) |
| C249 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | DOGEUSDT | 4h | 1.04 | 0.87 | +58.5% | 41% | 0.5x | [보기](C0249_squeeze_DOGEUSDT_4h.md) |
| C250 | Ornstein-Uhlenbeck 평균회귀 (z-score) | DOGEUSDT | 15m | 1.19 | 1.42 | +46.3% | 17% | 1.5x | [보기](C0250_zscore_mr_DOGEUSDT_15m.md) |
| C251 | 하이킨아시 연속봉 | SOLUSDT | 1d | 1.55 | 1.10 | +115.4% | 50% | 0.5x | [보기](C0251_heikin_SOLUSDT_1d.md) |
| C252 | 롱/숏 비율 포지셔닝 | LINKUSDT | 30m | 1.02 | 0.99 | +26.5% | 31% | 1.5x | [보기](C0252_positioning_LINKUSDT_30m.md) |
| C253 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | DOGEUSDT | 30m | 1.13 | 0.93 | +29.7% | 29% | 1x | [보기](C0253_squeeze_DOGEUSDT_30m.md) |
| C254 | 슈퍼트렌드 | ETHUSDT | 4h | 1.52 | 1.06 | +66.1% | 44% | 0.5x | [보기](C0254_supertrend_ETHUSDT_4h.md) |
| C255 | MACD | ETHUSDT | 4h | 1.27 | 1.73 | +52.9% | 23% | 1x | [보기](C0255_macd_ETHUSDT_4h.md) |
| C256 | 테이커 주문흐름 불균형 | DOGEUSDT | 4h | 1.12 | 0.72 | +30.5% | 18% | 1x | [보기](C0256_flow_DOGEUSDT_4h.md) |
| C257 | 파라볼릭 SAR | ALL | 1d | 1.15 | 0.95 | +41.8% | 35% | 0.5x | [보기](C0257_psar_ALL_1d.md) |
| C258 | 파라볼릭 SAR | DOGEUSDT | 4h | 1.47 | 0.92 | +31.8% | 29% | 1x | [보기](C0258_psar_DOGEUSDT_4h.md) |
| C259 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | LINKUSDT | 1h | 1.09 | 0.73 | +47.0% | 40% | 1x | [보기](C0259_squeeze_LINKUSDT_1h.md) |
| C260 | MFI (거래량 가중 RSI) 역추세 | DOGEUSDT | 5m | 1.48 | 0.88 | +28.0% | 13% | 0.5x | [보기](C0260_mfi_DOGEUSDT_5m.md) |
| C261 | 미결제약정(OI) × 가격 | ZECUSDT | 1h | 1.56 | 1.53 | +25.3% | 16% | 1x | [보기](C0261_oi_trend_ZECUSDT_1h.md) |
| C262 | MACD | SOLUSDT | 30m | 1.06 | 1.51 | +59.9% | 44% | 0.5x | [보기](C0262_macd_SOLUSDT_30m.md) |
| C263 | NR 협폭봉 돌파 | ALL | 4h | 1.15 | 1.21 | +7.9% | 6% | 1.5x | [보기](C0263_nr_breakout_ALL_4h.md) |
| C264 | OBV 거래량 모멘텀 | BTCUSDT | 4h | 1.26 | 0.58 | +34.9% | 56% | 1x | [보기](C0264_obv_BTCUSDT_4h.md) |
| C265 | ADX/DMI 추세 | BTCUSDT | 30m | 1.00 | 0.94 | +10.8% | 10% | 3.5x | [보기](C0265_adx_dmi_BTCUSDT_30m.md) |
| C266 | 펀딩비 쏠림 | ETHUSDT | 4h | 1.37 | 1.38 | +43.7% | 44% | 1x | [보기](C0266_funding_ETHUSDT_4h.md) |
| C267 | 펀딩비 쏠림 | ETHUSDT | 4h | 1.54 | 1.21 | +24.4% | 17% | 2x | [보기](C0267_funding_ETHUSDT_4h.md) |
| C268 | RSI 과매도/과매수 역추세 | ZECUSDT | 30m | 1.12 | 1.07 | +46.0% | 48% | 0.5x | [보기](C0268_rsi_mr_ZECUSDT_30m.md) |
| C269 | MACD | SOLUSDT | 4h | 1.37 | 1.51 | +30.1% | 18% | 2x | [보기](C0269_macd_SOLUSDT_4h.md) |
| C270 | 롱/숏 비율 포지셔닝 | ETHUSDT | 4h | 1.14 | 0.89 | +22.9% | 19% | 1.5x | [보기](C0270_positioning_ETHUSDT_4h.md) |
