import json
from typing import Dict, Any
from stock_data_fetcher import StockDataFetcher

class StockTradingAnalyzer:
    """
    10개 기술적 지표를 분석하여 거래 추천을 제공하는 클래스
    """
    
    def __init__(self):
        """
        기술적 지표 분석기 초기화
        """
        self.data_fetcher = StockDataFetcher()
        
        # 기술적 지표별 설명 매핑
        self.indicator_descriptions = {
            "RSI": {
                "name": "RSI (상대강도지수)",
                "type": "모멘텀 지표",
                "description": "주가가 과매수/과매도 상태인지 판단",
                "signals": {
                    "STRONG_OVERBOUGHT": "강한 과매수 (RSI ≥ 70)",
                    "WEAK_OVERBOUGHT": "약한 과매수 (RSI 60-70)",
                    "NEUTRAL": "중립 상태 (RSI 40-60)",
                    "WEAK_OVERSOLD": "약한 과매도 (RSI 30-40)",
                    "STRONG_OVERSOLD": "강한 과매도 (RSI < 30)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            },
            "MACD": {
                "name": "MACD",
                "type": "추세/모멘텀 지표",
                "description": "단기/장기 이동평균의 차이로 추세 방향 확인",
                "signals": {
                    "STRONG_BULLISH": "강한 상승 신호 (MACD > Signal 1%+)",
                    "WEAK_BULLISH": "약한 상승 신호 (MACD > Signal 0.2-1%)",
                    "NEUTRAL": "중립 상태 (MACD-Signal 차이 ±0.2%)",
                    "WEAK_BEARISH": "약한 하락 신호 (MACD < Signal 0.2-1%)",
                    "STRONG_BEARISH": "강한 하락 신호 (MACD < Signal 1%+)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            },
            "MA_CROSSOVER": {
                "name": "이동평균 크로스오버",
                "type": "추세 지표",
                "description": "단기/장기 이동평균 교차로 추세 전환 감지",
                "signals": {
                    "STRONG_GOLDEN": "강한 골든크로스 (단기MA > 장기MA 1%+)",
                    "WEAK_GOLDEN": "약한 골든크로스 (단기MA > 장기MA 0.2-1%)",
                    "NEUTRAL": "중립 상태 (MA 차이 ±0.2%)",
                    "WEAK_DEAD": "약한 데드크로스 (단기MA < 장기MA 0.2-1%)",
                    "STRONG_DEAD": "강한 데드크로스 (단기MA < 장기MA 1%+)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            },
            "ADX": {
                "name": "ADX (평균방향지수)",
                "type": "추세 강도 지표",
                "description": "현재 추세가 얼마나 강한지 측정",
                "signals": {
                    "STRONG_TREND": "강한 추세 (ADX ≥ 40)",
                    "WEAK_TREND": "약한 추세 (ADX 25-40)",
                    "NEUTRAL": "중립 상태 (ADX 20-25)",
                    "WEAK_RANGE": "약한 횡보 (ADX 15-20)",
                    "STRONG_RANGE": "강한 횡보 (ADX < 15)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            },
            "BREAKOUT": {
                "name": "돌파 신호",
                "type": "가격 행동 지표",
                "description": "주요 저항/지지선 돌파 여부 확인",
                "signals": {
                    "STRONG_BREAKOUT": "강한 상향 돌파 (저항선 2%+ 돌파)",
                    "WEAK_BREAKOUT": "약한 상향 돌파 (저항선 0.5-2% 돌파)",
                    "NEUTRAL": "범위 내 움직임 (중립)",
                    "WEAK_BREAKDOWN": "약한 하향 돌파 (지지선 0.5-2% 하향)",
                    "STRONG_BREAKDOWN": "강한 하향 돌파 (지지선 2%+ 하향)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            },
            "ATR": {
                "name": "ATR (평균진폭)",
                "type": "변동성 지표",
                "description": "주가의 변동성이 얼마나 큰지 측정",
                "signals": {
                    "STRONG_VOLATILITY": "강한 변동성 (ATR ≥ 2%)",
                    "WEAK_VOLATILITY": "약한 변동성 (ATR 1-2%)",
                    "NEUTRAL": "보통 변동성 (ATR 0.5-1%)",
                    "WEAK_STABILITY": "약한 안정성 (ATR 0.2-0.5%)",
                    "STRONG_STABILITY": "강한 안정성 (ATR < 0.2%)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            },
            "VWAP": {
                "name": "VWAP (거래량가중평균가)",
                "type": "가격/거래량 지표",
                "description": "거래량을 고려한 공정가치 대비 현재가 위치",
                "signals": {
                    "STRONG_UNDER": "강한 저평가 (VWAP 1%+ 아래)",
                    "WEAK_UNDER": "약한 저평가 (VWAP 0.2-1% 아래)",
                    "NEUTRAL": "공정가치 (VWAP ±0.2%)",
                    "WEAK_OVER": "약한 고평가 (VWAP 0.2-1% 위)",
                    "STRONG_OVER": "강한 고평가 (VWAP 1%+ 위)",
                    "INSUFFICIENT_DATA": "데이터 부족"
                }
            }
        }
    
    def analyze_stock(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """
        주식 심볼로부터 데이터를 가져와서 분석하는 메인 함수
        
        Args:
            symbol (str): 주식 심볼 (예: "AAPL")
            period (str): 데이터 기간
            
        Returns:
            Dict[str, Any]: 분석 결과
        """
        print(f"🔍 {symbol} 주식 분석 시작...")
        
        # 1. 주식 데이터 가져오기
        stock_data = self.data_fetcher.fetch_stock_data(symbol, period)
        
        if stock_data.empty:
            return {"error": f"{symbol} 주식 데이터를 가져올 수 없습니다."}
        
        # 2. 기술적 지표 신호 생성
        signal_result = self.data_fetcher.generate_signals(stock_data)
        if not signal_result or not signal_result.get("signals"):
            return {"error": "기술적 지표 신호를 생성할 수 없습니다."}

        signals = signal_result["signals"]
        scores = signal_result.get("scores", {})
        insufficient = signal_result.get("insufficient", {})
        
        # 3. 신호 해석
        result = self.analyze_signals(signals, scores, insufficient)
        
        # 4. 주식 정보 추가
        result["stock_info"] = {
            "symbol": symbol,
            "period": period,
            "data_points": len(stock_data),
            "latest_price": float(stock_data['Close'].iloc[-1]),
            "latest_date": stock_data.index[-1].strftime('%Y-%m-%d')
        }
        
        return result
    
    def analyze_signals(self, signals: Dict[str, str], scores: Dict[str, int], insufficient: Dict[str, bool]) -> Dict[str, Any]:
        """
        기술적 지표 신호들을 개별적으로 해석하여 출력하는 함수
        
        Args:
            signals (Dict[str, str]): 기술적 지표별 신호 딕셔너리
            
        Returns:
            Dict[str, Any]: 각 지표별 해석 결과
        """
        interpreted_signals = {}
        total_score = 0
        for sc in scores.values():
            total_score += sc
        
        print("=== 기술적 지표 분석 결과 ===\n")
        
        for indicator_key, signal in signals.items():
            if indicator_key in self.indicator_descriptions:
                indicator_info = self.indicator_descriptions[indicator_key]
                signal_description = indicator_info["signals"].get(signal, signal)
                
                interpretation = {
                    "indicator_name": indicator_info["name"],
                    "type": indicator_info["type"],
                    "signal": signal,
                    "description": signal_description
                }
                
                interpretation["score"] = scores.get(indicator_key)
                interpretation["insufficient_data"] = insufficient.get(indicator_key, False)
                interpreted_signals[indicator_key] = interpretation
                
                # 개별 지표 결과 출력
                print(f"📊 {indicator_info['name']} ({indicator_info['type']})")
                print(f"   신호: {signal}")
                print(f"   해석: {signal_description}")
                print()
            else:
                # 알 수 없는 지표인 경우
                interpreted_signals[indicator_key] = {
                    "indicator_name": indicator_key,
                    "type": "Unknown",
                    "signal": signal,
                    "description": "정의되지 않은 지표입니다."
                }
                print(f"❓ {indicator_key}")
                print(f"   신호: {signal}")
                print(f"   해석: 정의되지 않은 지표입니다.")
                print()
        
        # 종합 추천
        if total_score >= 8:
            overall = "STRONG_BUY"
        elif total_score >= 3:
            overall = "BUY"
        elif total_score <= -7:
            overall = "STRONG_SELL"
        elif total_score <= -2:
            overall = "SELL"
        else:
            overall = "HOLD"

        return {
            "signals": signals,
            "scores": scores,
            "total_score": total_score,
            "recommendation": overall,
            "interpreted_signals": interpreted_signals,
            "insufficient": insufficient
        }


# 사용 예시 함수
def analyze_apple_stock():
    """
    애플 주식 분석 예시
    """
    analyzer = StockTradingAnalyzer()
    
    # 애플 주식 분석
    result = analyzer.analyze_stock("AAPL", period="1y")
    
    if "error" in result:
        print(f"❌ 오류: {result['error']}")
        return
    
    # 결과 출력
    print("=== 주식 정보 ===")
    stock_info = result["stock_info"]
    print(f"심볼: {stock_info['symbol']}")
    print(f"최신 가격: ${stock_info['latest_price']:.2f}")
    print(f"최신 날짜: {stock_info['latest_date']}")
    print(f"데이터 포인트: {stock_info['data_points']}일")
    
    return result


if __name__ == "__main__":
    # 애플 주식 분석 실행
    analyze_apple_stock()
