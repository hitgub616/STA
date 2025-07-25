import os
from flask import Flask, render_template, request, jsonify
from stock_data_fetcher import StockDataFetcher
from stock_trading_analyzer import StockTradingAnalyzer
from chatgpt_analyzer import ChatGPTAnalyzer
from datetime import datetime

app = Flask(__name__)
app.debug = False

# 환경변수에서 API 키 가져오기
CHATGPT_API_KEY = os.environ.get('CHATGPT_API_KEY')
if not CHATGPT_API_KEY:
    print("⚠️ CHATGPT_API_KEY 환경변수가 설정되지 않았습니다.")

# 분석기 초기화
stock_fetcher = StockDataFetcher()
trading_analyzer = StockTradingAnalyzer()
chatgpt_analyzer = ChatGPTAnalyzer(CHATGPT_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL').upper()
        period = data.get('period', '1y') # 'period'도 받아오도록 수정

        print(f"🔍 {symbol} 주식 분석 시작 (기간: {period})...")

        # 주식 데이터 가져오기
        stock_data = stock_fetcher.fetch_stock_data(symbol, period)
        if stock_data.empty:
            return jsonify({'error': f'{symbol} 주식 데이터를 가져올 수 없습니다.'}), 400

        # 신호 생성
        signal_result = stock_fetcher.generate_signals(stock_data)
        if any(signal_result['insufficient'].values()):
            # 데이터 부족에 대한 경고를 좀 더 유연하게 처리 (오류 대신)
            print(f"⚠️ {symbol} 분석에 일부 데이터가 부족합니다.")

        # 신호 분석
        analysis_result = trading_analyzer.analyze_signals(
            signal_result['signals'],
            signal_result['scores'],
            signal_result['insufficient']
        )

        # 주식 정보 생성
        stock_info = {
            "symbol": symbol,
            "period": period,
            "latest_price": float(stock_data['Close'].iloc[-1]),
            "latest_date": stock_data.index[-1].strftime('%Y-%m-%d')
        }

        # ChatGPT 전문가 요약 생성을 위한 데이터 준비
        stock_data_for_chatgpt = {
            'symbol': stock_info['symbol'],
            'current_price': stock_info['latest_price'],
            'analysis_date': stock_info['latest_date'],
            'interpreted_signals': analysis_result['interpreted_signals'],
            'total_score': analysis_result['total_score'],
            'recommendation': analysis_result['recommendation']
        }

        expert_summary = chatgpt_analyzer.generate_expert_summary(stock_data_for_chatgpt)

        # 최종 결과 반환
        result = {
            'symbol': symbol,
            'stock_info': stock_info, # stock_info 추가
            'signals': signal_result['signals'],
            'scores': signal_result['scores'],
            'total_score': analysis_result['total_score'],
            'recommendation': analysis_result['recommendation'],
            'interpreted_signals': analysis_result['interpreted_signals'],
            'expert_summary': expert_summary,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 분석 시간 추가
        }

        print(f"✅ {symbol} 분석 완료")
        return jsonify(result)

    except Exception as e:
        # 오류 발생 시 더 자세한 로그를 남기도록 수정
        import traceback
        print(f"❌ 분석 중 오류 발생: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'분석 중 오류 발생: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 