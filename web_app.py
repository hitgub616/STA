from flask import Flask, render_template, request, jsonify
from stock_trading_analyzer import StockTradingAnalyzer
from chatgpt_analyzer import ChatGPTAnalyzer
import json
import os
from datetime import datetime

app = Flask(__name__)

# API 키 설정 (환경변수에서 가져오기)
CHATGPT_API_KEY = os.environ.get('CHATGPT_API_KEY')

if not CHATGPT_API_KEY:
    raise ValueError("CHATGPT_API_KEY 환경변수가 설정되지 않았습니다. Vercel 대시보드에서 환경변수를 설정해주세요.")

# 분석기 초기화
analyzer = StockTradingAnalyzer()
chatgpt_analyzer = ChatGPTAnalyzer(CHATGPT_API_KEY)

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """주식 분석 API 엔드포인트"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL').upper()
        period = data.get('period', '1y')
        
        # 주식 분석 실행
        result = analyzer.analyze_stock(symbol, period)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 400
        
        # ChatGPT 전문가 분석
        stock_info = result["stock_info"]
        signals = result["signals"]
        
        # ChatGPT 분석을 위한 데이터 준비
        stock_data_for_chatgpt = {
            'symbol': symbol,
            'current_price': stock_info['latest_price'],
            'analysis_date': stock_info['latest_date'],
            'interpreted_signals': result["interpreted_signals"],
            'total_score': result.get("total_score", 0),
            'recommendation': result.get("recommendation", "HOLD")
        }
        
        expert_summary = chatgpt_analyzer.generate_expert_summary(stock_data_for_chatgpt)
        
        # 결과 데이터 구성
        analysis_result = {
            "symbol": symbol,
            "stock_info": stock_info,
            "signals": signals,
            "scores": result.get("scores", {}),
            "total_score": result.get("total_score", 0),
            "recommendation": result.get("recommendation", "HOLD"),
            "interpreted_signals": result["interpreted_signals"],
            "expert_summary": expert_summary,
            "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({"error": f"분석 중 오류 발생: {str(e)}"}), 500

@app.route('/api/symbols')
def get_popular_symbols():
    """인기 주식 심볼 목록"""
    popular_symbols = [
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
        {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Automotive"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology"},
        {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Technology"},
        {"symbol": "NFLX", "name": "Netflix Inc.", "sector": "Communication Services"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial"},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare"}
    ]
    return jsonify(popular_symbols)

# Vercel 배포를 위한 app 객체 export
app.debug = False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 