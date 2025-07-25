from stock_trading_analyzer import StockTradingAnalyzer
from chatgpt_analyzer import ChatGPTAnalyzer
import os

def main():
    """
    메인 실행 함수
    """
    print("🚀 주식 기술적 분석 시스템 시작\n")
    
    # 분석기 초기화
    analyzer = StockTradingAnalyzer()
    
    # ChatGPT 분석기 초기화 (API 키는 환경변수에서 가져옴)
    chatgpt_analyzer = ChatGPTAnalyzer(os.environ.get('CHATGPT_API_KEY'))
    
    # 애플 주식 분석
    print("=" * 60)
    print("🍎 애플(AAPL) 주식 분석")
    print("=" * 60)
    
    result = analyzer.analyze_stock("AAPL", period="1y")  # 1년 데이터
    
    if "error" not in result:
        print("\n✅ 분석 완료!")
        
        # 간단한 요약
        stock_info = result["stock_info"]
        signals = result["signals"]
        
        print(f"\n📈 {stock_info['symbol']} 현재 상황:")
        print(f"   가격: ${stock_info['latest_price']:.2f}")
        print(f"   날짜: {stock_info['latest_date']}")
        
        # 주요 신호들 요약
        key_signals = ["RSI", "MACD", "MA_CROSSOVER", "BOLLINGER_BANDS", "ADX"]
        print(f"\n🔍 주요 기술적 지표 요약:")
        for signal_name in key_signals:
            if signal_name in signals:
                print(f"   {signal_name}: {signals[signal_name]}")
        
        # ChatGPT 전문가 분석 생성
        print("\n🤖 ChatGPT 전문가 분석 중...\n")
        
        # ChatGPT 분석을 위한 데이터 준비
        stock_data_for_chatgpt = {
            'symbol': stock_info['symbol'],
            'current_price': stock_info['latest_price'],
            'analysis_date': stock_info['latest_date'],
            'interpreted_signals': result['interpreted_signals'],
            'total_score': result['total_score'],
            'recommendation': result['recommendation']
        }
        
        expert_summary = chatgpt_analyzer.generate_expert_summary(stock_data_for_chatgpt)
        
        print(f"\n{expert_summary}")
    
    else:
        print(f"❌ 분석 실패: {result['error']}")


if __name__ == "__main__":
    main()
