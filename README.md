# KB HUG AI - 직원 힐링 AI 챗봇

## 프로젝트 개요

KB HUG AI는 직원들의 스트레스와 고민을 해소하기 위한 AI 상담 챗봇 시스템입니다. 사용자가 선택한 카테고리에 따라 맞춤형 AI 캐릭터와 대화하며, 대화 내용을 바탕으로 관련 리소스를 추천해주는 서비스입니다.

**구현 범위**: 프론트엔드 UI/UX 및 AI 서비스 모듈 (백엔드는 Spring Boot + MySQL로 별도 구현)

### 주요 기능

1. **카테고리별 AI 캐릭터 선택**
   - **롤로라무**: 고객 관련 스트레스 전문
   - **심쿵비비**: 조직/업무 관련 스트레스 전문  
   - **멜랑콜리**: 개인/번아웃 전문

2. **자연스러운 AI 대화**
   - ChatGPT API 기반 심리 상담 기법 적용
   - 감정에 맞춘 위로와 격려 메시지
   - 대화 내용 기반 키워드 추출

3. **맞춤형 리소스 추천**
   - 대화 내용 분석을 통한 키워드 추출
   - 네이버 블로그 실시간 크롤링
   - 관련 상담, 블로그, 서적 추천

4. **대화 기록 관리**
   - 사용자별 대화 히스토리 저장
   - 카테고리별 통계 분석
   - 관리자 대시보드 지원

## 설치 및 실행

### 1. AI 서비스 모듈 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 설정
`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Spring Boot 백엔드 연동
- AI 서비스 모듈을 Spring Boot 프로젝트에 통합
- `CounselingChatbot` 클래스를 Spring Bean으로 등록
- RESTful API 엔드포인트를 통해 AI 서비스 호출
- MySQL 데이터베이스 연동

### 4. 프론트엔드 개발 완료
- HTML/CSS/JavaScript 기반 사용자 인터페이스 구현 완료
- 배포 환경 구성 후 웹 서비스 제공 예정
- MySQL 데이터베이스와 연동하여 사용자 데이터 관리 (백엔드)

## 기술 스택 및 시스템 아키텍처

### 🛠️ 기술 스택

| 분류 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **Backend** | Spring Boot | - | RESTful API 서버 (외부 구현) |
| **Database** | MySQL | - | 데이터 저장 및 관리 |
| **AI/ML** | OpenAI GPT-3.5 Turbo | - | 자연어 처리 및 대화 생성 |
| **Web Scraping** | BeautifulSoup4 | - | 네이버 블로그 크롤링 |
| **HTTP Client** | Requests | 2.31.0 | 외부 API 호출 |
| **Environment** | python-dotenv | 1.0.0 | 환경 변수 관리 |
| **Frontend** | HTML5/CSS3/JavaScript | - | 사용자 인터페이스 |
| **Storage** | localStorage | - | 클라이언트 사이드 상태 관리 |

### 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (Browser)     │    │   (Spring Boot) │    │   Services      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • HTML5/CSS3    │◄──►│ • Spring Server │◄──►│ • OpenAI API    │
│ • JavaScript    │    │ • RESTful API   │    │ • GPT-3.5 Turbo │
│ • localStorage  │    │ • Business Logic│    │                 │
│ • Real-time UI  │    │ • MySQL DB      │    │ • Naver Search  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔧 핵심 모듈 구조

#### 1. **CounselingChatbot** (`app/chatbot.py`)
```python
class CounselingChatbot:
    ├── __init__(api_key)           # OpenAI 클라이언트 초기화
    ├── process_message()           # 메인 대화 처리 로직
    ├── recommend_resources()       # 리소스 추천 엔진
    ├── _search_naver_blog()        # 네이버 블로그 크롤링
    ├── _extract_keywords()         # GPT 기반 키워드 추출
    └── _generate_smart_response()  # 폴백 응답 생성
```

#### 2. **AI 서비스 모듈** (`app/chatbot.py`)
```python
AI Service Module:
    ├── CounselingChatbot           # AI 챗봇 핵심 로직
    ├── process_message()           # 대화 처리 및 GPT API 연동
    ├── recommend_resources()       # 리소스 추천 엔진
    ├── _search_naver_blog()        # 네이버 블로그 크롤링
    └── _generate_smart_response()  # 폴백 응답 생성
```

#### 3. **프론트엔드 모듈** (`app/templates/`)
```
Frontend Templates:
    ├── home.html                   # 메인 홈 화면
    ├── chat_topics.html            # 캐릭터 선택 화면
    ├── chat_interface.html         # 실시간 채팅 UI
    ├── resources.html              # 리소스 추천 화면
    └── records.html                # 대화 기록 화면

JavaScript Features:
    ├── Real-time Chat Interface    # 실시간 채팅 기능
    ├── Character Selection         # 캐릭터 선택 및 상태 관리
    ├── Resource Recommendation     # 리소스 추천 UI
    ├── Local Storage Management    # 사용자 상태 저장
    └── Error Handling              # 클라이언트 사이드 오류 처리
```

### 📊 데이터 흐름 다이어그램

```
1. 사용자 카테고리 선택 (고객/업무/개인)
   ↓
2. AI 캐릭터 페르소나 설정 (플로라무/심쿵비비/멜랑콜리)
   ↓
3. ChatGPT API 호출 (GPT-3.5 Turbo)
   ├── 시스템 프롬프트 구성
   ├── 대화 컨텍스트 관리
   └── 자연스러운 응답 생성
   ↓
4. 대화 내용 분석 및 키워드 추출
   ├── GPT 기반 키워드 추출
   ├── 카테고리별 검색 쿼리 구성
   └── 검색 최적화
   ↓
5. 네이버 블로그 실시간 크롤링
   ├── BeautifulSoup4 HTML 파싱
   ├── 블로그 포스트 정보 추출
   └── 중복 제거 및 정렬
   ↓
6. 맞춤형 리소스 추천 및 제공
   ├── 관련성 점수 계산
   ├── 카테고리별 필터링
   └── 사용자 친화적 UI 제공
```

## 사용자 인터페이스

### 1. 홈 화면 (`/home`)
- **기록 보기** 버튼: 과거 대화 기록 확인
- **대화 시작하기** 버튼: 카테고리 선택 화면으로 이동

### 2. 카테고리 선택 화면 (`/chat_topics`)
- 3개 카테고리별 KB 캐릭터 표시
- 클릭 시 해당 캐릭터와 대화 시작
- localStorage를 통한 선택 정보 저장

### 3. AI 대화 화면 (`/chat_interface`)
- 실시간 채팅 인터페이스
- 자동 높이 조절 텍스트 입력
- 타이핑 인디케이터
- 제안 버튼을 통한 빠른 대화 시작

### 4. 리소스 추천 화면 (`/resources`)
- 대화 내용 기반 추천 리소스 표시
- 실제 네이버 블로그 포스트 링크
- 블로그명, 작성일, 미리보기 제공
- 썸네일 이미지 표시

## 기술적 구현

### 1. AI 챗봇 엔진 (OpenAI GPT-3.5 Turbo)
```python
# app/chatbot.py - CounselingChatbot 클래스
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
        # 시스템 프롬프트 구성
        system_prompt = f"""당신은 KB HUG의 {character_info['role']}입니다.
        특징: {character_info['personality']}
        대화 원칙: 공감적 경청, 감정 탐색, 위로와 격려, 실용적 조언
        응답은 2-3문장으로 간결하게 작성하되, 공감적이고 도움이 되도록 구성하세요."""
        
        # ChatGPT API 호출
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}] + recent_messages,
            max_tokens=300,
            temperature=0.7
        )
```

### 2. 실시간 웹 크롤링 시스템 (BeautifulSoup4)
```python
# app/chatbot.py - 네이버 블로그 크롤링
def _search_naver_blog(self, query):
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse
    
    # 검색 URL 구성 및 User-Agent 설정
    search_url = f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 웹 페이지 요청 및 HTML 파싱
    response = requests.get(search_url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 블로그 포스트 정보 추출
    blog_posts = soup.find_all('li', class_='bx')
    resources = []
    
    for post in blog_posts:
        title_elem = post.find('a', class_='title_link')
        blog_name_elem = post.find('a', class_='sub_time')
        
        if title_elem and blog_name_elem:
            resources.append({
                'title': title_elem.get_text(strip=True),
                'url': title_elem.get('href', ''),
                'blog_name': blog_name_elem.get_text(strip=True),
                'type': 'blog'
            })
    
    return resources[:6]  # 최대 6개 결과 반환
```

### 3. 키워드 추출 및 리소스 추천 엔진
```python
# app/chatbot.py - 대화 기반 키워드 추출
def recommend_resources(self, conversation_history, category):
    # 대화 내용 요약
    conversation_text = " ".join([
        f"{msg.get('user', '')} {msg.get('bot', '')}" 
        for msg in conversation_history
    ])

    # GPT를 활용한 키워드 추출
    keyword_prompt = f"""다음 대화 내용에서 핵심 키워드 3-5개를 추출해주세요.
    대화 내용: {conversation_text[:500]}...
    키워드:"""

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
    
    # 키워드와 카테고리 쿼리 조합으로 검색
    search_queries = [f"{keyword} {base_query}" for keyword in keywords.split(',')[:3] 
                     for base_query in category_queries.get(category, ['스트레스 관리'])[:2]]
```

### 4. AI 서비스 및 외부 API 연동
```python
# app/chatbot.py - AI 서비스 모듈
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

    # Spring Boot 백엔드와 연동되는 메서드들
    def process_message(self, user_id, message, character=None, category=None):
        # GPT API 호출 및 응답 생성
        # Spring Boot에서 호출하여 사용
        pass

    def recommend_resources(self, conversation_history, category):
        # 리소스 추천 로직
        # Spring Boot에서 호출하여 사용
        pass
```

### 5. 프론트엔드 상태 관리 (JavaScript)
```javascript
// app/templates/chat_interface.html - 실시간 채팅 인터페이스
function selectCharacter(category, characterName) {
    localStorage.setItem('selectedCategory', category);
    localStorage.setItem('selectedCharacter', characterName);
    window.location.href = '/chat_interface';
}

// Spring Boot 백엔드와의 실시간 API 통신
async function sendMessage() {
    const message = document.getElementById('messageInput').value;
    const character = localStorage.getItem('selectedCharacter') || '멜랑콜리';
    const category = localStorage.getItem('selectedCategory') || 'personal';
    
    // 사용자 메시지 UI 업데이트
    addMessageToChat('user', message);
    
    // Spring Boot 백엔드 API 호출
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            user_id: 'user_' + Date.now(),
            message: message,
            character: character,
            category: category
        })
    });
    
    const data = await response.json();
    
    // AI 응답 UI 업데이트
    addMessageToChat('bot', data.response);
    
    // 대화 히스토리 저장
    conversationHistory.push({
        user: message,
        bot: data.response,
        timestamp: new Date().toISOString()
    });
}

// 리소스 추천 요청
async function requestResources() {
    const response = await fetch('/api/recommend-resources', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            conversation_history: conversationHistory,
            category: localStorage.getItem('selectedCategory') || 'personal'
        })
    });
    
    const data = await response.json();
    displayResources(data.resources);
}
```

### 6. 오류 처리 및 폴백 시스템
```python
# app/chatbot.py - 스마트 폴백 응답
def _generate_smart_response(self, message, character, user_id):
    # ChatGPT API 실패 시 기본 응답 생성
    fallback_responses = {
        '플로라무': [
            "고객과의 갈등 상황이 힘드셨겠어요. 당신의 감정을 이해합니다.",
            "고객 서비스 업무는 정말 어려운 일이죠. 오늘 하루도 수고하셨습니다."
        ],
        '심쿵비비': [
            "직장에서의 스트레스가 많이 쌓이셨겠어요. 천천히 해결해보아요.",
            "동료들과의 관계가 복잡할 때가 있죠. 당신의 입장을 이해합니다."
        ],
        '멜랑콜리': [
            "지치고 힘드신 것 같아요. 충분히 쉬어도 괜찮아요.",
            "번아웃이 오는 것 같네요. 당신의 감정을 인정해주세요."
        ]
    }
    
    import random
    responses = fallback_responses.get(character, fallback_responses['멜랑콜리'])
    return {"response": random.choice(responses), "status": "fallback"}
```

## 오류 처리 및 안정성

### 1. API 오류 대응 시스템
```python
# app/chatbot.py - 다층 오류 처리
def process_message(self, user_id, message, character=None, category=None):
    try:
        # 1차: ChatGPT API 호출
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}] + recent_messages,
            max_tokens=300,
            temperature=0.7
        )
        return {"response": response.choices[0].message.content, "status": "success"}
        
    except openai.RateLimitError:
        # 2차: Rate Limit 오류 시 대기 후 재시도
        time.sleep(2)
        return self._retry_api_call(system_prompt, recent_messages)
        
    except openai.APIError as e:
        # 3차: API 오류 시 스마트 폴백 응답
        print(f"OpenAI API 오류: {str(e)}")
        return self._generate_smart_response(message, character, user_id)
        
    except Exception as e:
        # 4차: 기타 예외 상황 처리
        print(f"예상치 못한 오류: {str(e)}")
        return {"response": "죄송합니다. 일시적인 오류가 발생했습니다.", "status": "error"}
```

### 2. 웹 크롤링 안정성 보장
```python
# app/chatbot.py - 크롤링 오류 처리
def _search_naver_blog(self, query):
    try:
        # 1차: 정상적인 크롤링 시도
        search_url = f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTML 파싱 및 데이터 추출
        soup = BeautifulSoup(response.text, 'html.parser')
        resources = self._extract_blog_data(soup)
        
        if resources:
            return resources
            
    except requests.Timeout:
        # 2차: 타임아웃 시 기본 검색 링크 제공
        print(f"크롤링 타임아웃: {query}")
        return [{"url": f"https://search.naver.com/search.naver?where=blog&query={query}", 
                "title": f"'{query}' 관련 블로그 검색 결과", "type": "fallback"}]
                
    except requests.RequestException as e:
        # 3차: 네트워크 오류 시 기본 리소스 반환
        print(f"크롤링 네트워크 오류: {e}")
        return self._get_default_resources(query)
        
    except Exception as e:
        # 4차: 기타 크롤링 오류 처리
        print(f"크롤링 예외: {e}")
        return []
```

### 3. 프론트엔드 오류 처리
```javascript
// app/templates/chat_interface.html - 클라이언트 사이드 오류 처리
async function sendMessage() {
    try {
        const message = document.getElementById('messageInput').value;
        
        // 입력 검증
        if (!message.trim()) {
            showError('메시지를 입력해주세요.');
            return;
        }
        
        // 로딩 상태 표시
        showLoading(true);
        
        // API 호출
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: 'user_' + Date.now(),
                message: message,
                character: localStorage.getItem('selectedCharacter') || '멜랑콜리',
                category: localStorage.getItem('selectedCategory') || 'personal'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'error') {
            throw new Error(data.response || '알 수 없는 오류가 발생했습니다.');
        }
        
        // 성공적인 응답 처리
        addMessageToChat('bot', data.response);
        
    } catch (error) {
        console.error('메시지 전송 오류:', error);
        showError('메시지 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
        
        // 폴백 메시지 표시
        addMessageToChat('bot', '죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
        
    } finally {
        showLoading(false);
    }
}

// 오류 메시지 표시 함수
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}
```

### 4. 시스템 모니터링 및 로깅
```python
# app/chatbot.py - 시스템 상태 모니터링
import logging
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('kb_hug_ai.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_api_call(self, endpoint, status, response_time):
        self.logger.info(f"API Call: {endpoint} | Status: {status} | Response Time: {response_time}ms")
    
    def log_error(self, error_type, error_message, user_id=None):
        self.logger.error(f"Error: {error_type} | Message: {error_message} | User: {user_id}")
    
    def log_user_activity(self, user_id, action, category=None):
        self.logger.info(f"User Activity: {user_id} | Action: {action} | Category: {category}")
```

### 5. 성능 최적화 및 캐싱
```python
# app/chatbot.py - 응답 캐싱 시스템
from functools import lru_cache
import hashlib

class ResponseCache:
    def __init__(self):
        self.cache = {}
        self.max_cache_size = 1000
    
    @lru_cache(maxsize=100)
    def get_cached_response(self, message_hash, character):
        """자주 사용되는 응답 패턴 캐싱"""
        return self.cache.get(f"{message_hash}_{character}")
    
    def cache_response(self, message_hash, character, response):
        """응답 캐싱"""
        if len(self.cache) >= self.max_cache_size:
            # LRU 방식으로 오래된 캐시 제거
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[f"{message_hash}_{character}"] = response
    
    def generate_message_hash(self, message):
        """메시지 해시 생성"""
        return hashlib.md5(message.encode()).hexdigest()
```

## 데이터 구조

### 대화 히스토리
```python
conversation_history = [
    {
        "user": "사용자 메시지",
        "bot": "AI 응답",
        "timestamp": "2024-01-01T12:00:00Z"
    }
]
```

### 리소스 추천 데이터
```python
resources = [
    {
        "title": "블로그 포스트 제목",
        "url": "실제 블로그 URL",
        "description": "포스트 미리보기",
        "blog_name": "블로그명",
        "date": "작성일",
        "thumbnail": "썸네일 URL",
        "type": "blog"
    }
]
```