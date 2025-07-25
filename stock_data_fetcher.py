import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any
import logging
import requests

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataFetcher:
    """
    주식 데이터를 가져오고 기본적인 기술적 지표를 계산하는 클래스
    """
    
    # 각 지표별 필요한 데이터 윈도우 정의
    REQUIRED_DATA_WINDOW = {
        "RSI": 20,               # Short-term momentum
        "MACD": 50,              # Medium trend (12/26 EMA)
        "MA_CROSSOVER": 60,      # For 20/60 MA crossover
        "ADX": 20,               # Trend strength over recent period
        "BREAKOUT": 40,          # Short-term price consolidation breakout
        "ATR": 20,               # Average True Range for volatility
        "VWAP": 1                # Volume Weighted Average Price (daily)
    }
    
    def __init__(self):
        """
        클라우드 환경에서 yfinance 차단을 우회하기 위해 세션을 초기화합니다.
        """
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    def fetch_stock_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        주식 데이터를 가져오는 함수
        
        Args:
            symbol (str): 주식 심볼
            period (str): 데이터 기간
            
        Returns:
            pd.DataFrame: 주식 데이터
        """
        try:
            # 최대 필요한 윈도우 + 50일 버퍼로 충분한 데이터 확보
            max_window = max(self.REQUIRED_DATA_WINDOW.values()) if self.REQUIRED_DATA_WINDOW else 250
            
            # period를 required_days에 맞게 조정
            if max_window + 50 > 250:
                period = "2y"
            elif max_window + 50 > 125:
                period = "1y"
            elif max_window + 50 > 60:
                period = "6mo"
            else:
                period = "3mo"
            
            print(f"📊 {symbol} 데이터 요청: {period} (최소 {max_window + 50}일 필요)")
            
            # yfinance 호출 시, 생성자에서 만든 세션을 사용합니다.
            stock = yf.Ticker(symbol, session=self.session)
            data = stock.history(period=f"{max_window + 50}d", interval=interval)
            
            if len(data) < max_window + 50:
                print(f"⚠️  경고: {symbol} 데이터가 부족합니다. 요청: {max_window + 50}일, 실제: {len(data)}일")
                # 더 긴 기간으로 재시도
                if period != "2y":
                    print(f"🔄 더 긴 기간으로 재시도 중...")
                    data = stock.history(period="2y")
                    if len(data) < max_window + 50:
                        print(f"❌ {symbol} 데이터가 여전히 부족합니다. 일부 지표가 제한될 수 있습니다.")
            
            print(f"✅ {symbol} 주식 데이터 가져오기 완료 ({len(data)}일치 데이터)")
            print(f"   기간: {data.index[0].strftime('%Y-%m-%d')} ~ {data.index[-1].strftime('%Y-%m-%d')}")
            print(f"   최신 가격: ${data['Close'].iloc[-1]:.2f}")
            
            return data
            
        except Exception as e:
            print(f"❌ {symbol} 데이터 가져오기 실패: {str(e)}")
            return pd.DataFrame()
    
    def get_indicator_data(self, data: pd.DataFrame, indicator: str) -> pd.DataFrame:
        """
        특정 지표에 필요한 데이터 윈도우를 반환
        
        Args:
            data (pd.DataFrame): 전체 주식 데이터
            indicator (str): 지표 이름
            
        Returns:
            pd.DataFrame: 지표에 필요한 데이터 윈도우
        """
        window = self.REQUIRED_DATA_WINDOW.get(indicator, 50)  # 기본값 50일
        required_days = min(window, len(data))
        sliced_data = data.tail(required_days)
        
        print(f"   {indicator} 계산: 최근 {required_days}일 데이터 사용 ({sliced_data.index[0].strftime('%Y-%m-%d')} ~ {sliced_data.index[-1].strftime('%Y-%m-%d')})")
        
        return sliced_data
    
    def calculate_moving_averages(self, data: pd.DataFrame, short_window: int = 20, long_window: int = 60) -> Tuple[pd.Series, pd.Series]:
        """
        단기 및 장기 이동평균 계산
        
        Args:
            data (pd.DataFrame): 주식 데이터
            short_window (int): 단기 이동평균 기간
            long_window (int): 장기 이동평균 기간
            
        Returns:
            Tuple[pd.Series, pd.Series]: (단기 이동평균, 장기 이동평균)
        """
        short_ma = data['Close'].rolling(window=short_window).mean()
        long_ma = data['Close'].rolling(window=long_window).mean()
        return short_ma, long_ma
    
    def calculate_rsi(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        RSI (Relative Strength Index) 계산
        
        Args:
            data (pd.DataFrame): 주식 데이터
            window (int): RSI 계산 기간
            
        Returns:
            pd.Series: RSI 값
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD 계산
        
        Args:
            data (pd.DataFrame): 주식 데이터
            fast (int): 빠른 EMA 기간
            slow (int): 느린 EMA 기간
            signal (int): 시그널 라인 기간
            
        Returns:
            Tuple[pd.Series, pd.Series, pd.Series]: (MACD 라인, 시그널 라인, 히스토그램)
        """
        ema_fast = data['Close'].ewm(span=fast).mean()
        ema_slow = data['Close'].ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, window: int = 20, num_std: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        볼린저 밴드 계산
        
        Args:
            data (pd.DataFrame): 주식 데이터
            window (int): 이동평균 기간
            num_std (float): 표준편차 배수
            
        Returns:
            Tuple[pd.Series, pd.Series, pd.Series]: (상단 밴드, 중간 밴드, 하단 밴드)
        """
        middle_band = data['Close'].rolling(window=window).mean()
        std = data['Close'].rolling(window=window).std()
        upper_band = middle_band + (std * num_std)
        lower_band = middle_band - (std * num_std)
        return upper_band, middle_band, lower_band
    
    def calculate_adx(self, data: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        ADX (Average Directional Index) 계산 (간단한 버전)
        
        Args:
            data (pd.DataFrame): 주식 데이터
            window (int): ADX 계산 기간
            
        Returns:
            pd.Series: ADX 값
        """
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        # True Range 계산
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # ATR 계산
        atr = tr.rolling(window=window).mean()
        
        # 간단한 ADX 근사치 (실제 ADX는 더 복잡함)
        price_change = abs(close.diff())
        adx_approx = (price_change.rolling(window=window).mean() / atr) * 100
        
        return adx_approx.fillna(0)
    
    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Average True Range (ATR) 계산
        """
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        # True Range 계산
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    def calculate_vwap(self, data: pd.DataFrame) -> pd.Series:
        """
        Volume Weighted Average Price (VWAP) 계산
        """
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        vwap = (typical_price * data['Volume']).cumsum() / data['Volume'].cumsum()
        return vwap
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        주식 데이터로부터 기술적 지표 신호를 생성 (각 지표별 적절한 데이터 윈도우 사용)
        
        Args:
            data (pd.DataFrame): 주식 데이터
            
        Returns:
            Dict[str, Any]: 기술적 지표별 신호, 점수, 부족한 데이터 정보
        """
        if len(data) < 50:
            print("❌ 신호 생성을 위한 충분한 데이터가 없습니다 (최소 50일 필요)")
            return {}
        
        signals = {}
        scores = {}
        insufficient = {}
        latest_close = data['Close'].iloc[-1]
        
        print(f"\n📊 기술적 지표 계산 중...")
        
        # 1. RSI 신호 (단기 모멘텀 - 최근 20일)
        rsi_data = self.get_indicator_data(data, "RSI")
        if len(rsi_data) < self.REQUIRED_DATA_WINDOW["RSI"]:
            insufficient["RSI"] = True
            signals["RSI"] = "INSUFFICIENT_DATA"
            scores["RSI"] = 0
            print(f"   RSI: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['RSI']}일, 실제: {len(rsi_data)}일)")
        else:
            rsi = self.calculate_rsi(rsi_data)
            latest_rsi = rsi.iloc[-1]
            
            # 5단계 점수 체계 (-2 ~ +2)
            if latest_rsi >= 70:
                signals["RSI"] = "STRONG_OVERBOUGHT"
                scores["RSI"] = -2
            elif 60 <= latest_rsi < 70:
                signals["RSI"] = "WEAK_OVERBOUGHT"
                scores["RSI"] = -1
            elif 40 <= latest_rsi < 60:
                signals["RSI"] = "NEUTRAL"
                scores["RSI"] = 0
            elif 30 <= latest_rsi < 40:
                signals["RSI"] = "WEAK_OVERSOLD"
                scores["RSI"] = 1
            else:
                signals["RSI"] = "STRONG_OVERSOLD"
                scores["RSI"] = 2
            
            print(f"   RSI raw={latest_rsi:.2f} → {signals['RSI']}, score={scores['RSI']} using last {len(rsi_data)} days ({rsi_data.index[0].strftime('%Y-%m-%d')} ~ {rsi_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 2. MACD 신호 (중기 추세 - 최근 50일)
        macd_data = self.get_indicator_data(data, "MACD")
        if len(macd_data) < self.REQUIRED_DATA_WINDOW["MACD"]:
            insufficient["MACD"] = True
            signals["MACD"] = "INSUFFICIENT_DATA"
            scores["MACD"] = 0
            print(f"   MACD: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['MACD']}일, 실제: {len(macd_data)}일)")
        else:
            macd_line, signal_line, histogram = self.calculate_macd(macd_data)
            if pd.notna(macd_line.iloc[-1]) and pd.notna(signal_line.iloc[-1]):
                macd_diff_pct = (macd_line.iloc[-1] - signal_line.iloc[-1]) / latest_close * 100
                
                # 5단계 점수 체계
                if macd_diff_pct >= 1.0:
                    signals["MACD"] = "STRONG_BULLISH"
                    scores["MACD"] = 2
                elif 0.2 <= macd_diff_pct < 1.0:
                    signals["MACD"] = "WEAK_BULLISH"
                    scores["MACD"] = 1
                elif -0.2 < macd_diff_pct < 0.2:
                    signals["MACD"] = "NEUTRAL"
                    scores["MACD"] = 0
                elif -1.0 < macd_diff_pct <= -0.2:
                    signals["MACD"] = "WEAK_BEARISH"
                    scores["MACD"] = -1
                else:
                    signals["MACD"] = "STRONG_BEARISH"
                    scores["MACD"] = -2
            else:
                signals["MACD"] = "NEUTRAL"
                scores["MACD"] = 0
                macd_diff_pct = 0
            
            print(f"   MACD raw={macd_diff_pct:.3f}% → {signals['MACD']}, score={scores['MACD']} using last {len(macd_data)} days ({macd_data.index[0].strftime('%Y-%m-%d')} ~ {macd_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 3. 이동평균 크로스오버 (중기 추세 - 최근 60일)
        ma_data = self.get_indicator_data(data, "MA_CROSSOVER")
        if len(ma_data) < self.REQUIRED_DATA_WINDOW["MA_CROSSOVER"]:
            insufficient["MA_CROSSOVER"] = True
            signals["MA_CROSSOVER"] = "INSUFFICIENT_DATA"
            scores["MA_CROSSOVER"] = 0
            print(f"   MA_CROSSOVER: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['MA_CROSSOVER']}일, 실제: {len(ma_data)}일)")
        else:
            short_ma, long_ma = self.calculate_moving_averages(ma_data)
            if pd.notna(short_ma.iloc[-1]) and pd.notna(long_ma.iloc[-1]):
                ma_diff_pct = (short_ma.iloc[-1] - long_ma.iloc[-1]) / long_ma.iloc[-1] * 100
                
                # 5단계 점수 체계
                if ma_diff_pct >= 1.0:
                    signals["MA_CROSSOVER"] = "STRONG_GOLDEN"
                    scores["MA_CROSSOVER"] = 2
                elif 0.2 <= ma_diff_pct < 1.0:
                    signals["MA_CROSSOVER"] = "WEAK_GOLDEN"
                    scores["MA_CROSSOVER"] = 1
                elif -0.2 < ma_diff_pct < 0.2:
                    signals["MA_CROSSOVER"] = "NEUTRAL"
                    scores["MA_CROSSOVER"] = 0
                elif -1.0 < ma_diff_pct <= -0.2:
                    signals["MA_CROSSOVER"] = "WEAK_DEAD"
                    scores["MA_CROSSOVER"] = -1
                else:
                    signals["MA_CROSSOVER"] = "STRONG_DEAD"
                    scores["MA_CROSSOVER"] = -2
            else:
                signals["MA_CROSSOVER"] = "NEUTRAL"
                scores["MA_CROSSOVER"] = 0
                ma_diff_pct = 0
            
            print(f"   MA_CROSSOVER raw={ma_diff_pct:.2f}% → {signals['MA_CROSSOVER']}, score={scores['MA_CROSSOVER']} using last {len(ma_data)} days ({ma_data.index[0].strftime('%Y-%m-%d')} ~ {ma_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 4. ADX (단기 추세 강도 - 최근 20일)
        adx_data = self.get_indicator_data(data, "ADX")
        if len(adx_data) < self.REQUIRED_DATA_WINDOW["ADX"]:
            insufficient["ADX"] = True
            signals["ADX"] = "INSUFFICIENT_DATA"
            scores["ADX"] = 0
            print(f"   ADX: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['ADX']}일, 실제: {len(adx_data)}일)")
        else:
            adx = self.calculate_adx(adx_data)
            latest_adx = adx.iloc[-1]
            
            # 5단계 점수 체계
            if latest_adx >= 40:
                signals["ADX"] = "STRONG_TREND"
                scores["ADX"] = 2
            elif 25 <= latest_adx < 40:
                signals["ADX"] = "WEAK_TREND"
                scores["ADX"] = 1
            elif 20 <= latest_adx < 25:
                signals["ADX"] = "NEUTRAL"
                scores["ADX"] = 0
            elif 15 <= latest_adx < 20:
                signals["ADX"] = "WEAK_RANGE"
                scores["ADX"] = -1
            else:
                signals["ADX"] = "STRONG_RANGE"
                scores["ADX"] = -2
            
            print(f"   ADX raw={latest_adx:.2f} → {signals['ADX']}, score={scores['ADX']} using last {len(adx_data)} days ({adx_data.index[0].strftime('%Y-%m-%d')} ~ {adx_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 5. Breakout Signal (단기 돌파 - 최근 40일)
        breakout_data = self.get_indicator_data(data, "BREAKOUT")
        if len(breakout_data) < self.REQUIRED_DATA_WINDOW["BREAKOUT"]:
            insufficient["BREAKOUT"] = True
            signals["BREAKOUT"] = "INSUFFICIENT_DATA"
            scores["BREAKOUT"] = 0
            print(f"   BREAKOUT: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['BREAKOUT']}일, 실제: {len(breakout_data)}일)")
        else:
            recent_high = breakout_data['High'].iloc[-20:].max()
            recent_low = breakout_data['Low'].iloc[-20:].min()
            current_price = breakout_data['Close'].iloc[-1]
            
            # 돌파/하향 돌파 계산
            breakout_pct = (current_price - recent_high) / recent_high * 100
            breakdown_pct = (recent_low - current_price) / recent_low * 100
            
            # 5단계 점수 체계
            if breakout_pct >= 2.0:
                signals["BREAKOUT"] = "STRONG_BREAKOUT"
                scores["BREAKOUT"] = 2
            elif 0.5 <= breakout_pct < 2.0:
                signals["BREAKOUT"] = "WEAK_BREAKOUT"
                scores["BREAKOUT"] = 1
            elif -0.5 < breakout_pct < 0.5 and breakdown_pct < 0.5:
                signals["BREAKOUT"] = "NEUTRAL"
                scores["BREAKOUT"] = 0
            elif 0.5 <= breakdown_pct < 2.0:
                signals["BREAKOUT"] = "WEAK_BREAKDOWN"
                scores["BREAKOUT"] = -1
            else:
                signals["BREAKOUT"] = "STRONG_BREAKDOWN"
                scores["BREAKOUT"] = -2
            
            print(f"   BREAKOUT raw={breakout_pct:.2f}% → {signals['BREAKOUT']}, score={scores['BREAKOUT']} using last {len(breakout_data)} days ({breakout_data.index[0].strftime('%Y-%m-%d')} ~ {breakout_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 6. ATR (변동성 - 최근 20일)
        atr_data = self.get_indicator_data(data, "ATR")
        if len(atr_data) < self.REQUIRED_DATA_WINDOW["ATR"]:
            insufficient["ATR"] = True
            signals["ATR"] = "INSUFFICIENT_DATA"
            scores["ATR"] = 0
            print(f"   ATR: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['ATR']}일, 실제: {len(atr_data)}일)")
        else:
            atr = self.calculate_atr(atr_data)
            latest_atr = atr.iloc[-1]
            atr_pct = latest_atr / latest_close * 100
            
            # 5단계 점수 체계
            if atr_pct >= 2.0:
                signals["ATR"] = "STRONG_VOLATILITY"
                scores["ATR"] = 2
            elif 1.0 <= atr_pct < 2.0:
                signals["ATR"] = "WEAK_VOLATILITY"
                scores["ATR"] = 1
            elif 0.5 <= atr_pct < 1.0:
                signals["ATR"] = "NEUTRAL"
                scores["ATR"] = 0
            elif 0.2 <= atr_pct < 0.5:
                signals["ATR"] = "WEAK_STABILITY"
                scores["ATR"] = -1
            else:
                signals["ATR"] = "STRONG_STABILITY"
                scores["ATR"] = -2
            
            print(f"   ATR raw={atr_pct:.2f}% → {signals['ATR']}, score={scores['ATR']} using last {len(atr_data)} days ({atr_data.index[0].strftime('%Y-%m-%d')} ~ {atr_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 7. VWAP (거래량 가중 평균가 - 최근 1일)
        vwap_data = self.get_indicator_data(data, "VWAP")
        if len(vwap_data) < self.REQUIRED_DATA_WINDOW["VWAP"]:
            insufficient["VWAP"] = True
            signals["VWAP"] = "INSUFFICIENT_DATA"
            scores["VWAP"] = 0
            print(f"   VWAP: INSUFFICIENT_DATA (필요: {self.REQUIRED_DATA_WINDOW['VWAP']}일, 실제: {len(vwap_data)}일)")
        else:
            vwap = self.calculate_vwap(vwap_data)
            latest_vwap = vwap.iloc[-1]
            vwap_diff_pct = (latest_close - latest_vwap) / latest_vwap * 100
            
            # 5단계 점수 체계
            if vwap_diff_pct <= -1.0:
                signals["VWAP"] = "STRONG_UNDER"
                scores["VWAP"] = 2
            elif -1.0 < vwap_diff_pct <= -0.2:
                signals["VWAP"] = "WEAK_UNDER"
                scores["VWAP"] = 1
            elif -0.2 < vwap_diff_pct < 0.2:
                signals["VWAP"] = "NEUTRAL"
                scores["VWAP"] = 0
            elif 0.2 <= vwap_diff_pct < 1.0:
                signals["VWAP"] = "WEAK_OVER"
                scores["VWAP"] = -1
            else:
                signals["VWAP"] = "STRONG_OVER"
                scores["VWAP"] = -2
            
            print(f"   VWAP raw={vwap_diff_pct:.2f}% → {signals['VWAP']}, score={scores['VWAP']} using last {len(vwap_data)} days ({vwap_data.index[0].strftime('%Y-%m-%d')} ~ {vwap_data.index[-1].strftime('%Y-%m-%d')})")
        
        # 부족한 데이터 경고
        if insufficient:
            print(f"\n⚠️  부족한 데이터 경고:")
            for indicator, is_insufficient in insufficient.items():
                if is_insufficient:
                    print(f"   {indicator}: 필요한 {self.REQUIRED_DATA_WINDOW.get(indicator, 'N/A')}일 데이터가 부족합니다.")
        
        print(f"✅ 총 {len(signals)}개 지표 신호 생성 완료\n")
        
        return {"signals": signals, "scores": scores, "insufficient": insufficient}


def test_apple_stock():
    """
    애플 주식으로 테스트
    """
    print("🍎 애플(AAPL) 주식 데이터 분석 시작...")
    
    # 데이터 가져오기
    fetcher = StockDataFetcher()
    apple_data = fetcher.fetch_stock_data("AAPL", period="6mo")  # 6개월 데이터
    
    if apple_data.empty:
        print("❌ 애플 주식 데이터를 가져올 수 없습니다.")
        return None
    
    # 기술적 지표 신호 생성
    signals = fetcher.generate_signals(apple_data)
    
    return signals, apple_data


if __name__ == "__main__":
    # 애플 주식 테스트
    result = test_apple_stock()
    if result:
        signals, data = result
        print("생성된 신호:", signals)
