from stock_trading_analyzer import StockTradingAnalyzer
import json

def main():
    """
    실제 사용 예시
    """
    # 분석기 초기화 (API 키 불필요)
    analyzer = StockTradingAnalyzer()
    
    # 다양한 시나리오 테스트
    scenarios = {
        "강세 시나리오": {
            "RSI": "NEUTRAL",
            "MACD": "BUY",
            "ADX": "TRENDING",
            "BOLLINGER_BANDS": "BREAKOUT",
            "MA_CROSSOVER": "GOLDEN",
            "OBV": "ACCUMULATING",
            "HEAD_SHOULDERS": "NO_PATTERN",
            "FIBONACCI": "ABOVE",
            "ELLIOTT_WAVE": "WAVE_3",
            "BREAKOUT": "BREAKOUT"
        },
        "약세 시나리오": {
            "RSI": "OVERBOUGHT",
            "MACD": "SELL",
            "ADX": "TRENDING",
            "BOLLINGER_BANDS": "NORMAL",
            "MA_CROSSOVER": "DEAD",
            "OBV": "DISTRIBUTING",
            "HEAD_SHOULDERS": "REVERSAL",
            "FIBONACCI": "BELOW",
            "ELLIOTT_WAVE": "CORRECTIVE",
            "BREAKOUT": "FAKEOUT"
        },
        "혼재 시나리오": {
            "RSI": "OVERSOLD",
            "MACD": "SELL",
            "ADX": "RANGE",
            "BOLLINGER_BANDS": "NORMAL",
            "MA_CROSSOVER": "NEUTRAL",
            "OBV": "NEUTRAL",
            "HEAD_SHOULDERS": "NO_PATTERN",
            "FIBONACCI": "AT_RETRACEMENT",
            "ELLIOTT_WAVE": "WAVE_4",
            "BREAKOUT": "INSIDE_RANGE"
        }
    }
    
    for scenario_name, signals in scenarios.items():
        print(f"\n{'='*60}")
        print(f"시나리오: {scenario_name}")
        print(f"{'='*60}")
        
        try:
            result = analyzer.analyze_signals(signals)
            print(f"총 {len(result['interpreted_signals'])}개 지표 분석 완료\n")
            
        except Exception as e:
            print(f"분석 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
