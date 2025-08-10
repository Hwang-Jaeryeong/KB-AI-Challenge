import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from openai import OpenAI
import os

class EmotionAnalyzer:
    def __init__(self, api_key: str):
        """감정 분석기 초기화"""
        self.client = OpenAI(api_key=api_key)
        self.emotion_categories = {
            "긍정": ["기쁨", "만족", "희망", "감사", "사랑"],
            "부정": ["슬픔", "실망", "우울", "절망", "고독"],
            "분노": ["화남", "짜증", "분노", "적대감", "원망"],
            "불안": ["걱정", "불안", "긴장", "두려움", "스트레스"],
            "중립": ["평온", "무관심", "차분함", "평범함"]
        }
        
        # 사용자별 데이터 저장 (실제로는 데이터베이스 사용)
        self.user_data = {}
        
    def analyze_emotion(self, text: str) -> Dict:
        """텍스트에서 감정 분석 수행"""
        prompt = f"""
다음 텍스트의 감정을 분석해주세요:

텍스트: "{text}"

다음 JSON 형식으로 응답해주세요:
{{
    "primary_emotion": "주요 감정 (긍정/부정/분노/불안/중립)",
    "emotion_intensity": 감정 강도 (1-10),
    "specific_emotions": ["구체적인 감정들"],
    "stress_level": 스트레스 수준 (1-10),
    "confidence": 분석 신뢰도 (0.0-1.0)
}}

감정 강도 기준:
- 1-3: 약함
- 4-6: 보통
- 7-8: 강함
- 9-10: 매우 강함
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 감정 분석 AI입니다. 정확하고 객관적으로 감정을 분석해주세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"감정 분석 중 오류 발생: {e}")
            return {
                "primary_emotion": "중립",
                "emotion_intensity": 5,
                "specific_emotions": ["분석 실패"],
                "stress_level": 5,
                "confidence": 0.0
            }
    
    def calculate_stress_score(self, user_id: str, current_emotion: Dict) -> Dict:
        """스트레스 점수 계산"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "sessions": [],
                "emotion_history": [],
                "stress_scores": []
            }
        
        user = self.user_data[user_id]
        current_time = datetime.now()
        
        # 현재 감정 데이터 저장
        emotion_data = {
            "timestamp": current_time,
            "emotion": current_emotion,
            "text": current_emotion.get("text", "")
        }
        user["emotion_history"].append(emotion_data)
        
        # 최근 30일 데이터만 유지
        cutoff_date = current_time - timedelta(days=30)
        user["emotion_history"] = [
            e for e in user["emotion_history"] 
            if e["timestamp"] > cutoff_date
        ]
        
        # 스트레스 점수 계산
        stress_score = self._compute_stress_score(user, current_emotion)
        
        # 세션 정보 업데이트
        session_data = {
            "timestamp": current_time,
            "stress_score": stress_score,
            "emotion": current_emotion
        }
        user["sessions"].append(session_data)
        user["stress_scores"].append(stress_score)
        
        return {
            "current_stress_score": stress_score,
            "trend": self._calculate_trend(user["stress_scores"]),
            "risk_level": self._assess_risk_level(stress_score),
            "session_count": len(user["sessions"]),
            "recent_emotions": user["emotion_history"][-5:]  # 최근 5개 감정
        }
    
    def _compute_stress_score(self, user: Dict, current_emotion: Dict) -> float:
        """스트레스 점수 계산 로직"""
        base_score = current_emotion.get("stress_level", 5)
        emotion_intensity = current_emotion.get("emotion_intensity", 5)
        
        # 감정 타입별 가중치
        emotion_weights = {
            "긍정": 0.3,
            "부정": 0.8,
            "분노": 0.9,
            "불안": 1.0,
            "중립": 0.5
        }
        
        primary_emotion = current_emotion.get("primary_emotion", "중립")
        emotion_weight = emotion_weights.get(primary_emotion, 0.5)
        
        # 최근 상담 빈도 고려
        recent_sessions = len([s for s in user["sessions"] 
                             if s["timestamp"] > datetime.now() - timedelta(days=7)])
        frequency_factor = min(recent_sessions * 0.2, 2.0)  # 최대 2점 추가
        
        # 감정 누적 효과
        recent_emotions = user["emotion_history"][-10:]  # 최근 10개
        negative_count = sum(1 for e in recent_emotions 
                           if e["emotion"].get("primary_emotion") in ["부정", "분노", "불안"])
        cumulative_factor = negative_count * 0.1
        
        # 최종 스트레스 점수 계산
        stress_score = (base_score * emotion_weight + 
                       emotion_intensity * 0.3 + 
                       frequency_factor + 
                       cumulative_factor)
        
        return min(stress_score, 10.0)  # 최대 10점
    
    def _calculate_trend(self, stress_scores: List[float]) -> str:
        """스트레스 점수 트렌드 계산"""
        if len(stress_scores) < 3:
            return "안정"
        
        recent_avg = sum(stress_scores[-3:]) / 3
        previous_avg = sum(stress_scores[-6:-3]) / 3 if len(stress_scores) >= 6 else stress_scores[0]
        
        if recent_avg > previous_avg + 1:
            return "상승"
        elif recent_avg < previous_avg - 1:
            return "하락"
        else:
            return "안정"
    
    def _assess_risk_level(self, stress_score: float) -> str:
        """위험도 평가"""
        if stress_score >= 8:
            return "높음"
        elif stress_score >= 6:
            return "보통"
        else:
            return "낮음"
    
    def recommend_counseling(self, user_id: str, current_emotion: Dict) -> Dict:
        """상담 프로그램 추천"""
        primary_emotion = current_emotion.get("primary_emotion", "중립")
        stress_level = current_emotion.get("stress_level", 5)
        
        recommendations = {
            "긍정": {
                "programs": ["긍정심리학 워크샵", "감사일기 작성법", "행복한 습관 만들기"],
                "resources": ["긍정심리학 도서", "명상 앱", "감사 연습 가이드"],
                "priority": "낮음"
            },
            "부정": {
                "programs": ["인지행동치료", "우울증 관리 프로그램", "자기돌봄 워크샵"],
                "resources": ["전문 상담사 연결", "우울증 관리 앱", "자기돌봄 체크리스트"],
                "priority": "높음"
            },
            "분노": {
                "programs": ["분노 관리 프로그램", "스트레스 해소 기법", "감정 조절 훈련"],
                "resources": ["분노 관리 가이드", "호흡법 훈련", "감정 일기"],
                "priority": "높음"
            },
            "불안": {
                "programs": ["불안 관리 프로그램", "마음챙김 명상", "이완 기법 훈련"],
                "resources": ["불안 관리 앱", "명상 가이드", "이완 운동 동영상"],
                "priority": "높음"
            },
            "중립": {
                "programs": ["일반 상담", "자기계발 프로그램", "스트레스 예방 교육"],
                "resources": ["상담 서비스 안내", "자기계발 도서", "건강 관리 팁"],
                "priority": "보통"
            }
        }
        
        recommendation = recommendations.get(primary_emotion, recommendations["중립"])
        
        # 스트레스 수준에 따른 추가 권장사항
        if stress_level >= 8:
            recommendation["urgent_action"] = "즉시 전문 상담사 상담 권장"
        elif stress_level >= 6:
            recommendation["urgent_action"] = "일주일 내 상담 예약 권장"
        else:
            recommendation["urgent_action"] = "정기적인 모니터링 권장"
        
        return recommendation 