# 페이퍼 트레이딩 후보 목록

엄격한 과최적화 검정 없이 검증·홀드아웃 구간 수익, 비용 스트레스, 파라미터 안정성만 통과한 후보입니다. 같은 아이디어의 변형은 더 좋은 것이 나오면 교체되고, 목록은 min(검증, 홀드아웃 샤프) 상위 최대 50개만 유지합니다 (밀려난 후보는 [archive](archive/)에 보관되며 번호로 계속 실행 가능). `python run_strategy.py paper --pick C번호` 로 모의매매할 수 있습니다.

| # | 등급 | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | B | 선형회귀 추세 유의성 | ALL | 30m | 2.40 | 2.30 | +35.4% | 16% | 1x | [보기](C0001_linreg_ALL_30m.md) |
| C3 | B | 거래량 급증 돌파 | ALL | 30m | 2.37 | 2.19 | +21.0% | 8% | 1x | [보기](C0003_vol_breakout_ALL_30m.md) |
| C20 | B | 아룬 추세 | ALL | 4h | 2.49 | 2.28 | +34.4% | 12% | 0.5x | [보기](C0020_aroon_ALL_4h.md) |
| C39 | B | 파라볼릭 SAR | ALL | 1d | 1.89 | 1.85 | +36.0% | 23% | 0.5x | [보기](C0039_psar_ALL_1d.md) |
| C49 | B | 캔들 패턴 | ALL | 4h | 1.80 | 1.62 | +17.4% | 11% | 1.5x | [보기](C0049_candle_ALL_4h.md) |
| C53 | B | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 1d | 1.63 | 1.76 | +22.3% | 14% | 1x | [보기](C0053_regime_ALL_1d.md) |
| C59 | B | 롤링 VWAP 이격 | XRPUSDT | 5m | 2.20 | 2.34 | +48.7% | 16% | 1x | [보기](C0059_vwap_dev_XRPUSDT_5m.md) |
| C108 | B | 롤링 VWAP 이격 | DOGEUSDT | 5m | 1.97 | 2.09 | +56.0% | 11% | 0.5x | [보기](C0108_vwap_dev_DOGEUSDT_5m.md) |
| C304 | B | 하이킨아시 연속봉 | ALL | 1d | 2.07 | 2.49 | +37.7% | 14% | 0.5x | [보기](C0304_heikin_ALL_1d.md) |
| C321 | B | OBV 거래량 모멘텀 | ALL | 1h | 2.12 | 2.07 | +6.8% | 6% | 1x | [보기](C0321_obv_ALL_1h.md) |
| C373 | B | 켈트너 채널 | ALL | 15m | 2.31 | 2.71 | +5.4% | 3% | 1x | [보기](C0373_keltner_ALL_15m.md) |
| C385 | B | 미결제약정(OI) × 가격 | ALL | 30m | 2.50 | 1.52 | +11.2% | 5% | 0.5x | [보기](C0385_oi_trend_ALL_30m.md) |
| C2 | C | MACD | ALL | 1d | 2.06 | 2.70 | +43.9% | 18% | 0.5x | [보기](C0002_macd_ALL_1d.md) |
| C5 | C | 켈트너 채널 | ETHUSDT | 30m | 1.93 | 2.29 | +17.0% | 7% | 3.5x | [보기](C0005_keltner_ETHUSDT_30m.md) |
| C9 | C | 캔들 패턴 | ALL | 4h | 2.08 | 1.98 | +37.8% | 19% | 0.5x | [보기](C0009_candle_ALL_4h.md) |
| C11 | C | 켈트너 채널 | ALL | 15m | 2.57 | 2.61 | +5.2% | 4% | 2.5x | [보기](C0011_keltner_ALL_15m.md) |
| C13 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | ALL | 1h | 2.20 | 1.90 | +4.6% | 3% | 2x | [보기](C0013_zscore_mr_ALL_1h.md) |
| C23 | C | 슈퍼트렌드 | ALL | 4h | 2.01 | 2.37 | +13.2% | 12% | 0.5x | [보기](C0023_supertrend_ALL_4h.md) |
| C26 | C | 거래량 급증 돌파 | ETHUSDT | 1h | 2.41 | 2.55 | +9.7% | 5% | 5x | [보기](C0026_vol_breakout_ETHUSDT_1h.md) |
| C27 | C | 테이커 주문흐름 불균형 | ALL | 4h | 1.99 | 1.96 | +30.1% | 34% | 0.5x | [보기](C0027_flow_ALL_4h.md) |
| C28 | C | OBV 거래량 모멘텀 | ALL | 4h | 2.17 | 2.22 | +13.1% | 11% | 1.5x | [보기](C0028_obv_ALL_4h.md) |
| C33 | C | 켈트너 채널 | ALL | 1h | 2.14 | 1.81 | +12.6% | 10% | 1x | [보기](C0033_keltner_ALL_1h.md) |
| C40 | C | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 2.19 | 2.09 | +19.7% | 11% | 1x | [보기](C0040_regime_ALL_4h.md) |
| C41 | C | 이동평균 교차 추세추종 | ALL | 4h | 1.94 | 1.74 | +14.4% | 11% | 2x | [보기](C0041_ma_cross_ALL_4h.md) |
| C42 | C | 캔들 패턴 | SOLUSDT | 4h | 1.87 | 2.81 | +67.3% | 48% | 0.5x | [보기](C0042_candle_SOLUSDT_4h.md) |
| C54 | C | 켈트너 채널 | SOLUSDT | 30m | 1.96 | 1.86 | +23.1% | 9% | 2x | [보기](C0054_keltner_SOLUSDT_30m.md) |
| C60 | C | 롤링 VWAP 이격 | ALL | 1h | 1.90 | 2.03 | +29.2% | 15% | 0.5x | [보기](C0060_vwap_dev_ALL_1h.md) |
| C61 | C | 슈퍼트렌드 | SOLUSDT | 1d | 1.67 | 1.82 | +119.6% | 56% | 0.5x | [보기](C0061_supertrend_SOLUSDT_1d.md) |
| C69 | C | 롱/숏 비율 포지셔닝 | ALL | 30m | 2.55 | 2.22 | +32.1% | 16% | 1x | [보기](C0069_positioning_ALL_30m.md) |
| C72 | C | 일목균형표 | ZECUSDT | 1h | 2.29 | 2.31 | +124.4% | 47% | 0.5x | [보기](C0072_ichimoku_ZECUSDT_1h.md) |
| C75 | C | 횡단면 모멘텀/리버설 (10개 코인 순위) | ALL | 15m | 1.73 | 1.66 | +39.0% | 23% | 1.5x | [보기](C0075_xsmom_ALL_15m.md) |
| C80 | C | MACD | ALL | 1d | 1.68 | 1.87 | +44.9% | 35% | 1x | [보기](C0080_macd_ALL_1d.md) |
| C88 | C | 파라볼릭 SAR | SOLUSDT | 1d | 1.62 | 2.14 | +60.6% | 52% | 0.5x | [보기](C0088_psar_SOLUSDT_1d.md) |
| C94 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 4h | 2.16 | 1.83 | +54.3% | 27% | 1x | [보기](C0094_squeeze_ZECUSDT_4h.md) |
| C102 | C | 아룬 추세 | ETHUSDT | 4h | 1.96 | 1.73 | +50.6% | 23% | 1x | [보기](C0102_aroon_ETHUSDT_4h.md) |
| C109 | C | 거래량 급증 돌파 | ETHUSDT | 15m | 2.35 | 2.21 | +84.4% | 27% | 1x | [보기](C0109_vol_breakout_ETHUSDT_15m.md) |
| C133 | C | 펀딩비 쏠림 | ALL | 1h | 1.89 | 1.69 | +24.1% | 28% | 0.5x | [보기](C0133_funding_ALL_1h.md) |
| C136 | C | 켈트너 채널 | BNBUSDT | 15m | 2.08 | 2.19 | +28.0% | 11% | 3x | [보기](C0136_keltner_BNBUSDT_15m.md) |
| C234 | C | 돈치안 채널 돌파 (터틀) | ALL | 1d | 1.75 | 2.01 | +17.6% | 13% | 0.5x | [보기](C0234_donchian_ALL_1d.md) |
| C242 | C | 돈치안 채널 돌파 (터틀) | DOGEUSDT | 4h | 2.07 | 1.95 | +41.5% | 17% | 1.5x | [보기](C0242_donchian_DOGEUSDT_4h.md) |
| C284 | C | 롱/숏 비율 포지셔닝 | BTCUSDT | 1h | 2.00 | 1.74 | +28.6% | 11% | 2.5x | [보기](C0284_positioning_BTCUSDT_1h.md) |
| C285 | C | 일목균형표 | BNBUSDT | 1h | 2.10 | 1.77 | +45.1% | 24% | 1x | [보기](C0285_ichimoku_BNBUSDT_1h.md) |
| C289 | C | 미결제약정(OI) × 가격 | ALL | 30m | 2.50 | 1.97 | +13.2% | 7% | 0.5x | [보기](C0289_oi_trend_ALL_30m.md) |
| C292 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 4h | 2.48 | 2.24 | +23.5% | 15% | 1x | [보기](C0292_squeeze_ALL_4h.md) |
| C300 | C | 롱/숏 비율 포지셔닝 | ALL | 4h | 2.38 | 2.37 | +13.0% | 7% | 1.5x | [보기](C0300_positioning_ALL_4h.md) |
| C311 | C | RSI 과매도/과매수 역추세 | ZECUSDT | 30m | 1.87 | 2.25 | +31.8% | 23% | 1.5x | [보기](C0311_rsi_mr_ZECUSDT_30m.md) |
| C317 | C | 거래량 급증 돌파 | ALL | 4h | 2.32 | 2.50 | +8.5% | 7% | 1.5x | [보기](C0317_vol_breakout_ALL_4h.md) |
| C341 | C | 미결제약정(OI) × 가격 | BNBUSDT | 1h | 2.60 | 2.01 | +15.1% | 8% | 4x | [보기](C0341_oi_trend_BNBUSDT_1h.md) |
| C344 | C | 돈치안 채널 돌파 (터틀) | XRPUSDT | 1h | 1.71 | 1.69 | +70.0% | 48% | 0.5x | [보기](C0344_donchian_XRPUSDT_1h.md) |
| C364 | C | 거래량 급증 돌파 | SOLUSDT | 4h | 1.98 | 1.98 | +47.3% | 32% | 0.5x | [보기](C0364_vol_breakout_SOLUSDT_4h.md) |
| C377 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | DOGEUSDT | 4h | 1.62 | 1.85 | +52.5% | 41% | 1x | [보기](C0377_squeeze_DOGEUSDT_4h.md) |
| C378 | C | 시계열 모멘텀 (변동성 정규화) | SOLUSDT | 15m | 2.51 | 2.64 | +59.6% | 44% | 1x | [보기](C0378_tsmom_SOLUSDT_15m.md) |
| C379 | C | 일목균형표 | ALL | 4h | 2.01 | 1.77 | +21.3% | 22% | 0.5x | [보기](C0379_ichimoku_ALL_4h.md) |
| C380 | C | 켈트너 채널 | ZECUSDT | 15m | 1.98 | 1.94 | +17.2% | 10% | 1x | [보기](C0380_keltner_ZECUSDT_15m.md) |
| C381 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | ZECUSDT | 1h | 1.81 | 2.42 | +30.6% | 16% | 2x | [보기](C0381_zscore_mr_ZECUSDT_1h.md) |
| C382 | C | OBV 거래량 모멘텀 | ZECUSDT | 30m | 2.01 | 1.72 | +23.1% | 38% | 2x | [보기](C0382_obv_ZECUSDT_30m.md) |
| C383 | C | 이동평균 교차 추세추종 | BNBUSDT | 4h | 1.47 | 1.76 | +40.9% | 28% | 1x | [보기](C0383_ma_cross_BNBUSDT_4h.md) |
| C384 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | BNBUSDT/ETHUSDT | 4h | 1.21 | 1.22 | +18.0% | 12% | 2.5x | [보기](C0384_pairs_BNBUSDT-ETHUSDT_4h.md) |
