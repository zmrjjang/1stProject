# 페이퍼 트레이딩 후보 목록

엄격한 과최적화 검정 없이 검증·홀드아웃 구간 수익, 비용 스트레스, 파라미터 안정성만 통과한 후보입니다. 같은 아이디어의 변형은 더 좋은 것이 나오면 교체되고, 목록은 min(검증, 홀드아웃 샤프) 상위 최대 50개만 유지합니다 (밀려난 후보는 [archive](archive/)에 보관되며 번호로 계속 실행 가능). `python run_strategy.py paper --pick C번호` 로 모의매매할 수 있습니다.

| # | 등급 | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | B | 선형회귀 추세 유의성 | ALL | 30m | 2.40 | 2.30 | +35.4% | 16% | 1x | [보기](C0001_linreg_ALL_30m.md) |
| C3 | B | 거래량 급증 돌파 | ALL | 1h | 2.49 | 2.88 | +16.7% | 13% | 0.5x | [보기](C0003_vol_breakout_ALL_1h.md) |
| C9 | B | 슈퍼트렌드 | ALL | 4h | 2.10 | 2.16 | +40.8% | 15% | 0.5x | [보기](C0009_supertrend_ALL_4h.md) |
| C20 | B | 아룬 추세 | ALL | 4h | 2.49 | 2.28 | +34.4% | 12% | 0.5x | [보기](C0020_aroon_ALL_4h.md) |
| C23 | B | 슈퍼트렌드 | ALL | 4h | 2.03 | 2.11 | +35.4% | 18% | 0.5x | [보기](C0023_supertrend_ALL_4h.md) |
| C39 | B | 하이킨아시 연속봉 | ALL | 1d | 2.35 | 2.16 | +41.6% | 16% | 1x | [보기](C0039_heikin_ALL_1d.md) |
| C49 | B | 캔들 패턴 | ALL | 4h | 1.80 | 1.62 | +17.4% | 11% | 1.5x | [보기](C0049_candle_ALL_4h.md) |
| C53 | B | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 1d | 1.63 | 1.76 | +22.3% | 14% | 1x | [보기](C0053_regime_ALL_1d.md) |
| C59 | B | 롤링 VWAP 이격 | XRPUSDT | 5m | 2.20 | 2.34 | +48.7% | 16% | 1x | [보기](C0059_vwap_dev_XRPUSDT_5m.md) |
| C108 | B | 롤링 VWAP 이격 | DOGEUSDT | 5m | 1.97 | 2.09 | +56.0% | 11% | 0.5x | [보기](C0108_vwap_dev_DOGEUSDT_5m.md) |
| C234 | B | 돈치안 채널 돌파 (터틀) | ALL | 1d | 1.77 | 2.15 | +21.5% | 13% | 0.5x | [보기](C0234_donchian_ALL_1d.md) |
| C304 | B | 하이킨아시 연속봉 | ALL | 1d | 2.07 | 2.49 | +37.7% | 14% | 0.5x | [보기](C0304_heikin_ALL_1d.md) |
| C321 | B | OBV 거래량 모멘텀 | ALL | 1h | 2.12 | 2.07 | +6.8% | 6% | 1x | [보기](C0321_obv_ALL_1h.md) |
| C373 | B | 켈트너 채널 | ALL | 15m | 2.31 | 2.71 | +5.4% | 3% | 1x | [보기](C0373_keltner_ALL_15m.md) |
| C385 | B | 미결제약정(OI) × 가격 | ALL | 1h | 3.18 | 1.62 | +9.5% | 3% | 0.5x | [보기](C0385_oi_trend_ALL_1h.md) |
| C398 | B | MACD | ALL | 1d | 2.53 | 2.62 | +25.6% | 9% | 2x | [보기](C0398_macd_ALL_1d.md) |
| C415 | B | ADX/DMI 추세 | ALL | 4h | 1.63 | 1.51 | +25.6% | 13% | 0.5x | [보기](C0415_adx_dmi_ALL_4h.md) |
| C424 | B | 파라볼릭 SAR | ALL | 1d | 2.16 | 1.85 | +22.4% | 7% | 1x | [보기](C0424_psar_ALL_1d.md) |
| C427 | B | 거래량 급증 돌파 | ALL | 4h | 1.83 | 2.23 | +28.6% | 17% | 0.5x | [보기](C0427_vol_breakout_ALL_4h.md) |
| C430 | B | 이동평균 교차 추세추종 | ALL | 4h | 2.30 | 2.00 | +12.8% | 6% | 1x | [보기](C0430_ma_cross_ALL_4h.md) |
| C438 | B | 아룬 추세 | ETHUSDT | 1h | 1.71 | 2.51 | +75.7% | 21% | 1x | [보기](C0438_aroon_ETHUSDT_1h.md) |
| C440 | B | 롤링 VWAP 이격 | ALL | 1h | 1.80 | 2.19 | +33.4% | 18% | 1x | [보기](C0440_vwap_dev_ALL_1h.md) |
| C441 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ETHUSDT | 30m | 1.78 | 1.60 | +65.3% | 17% | 1x | [보기](C0441_squeeze_ETHUSDT_30m.md) |
| C445 | B | 선형회귀 추세 유의성 | ETHUSDT | 1h | 1.56 | 1.78 | +39.4% | 18% | 1.5x | [보기](C0445_linreg_ETHUSDT_1h.md) |
| C464 | B | 시장 구조 (고점·저점 낮아짐) | ALL | 1h | 1.96 | 2.48 | +23.6% | 7% | 1x | [보기](C0464_structure_ALL_1h.md) |
| C467 | B | 하방 변동성 확대 (레버리지 효과) | ALL | 1h | 3.01 | 2.78 | +7.8% | 3% | 1.5x | [보기](C0467_vol_down_ALL_1h.md) |
| C477 | B | 하락추세 반등 매도 (상승추세 눌림 매수) | ALL | 1h | 2.28 | 2.37 | +9.7% | 6% | 1x | [보기](C0477_rally_fade_ALL_1h.md) |
| C490 | B | 미결제약정(OI) × 가격 | SOLUSDT | 30m | 2.43 | 1.84 | +42.1% | 24% | 1.5x | [보기](C0490_oi_trend_SOLUSDT_30m.md) |
| C491 | B | 미결제약정(OI) × 가격 | SOLUSDT | 30m | 1.81 | 1.69 | +33.2% | 19% | 1.5x | [보기](C0491_oi_trend_SOLUSDT_30m.md) |
| C492 | B | 하락추세 반등 매도 (상승추세 눌림 매수) | ALL | 4h | 2.05 | 2.00 | +17.1% | 10% | 1x | [보기](C0492_rally_fade_ALL_4h.md) |
| C496 | B | 롱/숏 비율 포지셔닝 | BTCUSDT | 30m | 1.77 | 1.52 | +51.5% | 21% | 1.5x | [보기](C0496_positioning_BTCUSDT_30m.md) |
| C522 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 4h | 1.76 | 2.12 | +11.5% | 8% | 2.5x | [보기](C0522_squeeze_ALL_4h.md) |
| C528 | B | Ornstein-Uhlenbeck 평균회귀 (z-score) | ALL | 1h | 2.31 | 1.82 | +9.5% | 4% | 1.5x | [보기](C0528_zscore_mr_ALL_1h.md) |
| C529 | B | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/BTCUSDT | 30m | 1.58 | 2.08 | +39.1% | 17% | 1.5x | [보기](C0529_pairs_DOGEUSDT-BTCUSDT_30m.md) |
| C531 | B | 파라볼릭 SAR | DOGEUSDT | 4h | 1.64 | 1.63 | +46.7% | 19% | 1.5x | [보기](C0531_psar_DOGEUSDT_4h.md) |
| C540 | B | 과열 소진 역추세 (블로오프) | ALL | 15m | 1.61 | 1.64 | +7.8% | 2% | 1x | [보기](C0540_blowoff_ALL_15m.md) |
| C545 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 30m | 1.54 | 1.60 | +37.1% | 15% | 2x | [보기](C0545_squeeze_SOLUSDT_30m.md) |
| C547 | B | 아룬 추세 | ALL | 4h | 1.71 | 2.04 | +41.6% | 15% | 0.5x | [보기](C0547_aroon_ALL_4h.md) |
| C548 | B | MACD | ALL | 1d | 1.65 | 1.95 | +38.3% | 23% | 0.5x | [보기](C0548_macd_ALL_1d.md) |
| C549 | B | ADX/DMI 추세 | ETHUSDT | 15m | 3.10 | 2.13 | +18.3% | 10% | 3.5x | [보기](C0549_adx_dmi_ETHUSDT_15m.md) |
| C551 | B | 켈트너 채널 | SOLUSDT | 5m | 1.51 | 1.59 | +57.4% | 21% | 0.5x | [보기](C0551_keltner_SOLUSDT_5m.md) |
| C2 | C | 돈치안 채널 돌파 (터틀) | ALL | 4h | 2.13 | 2.14 | +47.6% | 35% | 0.5x | [보기](C0002_donchian_ALL_4h.md) |
| C5 | C | 켈트너 채널 | ETHUSDT | 30m | 1.98 | 1.94 | +16.5% | 8% | 3.5x | [보기](C0005_keltner_ETHUSDT_30m.md) |
| C11 | C | 켈트너 채널 | ALL | 15m | 2.57 | 2.61 | +5.2% | 4% | 2.5x | [보기](C0011_keltner_ALL_15m.md) |
| C26 | C | 거래량 급증 돌파 | ETHUSDT | 1h | 3.25 | 3.32 | +16.4% | 12% | 2x | [보기](C0026_vol_breakout_ETHUSDT_1h.md) |
| C27 | C | 테이커 주문흐름 불균형 | ALL | 4h | 1.99 | 1.96 | +30.1% | 34% | 0.5x | [보기](C0027_flow_ALL_4h.md) |
| C28 | C | OBV 거래량 모멘텀 | ALL | 4h | 2.28 | 2.85 | +16.2% | 23% | 1.5x | [보기](C0028_obv_ALL_4h.md) |
| C33 | C | 켈트너 채널 | ALL | 1h | 2.20 | 2.28 | +9.0% | 5% | 1x | [보기](C0033_keltner_ALL_1h.md) |
| C40 | C | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 2.47 | 2.47 | +17.8% | 16% | 0.5x | [보기](C0040_regime_ALL_4h.md) |
| C42 | C | 캔들 패턴 | SOLUSDT | 4h | 1.93 | 1.92 | +69.4% | 31% | 1x | [보기](C0042_candle_SOLUSDT_4h.md) |
| C60 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 1h | 2.72 | 2.69 | +18.5% | 12% | 2x | [보기](C0060_squeeze_ALL_1h.md) |
| C69 | C | 롱/숏 비율 포지셔닝 | ALL | 30m | 2.55 | 2.22 | +32.1% | 16% | 1x | [보기](C0069_positioning_ALL_30m.md) |
| C72 | C | 일목균형표 | ZECUSDT | 1h | 2.29 | 2.31 | +124.4% | 47% | 0.5x | [보기](C0072_ichimoku_ZECUSDT_1h.md) |
| C94 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 1h | 2.10 | 1.97 | +48.2% | 17% | 1.5x | [보기](C0094_squeeze_ZECUSDT_1h.md) |
| C109 | C | 거래량 급증 돌파 | ETHUSDT | 15m | 2.34 | 2.46 | +93.7% | 32% | 0.5x | [보기](C0109_vol_breakout_ETHUSDT_15m.md) |
| C136 | C | 켈트너 채널 | BNBUSDT | 15m | 2.30 | 2.15 | +27.9% | 10% | 3x | [보기](C0136_keltner_BNBUSDT_15m.md) |
| C242 | C | 돈치안 채널 돌파 (터틀) | DOGEUSDT | 4h | 2.07 | 1.95 | +41.5% | 17% | 1.5x | [보기](C0242_donchian_DOGEUSDT_4h.md) |
| C289 | C | 미결제약정(OI) × 가격 | ALL | 30m | 2.21 | 2.81 | +10.0% | 6% | 0.5x | [보기](C0289_oi_trend_ALL_30m.md) |
| C292 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 1h | 2.40 | 2.34 | +20.4% | 15% | 2x | [보기](C0292_squeeze_ALL_1h.md) |
| C300 | C | 롱/숏 비율 포지셔닝 | ALL | 4h | 2.38 | 2.37 | +13.0% | 7% | 1.5x | [보기](C0300_positioning_ALL_4h.md) |
| C311 | C | RSI 과매도/과매수 역추세 | ZECUSDT | 5m | 2.42 | 2.43 | +32.2% | 21% | 2x | [보기](C0311_rsi_mr_ZECUSDT_5m.md) |
| C317 | C | 거래량 급증 돌파 | ALL | 4h | 2.32 | 2.50 | +8.5% | 7% | 1.5x | [보기](C0317_vol_breakout_ALL_4h.md) |
| C341 | C | 미결제약정(OI) × 가격 | BNBUSDT | 1h | 3.96 | 2.24 | +20.3% | 10% | 2.5x | [보기](C0341_oi_trend_BNBUSDT_1h.md) |
| C364 | C | 거래량 급증 돌파 | SOLUSDT | 4h | 1.98 | 1.98 | +47.3% | 32% | 0.5x | [보기](C0364_vol_breakout_SOLUSDT_4h.md) |
| C378 | C | 시계열 모멘텀 (변동성 정규화) | SOLUSDT | 15m | 2.51 | 2.64 | +59.6% | 44% | 1x | [보기](C0378_tsmom_SOLUSDT_15m.md) |
| C380 | C | 켈트너 채널 | ZECUSDT | 15m | 1.98 | 1.94 | +17.2% | 10% | 1x | [보기](C0380_keltner_ZECUSDT_15m.md) |
| C402 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | ALL | 1h | 2.09 | 1.99 | +5.7% | 3% | 2x | [보기](C0402_zscore_mr_ALL_1h.md) |
| C404 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/BNBUSDT | 15m | 2.16 | 2.41 | +20.5% | 14% | 3x | [보기](C0404_pairs_DOGEUSDT-BNBUSDT_15m.md) |
| C409 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 4h | 2.14 | 2.10 | +48.0% | 28% | 1x | [보기](C0409_squeeze_SOLUSDT_4h.md) |
| C417 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | XRPUSDT | 4h | 1.95 | 2.33 | +27.8% | 21% | 2x | [보기](C0417_squeeze_XRPUSDT_4h.md) |
| C419 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | SOLUSDT | 15m | 2.26 | 2.14 | +19.1% | 8% | 1.5x | [보기](C0419_zscore_mr_SOLUSDT_15m.md) |
| C423 | C | 선형회귀 추세 유의성 | ZECUSDT | 15m | 2.33 | 2.20 | +123.7% | 41% | 0.5x | [보기](C0423_linreg_ZECUSDT_15m.md) |
| C426 | C | 시계열 모멘텀 (변동성 정규화) | BTCUSDT | 15m | 1.96 | 2.87 | +13.9% | 6% | 5x | [보기](C0426_tsmom_BTCUSDT_15m.md) |
| C429 | C | 켈트너 채널 | XRPUSDT | 15m | 1.94 | 2.20 | +13.9% | 10% | 2.5x | [보기](C0429_keltner_XRPUSDT_15m.md) |
| C436 | C | OBV 거래량 모멘텀 | XRPUSDT | 15m | 3.05 | 2.17 | +33.9% | 16% | 1x | [보기](C0436_obv_XRPUSDT_15m.md) |
| C437 | C | 파라볼릭 SAR | SOLUSDT | 1d | 2.12 | 2.53 | +77.6% | 48% | 0.5x | [보기](C0437_psar_SOLUSDT_1d.md) |
| C439 | C | 롤링 VWAP 이격 | ZECUSDT | 15m | 1.97 | 2.10 | +39.8% | 18% | 1.5x | [보기](C0439_vwap_dev_ZECUSDT_15m.md) |
| C443 | C | 아룬 추세 | SOLUSDT | 1h | 2.32 | 2.69 | +20.7% | 25% | 1x | [보기](C0443_aroon_SOLUSDT_1h.md) |
| C444 | C | MACD | ETHUSDT | 15m | 1.96 | 2.25 | +4.2% | 2% | 5x | [보기](C0444_macd_ETHUSDT_15m.md) |
| C446 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | ZECUSDT/DOGEUSDT | 30m | 2.21 | 2.55 | +108.3% | 39% | 0.5x | [보기](C0446_pairs_ZECUSDT-DOGEUSDT_30m.md) |
| C447 | C | 일목균형표 | SOLUSDT | 4h | 2.03 | 2.45 | +54.8% | 48% | 1x | [보기](C0447_ichimoku_SOLUSDT_4h.md) |
| C448 | C | 켈트너 채널 | LINKUSDT | 5m | 3.01 | 2.79 | +15.4% | 15% | 3.5x | [보기](C0448_keltner_LINKUSDT_5m.md) |
| C456 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | DOGEUSDT | 4h | 2.19 | 2.05 | +60.8% | 25% | 1x | [보기](C0456_squeeze_DOGEUSDT_4h.md) |
| C471 | C | ADX/DMI 추세 | SOLUSDT | 1h | 2.82 | 2.38 | +19.2% | 15% | 2x | [보기](C0471_adx_dmi_SOLUSDT_1h.md) |
| C478 | C | 하락추세 반등 매도 (상승추세 눌림 매수) | SOLUSDT | 1h | 2.00 | 2.26 | +26.9% | 23% | 1x | [보기](C0478_rally_fade_SOLUSDT_1h.md) |
| C481 | C | 일목균형표 | SOLUSDT | 4h | 2.37 | 2.03 | +39.5% | 33% | 1.5x | [보기](C0481_ichimoku_SOLUSDT_4h.md) |
| C482 | C | 테이커 주문흐름 불균형 | ZECUSDT | 4h | 2.15 | 2.61 | +125.3% | 60% | 0.5x | [보기](C0482_flow_ZECUSDT_4h.md) |
| C495 | C | 롱/숏 비율 포지셔닝 | DOGEUSDT | 4h | 2.06 | 2.45 | +55.0% | 38% | 1x | [보기](C0495_positioning_DOGEUSDT_4h.md) |
| C498 | C | MACD | XRPUSDT | 4h | 2.06 | 2.37 | +32.4% | 20% | 1.5x | [보기](C0498_macd_XRPUSDT_4h.md) |
| C502 | C | MACD | DOGEUSDT | 1h | 2.63 | 2.00 | +40.2% | 21% | 1x | [보기](C0502_macd_DOGEUSDT_1h.md) |
| C507 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | SOLUSDT | 15m | 2.47 | 2.69 | +4.7% | 2% | 5x | [보기](C0507_zscore_mr_SOLUSDT_15m.md) |
| C509 | C | 선형회귀 추세 유의성 | SOLUSDT | 1h | 2.07 | 2.06 | +53.9% | 42% | 0.5x | [보기](C0509_linreg_SOLUSDT_1h.md) |
| C512 | C | 롱/숏 비율 포지셔닝 | SOLUSDT | 30m | 2.25 | 3.20 | +16.2% | 9% | 4x | [보기](C0512_positioning_SOLUSDT_30m.md) |
| C513 | C | 아룬 추세 | DOGEUSDT | 15m | 2.09 | 2.06 | +88.4% | 53% | 0.5x | [보기](C0513_aroon_DOGEUSDT_15m.md) |
| C516 | C | 이동평균 교차 추세추종 | BTCUSDT | 1h | 2.41 | 2.18 | +7.6% | 6% | 5x | [보기](C0516_ma_cross_BTCUSDT_1h.md) |
| C517 | C | 횡단면 모멘텀/리버설 (10개 코인 순위) | ALL | 4h | 2.21 | 2.32 | +47.6% | 36% | 1.5x | [보기](C0517_xsmom_ALL_4h.md) |
| C521 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | DOGEUSDT | 15m | 2.09 | 2.00 | +11.2% | 3% | 5x | [보기](C0521_zscore_mr_DOGEUSDT_15m.md) |
| C523 | C | 하방 변동성 확대 (레버리지 효과) | SOLUSDT | 1h | 2.06 | 2.33 | +26.5% | 15% | 2x | [보기](C0523_vol_down_SOLUSDT_1h.md) |
| C527 | C | ADX/DMI 추세 | BTCUSDT | 30m | 1.97 | 2.09 | +7.7% | 7% | 4.5x | [보기](C0527_adx_dmi_BTCUSDT_30m.md) |
| C533 | C | 펀딩비 쏠림 | ETHUSDT | 1h | 2.18 | 2.08 | +23.3% | 10% | 2.5x | [보기](C0533_funding_ETHUSDT_1h.md) |
| C535 | C | 이동평균 교차 추세추종 | SOLUSDT | 1h | 2.57 | 2.55 | +23.3% | 41% | 2x | [보기](C0535_ma_cross_SOLUSDT_1h.md) |
| C536 | C | 하방 변동성 확대 (레버리지 효과) | ETHUSDT | 30m | 2.09 | 2.16 | +17.2% | 10% | 2x | [보기](C0536_vol_down_ETHUSDT_30m.md) |
| C537 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ZECUSDT | 1h | 2.16 | 1.99 | +42.8% | 38% | 1.5x | [보기](C0537_squeeze_ZECUSDT_1h.md) |
| C538 | C | 이동평균 교차 추세추종 | DOGEUSDT | 1h | 2.60 | 2.11 | +68.2% | 37% | 1x | [보기](C0538_ma_cross_DOGEUSDT_1h.md) |
| C541 | C | 하방 변동성 확대 (레버리지 효과) | BTCUSDT | 1h | 2.09 | 2.21 | +13.3% | 5% | 4.5x | [보기](C0541_vol_down_BTCUSDT_1h.md) |
| C542 | C | 하방 변동성 확대 (레버리지 효과) | DOGEUSDT | 1h | 2.41 | 2.42 | +20.1% | 16% | 2.5x | [보기](C0542_vol_down_DOGEUSDT_1h.md) |
| C544 | C | 하방 변동성 확대 (레버리지 효과) | ETHUSDT | 1h | 2.39 | 2.30 | +26.8% | 25% | 2.5x | [보기](C0544_vol_down_ETHUSDT_1h.md) |
| C550 | C | RSI 과매도/과매수 역추세 | SOLUSDT | 30m | 2.29 | 2.34 | +8.4% | 7% | 5x | [보기](C0550_rsi_mr_SOLUSDT_30m.md) |
| C552 | C | 펀딩비 쏠림 | ZECUSDT | 30m | 2.14 | 2.18 | +28.1% | 29% | 2x | [보기](C0552_funding_ZECUSDT_30m.md) |
| C553 | C | 하방 변동성 확대 (레버리지 효과) | ETHUSDT | 1h | 2.26 | 2.73 | +20.0% | 19% | 2.5x | [보기](C0553_vol_down_ETHUSDT_1h.md) |
| C554 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 4h | 1.92 | 2.76 | +79.2% | 40% | 1x | [보기](C0554_squeeze_SOLUSDT_4h.md) |
