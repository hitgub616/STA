from stock_trading_analyzer import StockTradingAnalyzer

def simple_test():
    """
    간단한 테스트 예시
    """
    # 분석기 초기화
    analyzer = StockTradingAnalyzer()
    
    # 예시 신호 데이터
    sample_signals = {
        "RSI": "OVERSOLD",
        "MACD": "BUY", 
        "ADX": "TRENDING",
        "BOLLINGER_BANDS": "REBOUND",
        "MA_CROSSOVER": "GOLDEN",
        "OBV": "ACCUMULATING",
        "HEAD_SHOULDERS": "NO_PATTERN",
        "FIBONACCI": "AT_RETRACEMENT",
        "ELLIOTT_WAVE": "WAVE_3",
        "BREAKOUT": "BREAKOUT"
    }
    
    # 분석 실행
    result = analyzer.analyze_signals(sample_signals)
    
    # 결과를 딕셔너리 형태로도 확인 가능
    print("\n=== 딕셔너리 형태 결과 ===")
    for indicator, interpretation in result['interpreted_signals'].items():
        print(f"{indicator}: {interpretation['signal']} - {interpretation['description']}")

if __name__ == "__main__":
    simple_test()
