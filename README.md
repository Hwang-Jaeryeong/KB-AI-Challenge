# KB HUG AI - 직원 힐링 AI 챗봇

## 프로젝트 개요

KB HUG AI는 직원들의 스트레스와 고민을 해소하기 위한 AI 상담 챗봇 시스템입니다. 사용자가 선택한 카테고리에 따라 맞춤형 AI 캐릭터와 대화하며, 대화 내용을 바탕으로 관련 리소스를 추천해주는 서비스입니다.

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

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 설정
`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 애플리케이션 실행
```bash
python run_server.py
```

### 4. 웹 브라우저에서 접속
- 메인 홈: http://localhost:5000/home
- 기록 보기: http://localhost:5000/records
- 대화 시작: http://localhost:5000/chat_topics

## 시스템 아키텍처

### 핵심 모듈

1. **CounselingChatbot** (`app/chatbot.py`)
   - ChatGPT API 연동을 통한 AI 대화 생성
   - 캐릭터별 페르소나 설정 및 응답 생성
   - 대화 히스토리 관리 및 키워드 추출
   - 네이버 블로그 크롤링을 통한 리소스 추천

2. **Flask 웹 애플리케이션** (`run_server.py`)
   - RESTful API 엔드포인트 (`/chat`, `/recommend_resources`)
   - 정적 파일 서빙 (이미지, CSS, JS)
   - 웹 인터페이스 라우팅

3. **프론트엔드** (`app/templates/`)
   - 반응형 웹 디자인
   - JavaScript를 통한 동적 UI 업데이트
   - localStorage를 활용한 상태 관리

### 데이터 흐름

```
[1] 사용자 카테고리 선택 (고객/업무/개인)
    ↓
[2] AI 캐릭터 페르소나 설정
    ↓
[3] ChatGPT API를 통한 자연스러운 대화
    ↓
[4] 대화 내용 분석 및 키워드 추출
    ↓
[5] 네이버 블로그 크롤링으로 관련 리소스 검색
    ↓
[6] 맞춤형 리소스 추천 및 제공
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

### 1. ChatGPT API 연동
```python
# app/chatbot.py
def process_message(self, user_id, message, character, category):
    # 캐릭터별 페르소나 설정
    character_info = self.character_personas[character]
    system_prompt = f"당신은 {character_info['name']}입니다. {character_info['personality']}"
    
    # ChatGPT API 호출
    response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt}] + recent_messages
    )
```

### 2. 웹 크롤링 구현
```python
# app/chatbot.py
def _search_naver_blog(self, query):
    # 네이버 블로그 검색 URL 구성
    search_url = f"https://search.naver.com/search.naver?where=blog&query={urllib.parse.quote(query)}"
    
    # BeautifulSoup을 통한 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    blog_posts = soup.find_all('li', class_='bx')
    
    # 실제 블로그 포스트 정보 추출
    for post in blog_posts:
        title = post.find('a', class_='title_link')
        blog_name = post.find('a', class_='sub_time')
        # 실제 URL, 제목, 블로그명, 날짜 추출
```

### 3. 프론트엔드 상태 관리
```javascript
// app/templates/chat_interface.html
function selectCharacter(category, characterName) {
    localStorage.setItem('selectedCategory', category);
    localStorage.setItem('selectedCharacter', characterName);
    window.location.href = '/chat_interface';
}

// 대화 히스토리 관리
conversationHistory.push({
    user: message, 
    bot: data.response, 
    timestamp: new Date().toISOString()
});
```

### 4. API 엔드포인트
```python
# run_server.py
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    result = chatbot.process_message(
        user_id=data.get('user_id'),
        message=data.get('message'),
        character=data.get('character'),
        category=data.get('category')
    )
    return jsonify(result)

@app.route('/recommend_resources', methods=['POST'])
def recommend_resources():
    data = request.get_json()
    result = chatbot.recommend_resources(
        conversation_history=data.get('conversation_history'),
        category=data.get('category')
    )
    return jsonify(result)
```

## 오류 처리 및 안정성

### 1. API 오류 대응
```python
# ChatGPT API 실패 시 스마트 폴백 응답
try:
    response = self.client.chat.completions.create(...)
except Exception as e:
    return self._generate_smart_response(message, character, user_id)
```

### 2. 크롤링 실패 대응
```python
# 네이버 크롤링 실패 시 기본 검색 링크 제공
try:
    # 실제 크롤링 시도
    return crawled_resources
except:
    # 기본 네이버 검색 링크 반환
    return [{"url": f"https://search.naver.com/search.naver?where=blog&query={query}"}]
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

## 향후 개선 사항

1. **관리자 대시보드**: 카테고리별 통계, 키워드 분석 차트
2. **데이터베이스 연동**: PostgreSQL을 통한 영구 데이터 저장
3. **실시간 알림**: 고위험 사용자 자동 감지 및 알림
4. **모바일 최적화**: PWA 지원 및 모바일 앱 개발
5. **다국어 지원**: 영어, 일본어 등 추가 언어 지원