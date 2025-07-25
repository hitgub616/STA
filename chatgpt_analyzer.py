import openai
from typing import Dict, Any
import json

class ChatGPTAnalyzer:
    """
    ChatGPT API를 사용하여 주식 기술적 분석 결과를 전문가적으로 요약하는 클래스
    """
    
    def __init__(self, api_key: str):
        """
        ChatGPT 분석기 초기화
        
        Args:
            api_key (str): OpenAI API 키
        """
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate_expert_summary(self, stock_data: Dict[str, Any]) -> str:
        """
        주식 데이터를 바탕으로 ChatGPT 전문가 분석 생성
        
        Args:
            stock_data (Dict): 주식 분석 데이터
            
        Returns:
            str: 전문가 분석 결과
        """
        try:
            prompt = self._create_analysis_prompt(stock_data)
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 20년 경력의 주식 투자 전문가입니다. 일반 투자자들이 쉽게 이해할 수 있도록 친근하고 정성적으로 설명해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"ChatGPT 분석 중 오류 발생: {str(e)}"
    
    def _create_analysis_prompt(self, stock_data: Dict[str, Any]) -> str:
        """
        ChatGPT 분석을 위한 프롬프트 생성
        """
        prompt = f"""
당신은 20년 경력의 주식 투자 전문가입니다. 일반 투자자들이 쉽게 이해할 수 있도록 친근하고 정성적으로 설명해주세요.

다음은 {stock_data['symbol']} 주식의 기술적 분석 결과입니다:

📊 현재 주식 정보:
- 현재가: ${stock_data['current_price']}
- 분석일: {stock_data['analysis_date']}

📈 기술적 지표 분석 결과:
"""
        
        # 각 지표별 결과 추가
        for indicator, data in stock_data['interpreted_signals'].items():
            prompt += f"- {data['indicator_name']}: {data['signal']} ({data['description']})\n"
        
        prompt += f"""
📊 종합 점수: {stock_data['total_score']}점
🎯 전체 추천: {stock_data['recommendation']}

위의 기술적 분석 결과를 바탕으로, 일반 투자자들이 이해하기 쉽게 다음 형식으로 답변해주세요:

🧠 전문가 종합평가:

(여기서는 각 지표의 수치를 나열하는 것이 아니라, 마치 친한 투자 상담사가 설명하는 것처럼 자연스럽고 이해하기 쉽게 현재 상황을 종합적으로 분석해주세요. 전문 용어는 최소화하고, 실제 투자 결정에 도움이 되는 인사이트를 제공해주세요.)

📈 투자자별 전략 제안:

👤 주식 미보유자:
(현재 주식을 보유하지 않은 투자자를 위한 구체적이고 실용적인 조언을 제공해주세요. 언제 매수할지, 어떤 조건을 확인해야 하는지 등을 친근하게 설명해주세요.)

💼 주식 보유자:
(현재 주식을 보유한 투자자를 위한 전략을 제시해주세요. 보유 유지, 추가 매수, 매도 시점 등에 대한 실용적인 조언을 제공해주세요.)

주의사항: 답변에서 큰따옴표를 사용하지 마시고, 자연스러운 한국어로 작성해주세요.
"""
        
        return prompt 