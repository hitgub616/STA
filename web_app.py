import os
from flask import Flask, render_template, request, jsonify
from stock_data_fetcher import StockDataFetcher
from stock_trading_analyzer import StockTradingAnalyzer
from chatgpt_analyzer import ChatGPTAnalyzer

app = Flask(__name__)
app.debug = False

# 환경변수에서 API 키 가져오기
CHATGPT_API_KEY = os.environ.get('CHATGPT_API_KEY')
if not CHATGPT_API_KEY:
    print("⚠️ CHATGPT_API_KEY 환경변수가 설정되지 않았습니다.")

# 분석기 초기화
stock_fetcher = StockDataFetcher()
trading_analyzer = StockTradingAnalyzer()
chatgpt_analyzer = ChatGPTAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL').upper()
        
        print(f"🔍 {symbol} 주식 분석 시작...")
        
        # 주식 데이터 가져오기
        stock_data = stock_fetcher.fetch_stock_data(symbol)
        if stock_data.empty:
            return jsonify({'error': f'{symbol} 주식 데이터를 가져올 수 없습니다.'}), 400
        
        # 신호 생성
        signal_result = stock_fetcher.generate_signals(stock_data)
        if signal_result['insufficient']:
            return jsonify({'error': f'{symbol} 분석에 필요한 충분한 데이터가 없습니다.'}), 400
        
        # 신호 분석
        analysis_result = trading_analyzer.analyze_signals(
            signal_result['signals'], 
            signal_result['scores'], 
            signal_result['insufficient']
        )
        
        # ChatGPT 전문가 요약 생성
        stock_data_for_chatgpt = {
            'interpreted_signals': analysis_result['interpreted_signals'],
            'total_score': analysis_result['total_score'],
            'recommendation': analysis_result['recommendation']
        }
        
        expert_summary = chatgpt_analyzer.generate_expert_summary(stock_data_for_chatgpt)
        
        # 결과 반환
        result = {
            'symbol': symbol,
            'signals': signal_result['signals'],
            'scores': signal_result['scores'],
            'total_score': analysis_result['total_score'],
            'recommendation': analysis_result['recommendation'],
            'interpreted_signals': analysis_result['interpreted_signals'],
            'expert_summary': expert_summary
        }
        
        print(f"✅ {symbol} 분석 완료")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {str(e)}")
        return jsonify({'error': f'분석 중 오류 발생: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 