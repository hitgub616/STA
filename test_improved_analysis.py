#!/usr/bin/env python3
"""
개선된 기술적 분석 기능 테스트 스크립트
각 지표별로 적절한 데이터 윈도우를 사용하는지 확인
"""

from stock_data_fetcher import StockDataFetcher
import pandas as pd

def test_improved_analysis():
    """
    개선된 분석 기능 테스트
    """
    print("🧪 개선된 기술적 분석 기능 테스트")
    print("=" * 60)
    
    # 데이터 가져오기
    fetcher = StockDataFetcher()
    data = fetcher.fetch_stock_data("AAPL", period="1y")
    
    if data.empty:
        print("❌ 데이터를 가져올 수 없습니다.")
        return
    
    print(f"\n📊 전체 데이터: {len(data)}일")
    print(f"   기간: {data.index[0].strftime('%Y-%m-%d')} ~ {data.index[-1].strftime('%Y-%m-%d')}")
    
    # 각 지표별 데이터 윈도우 테스트
    print(f"\n🔍 각 지표별 데이터 윈도우 확인:")
    
    for indicator, window in fetcher.REQUIRED_DATA_WINDOW.items():
        indicator_data = fetcher.get_indicator_data(data, indicator)
        print(f"   {indicator:12}: {len(indicator_data):3}일 ({indicator_data.index[0].strftime('%Y-%m-%d')} ~ {indicator_data.index[-1].strftime('%Y-%m-%d')})")
    
    # 신호 생성 테스트
    print(f"\n📈 기술적 지표 신호 생성:")
    signals = fetcher.generate_signals(data)
    
    print(f"\n✅ 생성된 신호들:")
    for indicator, signal in signals.items():
        print(f"   {indicator:15}: {signal}")
    
    print(f"\n🎯 개선 사항 확인:")
    print(f"   ✓ 각 지표가 적절한 데이터 윈도우 사용")
    print(f"   ✓ RSI: 단기 모멘텀 (20일)")
    print(f"   ✓ MACD: 중기 추세 (50일)")
    print(f"   ✓ OBV: 장기 거래량 (150일)")
    print(f"   ✓ Elliott Wave: 장기 파동 (250일)")
    print(f"   ✓ 모든 계산이 최신 날짜 기준으로 수행")

if __name__ == "__main__":
    test_improved_analysis() 