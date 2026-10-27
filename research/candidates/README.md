# 페이퍼 트레이딩 후보 목록

엄격한 과최적화 검정 없이 검증·홀드아웃 구간 수익, 비용 스트레스, 파라미터 안정성만 통과한 후보입니다. 같은 아이디어의 변형은 더 좋은 것이 나오면 교체되고, 목록은 min(검증, 홀드아웃 샤프) 상위 최대 50개만 유지합니다 (밀려난 후보는 [archive](archive/)에 보관되며 번호로 계속 실행 가능). `python run_strategy.py paper --pick C번호` 로 모의매매할 수 있습니다.

| # | 등급 | 전략 | 대상 | 봉 | 검증 샤프 | 홀드아웃 샤프 | 거래/년 | 전체 연수익(1x) | MDD(1x) | 권장 레버리지 | 상세 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | B | 선형회귀 추세 유의성 | ALL | 30m | 2.40 | 2.30 | 392 | +35.4% | 16% | 1x | [보기](C0001_linreg_ALL_30m.md) |
| C23 | B | 슈퍼트렌드 | ALL | 4h | 2.03 | 2.11 | 241 | +35.4% | 18% | 0.5x | [보기](C0023_supertrend_ALL_4h.md) |
| C59 | B | 롤링 VWAP 이격 | XRPUSDT | 5m | 2.20 | 2.34 | 80 | +48.7% | 16% | 1x | [보기](C0059_vwap_dev_XRPUSDT_5m.md) |
| C427 | B | 거래량 급증 돌파 | ALL | 4h | 1.83 | 2.23 | 299 | +28.6% | 17% | 0.5x | [보기](C0427_vol_breakout_ALL_4h.md) |
| C438 | B | 아룬 추세 | ETHUSDT | 1h | 1.71 | 2.51 | 57 | +75.7% | 21% | 1x | [보기](C0438_aroon_ETHUSDT_1h.md) |
| C440 | B | 롤링 VWAP 이격 | ALL | 1h | 1.80 | 2.19 | 244 | +33.4% | 18% | 1x | [보기](C0440_vwap_dev_ALL_1h.md) |
| C441 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ETHUSDT | 30m | 1.78 | 1.60 | 71 | +65.3% | 17% | 1x | [보기](C0441_squeeze_ETHUSDT_30m.md) |
| C445 | B | 선형회귀 추세 유의성 | ETHUSDT | 1h | 1.56 | 1.78 | 54 | +39.4% | 18% | 1.5x | [보기](C0445_linreg_ETHUSDT_1h.md) |
| C464 | B | 시장 구조 (고점·저점 낮아짐) | ALL | 1h | 1.96 | 2.48 | 194 | +23.6% | 7% | 1x | [보기](C0464_structure_ALL_1h.md) |
| C496 | B | 롱/숏 비율 포지셔닝 | BTCUSDT | 30m | 1.77 | 1.52 | 76 | +51.5% | 21% | 1.5x | [보기](C0496_positioning_BTCUSDT_30m.md) |
| C522 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 4h | 1.76 | 2.12 | 228 | +11.5% | 8% | 2.5x | [보기](C0522_squeeze_ALL_4h.md) |
| C528 | B | Ornstein-Uhlenbeck 평균회귀 (z-score) | ALL | 1h | 2.31 | 1.82 | 157 | +9.5% | 4% | 1.5x | [보기](C0528_zscore_mr_ALL_1h.md) |
| C529 | B | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/BTCUSDT | 30m | 1.58 | 2.08 | 97 | +39.1% | 17% | 1.5x | [보기](C0529_pairs_DOGEUSDT-BTCUSDT_30m.md) |
| C531 | B | 파라볼릭 SAR | DOGEUSDT | 4h | 1.64 | 1.63 | 73 | +46.7% | 19% | 1.5x | [보기](C0531_psar_DOGEUSDT_4h.md) |
| C545 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | SOLUSDT | 30m | 1.54 | 1.60 | 76 | +37.1% | 15% | 2x | [보기](C0545_squeeze_SOLUSDT_30m.md) |
| C547 | B | 아룬 추세 | ALL | 4h | 1.71 | 2.04 | 236 | +41.6% | 15% | 0.5x | [보기](C0547_aroon_ALL_4h.md) |
| C548 | B | MACD | ALL | 1d | 1.65 | 1.95 | 210 | +38.3% | 23% | 0.5x | [보기](C0548_macd_ALL_1d.md) |
| C551 | B | 켈트너 채널 | SOLUSDT | 5m | 1.51 | 1.59 | 96 | +57.4% | 21% | 0.5x | [보기](C0551_keltner_SOLUSDT_5m.md) |
| C567 | B | 하락추세 반등 매도 (상승추세 눌림 매수) | ALL | 15m | 1.68 | 1.57 | 349 | +12.5% | 12% | 1x | [보기](C0567_rally_fade_ALL_15m.md) |
| C570 | B | 롤링 VWAP 이격 | DOGEUSDT | 5m | 1.82 | 1.64 | 76 | +72.0% | 14% | 0.5x | [보기](C0570_vwap_dev_DOGEUSDT_5m.md) |
| C572 | B | 이동평균 교차 추세추종 | ALL | 1h | 1.50 | 1.66 | 508 | +28.8% | 14% | 1.5x | [보기](C0572_ma_cross_ALL_1h.md) |
| C584 | B | 변동성 수축 후 돌파 (볼린저 스퀴즈) | XRPUSDT | 30m | 1.54 | 1.65 | 63 | +32.2% | 17% | 2x | [보기](C0584_squeeze_XRPUSDT_30m.md) |
| C607 | B | 켈트너 채널 | ETHUSDT | 30m | 1.84 | 1.65 | 104 | +33.3% | 13% | 2x | [보기](C0607_keltner_ETHUSDT_30m.md) |
| C27 | C | 테이커 주문흐름 불균형 | ALL | 4h | 1.99 | 1.96 | 365 | +30.1% | 34% | 0.5x | [보기](C0027_flow_ALL_4h.md) |
| C28 | C | OBV 거래량 모멘텀 | ALL | 4h | 2.28 | 2.85 | 248 | +16.2% | 23% | 1.5x | [보기](C0028_obv_ALL_4h.md) |
| C40 | C | 국면 전환 (추세/횡보 판별 후 전략 선택) | ALL | 4h | 2.47 | 2.47 | 200 | +17.8% | 16% | 0.5x | [보기](C0040_regime_ALL_4h.md) |
| C109 | C | 거래량 급증 돌파 | ETHUSDT | 15m | 2.34 | 2.46 | 70 | +93.7% | 32% | 0.5x | [보기](C0109_vol_breakout_ETHUSDT_15m.md) |
| C404 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/BNBUSDT | 15m | 2.16 | 2.41 | 135 | +20.5% | 14% | 3x | [보기](C0404_pairs_DOGEUSDT-BNBUSDT_15m.md) |
| C423 | C | 선형회귀 추세 유의성 | ZECUSDT | 15m | 2.33 | 2.20 | 59 | +123.7% | 41% | 0.5x | [보기](C0423_linreg_ZECUSDT_15m.md) |
| C446 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | ZECUSDT/DOGEUSDT | 30m | 2.21 | 2.55 | 64 | +108.3% | 39% | 0.5x | [보기](C0446_pairs_ZECUSDT-DOGEUSDT_30m.md) |
| C456 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | DOGEUSDT | 4h | 2.19 | 2.05 | 68 | +60.8% | 25% | 1x | [보기](C0456_squeeze_DOGEUSDT_4h.md) |
| C482 | C | 테이커 주문흐름 불균형 | ZECUSDT | 4h | 2.15 | 2.61 | 73 | +125.3% | 60% | 0.5x | [보기](C0482_flow_ZECUSDT_4h.md) |
| C513 | C | 아룬 추세 | DOGEUSDT | 15m | 2.09 | 2.06 | 70 | +88.4% | 53% | 0.5x | [보기](C0513_aroon_DOGEUSDT_15m.md) |
| C517 | C | 횡단면 모멘텀/리버설 (10개 코인 순위) | ALL | 4h | 2.21 | 2.32 | 516 | +47.6% | 36% | 1.5x | [보기](C0517_xsmom_ALL_4h.md) |
| C538 | C | 이동평균 교차 추세추종 | DOGEUSDT | 1h | 2.60 | 2.11 | 64 | +68.2% | 37% | 1x | [보기](C0538_ma_cross_DOGEUSDT_1h.md) |
| C559 | C | 거래량 급증 돌파 | ALL | 15m | 2.12 | 2.07 | 171 | +12.2% | 11% | 1.5x | [보기](C0559_vol_breakout_ALL_15m.md) |
| C560 | C | 선형회귀 추세 유의성 | DOGEUSDT | 5m | 1.84 | 2.17 | 171 | +125.0% | 45% | 0.5x | [보기](C0560_linreg_DOGEUSDT_5m.md) |
| C561 | C | 선형회귀 추세 유의성 | XRPUSDT | 30m | 1.59 | 1.97 | 111 | +51.8% | 29% | 1x | [보기](C0561_linreg_XRPUSDT_30m.md) |
| C562 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | ALL | 4h | 1.85 | 1.94 | 237 | +31.7% | 28% | 1.5x | [보기](C0562_squeeze_ALL_4h.md) |
| C563 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | LINKUSDT/ETHUSDT | 15m | 1.59 | 1.27 | 56 | +21.0% | 14% | 2.5x | [보기](C0563_pairs_LINKUSDT-ETHUSDT_15m.md) |
| C564 | C | 켈트너 채널 | ALL | 1h | 1.64 | 1.88 | 361 | +27.5% | 15% | 2x | [보기](C0564_keltner_ALL_1h.md) |
| C565 | C | 거래량 급증 돌파 | ETHUSDT | 30m | 1.49 | 1.63 | 73 | +35.4% | 24% | 1x | [보기](C0565_vol_breakout_ETHUSDT_30m.md) |
| C566 | C | 파라볼릭 SAR | ALL | 1d | 2.09 | 1.48 | 176 | +29.7% | 20% | 0.5x | [보기](C0566_psar_ALL_1d.md) |
| C568 | C | 하방 변동성 확대 (레버리지 효과) | ALL | 1h | 1.77 | 1.71 | 345 | +18.8% | 13% | 1x | [보기](C0568_vol_down_ALL_1h.md) |
| C569 | C | 이동평균 교차 추세추종 | ALL | 1h | 1.07 | 1.03 | 221 | +6.6% | 5% | 2x | [보기](C0569_ma_cross_ALL_1h.md) |
| C571 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | ETHUSDT/TRXUSDT | 15m | 1.97 | 1.23 | 158 | +39.7% | 29% | 1x | [보기](C0571_pairs_ETHUSDT-TRXUSDT_15m.md) |
| C573 | C | 펀딩비 쏠림 | ALL | 30m | 1.53 | 1.47 | 304 | +52.7% | 51% | 0.5x | [보기](C0573_funding_ALL_30m.md) |
| C574 | C | MACD | ALL | 4h | 1.87 | 1.54 | 284 | +35.3% | 24% | 1.5x | [보기](C0574_macd_ALL_4h.md) |
| C575 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | ZECUSDT/BTCUSDT | 15m | 1.93 | 1.23 | 65 | +30.2% | 15% | 1.5x | [보기](C0575_pairs_ZECUSDT-BTCUSDT_15m.md) |
| C576 | C | 캔들 패턴 | ALL | 4h | 1.39 | 1.61 | 234 | +13.0% | 10% | 1x | [보기](C0576_candle_ALL_4h.md) |
| C577 | C | 하이킨아시 연속봉 | ALL | 4h | 1.23 | 2.04 | 658 | +21.8% | 33% | 1.5x | [보기](C0577_heikin_ALL_4h.md) |
| C578 | C | 하락추세 반등 매도 (상승추세 눌림 매수) | ALL | 4h | 1.54 | 1.43 | 187 | +16.4% | 11% | 1x | [보기](C0578_rally_fade_ALL_4h.md) |
| C579 | C | 시계열 모멘텀 (변동성 정규화) | ZECUSDT | 5m | 1.39 | 1.76 | 57 | +62.2% | 52% | 0.5x | [보기](C0579_tsmom_ZECUSDT_5m.md) |
| C580 | C | OBV 거래량 모멘텀 | SOLUSDT | 15m | 1.67 | 1.33 | 114 | +55.8% | 32% | 1x | [보기](C0580_obv_SOLUSDT_15m.md) |
| C581 | C | ADX/DMI 추세 | ALL | 4h | 1.31 | 1.33 | 184 | +18.1% | 17% | 0.5x | [보기](C0581_adx_dmi_ALL_4h.md) |
| C582 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | BNBUSDT/ETHUSDT | 30m | 1.21 | 1.36 | 46 | +21.8% | 19% | 2x | [보기](C0582_pairs_BNBUSDT-ETHUSDT_30m.md) |
| C583 | C | 선형회귀 추세 유의성 | SOLUSDT | 30m | 1.84 | 1.59 | 65 | +63.4% | 37% | 1x | [보기](C0583_linreg_SOLUSDT_30m.md) |
| C585 | C | 롱/숏 비율 포지셔닝 | BTCUSDT | 1h | 1.02 | 1.05 | 65 | +26.2% | 19% | 1.5x | [보기](C0585_positioning_BTCUSDT_1h.md) |
| C586 | C | 하방 변동성 확대 (레버리지 효과) | SOLUSDT | 1h | 1.30 | 1.25 | 85 | +167.4% | 36% | 0.5x | [보기](C0586_vol_down_SOLUSDT_1h.md) |
| C587 | C | 롱/숏 비율 포지셔닝 | ALL | 1h | 1.88 | 1.77 | 681 | +44.7% | 19% | 1x | [보기](C0587_positioning_ALL_1h.md) |
| C588 | C | 하이킨아시 연속봉 | DOGEUSDT | 4h | 1.81 | 1.44 | 127 | +60.6% | 50% | 0.5x | [보기](C0588_heikin_DOGEUSDT_4h.md) |
| C589 | C | Ornstein-Uhlenbeck 평균회귀 (z-score) | ZECUSDT | 5m | 2.05 | 1.52 | 157 | +47.3% | 39% | 1x | [보기](C0589_zscore_mr_ZECUSDT_5m.md) |
| C590 | C | 일목균형표 | TRXUSDT | 1h | 1.21 | 1.25 | 64 | +52.4% | 60% | 0.5x | [보기](C0590_ichimoku_TRXUSDT_1h.md) |
| C591 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | XRPUSDT/SOLUSDT | 15m | 1.42 | 1.31 | 115 | +30.6% | 31% | 1.5x | [보기](C0591_pairs_XRPUSDT-SOLUSDT_15m.md) |
| C592 | C | OBV 거래량 모멘텀 | ZECUSDT | 15m | 1.23 | 1.75 | 59 | +39.7% | 32% | 1x | [보기](C0592_obv_ZECUSDT_15m.md) |
| C593 | C | 롱/숏 비율 포지셔닝 | BTCUSDT | 1h | 1.36 | 1.45 | 69 | +40.1% | 12% | 1.5x | [보기](C0593_positioning_BTCUSDT_1h.md) |
| C594 | C | MACD | XRPUSDT | 1h | 1.25 | 1.79 | 64 | +33.4% | 25% | 1x | [보기](C0594_macd_XRPUSDT_1h.md) |
| C595 | C | 변동성 수축 후 돌파 (볼린저 스퀴즈) | LINKUSDT | 30m | 1.08 | 1.08 | 73 | +33.6% | 17% | 1.5x | [보기](C0595_squeeze_LINKUSDT_30m.md) |
| C596 | C | 일목균형표 | ALL | 1h | 1.62 | 2.29 | 452 | +25.7% | 25% | 1x | [보기](C0596_ichimoku_ALL_1h.md) |
| C597 | C | 아룬 추세 | ALL | 30m | 1.47 | 1.47 | 419 | +28.2% | 27% | 1x | [보기](C0597_aroon_ALL_30m.md) |
| C598 | C | 일목균형표 | DOGEUSDT | 15m | 1.14 | 1.17 | 236 | +49.6% | 56% | 0.5x | [보기](C0598_ichimoku_DOGEUSDT_15m.md) |
| C599 | C | 횡단면 모멘텀/리버설 (10개 코인 순위) | ALL | 15m | 1.49 | 1.82 | 306 | +201.5% | 56% | 0.5x | [보기](C0599_xsmom_ALL_15m.md) |
| C600 | C | 하이킨아시 연속봉 | ALL | 1d | 1.70 | 1.72 | 355 | +41.9% | 38% | 0.5x | [보기](C0600_heikin_ALL_1d.md) |
| C601 | C | 롱/숏 비율 포지셔닝 | ALL | 30m | 1.98 | 2.18 | 246 | +27.0% | 12% | 1x | [보기](C0601_positioning_ALL_30m.md) |
| C602 | C | 하락추세 반등 매도 (상승추세 눌림 매수) | ZECUSDT | 15m | 2.98 | 1.66 | 69 | +27.7% | 15% | 1x | [보기](C0602_rally_fade_ZECUSDT_15m.md) |
| C603 | C | 슈퍼트렌드 | DOGEUSDT | 4h | 1.18 | 1.17 | 68 | +32.0% | 29% | 1x | [보기](C0603_supertrend_DOGEUSDT_4h.md) |
| C604 | C | 아룬 추세 | DOGEUSDT | 4h | 1.45 | 1.05 | 68 | +55.4% | 46% | 0.5x | [보기](C0604_aroon_DOGEUSDT_4h.md) |
| C605 | C | MACD | DOGEUSDT | 1h | 1.05 | 1.40 | 131 | +59.2% | 36% | 0.5x | [보기](C0605_macd_DOGEUSDT_1h.md) |
| C606 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | BTCUSDT/BNBUSDT | 4h | 1.77 | 1.70 | 54 | +39.0% | 44% | 1x | [보기](C0606_pairs_BTCUSDT-BNBUSDT_4h.md) |
| C608 | C | 켈트너 채널 | ALL | 30m | 1.34 | 1.22 | 229 | +13.0% | 10% | 0.5x | [보기](C0608_keltner_ALL_30m.md) |
| C609 | C | 페어 트레이딩 (공적분 스프레드 평균회귀) | DOGEUSDT/LINKUSDT | 1h | 1.26 | 1.21 | 58 | +18.7% | 14% | 2x | [보기](C0609_pairs_DOGEUSDT-LINKUSDT_1h.md) |
| C610 | C | 하방 변동성 확대 (레버리지 효과) | ETHUSDT | 30m | 1.42 | 1.20 | 65 | +63.3% | 39% | 0.5x | [보기](C0610_vol_down_ETHUSDT_30m.md) |
