# 주식 기술적 분석 시스템

AI 기반 주식 기술적 분석 및 투자 조언 시스템입니다.

## 🚀 주요 기능

- **7가지 기술적 지표 분석**: RSI, MACD, 이동평균 크로스오버, ADX, 돌파 신호, ATR, VWAP
- **AI 전문가 분석**: ChatGPT를 활용한 종합적 투자 조언
- **사용자 친화적 UI**: 일반 투자자도 쉽게 이해할 수 있는 인터페이스
- **실시간 데이터**: Yahoo Finance API를 통한 실시간 주식 데이터

## 🛠️ 기술 스택

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **AI**: OpenAI GPT-4o
- **Data**: yfinance, pandas, numpy
- **Deployment**: Vercel

## 📦 설치 및 실행

### 로컬 개발 환경

1. **저장소 클론**
```bash
git clone <repository-url>
cd stock-trading-analyzer
```

2. **가상환경 생성 및 활성화**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정**
```bash
export CHATGPT_API_KEY="your-openai-api-key"
```

5. **애플리케이션 실행**
```bash
python web_app.py
```

6. **브라우저에서 접속**
```
http://localhost:8080
```

### Vercel 배포 (추천)

1. **Vercel CLI 설치**
```bash
npm i -g vercel
```

2. **Vercel 로그인**
```bash
vercel login
```

3. **프로젝트 배포**
```bash
vercel
```

4. **환경변수 설정**
   - Vercel 대시보드에서 "Settings" → "Environment Variables"
   - `CHATGPT_API_KEY` 환경변수 추가

5. **배포 완료**
   - 자동으로 배포가 완료되면 제공되는 URL로 접속 가능

### GitHub 연동 배포

1. **GitHub 저장소에 코드 푸시**
```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

2. **Vercel 웹사이트에서 배포**
   - [vercel.com](https://vercel.com) 접속
   - "New Project" 클릭
   - GitHub 저장소 연결
   - 환경변수 설정 후 배포

## 📊 기술적 지표

| 지표 | 설명 | 윈도우 |
|------|------|--------|
| RSI | 상대강도지수 - 과매수/과매도 판단 | 20일 |
| MACD | 이동평균 수렴확산 - 추세 방향 확인 | 50일 |
| 이동평균 크로스오버 | 단기/장기 MA 교차 - 추세 전환 감지 | 60일 |
| ADX | 평균방향지수 - 추세 강도 측정 | 20일 |
| 돌파 신호 | 저항/지지선 돌파 여부 확인 | 40일 |
| ATR | 평균진폭 - 변동성 측정 | 20일 |
| VWAP | 거래량가중평균가 - 공정가치 대비 위치 | 1일 |

## 🎯 분석 결과

- **5단계 점수 체계**: -2 ~ +2 (강한 매도 ~ 강한 매수)
- **종합 추천**: STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL
- **AI 전문가 분석**: 일반 투자자를 위한 친근한 설명

## 🔧 환경변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `CHATGPT_API_KEY` | OpenAI API 키 | ✅ |

## 📝 라이선스

MIT License

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 