import openai
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class CounselingChatbot:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.conversation_history = {}
        
        # 캐릭터별 페르소나 정의
        self.character_personas = {
            '플로라무': {
                'role': '고객 관련 스트레스 전문 상담사',
                'personality': '부드럽고 공감적인 톤으로 고객과의 갈등 상황을 해소해주는 상담사',
                'specialty': '고객 민원, 폭언, 과도한 요구 등 외부 스트레스 상황'
            },
            '심쿵비비': {
                'role': '조직·업무 관련 스트레스 전문 상담사',
                'personality': '포근하고 따뜻한 마음으로 직장 내 인간관계와 업무 압박을 조율하는 상담사',
                'specialty': '상사·동료 갈등, 업무 압박, 조직 문화 등 내부 스트레스 상황'
            },
            '멜랑콜리': {
                'role': '개인·번아웃 전문 상담사',
                'personality': '초록빛 위로로 지친 몸과 마음을 치유하는 힐링 상담사',
                'specialty': '피로, 무기력, 개인적 번아웃 등 내적 스트레스 상황'
            }
        }

    def process_message(self, user_id, message, character=None, category=None):
        try:
            # 대화 기록 초기화
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # 캐릭터 정보 가져오기
            character_info = self.character_personas.get(character, self.character_personas['멜랑콜리'])
            
            # 시스템 프롬프트 구성
            system_prompt = f"""당신은 KB HUG의 {character_info['role']}입니다.

특징:
- {character_info['personality']}
- {character_info['specialty']}에 특화되어 있습니다
- 심리상담 기법을 사용하여 공감적이고 위로가 되는 대화를 제공합니다
- 사용자의 감정을 깊이 탐색하고 적절한 조언을 제공합니다
- 한국어로 자연스럽고 따뜻한 톤으로 대화합니다
- 반복적인 마무리 문구는 사용하지 않습니다

대화 원칙:
1. 공감적 경청과 반영
2. 감정 탐색을 위한 깊이 있는 질문
3. 위로와 격려 제공
4. 실용적인 조언과 해결책 제시
5. 전문적이면서도 친근한 톤 유지

응답은 2-3문장으로 간결하게 작성하되, 공감적이고 도움이 되도록 구성하세요."""

            # 대화 기록에 사용자 메시지 추가
            self.conversation_history[user_id].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })

            # ChatGPT API 호출
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[{"role": msg["role"], "content": msg["content"]} 
                      for msg in self.conversation_history[user_id][-10:]]  # 최근 10개 메시지만 사용
                ],
                max_tokens=300,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content

            # 대화 기록에 AI 응답 추가
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })

            return {
                "response": ai_response,
                "status": "success"
            }

        except Exception as e:
            print(f"ChatGPT API 오류: {str(e)}")  # 디버깅을 위한 로그
            # API 오류 시 다양한 기본 응답 제공
            return self._generate_smart_response(message, character, user_id)

    def recommend_resources(self, conversation_history, category):
        # 대화 내용을 바탕으로 관련 리소스를 검색 and 추천
        try:
            # 대화 내용 요약
            conversation_text = " ".join([
                f"{msg.get('user', '')} {msg.get('bot', '')}" 
                for msg in conversation_history
            ])

            # 키워드 추출을 위한 프롬프트
            keyword_prompt = f"""다음 대화 내용에서 핵심 키워드 3-5개를 추출해주세요. 
            각 키워드는 쉼표로 구분하고, 검색에 적합한 형태로 작성해주세요.

            대화 내용: {conversation_text[:500]}...

            키워드:"""

            # 키워드 추출
            keyword_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": keyword_prompt}],
                max_tokens=100,
                temperature=0.3
            )

            keywords = keyword_response.choices[0].message.content.strip()
            
            # 카테고리별 검색 쿼리 구성
            category_queries = {
                'customer': ['고객 스트레스 관리', '민원 대응 방법', '고객 서비스 스킬'],
                'work': ['직장 스트레스 해소', '동료 관계 개선', '업무 압박 관리'],
                'personal': ['번아웃 예방', '스트레스 해소법', '마음 건강 관리']
            }

            base_queries = category_queries.get(category, ['스트레스 관리', '심리 상담'])
            
            # 검색 쿼리 조합
            search_queries = [f"{keyword} {base_query}" for keyword in keywords.split(',')[:3] 
                            for base_query in base_queries[:2]]

            resources = []
            
            for query in search_queries[:5]:  # 최대 5개 쿼리로 제한
                try:
                    # 후에 더 정교한 api로 발전시키기!
                    search_results = self._search_naver_blog(query)
                    resources.extend(search_results[:2])  # 쿼리당 2개 결과
                except Exception as e:
                    print(f"검색 오류: {e}")
                    continue

            # 중복 제거 및 정렬
            unique_resources = []
            seen_urls = set()
            
            for resource in resources:
                if resource['url'] not in seen_urls:
                    unique_resources.append(resource)
                    seen_urls.add(resource['url'])

            # 기본 리소스 추가
            default_resources = self._get_default_resources(category)
            resources_with_defaults = default_resources + unique_resources[:6]

            return {
                "resources": resources_with_defaults,
                "keywords": keywords,
                "category": category
            }

        except Exception as e:
            print(f"리소스 추천 오류: {e}")
            # 기본 리소스 반환
            return {
                "resources": self._get_default_resources(category),
                "keywords": "스트레스 관리, 심리 상담",
                "category": category
            }

    def _search_naver_blog(self, query):
        # 네이버 블로그 검색
        try:
            import requests
            from bs4 import BeautifulSoup
            import urllib.parse
            import re
            
            # 검색 URL 구성
            search_url = f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}"
            
            # User-Agent 설정
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 웹 페이지 요청
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 블로그 포스트 찾기 (실제 네이버 검색 결과 구조에 맞게 수정)
            blog_posts = soup.find_all('li', class_='bx')
            resources = []
            
            for post in blog_posts[:4]:  # 최대 4개 결과
                try:
                    # 제목과 링크 추출
                    title_elem = post.find('a', class_='title_link')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    # 실제 블로그 포스트 URL로 변환 (네이버 검색 결과에서 실제 블로그 URL 추출)
                    if 'blog.naver.com' in url:
                        # 이미 실제 블로그 URL인 경우
                        actual_url = url
                    else:
                        # 검색 결과 URL에서 실제 블로그 URL 추출
                        actual_url = url
                    
                    # 설명/미리보기 추출
                    desc_elem = post.find('div', class_='dsc')
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
                        # 설명이 너무 길면 자르기
                        if len(description) > 150:
                            description = description[:150] + "..."
                    else:
                        description = f"{query}에 대한 유용한 정보를 제공하는 블로그 포스트입니다."
                    
                    # 블로그명과 날짜 추출
                    blog_elem = post.find('a', class_='sub_time')
                    blog_name = blog_elem.get_text(strip=True) if blog_elem else "네이버 블로그"
                    
                    # 날짜 추출
                    date_elem = post.find('span', class_='sub_time')
                    date = date_elem.get_text(strip=True) if date_elem else ""
                    
                    # 썸네일 이미지 추출 (있는 경우)
                    img_elem = post.find('img')
                    thumbnail = img_elem.get('src', '') if img_elem else ""
                    
                    resources.append({
                        "title": title,
                        "url": actual_url,
                        "description": description,
                        "type": "blog",
                        "source": blog_name,
                        "date": date,
                        "thumbnail": thumbnail
                    })
                    
                except Exception as e:
                    print(f"블로그 포스트 파싱 오류: {e}")
                    continue
            
            # 결과가 없으면 기본 데이터 반환
            if not resources:
                return [
                    {
                        "title": f"{query} 관련 블로그 포스트",
                        "url": f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}",
                        "description": f"{query}에 대한 유용한 정보를 제공하는 블로그 포스트입니다.",
                        "type": "blog",
                        "source": "네이버 블로그",
                        "date": "",
                        "thumbnail": ""
                    }
                ]
            
            return resources
            
        except Exception as e:
            print(f"네이버 블로그 검색 오류: {e}")
            # 오류 시 기본 데이터 반환
            return [
                {
                    "title": f"{query} 관련 블로그 포스트",
                    "url": f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}",
                    "description": f"{query}에 대한 유용한 정보를 제공하는 블로그 포스트입니다.",
                    "type": "blog",
                    "source": "네이버 블로그",
                    "date": "",
                    "thumbnail": ""
                }
            ]

    def _get_default_resources(self, category):
        default_resources = {
            'customer': [
                {
                    "title": "고객 스트레스 관리 방법",
                    "url": "https://search.naver.com/search.naver?where=blog&query=고객+스트레스+관리+방법",
                    "description": "고객 응대 시 스트레스를 관리하는 효과적인 방법들을 알아보세요",
                    "type": "blog",
                    "source": "네이버 블로그"
                },
                {
                    "title": "고객 서비스 스킬 향상법",
                    "url": "https://search.naver.com/search.naver?where=blog&query=고객+서비스+스킬+향상",
                    "description": "고객과의 효과적인 소통 방법과 스트레스 관리 기법",
                    "type": "blog",
                    "source": "네이버 블로그"
                }
            ],
            'work': [
                {
                    "title": "직장 내 인간관계 개선법",
                    "url": "https://search.naver.com/search.naver?where=blog&query=직장+인간관계+개선",
                    "description": "동료와의 관계 개선 및 업무 스트레스 해소 방법",
                    "type": "blog",
                    "source": "네이버 블로그"
                },
                {
                    "title": "업무 효율성 향상 가이드",
                    "url": "https://search.naver.com/search.naver?where=blog&query=업무+효율성+향상+방법",
                    "description": "업무 압박 관리와 효율적인 업무 처리 방법",
                    "type": "blog",
                    "source": "네이버 블로그"
                }
            ],
            'personal': [
                {
                    "title": "번아웃 예방과 회복",
                    "url": "https://search.naver.com/search.naver?where=blog&query=번아웃+예방+회복",
                    "description": "개인적 번아웃 예방과 회복을 위한 전문적인 조언",
                    "type": "blog",
                    "source": "네이버 블로그"
                },
                {
                    "title": "마음 건강 관리법",
                    "url": "https://search.naver.com/search.naver?where=blog&query=마음+건강+관리+방법",
                    "description": "일상에서 실천할 수 있는 마음 건강 관리 방법",
                    "type": "blog",
                    "source": "네이버 블로그"
                }
            ]
        }
        
        return default_resources.get(category, default_resources['personal'])

    def _generate_smart_response(self, message, character, user_id):
         """메시지 내용을 분석하여 다양한 응답 생성"""
         import random
         
         # 대화 기록 가져오기
         if user_id not in self.conversation_history:
             self.conversation_history[user_id] = []
         
         # 대화 기록에 사용자 메시지 추가
         self.conversation_history[user_id].append({
             "role": "user",
             "content": message,
             "timestamp": datetime.now().isoformat()
         })
         
         # 메시지 내용 분석
         message_lower = message.lower()
         
         # 감정 키워드 분석
         stress_keywords = ['스트레스', '힘들어', '지쳐', '피곤', '짜증', '화나', '답답', '불안', '걱정']
         positive_keywords = ['좋아', '행복', '기쁘', '감사', '만족', '편안']
         question_keywords = ['어떻게', '왜', '언제', '어디서', '무엇을', '?']
         
         # 캐릭터별 응답 템플릿
         character_responses = {
             '플로라무': {
                 'greeting': [
                     "안녕하세요! 고객 관련 고민이 있으시군요. 편하게 말씀해주세요.",
                     "고객과의 관계에서 힘드신 일이 있으신가요? 함께 이야기해보아요.",
                     "고객 서비스 업무를 하시면서 어려운 점이 있으시군요. 천천히 들려주세요."
                 ],
                 'stress': [
                     "고객과의 갈등 상황에서 스트레스를 받으시는군요. 그런 상황에서 정말 힘드셨을 것 같아요.",
                     "고객의 요구사항을 맞추려다 보니 많이 지치셨겠어요. 함께 해결방법을 찾아보아요.",
                     "고객 응대 과정에서 받는 스트레스가 크시군요. 그런 감정을 이해합니다."
                 ],
                 'question': [
                     "어떤 부분에서 가장 힘드신가요? 구체적으로 말씀해주시면 더 도움을 드릴 수 있어요.",
                     "고객과의 어떤 상황에서 이런 감정을 느끼셨나요?",
                     "이런 상황을 어떻게 해결하고 싶으신가요?"
                 ],
                 'support': [
                     "고객과의 소통에서 중요한 것은 공감과 이해예요. 함께 더 나은 방법을 찾아보아요.",
                     "고객 응대 스킬을 향상시키는 방법들이 있어요. 차근차근 연습해보시면 좋을 것 같아요.",
                     "고객과의 관계에서 경계를 설정하는 것도 중요해요. 건강한 관계를 만들어보아요."
                 ]
             },
             '심쿵비비': {
                 'greeting': [
                     "안녕하세요! 직장에서의 고민이 있으시군요. 편하게 이야기해주세요.",
                     "업무나 동료 관계에서 어려운 점이 있으신가요? 함께 고민해보아요.",
                     "직장 생활에서 힘드신 일이 있으시군요. 천천히 들려주세요."
                 ],
                 'stress': [
                     "업무 압박이나 동료 관계에서 스트레스를 받으시는군요. 그런 상황에서 정말 힘드셨을 것 같아요.",
                     "직장에서의 갈등이나 업무량이 많아서 지치셨겠어요. 함께 해결방법을 찾아보아요.",
                     "조직 내에서의 스트레스가 크시군요. 그런 감정을 이해합니다."
                 ],
                 'question': [
                     "어떤 상황에서 가장 힘드신가요? 구체적으로 말씀해주시면 더 도움을 드릴 수 있어요.",
                     "동료나 상사와의 어떤 관계에서 이런 감정을 느끼셨나요?",
                     "업무 환경에서 개선하고 싶은 부분이 있으신가요?"
                 ],
                 'support': [
                     "직장에서의 인간관계는 서로의 입장을 이해하는 것부터 시작해요. 함께 더 나은 방법을 찾아보아요.",
                     "업무 효율성을 높이는 방법들이 있어요. 체계적으로 접근해보시면 좋을 것 같아요.",
                     "직장에서의 경계 설정과 자기 관리도 중요해요. 건강한 업무 환경을 만들어보아요."
                 ]
             },
             '멜랑콜리': {
                 'greeting': [
                     "안녕하세요! 개인적인 고민이 있으시군요. 편하게 이야기해주세요.",
                     "마음이 지치거나 번아웃을 느끼고 계신가요? 함께 위로해드릴게요.",
                     "개인적인 스트레스나 피로를 느끼고 계시군요. 천천히 들려주세요."
                 ],
                 'stress': [
                     "개인적인 스트레스나 번아웃을 느끼고 계시는군요. 그런 상황에서 정말 힘드셨을 것 같아요.",
                     "지속적인 스트레스로 인해 많이 지치셨겠어요. 함께 회복 방법을 찾아보아요.",
                     "개인적인 고민이나 피로가 크시군요. 그런 감정을 이해합니다."
                 ],
                 'question': [
                     "어떤 부분에서 가장 힘드신가요? 구체적으로 말씀해주시면 더 도움을 드릴 수 있어요.",
                     "언제부터 이런 감정을 느끼기 시작하셨나요?",
                     "마음의 안정을 찾기 위해 어떤 것들을 시도해보셨나요?"
                 ],
                 'support': [
                     "개인적인 스트레스 관리는 자기 돌봄부터 시작해요. 함께 더 나은 방법을 찾아보아요.",
                     "마음의 건강을 위한 다양한 방법들이 있어요. 천천히 실천해보시면 좋을 것 같아요.",
                     "개인적인 경계 설정과 자기 관리도 중요해요. 건강한 마음 상태를 만들어보아요."
                 ]
             }
         }
         
         # 응답 카테고리 결정
         if any(keyword in message_lower for keyword in stress_keywords):
             category = 'stress'
         elif any(keyword in message_lower for keyword in positive_keywords):
             category = 'support'
         elif any(keyword in message_lower for keyword in question_keywords):
             category = 'question'
         else:
             category = 'greeting'
         
         # 대화 길이에 따른 응답 조정
         conversation_length = len(self.conversation_history[user_id])
         if conversation_length > 4:
             category = 'question'  # 더 깊이 있는 질문
         
         # 캐릭터별 응답 선택
         character_response = character_responses.get(character, character_responses['멜랑콜리'])
         responses = character_response.get(category, character_response['greeting'])
         
         # 랜덤 응답 선택
         response = random.choice(responses)
         
         # 대화 기록에 AI 응답 추가
         self.conversation_history[user_id].append({
             "role": "assistant",
             "content": response,
             "timestamp": datetime.now().isoformat()
         })
         
         return {
             "response": response,
             "status": "success"
         }

    def get_user_dashboard_data(self, user_id):
        # 사용자 대시보드 데이터
        if user_id not in self.conversation_history:
            return {
                "total_conversations": 0,
                "recent_messages": [],
                "mood_trend": []
            }
        
        conversations = self.conversation_history[user_id]
        return {
            "total_conversations": len(conversations) // 2,  # 사용자-봇 쌍으로 계산
            "recent_messages": conversations[-20:],  # 최근 20개 메시지
            "mood_trend": self._analyze_mood_trend(conversations)
        }

    def get_admin_dashboard_data(self):
        # 관리자 대시보드 데이터
        total_users = len(self.conversation_history)
        total_conversations = sum(len(conv) // 2 for conv in self.conversation_history.values())
        
        return {
            "total_users": total_users,
            "total_conversations": total_conversations,
            "category_distribution": self._get_category_distribution(),
            "recent_activity": self._get_recent_activity()
        }

    def _analyze_mood_trend(self, conversations):
        return [{"date": "2025-01-11", "mood": "neutral"}]

    def _get_category_distribution(self):
        # 카테고리 분포 데이터
        return [
            {"category": "고객", "count": 30, "percentage": 40},
            {"category": "조직·업무", "count": 25, "percentage": 33},
            {"category": "개인·번아웃", "count": 20, "percentage": 27}
        ]

    def _get_recent_activity(self):
        # 최근 활동 데이터
        return [
            {"user_id": "user1", "last_activity": "2025-01-11 14:30", "category": "고객"},
            {"user_id": "user2", "last_activity": "2025-01-11 13:45", "category": "조직·업무"},
            {"user_id": "user3", "last_activity": "2025-01-11 12:20", "category": "개인·번아웃"}
        ] 