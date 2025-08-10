import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트 경로를 Python 경로에 추가
project_root = Path(__file__).parent
app_path = project_root / "app"
sys.path.insert(0, str(app_path))

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from flask import Flask, render_template, request, jsonify
from chatbot import CounselingChatbot

app = Flask(__name__, 
           template_folder=str(app_path / "templates"),
           static_folder=str(project_root / "static"))

# 챗봇 초기화
chatbot = CounselingChatbot(os.environ['OPENAI_API_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/chat_topics')
def chat_topics():
    return render_template('chat_topics.html')

@app.route('/chat_interface')
def chat_interface():
    return render_template('chat_interface.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')

@app.route('/chat', methods=['POST'])
def chat():
    # 챗봇 대화 처리
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        message = data.get('message', '')
        character = data.get('character', '멜랑콜리')
        category = data.get('category', 'personal')
        
        if not message:
            return jsonify({'error': '메시지가 비어있습니다.'}), 400
        
        # 챗봇 처리
        result = chatbot.process_message(user_id, message, character, category)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'오류발생 : {str(e)}'}), 500

@app.route('/recommend_resources', methods=['POST'])
def recommend_resources():
    # 대화 내용을 바탕으로 리소스 추천
    try:
        data = request.get_json()
        conversation_history = data.get('conversation_history', [])
        category = data.get('category', 'personal')
        
        # 리소스 추천
        result = chatbot.recommend_resources(conversation_history, category)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'리소스 추천 중 오류 발생: {str(e)}'}), 500

@app.route('/dashboard/<user_id>')
def user_dashboard(user_id):
    #  대시보드
    dashboard_data = chatbot.get_user_dashboard_data(user_id)
    return render_template('dashboard.html', data=dashboard_data, user_id=user_id)

@app.route('/api/dashboard/<user_id>')
def api_user_dashboard(user_id):
    # 개인 대시보드 API
    dashboard_data = chatbot.get_user_dashboard_data(user_id)
    return jsonify(dashboard_data)

@app.route('/admin/dashboard')
def admin_dashboard():
    # 관리자 대시보드
    admin_data = chatbot.get_admin_dashboard_data()
    return render_template('admin_dashboard.html', data=admin_data)

@app.route('/api/admin/dashboard')
def api_admin_dashboard():
    admin_data = chatbot.get_admin_dashboard_data()
    return jsonify(admin_data)

if __name__ == '__main__':
    print("AI 상담 챗봇 서버를 시작...")
    print("http://localhost:5000")
    print("개인 대시보드: http://localhost:5000/dashboard/default_user")
    print("관리자 대시보드: http://localhost:5000/admin/dashboard")
    print("KB HUG 홈: http://localhost:5000/home")
    print("기록 보기: http://localhost:5000/records")
    print("대화하기: http://localhost:5000/chat_topics")
    print("채팅 인터페이스: http://localhost:5000/chat_interface")
    print("리소스: http://localhost:5000/resources")
    print("푸터: http://localhost:5000/footer")
    app.run(debug=True, host='0.0.0.0', port=5000) 