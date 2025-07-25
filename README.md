# 📈 주식 기술적 분석 시스템 (Stock Trading Analyzer)

AI 기반 전문가 분석과 웹 인터페이스를 제공하는 종합 주식 분석 시스템입니다.

## ✨ 주요 기능

- **7가지 기술적 지표 분석**: RSI, MACD, 이동평균선 교차, ADX, 브레이크아웃, ATR, VWAP
- **AI 전문가 분석**: ChatGPT GPT-4o 모델을 활용한 종합적 해석
- **웹 기반 UI**: 직관적이고 현대적인 사용자 인터페이스
- **실시간 데이터**: FMP API를 통한 안정적인 주식 데이터 제공
- **점수 기반 평가**: 각 지표별 점수와 종합 점수를 통한 객관적 평가

## 🛠 기술 스택

- **Backend**: Python 3.11, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data**: Financial Modeling Prep (FMP) API
- **AI**: OpenAI GPT-4o
- **Deployment**: Fly.io

## 📊 기술적 지표

| 지표 | 설명 | 데이터 기간 |
|------|------|-------------|
| RSI | 상대강도지수 - 과매수/과매도 판단 | 20일 |
| MACD | 이동평균수렴확산 - 추세 전환 신호 | 50일 |
| 이동평균선 교차 | 단기/장기 이동평균선 교차 신호 | 60일 |
| ADX | 평균방향지수 - 추세 강도 측정 | 20일 |
| 브레이크아웃 | 지지/저항선 돌파 신호 | 40일 |
| ATR | 평균진폭 - 변동성 측정 | 20일 |
| VWAP | 거래량가중평균가격 - 공정가격 측정 | 1일 |

## 🚀 로컬 실행

### 1. 저장소 클론
```bash
git clone https://github.com/hitgub616/STA.git
cd STA
```

### 2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
```bash
export CHATGPT_API_KEY="your_openai_api_key"
export FMP_API_KEY="your_fmp_api_key"
```

### 5. 애플리케이션 실행
```bash
python web_app.py
```

브라우저에서 `http://localhost:8080`으로 접속하세요.

## 🌐 Fly.io 배포

### 1. Fly.io CLI 설치
```bash
# macOS
brew install flyctl

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Linux
curl -L https://fly.io/install.sh | sh
```

### 2. Fly.io 로그인
```bash
fly auth login
```

### 3. 앱 생성 및 배포
```bash
fly launch
```

### 4. 환경변수 설정
```bash
fly secrets set CHATGPT_API_KEY="your_openai_api_key"
fly secrets set FMP_API_KEY="your_fmp_api_key"
```

### 5. 배포
```bash
fly deploy
```

## 🔧 환경변수

| 변수명 | 설명 | 필수 여부 |
|--------|------|-----------|
| `CHATGPT_API_KEY` | OpenAI API 키 | ✅ |
| `FMP_API_KEY` | Financial Modeling Prep API 키 | ✅ |

## 📝 API 키 발급 방법

### OpenAI API 키
1. [OpenAI 웹사이트](https://platform.openai.com/) 방문
2. 계정 생성 및 로그인
3. API Keys 섹션에서 새 키 생성

### FMP API 키
1. [Financial Modeling Prep](https://financialmodelingprep.com/) 방문
2. 무료 계정 가입
3. 대시보드에서 API 키 확인

## 🎯 사용법

1. 웹 인터페이스에서 주식 심볼 입력 (예: AAPL, GOOGL, TSLA)
2. "분석 시작" 버튼 클릭
3. 기술적 지표 분석 결과 확인
4. AI 전문가 종합평가 및 투자 전략 확인

## 📈 분석 결과 해석

### 종합 점수 기준
- **+8 이상**: 강력 매수
- **+3 ~ +7**: 매수
- **-2 ~ +2**: 관망
- **-7 ~ -3**: 매도
- **-8 이하**: 강력 매도

### 지표별 점수
- **+2**: 매우 강한 신호
- **+1**: 약한 신호
- **0**: 중립
- **-1**: 약한 반대 신호
- **-2**: 매우 강한 반대 신호

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## ⚠️ 면책 조항

이 시스템은 교육 및 정보 제공 목적으로 제작되었습니다. 실제 투자 결정에 사용하기 전에 전문가와 상담하시기 바랍니다. 투자 손실에 대한 책임은 투자자 본인에게 있습니다. 