from stock_trading_analyzer import StockTradingAnalyzer

def test_multiple_stocks():
    """
    여러 주식으로 테스트
    """
    analyzer = StockTradingAnalyzer()
    
    # 테스트할 주식들
    test_stocks = ["AAPL", "GOOGL", "MSFT", "TSLA"]
    
    for stock in test_stocks:
        print(f"\n{'='*60}")
        print(f"📊 {stock} 주식 분석")
        print(f"{'='*60}")
        
        try:
            result = analyzer.analyze_stock(stock, period="3mo")
            
            if "error" not in result:
                stock_info = result["stock_info"]
                print(f"✅ {stock} 분석 완료 - 현재가: ${stock_info['latest_price']:.2f}")
            else:
                print(f"❌ {stock} 분석 실패: {result['error']}")
                
        except Exception as e:
            print(f"❌ {stock} 분석 중 오류: {e}")


if __name__ == "__main__":
    test_multiple_stocks()
