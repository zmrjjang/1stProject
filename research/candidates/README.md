# 페이퍼 트레이딩 후보 목록

엄격한 과최적화 검정 없이 검증·홀드아웃 구간 수익, 비용 스트레스, 파라미터 안정성만 통과한 후보입니다. 같은 아이디어의 변형은 더 좋은 것이 나오면 교체됩니다. `python run_strategy.py paper --candidate C번호` 로 모의매매할 수 있습니다.

| # | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |
|---|---|---|---|---|---|---|---|---|---|
| C1 | 선형회귀 추세 유의성 | ALL | 4h | 2.17 | 1.99 | +14.7% | 10% | 1x | [보기](C0001_linreg_ALL_4h.md) |
| C2 | 돈치안 채널 돌파 (터틀) | ALL | 1d | 2.36 | 1.94 | +19.3% | 13% | 0.5x | [보기](C0002_donchian_ALL_1d.md) |
| C3 | 거래량 급증 돌파 | ALL | 4h | 2.13 | 2.05 | +9.1% | 11% | 1.5x | [보기](C0003_vol_breakout_ALL_4h.md) |
| C4 | 선형회귀 추세 유의성 | ALL | 4h | 1.93 | 1.84 | +38.4% | 28% | 0.5x | [보기](C0004_linreg_ALL_4h.md) |
| C5 | 하이킨아시 연속봉 | ETHUSDT | 1h | 1.04 | 0.67 | +13.7% | 15% | 2x | [보기](C0005_heikin_ETHUSDT_1h.md) |
| C6 | 선형회귀 추세 유의성 | ALL | 1h | 1.65 | 1.79 | +22.6% | 31% | 1x | [보기](C0006_linreg_ALL_1h.md) |
| C7 | 돈치안 채널 돌파 (터틀) | XRPUSDT | 4h | 1.66 | 1.64 | +76.7% | 44% | 0.5x | [보기](C0007_donchian_XRPUSDT_4h.md) |
| C8 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 4h | 2.10 | 2.02 | +20.9% | 17% | 2x | [보기](C0008_squeeze_ALL_4h.md) |
| C9 | 펀딩비 쏠림 | ETHUSDT | 1h | 1.21 | 0.51 | +49.2% | 45% | 0.5x | [보기](C0009_funding_ETHUSDT_1h.md) |
| C10 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 4h | 1.52 | 1.65 | +53.9% | 34% | 0.5x | [보기](C0010_squeeze_SOLUSDT_4h.md) |
| C11 | 켈트너 채널 | ALL | 15m | 2.27 | 1.97 | +7.5% | 5% | 1.5x | [보기](C0011_keltner_ALL_15m.md) |
| C12 | 거래량 급증 돌파 | ALL | 4h | 1.47 | 1.58 | +23.8% | 24% | 0.5x | [보기](C0012_vol_breakout_ALL_4h.md) |
| C13 | Ornstein-Uhlenbeck 평균회귀 (z-score) | ALL | 1h | 1.86 | 1.72 | +6.7% | 4% | 1x | [보기](C0013_zscore_mr_ALL_1h.md) |
| C14 | 거래량 급증 돌파 | ALL | 30m | 2.31 | 2.07 | +19.5% | 8% | 1x | [보기](C0014_vol_breakout_ALL_30m.md) |
| C15 | 시계열 모멘텀 (변동성 정규화) | XRPUSDT | 4h | 1.74 | 0.61 | +55.0% | 51% | 0.5x | [보기](C0015_tsmom_XRPUSDT_4h.md) |
| C16 | RSI 과매도/과매수 역추세 | DOGEUSDT | 30m | 1.18 | 1.08 | +18.8% | 8% | 2.5x | [보기](C0016_rsi_mr_DOGEUSDT_30m.md) |
| C17 | Ornstein-Uhlenbeck 평균회귀 (z-score) | XRPUSDT | 15m | 1.50 | 2.15 | +25.5% | 42% | 1x | [보기](C0017_zscore_mr_XRPUSDT_15m.md) |
| C18 | Ornstein-Uhlenbeck 평균회귀 (z-score) | DOGEUSDT | 5m | 1.05 | 0.78 | +39.3% | 47% | 0.5x | [보기](C0018_zscore_mr_DOGEUSDT_5m.md) |
| C19 | 캔들 패턴 | ALL | 1d | 1.92 | 2.04 | +43.1% | 31% | 1.5x | [보기](C0019_candle_ALL_1d.md) |
| C20 | 아룬 추세 | ALL | 1h | 2.28 | 2.37 | +15.7% | 10% | 1x | [보기](C0020_aroon_ALL_1h.md) |
| C21 | MACD | ALL | 1d | 2.01 | 2.09 | +54.3% | 27% | 1x | [보기](C0021_macd_ALL_1d.md) |
| C22 | 선형회귀 추세 유의성 | DOGEUSDT | 1h | 1.64 | 1.57 | +99.7% | 55% | 0.5x | [보기](C0022_linreg_DOGEUSDT_1h.md) |
| C23 | 일목균형표 | ALL | 4h | 1.72 | 1.72 | +12.5% | 11% | 0.5x | [보기](C0023_ichimoku_ALL_4h.md) |
| C24 | 거래량 급증 돌파 | ALL | 30m | 1.37 | 2.13 | +12.0% | 11% | 1x | [보기](C0024_vol_breakout_ALL_30m.md) |
| C25 | MACD | SOLUSDT | 4h | 2.12 | 1.56 | +42.2% | 33% | 1x | [보기](C0025_macd_SOLUSDT_4h.md) |
| C26 | 거래량 급증 돌파 | ETHUSDT | 1h | 1.99 | 1.98 | +51.0% | 16% | 1.5x | [보기](C0026_vol_breakout_ETHUSDT_1h.md) |
| C27 | 테이커 주문흐름 불균형 | ALL | 4h | 1.99 | 1.96 | +30.1% | 34% | 0.5x | [보기](C0027_flow_ALL_4h.md) |
| C28 | OBV 거래량 모멘텀 | ALL | 1h | 1.98 | 1.93 | +18.3% | 14% | 1.5x | [보기](C0028_obv_ALL_1h.md) |
| C29 | 선형회귀 추세 유의성 | SOLUSDT | 1h | 1.39 | 1.52 | +124.8% | 39% | 0.5x | [보기](C0029_linreg_SOLUSDT_1h.md) |
| C30 | 롤링 VWAP 이격 | ETHUSDT | 4h | 1.31 | 1.34 | +32.4% | 28% | 1x | [보기](C0030_vwap_dev_ETHUSDT_4h.md) |
| C31 | 거래량 급증 돌파 | BTCUSDT | 1h | 1.22 | 1.18 | +25.3% | 16% | 2x | [보기](C0031_vol_breakout_BTCUSDT_1h.md) |
| C32 | 아룬 추세 | ALL | 4h | 1.38 | 1.69 | +43.2% | 19% | 0.5x | [보기](C0032_aroon_ALL_4h.md) |
| C33 | 켈트너 채널 | ALL | 1d | 1.34 | 1.36 | +47.1% | 32% | 0.5x | [보기](C0033_keltner_ALL_1d.md) |
| C34 | 미결제약정(OI) × 가격 | ALL | 1h | 1.27 | 1.45 | +10.4% | 5% | 0.5x | [보기](C0034_oi_trend_ALL_1h.md) |
| C35 | 미결제약정(OI) × 가격 | ALL | 1h | 1.47 | 1.13 | +7.3% | 7% | 0.5x | [보기](C0035_oi_trend_ALL_1h.md) |
| C36 | 롤링 VWAP 이격 | ALL | 1h | 1.30 | 1.42 | +30.6% | 22% | 0.5x | [보기](C0036_vwap_dev_ALL_1h.md) |
| C37 | ADX/DMI 추세 | ALL | 4h | 1.63 | 1.57 | +24.5% | 15% | 0.5x | [보기](C0037_adx_dmi_ALL_4h.md) |
| C38 | 돈치안 채널 돌파 (터틀) | BTCUSDT | 30m | 1.39 | 1.22 | +27.8% | 30% | 1.5x | [보기](C0038_donchian_BTCUSDT_30m.md) |
| C39 | 파라볼릭 SAR | ALL | 1d | 1.71 | 2.39 | +16.6% | 13% | 1x | [보기](C0039_psar_ALL_1d.md) |
| C40 | 파라볼릭 SAR | ALL | 1d | 1.47 | 0.63 | +13.0% | 18% | 1.5x | [보기](C0040_psar_ALL_1d.md) |
| C41 | 이동평균 교차 추세추종 | ALL | 4h | 1.67 | 1.93 | +13.1% | 15% | 1x | [보기](C0041_ma_cross_ALL_4h.md) |
| C42 | 캔들 패턴 | SOLUSDT | 4h | 1.87 | 2.81 | +67.3% | 48% | 0.5x | [보기](C0042_candle_SOLUSDT_4h.md) |
| C43 | 아룬 추세 | ALL | 4h | 1.42 | 1.75 | +18.4% | 14% | 0.5x | [보기](C0043_aroon_ALL_4h.md) |
| C44 | 캔들 패턴 | ALL | 1d | 1.10 | 1.76 | +54.6% | 43% | 0.5x | [보기](C0044_candle_ALL_1d.md) |
| C45 | 아룬 추세 | ETHUSDT | 4h | 1.68 | 0.71 | +48.1% | 38% | 1x | [보기](C0045_aroon_ETHUSDT_4h.md) |
| C46 | 켈트너 채널 | ETHUSDT | 30m | 1.85 | 1.61 | +18.5% | 9% | 2x | [보기](C0046_keltner_ETHUSDT_30m.md) |
| C47 | 페어 트레이딩 (공적분 스프레드 평균회귀) | SOLUSDT/BNBUSDT | 1h | 1.03 | 1.15 | +30.4% | 30% | 1x | [보기](C0047_pairs_SOLUSDT-BNBUSDT_1h.md) |
| C48 | OBV 거래량 모멘텀 | LINKUSDT | 30m | 1.16 | 1.15 | +20.3% | 23% | 2x | [보기](C0048_obv_LINKUSDT_30m.md) |
| C49 | 캔들 패턴 | ALL | 4h | 1.80 | 1.62 | +17.4% | 11% | 1.5x | [보기](C0049_candle_ALL_4h.md) |
| C50 | 켈트너 채널 | ETHUSDT | 1h | 1.87 | 1.40 | +42.9% | 33% | 1x | [보기](C0050_keltner_ETHUSDT_1h.md) |
| C51 | 롤링 VWAP 이격 | SOLUSDT | 4h | 2.25 | 1.35 | +61.1% | 36% | 0.5x | [보기](C0051_vwap_dev_SOLUSDT_4h.md) |
| C52 | OBV 거래량 모멘텀 | TRXUSDT | 4h | 1.22 | 0.55 | +23.2% | 38% | 1.5x | [보기](C0052_obv_TRXUSDT_4h.md) |
| C53 | 슈퍼트렌드 | ETHUSDT | 4h | 1.47 | 1.14 | +57.6% | 42% | 0.5x | [보기](C0053_supertrend_ETHUSDT_4h.md) |
| C54 | 켈트너 채널 | SOLUSDT | 30m | 1.58 | 2.32 | +29.1% | 15% | 1.5x | [보기](C0054_keltner_SOLUSDT_30m.md) |
| C55 | 선형회귀 추세 유의성 | DOGEUSDT | 5m | 1.15 | 1.18 | +89.4% | 41% | 0.5x | [보기](C0055_linreg_DOGEUSDT_5m.md) |
| C56 | 켈트너 채널 | SOLUSDT | 4h | 1.35 | 1.11 | +39.6% | 51% | 1x | [보기](C0056_keltner_SOLUSDT_4h.md) |
| C57 | 파라볼릭 SAR | BNBUSDT | 4h | 1.22 | 1.28 | +52.0% | 34% | 0.5x | [보기](C0057_psar_BNBUSDT_4h.md) |
| C58 | 롱/숏 비율 포지셔닝 | ALL | 4h | 1.82 | 1.90 | +24.9% | 11% | 1x | [보기](C0058_positioning_ALL_4h.md) |
| C59 | 롤링 VWAP 이격 | XRPUSDT | 5m | 2.20 | 2.34 | +48.7% | 16% | 1x | [보기](C0059_vwap_dev_XRPUSDT_5m.md) |
| C60 | 롤링 VWAP 이격 | ALL | 1h | 1.90 | 2.03 | +29.2% | 15% | 0.5x | [보기](C0060_vwap_dev_ALL_1h.md) |
| C61 | 슈퍼트렌드 | SOLUSDT | 1d | 1.67 | 1.82 | +119.6% | 56% | 0.5x | [보기](C0061_supertrend_SOLUSDT_1d.md) |
| C62 | 롱/숏 비율 포지셔닝 | ETHUSDT | 1h | 1.58 | 0.89 | +48.2% | 30% | 1x | [보기](C0062_positioning_ETHUSDT_1h.md) |
| C63 | 롱/숏 비율 포지셔닝 | BTCUSDT | 4h | 1.61 | 1.61 | +30.6% | 8% | 2x | [보기](C0063_positioning_BTCUSDT_4h.md) |
| C64 | 롱/숏 비율 포지셔닝 | BTCUSDT | 4h | 1.75 | 1.67 | +59.2% | 24% | 1.5x | [보기](C0064_positioning_BTCUSDT_4h.md) |
| C65 | 선형회귀 추세 유의성 | DOGEUSDT | 1h | 1.45 | 0.95 | +90.9% | 49% | 0.5x | [보기](C0065_linreg_DOGEUSDT_1h.md) |
| C66 | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/BNBUSDT | 15m | 2.00 | 1.59 | +43.3% | 31% | 1x | [보기](C0066_pairs_DOGEUSDT-BNBUSDT_15m.md) |
| C67 | 일목균형표 | ALL | 1h | 1.19 | 1.08 | +42.6% | 29% | 0.5x | [보기](C0067_ichimoku_ALL_1h.md) |
| C68 | MACD | ALL | 1d | 1.69 | 2.19 | +24.6% | 21% | 0.5x | [보기](C0068_macd_ALL_1d.md) |
| C69 | 롱/숏 비율 포지셔닝 | ALL | 30m | 2.55 | 2.22 | +32.1% | 16% | 1x | [보기](C0069_positioning_ALL_30m.md) |
| C70 | 시계열 모멘텀 (변동성 정규화) | BNBUSDT | 4h | 1.13 | 0.74 | +37.3% | 44% | 1x | [보기](C0070_tsmom_BNBUSDT_4h.md) |
| C71 | 하이킨아시 연속봉 | ALL | 1d | 1.16 | 1.16 | +17.9% | 18% | 1x | [보기](C0071_heikin_ALL_1d.md) |
| C72 | 선형회귀 추세 유의성 | ZECUSDT | 30m | 1.44 | 1.72 | +90.6% | 36% | 0.5x | [보기](C0072_linreg_ZECUSDT_30m.md) |
| C73 | 켈트너 채널 | ZECUSDT | 5m | 1.67 | 1.17 | +49.1% | 19% | 1x | [보기](C0073_keltner_ZECUSDT_5m.md) |
| C74 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | XRPUSDT | 1h | 1.09 | 1.81 | +18.6% | 12% | 2.5x | [보기](C0074_squeeze_XRPUSDT_1h.md) |
| C75 | 횡단면 모멘텀/리버설 (10개 코인 순위) | ALL | 30m | 1.65 | 1.97 | +41.0% | 41% | 1x | [보기](C0075_xsmom_ALL_30m.md) |
| C76 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 4h | 1.66 | 1.12 | +8.1% | 5% | 5x | [보기](C0076_squeeze_ALL_4h.md) |
| C77 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 4h | 1.79 | 1.18 | +77.6% | 44% | 0.5x | [보기](C0077_squeeze_SOLUSDT_4h.md) |
| C78 | NR 협폭봉 돌파 | ALL | 1d | 1.19 | 1.70 | +13.8% | 16% | 1.5x | [보기](C0078_nr_breakout_ALL_1d.md) |
| C79 | RSI 과매도/과매수 역추세 | DOGEUSDT | 30m | 1.14 | 0.72 | +52.4% | 50% | 0.5x | [보기](C0079_rsi_mr_DOGEUSDT_30m.md) |
| C80 | MACD | ALL | 1d | 1.68 | 1.87 | +44.9% | 35% | 1x | [보기](C0080_macd_ALL_1d.md) |
| C81 | OBV 거래량 모멘텀 | ETHUSDT | 30m | 1.24 | 1.54 | +32.2% | 18% | 1.5x | [보기](C0081_obv_ETHUSDT_30m.md) |
| C82 | 아룬 추세 | DOGEUSDT | 1h | 1.23 | 0.84 | +45.3% | 47% | 0.5x | [보기](C0082_aroon_DOGEUSDT_1h.md) |
| C83 | ADX/DMI 추세 | SOLUSDT | 4h | 1.56 | 0.52 | +57.8% | 44% | 0.5x | [보기](C0083_adx_dmi_SOLUSDT_4h.md) |
| C84 | 선형회귀 추세 유의성 | BTCUSDT | 4h | 1.63 | 1.42 | +21.2% | 13% | 2.5x | [보기](C0084_linreg_BTCUSDT_4h.md) |
| C85 | 아룬 추세 | SOLUSDT | 4h | 1.42 | 1.49 | +61.3% | 39% | 0.5x | [보기](C0085_aroon_SOLUSDT_4h.md) |
| C86 | 시계열 모멘텀 (변동성 정규화) | ETHUSDT | 1d | 1.14 | 1.34 | +90.0% | 41% | 0.5x | [보기](C0086_tsmom_ETHUSDT_1d.md) |
| C87 | OBV 거래량 모멘텀 | SOLUSDT | 30m | 1.20 | 1.76 | +41.5% | 40% | 1x | [보기](C0087_obv_SOLUSDT_30m.md) |
| C88 | 파라볼릭 SAR | SOLUSDT | 1d | 1.23 | 1.27 | +48.3% | 48% | 0.5x | [보기](C0088_psar_SOLUSDT_1d.md) |
| C89 | 아룬 추세 | SOLUSDT | 4h | 1.00 | 1.35 | +88.0% | 36% | 0.5x | [보기](C0089_aroon_SOLUSDT_4h.md) |
| C90 | 일목균형표 | SOLUSDT | 4h | 1.17 | 1.68 | +25.3% | 26% | 1.5x | [보기](C0090_ichimoku_SOLUSDT_4h.md) |
| C91 | 일목균형표 | BNBUSDT | 1d | 1.33 | 1.37 | +69.5% | 55% | 0.5x | [보기](C0091_ichimoku_BNBUSDT_1d.md) |
| C92 | ADX/DMI 추세 | ALL | 1h | 1.32 | 0.61 | +8.3% | 9% | 1x | [보기](C0092_adx_dmi_ALL_1h.md) |
| C93 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 30m | 1.16 | 0.76 | +31.8% | 30% | 1x | [보기](C0093_squeeze_ZECUSDT_30m.md) |
| C94 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 30m | 1.63 | 1.62 | +33.8% | 17% | 1.5x | [보기](C0094_squeeze_ZECUSDT_30m.md) |
| C95 | 시계열 모멘텀 (변동성 정규화) | SOLUSDT | 4h | 1.42 | 0.92 | +66.5% | 35% | 0.5x | [보기](C0095_tsmom_SOLUSDT_4h.md) |
| C96 | RSI 과매도/과매수 역추세 | LINKUSDT | 15m | 1.45 | 1.20 | +10.4% | 9% | 3.5x | [보기](C0096_rsi_mr_LINKUSDT_15m.md) |
| C97 | ADX/DMI 추세 | ETHUSDT | 1h | 1.12 | 0.96 | +28.9% | 27% | 1x | [보기](C0097_adx_dmi_ETHUSDT_1h.md) |
| C98 | 캔들 패턴 | ALL | 4h | 1.73 | 1.01 | +20.4% | 9% | 1x | [보기](C0098_candle_ALL_4h.md) |
| C99 | 국면 전환 (추세/횡보 판별 후 전략 선택) | XRPUSDT | 4h | 1.46 | 1.07 | +56.1% | 61% | 0.5x | [보기](C0099_regime_XRPUSDT_4h.md) |
| C100 | OBV 거래량 모멘텀 | XRPUSDT | 5m | 2.06 | 1.33 | +24.7% | 10% | 0.5x | [보기](C0100_obv_XRPUSDT_5m.md) |
| C101 | 롤링 VWAP 이격 | ETHUSDT | 4h | 1.18 | 1.12 | +38.8% | 33% | 1x | [보기](C0101_vwap_dev_ETHUSDT_4h.md) |
| C102 | 슈퍼트렌드 | ETHUSDT | 4h | 1.44 | 0.52 | +32.7% | 31% | 1x | [보기](C0102_supertrend_ETHUSDT_4h.md) |
| C103 | 거래량 급증 돌파 | SOLUSDT | 4h | 1.11 | 1.92 | +35.5% | 39% | 1x | [보기](C0103_vol_breakout_SOLUSDT_4h.md) |
| C104 | RSI 과매도/과매수 역추세 | XRPUSDT | 5m | 1.47 | 0.91 | +7.8% | 7% | 2x | [보기](C0104_rsi_mr_XRPUSDT_5m.md) |
| C105 | 거래량 급증 돌파 | SOLUSDT | 4h | 1.12 | 1.12 | +120.4% | 54% | 0.5x | [보기](C0105_vol_breakout_SOLUSDT_4h.md) |
| C106 | 파라볼릭 SAR | TRXUSDT | 1d | 1.23 | 1.89 | +56.5% | 54% | 0.5x | [보기](C0106_psar_TRXUSDT_1d.md) |
| C107 | ADX/DMI 추세 | BTCUSDT | 1h | 1.14 | 1.22 | +19.5% | 23% | 2x | [보기](C0107_adx_dmi_BTCUSDT_1h.md) |
| C108 | 롤링 VWAP 이격 | DOGEUSDT | 5m | 1.81 | 1.78 | +56.9% | 11% | 0.5x | [보기](C0108_vwap_dev_DOGEUSDT_5m.md) |
| C109 | 거래량 급증 돌파 | ETHUSDT | 1h | 1.99 | 2.38 | +16.0% | 8% | 3.5x | [보기](C0109_vol_breakout_ETHUSDT_1h.md) |
| C110 | 슈퍼트렌드 | LINKUSDT | 4h | 1.01 | 0.71 | +53.2% | 44% | 0.5x | [보기](C0110_supertrend_LINKUSDT_4h.md) |
| C111 | 거래량 급증 돌파 | XRPUSDT | 15m | 1.21 | 2.04 | +43.4% | 34% | 1x | [보기](C0111_vol_breakout_XRPUSDT_15m.md) |
| C112 | 이동평균 교차 추세추종 | SOLUSDT | 30m | 1.20 | 0.90 | +14.2% | 12% | 3x | [보기](C0112_ma_cross_SOLUSDT_30m.md) |
| C113 | 펀딩비 쏠림 | SOLUSDT | 4h | 1.52 | 1.43 | +53.7% | 27% | 1x | [보기](C0113_funding_SOLUSDT_4h.md) |
| C114 | MACD | ALL | 1h | 1.75 | 2.03 | +29.9% | 26% | 1x | [보기](C0114_macd_ALL_1h.md) |
| C115 | Ornstein-Uhlenbeck 평균회귀 (z-score) | SOLUSDT | 5m | 1.26 | 1.32 | +8.3% | 14% | 2.5x | [보기](C0115_zscore_mr_SOLUSDT_5m.md) |
| C116 | 슈퍼트렌드 | BNBUSDT | 4h | 1.16 | 0.86 | +41.8% | 32% | 1x | [보기](C0116_supertrend_BNBUSDT_4h.md) |
| C117 | 슈퍼트렌드 | ZECUSDT | 1h | 1.39 | 2.23 | +78.4% | 38% | 0.5x | [보기](C0117_supertrend_ZECUSDT_1h.md) |
| C118 | 돈치안 채널 돌파 (터틀) | XRPUSDT | 4h | 1.37 | 2.06 | +34.4% | 18% | 1.5x | [보기](C0118_donchian_XRPUSDT_4h.md) |
| C119 | 돈치안 채널 돌파 (터틀) | ALL | 4h | 1.10 | 1.28 | +28.6% | 13% | 0.5x | [보기](C0119_donchian_ALL_4h.md) |
| C120 | 거래량 급증 돌파 | LINKUSDT | 1h | 1.34 | 1.13 | +44.1% | 35% | 1x | [보기](C0120_vol_breakout_LINKUSDT_1h.md) |
| C121 | RSI 과매도/과매수 역추세 | ALL | 5m | 1.07 | 0.87 | +9.0% | 3% | 1.5x | [보기](C0121_rsi_mr_ALL_5m.md) |
| C122 | 미결제약정(OI) × 가격 | ZECUSDT | 30m | 1.20 | 0.59 | +13.7% | 28% | 2x | [보기](C0122_oi_trend_ZECUSDT_30m.md) |
| C123 | ADX/DMI 추세 | ETHUSDT | 1h | 1.07 | 1.07 | +26.0% | 25% | 1.5x | [보기](C0123_adx_dmi_ETHUSDT_1h.md) |
| C124 | 롤링 VWAP 이격 | SOLUSDT | 30m | 1.17 | 1.36 | +44.6% | 32% | 1x | [보기](C0124_vwap_dev_SOLUSDT_30m.md) |
| C125 | 국면 전환 (추세/횡보 판별 후 전략 선택) | BTCUSDT | 1d | 1.51 | 0.82 | +43.6% | 39% | 1x | [보기](C0125_regime_BTCUSDT_1d.md) |
| C126 | 일목균형표 | ZECUSDT | 1h | 1.17 | 2.42 | +94.9% | 43% | 0.5x | [보기](C0126_ichimoku_ZECUSDT_1h.md) |
| C127 | 파라볼릭 SAR | SOLUSDT | 4h | 1.04 | 1.23 | +71.3% | 36% | 0.5x | [보기](C0127_psar_SOLUSDT_4h.md) |
| C128 | 아룬 추세 | ETHUSDT | 4h | 1.54 | 1.33 | +50.9% | 52% | 0.5x | [보기](C0128_aroon_ETHUSDT_4h.md) |
| C129 | 시계열 모멘텀 (변동성 정규화) | ETHUSDT | 1d | 1.00 | 1.16 | +59.3% | 49% | 0.5x | [보기](C0129_tsmom_ETHUSDT_1d.md) |
| C130 | ADX/DMI 추세 | ALL | 4h | 1.48 | 1.48 | +21.3% | 19% | 0.5x | [보기](C0130_adx_dmi_ALL_4h.md) |
| C131 | 거래량 급증 돌파 | XRPUSDT | 1h | 1.23 | 1.67 | +31.7% | 32% | 1x | [보기](C0131_vol_breakout_XRPUSDT_1h.md) |
| C132 | OBV 거래량 모멘텀 | BNBUSDT | 5m | 1.94 | 1.16 | +15.1% | 10% | 1x | [보기](C0132_obv_BNBUSDT_5m.md) |
| C133 | 펀딩비 쏠림 | ALL | 4h | 1.55 | 1.37 | +17.7% | 14% | 1x | [보기](C0133_funding_ALL_4h.md) |
| C134 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 1.66 | 1.64 | +29.0% | 22% | 1x | [보기](C0134_regime_ALL_4h.md) |
| C135 | 롱/숏 비율 포지셔닝 | SOLUSDT | 30m | 1.30 | 1.36 | +60.9% | 34% | 1x | [보기](C0135_positioning_SOLUSDT_30m.md) |
| C136 | 켈트너 채널 | BNBUSDT | 30m | 1.75 | 1.27 | +21.6% | 9% | 2.5x | [보기](C0136_keltner_BNBUSDT_30m.md) |
| C137 | OBV 거래량 모멘텀 | DOGEUSDT | 30m | 1.35 | 0.55 | +37.2% | 28% | 0.5x | [보기](C0137_obv_DOGEUSDT_30m.md) |
| C138 | 거래량 급증 돌파 | SOLUSDT | 4h | 1.91 | 1.32 | +91.2% | 46% | 0.5x | [보기](C0138_vol_breakout_SOLUSDT_4h.md) |
| C139 | RSI 과매도/과매수 역추세 | SOLUSDT | 30m | 1.67 | 0.55 | +14.7% | 14% | 1.5x | [보기](C0139_rsi_mr_SOLUSDT_30m.md) |
| C140 | 롤링 VWAP 이격 | ZECUSDT | 5m | 2.40 | 1.44 | +30.8% | 18% | 1x | [보기](C0140_vwap_dev_ZECUSDT_5m.md) |
| C141 | 돈치안 채널 돌파 (터틀) | BNBUSDT | 4h | 1.06 | 1.56 | +23.5% | 16% | 1.5x | [보기](C0141_donchian_BNBUSDT_4h.md) |
| C142 | MFI (거래량 가중 RSI) 역추세 | BNBUSDT | 1h | 1.12 | 0.97 | +49.3% | 25% | 1x | [보기](C0142_mfi_BNBUSDT_1h.md) |
| C143 | RSI 과매도/과매수 역추세 | ZECUSDT | 5m | 1.51 | 2.29 | +14.9% | 8% | 5x | [보기](C0143_rsi_mr_ZECUSDT_5m.md) |
| C144 | 파라볼릭 SAR | BTCUSDT | 1d | 1.15 | 0.55 | +29.0% | 31% | 1x | [보기](C0144_psar_BTCUSDT_1d.md) |
| C145 | 롤링 VWAP 이격 | TRXUSDT | 4h | 1.63 | 1.03 | +35.8% | 39% | 1x | [보기](C0145_vwap_dev_TRXUSDT_4h.md) |
| C146 | MACD | ETHUSDT | 4h | 1.26 | 0.77 | +48.9% | 49% | 0.5x | [보기](C0146_macd_ETHUSDT_4h.md) |
| C147 | NR 협폭봉 돌파 | ETHUSDT | 4h | 1.14 | 0.70 | +30.6% | 31% | 1.5x | [보기](C0147_nr_breakout_ETHUSDT_4h.md) |
| C148 | 페어 트레이딩 (공적분 스프레드 평균회귀) | LINKUSDT/SOLUSDT | 15m | 1.22 | 0.97 | +14.2% | 12% | 3x | [보기](C0148_pairs_LINKUSDT-SOLUSDT_15m.md) |
| C149 | 슈퍼트렌드 | ALL | 1d | 1.17 | 2.42 | +11.3% | 10% | 1.5x | [보기](C0149_supertrend_ALL_1d.md) |
| C150 | 슈퍼트렌드 | ALL | 1d | 1.08 | 1.72 | +16.6% | 12% | 0.5x | [보기](C0150_supertrend_ALL_1d.md) |
| C151 | 아룬 추세 | DOGEUSDT | 1h | 1.37 | 1.44 | +58.8% | 47% | 0.5x | [보기](C0151_aroon_DOGEUSDT_1h.md) |
| C152 | 일목균형표 | XRPUSDT | 4h | 1.61 | 0.97 | +59.9% | 45% | 0.5x | [보기](C0152_ichimoku_XRPUSDT_4h.md) |
| C153 | 거래량 급증 돌파 | DOGEUSDT | 1h | 1.50 | 0.87 | +47.6% | 49% | 0.5x | [보기](C0153_vol_breakout_DOGEUSDT_1h.md) |
| C154 | 시계열 모멘텀 (변동성 정규화) | ALL | 1d | 1.16 | 1.26 | +62.0% | 54% | 0.5x | [보기](C0154_tsmom_ALL_1d.md) |
| C155 | 선형회귀 추세 유의성 | TRXUSDT | 1h | 1.32 | 0.77 | +33.6% | 32% | 1x | [보기](C0155_linreg_TRXUSDT_1h.md) |
| C156 | 미결제약정(OI) × 가격 | DOGEUSDT | 30m | 1.67 | 0.97 | +16.5% | 13% | 0.5x | [보기](C0156_oi_trend_DOGEUSDT_30m.md) |
| C157 | 미결제약정(OI) × 가격 | DOGEUSDT | 30m | 2.05 | 0.57 | +15.6% | 9% | 0.5x | [보기](C0157_oi_trend_DOGEUSDT_30m.md) |
| C158 | 거래량 급증 돌파 | DOGEUSDT | 4h | 1.38 | 0.57 | +29.1% | 27% | 1x | [보기](C0158_vol_breakout_DOGEUSDT_4h.md) |
| C159 | 일목균형표 | ETHUSDT | 1h | 1.04 | 0.61 | +22.6% | 39% | 1.5x | [보기](C0159_ichimoku_ETHUSDT_1h.md) |
| C160 | MACD | BNBUSDT | 1h | 1.25 | 0.60 | +53.3% | 30% | 1x | [보기](C0160_macd_BNBUSDT_1h.md) |
| C161 | 선형회귀 추세 유의성 | ALL | 4h | 1.12 | 1.35 | +15.2% | 16% | 0.5x | [보기](C0161_linreg_ALL_4h.md) |
| C162 | 롱/숏 비율 포지셔닝 | BTCUSDT | 1h | 1.35 | 0.81 | +15.6% | 14% | 2.5x | [보기](C0162_positioning_BTCUSDT_1h.md) |
| C163 | ADX/DMI 추세 | ETHUSDT | 1h | 1.93 | 0.99 | +70.3% | 41% | 0.5x | [보기](C0163_adx_dmi_ETHUSDT_1h.md) |
| C164 | 일목균형표 | SOLUSDT | 4h | 1.68 | 0.50 | +124.2% | 57% | 0.5x | [보기](C0164_ichimoku_SOLUSDT_4h.md) |
| C165 | Ornstein-Uhlenbeck 평균회귀 (z-score) | ZECUSDT | 5m | 1.75 | 1.06 | +17.5% | 17% | 2.5x | [보기](C0165_zscore_mr_ZECUSDT_5m.md) |
| C166 | RSI 과매도/과매수 역추세 | BNBUSDT | 1h | 1.35 | 0.90 | +21.3% | 32% | 1.5x | [보기](C0166_rsi_mr_BNBUSDT_1h.md) |
| C167 | 캔들 패턴 | XRPUSDT | 1d | 1.15 | 1.04 | +40.8% | 38% | 0.5x | [보기](C0167_candle_XRPUSDT_1d.md) |
| C168 | 선형회귀 추세 유의성 | ETHUSDT | 1h | 1.05 | 1.11 | +42.2% | 25% | 1x | [보기](C0168_linreg_ETHUSDT_1h.md) |
| C169 | 페어 트레이딩 (공적분 스프레드 평균회귀) | XRPUSDT/BNBUSDT | 30m | 1.53 | 0.72 | +22.0% | 29% | 1.5x | [보기](C0169_pairs_XRPUSDT-BNBUSDT_30m.md) |
| C170 | 페어 트레이딩 (공적분 스프레드 평균회귀) | BNBUSDT/ETHUSDT | 30m | 1.01 | 0.80 | +34.3% | 32% | 1x | [보기](C0170_pairs_BNBUSDT-ETHUSDT_30m.md) |
| C171 | 켈트너 채널 | LINKUSDT | 15m | 1.11 | 0.53 | +22.7% | 25% | 1x | [보기](C0171_keltner_LINKUSDT_15m.md) |
| C172 | 하이킨아시 연속봉 | DOGEUSDT | 4h | 1.27 | 1.13 | +82.8% | 51% | 0.5x | [보기](C0172_heikin_DOGEUSDT_4h.md) |
| C173 | Ornstein-Uhlenbeck 평균회귀 (z-score) | LINKUSDT | 15m | 1.57 | 1.00 | +28.7% | 12% | 1.5x | [보기](C0173_zscore_mr_LINKUSDT_15m.md) |
| C174 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ETHUSDT | 4h | 1.43 | 1.31 | +39.6% | 31% | 1x | [보기](C0174_squeeze_ETHUSDT_4h.md) |
| C175 | 페어 트레이딩 (공적분 스프레드 평균회귀) | ETHUSDT/TRXUSDT | 4h | 1.43 | 0.95 | +35.4% | 22% | 1.5x | [보기](C0175_pairs_ETHUSDT-TRXUSDT_4h.md) |
| C176 | 이동평균 교차 추세추종 | ETHUSDT | 30m | 1.74 | 1.01 | +51.3% | 30% | 1x | [보기](C0176_ma_cross_ETHUSDT_30m.md) |
| C177 | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ETHUSDT | 4h | 1.48 | 1.19 | +41.5% | 26% | 1x | [보기](C0177_squeeze_ETHUSDT_4h.md) |
| C178 | MACD | TRXUSDT | 1d | 1.40 | 1.09 | +53.9% | 44% | 0.5x | [보기](C0178_macd_TRXUSDT_1d.md) |
| C179 | MACD | ETHUSDT | 30m | 1.17 | 0.94 | +27.4% | 22% | 1.5x | [보기](C0179_macd_ETHUSDT_30m.md) |
| C180 | 아룬 추세 | BNBUSDT | 30m | 1.04 | 0.60 | +37.2% | 23% | 1x | [보기](C0180_aroon_BNBUSDT_30m.md) |
| C181 | OBV 거래량 모멘텀 | ALL | 4h | 1.51 | 0.79 | +43.8% | 36% | 0.5x | [보기](C0181_obv_ALL_4h.md) |
| C182 | ADX/DMI 추세 | SOLUSDT | 1d | 1.31 | 0.88 | +100.4% | 54% | 0.5x | [보기](C0182_adx_dmi_SOLUSDT_1d.md) |
| C183 | 시계열 모멘텀 (변동성 정규화) | BTCUSDT | 15m | 1.10 | 0.91 | +40.5% | 42% | 1x | [보기](C0183_tsmom_BTCUSDT_15m.md) |
| C184 | 슈퍼트렌드 | SOLUSDT | 1d | 1.48 | 1.07 | +93.3% | 52% | 0.5x | [보기](C0184_supertrend_SOLUSDT_1d.md) |
| C185 | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 1.21 | 0.69 | +50.6% | 30% | 0.5x | [보기](C0185_regime_ALL_4h.md) |
| C186 | 선형회귀 추세 유의성 | ETHUSDT | 1d | 1.02 | 1.02 | +54.9% | 35% | 0.5x | [보기](C0186_linreg_ETHUSDT_1d.md) |
| C187 | 켈트너 채널 | XRPUSDT | 5m | 1.29 | 1.59 | +47.2% | 27% | 0.5x | [보기](C0187_keltner_XRPUSDT_5m.md) |
| C188 | OBV 거래량 모멘텀 | SOLUSDT | 4h | 1.38 | 3.70 | +44.0% | 38% | 1x | [보기](C0188_obv_SOLUSDT_4h.md) |
