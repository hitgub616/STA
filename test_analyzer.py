import unittest
from stock_trading_analyzer import StockTradingAnalyzer

class TestStockTradingAnalyzer(unittest.TestCase):
    """
    StockTradingAnalyzer 클래스의 단위 테스트
    """
    
    def setUp(self):
        """
        테스트 설정
        """
        self.analyzer = StockTradingAnalyzer()  # API 키 제거
        self.sample_signals = {
            "RSI": "OVERSOLD",
            "MACD": "BUY",
            "ADX": "TRENDING"
        }
    
    def test_analyze_signals(self):
        """
        전체 분석 프로세스 테스트
        """
        # 분석 실행
        result = self.analyzer.analyze_signals(self.sample_signals)
        
        # 결과 구조 확인
        self.assertIn("signals", result)
        self.assertIn("interpreted_signals", result)
        self.assertEqual(result["signals"], self.sample_signals)
        
        # 해석된 신호들 확인
        for key in self.sample_signals.keys():
            self.assertIn(key, result["interpreted_signals"])
            self.assertIn("indicator_name", result["interpreted_signals"][key])
            self.assertIn("signal", result["interpreted_signals"][key])
            self.assertIn("description", result["interpreted_signals"][key])

if __name__ == '__main__':
    unittest.main()
