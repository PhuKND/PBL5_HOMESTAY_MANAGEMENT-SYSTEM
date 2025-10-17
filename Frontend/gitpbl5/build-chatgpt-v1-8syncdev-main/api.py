from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import requests

app = Flask(__name__)
CORS(app)

# API endpoints
TOUR_API_BASE_URL = "http://localhost:8080"

def get_rooms():
    try:
        response = requests.get(f"{TOUR_API_BASE_URL}/api/listings", headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if response.status_code == 200:
            data = response.json()
            return data.get('result', [])
        return []
    except Exception as e:
        print(f"Error fetching rooms: {e}")
        return []

def get_amenities():
    try:
        response = requests.get(f"{TOUR_API_BASE_URL}/api/amenities/getAll",
                              headers={
                                  "Content-Type": "application/json",
                                  "Accept": "application/json"
                              })
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching amenities: {e}")
        return []

def get_room_details(room_id):
    try:
        response = requests.get(f"{TOUR_API_BASE_URL}/api/listings/{room_id}",
                              headers={
                                  "Content-Type": "application/json",
                                  "Accept": "application/json"
                              })
        if response.status_code == 200:
            data = response.json()
            return data.get('result', None)
        return None
    except Exception as e:
        print(f"Error fetching room details: {e}")
        return None

# Create dynamic prompt template
def create_prompt():
    rooms = get_rooms()
    amenities = get_amenities()
    
    # Format room information
    rooms_info = ""
    if rooms:
        rooms_info = "\n".join([
            f"- {room.get('title', room.get('name', 'N/A'))} (ID: {room.get('id', 'N/A')}, Địa chỉ: {room.get('address', 'N/A')}, "
            f"Thành phố: {room.get('city', 'N/A')}, Quốc gia: {room.get('country', 'N/A')}, "
            f"Giá: {room.get('price', 'N/A')}đ/đêm, Đánh giá: {room.get('avgStart', 'N/A')}, "
            f"Link: http://localhost:5173/property/{room.get('id', 'N/A')})"
            for room in rooms
        ])
    else:
        rooms_info = "Hiện không có thông tin về phòng."
    
    # Format amenities information
    amenities_info = ""
    if amenities:
        amenities_info = "\n".join([
            f"- {amenity.get('name', 'N/A')}: {amenity.get('description', 'N/A')}"
            for amenity in amenities
        ])
    else:
        amenities_info = "Hiện không có thông tin về tiện ích."
    
    prompt_text = f"""Bạn là một trợ lý Ai chuyên nghiệp. Hãy trả lời câu hỏi của khách hàng một cách thân thiện và hữu ích.

Context: Khách sạn có các loại phòng sau:
{rooms_info}

Tiện ích khách sạn:
{amenities_info}

Câu hỏi của khách hàng: {{question}}

Hãy trả lời theo các nguyên tắc:
1. Luôn thân thiện và chuyên nghiệp
2. Cung cấp thông tin chính xác về giá và tiện ích
3. Nếu không biết câu trả lời, hãy chuyển đến bộ phận hỗ trợ
4. Đề xuất các lựa chọn phù hợp với nhu cầu của khách hàng
5. Trả lời bằng tiếng Việt

Trả lời:"""
    print("=== PROMPT GỬI VÀO AI ===")
    print(prompt_text)
    return prompt_text

# Initialize model
model = OllamaLLM(
    model="mistral",
    temperature=0.7,
    num_ctx=2048,
    num_thread=4
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message')
        history = data.get('history', [])

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Tạo lịch sử hội thoại dạng text
        history_text = ""
        for turn in history:
            if turn.get("role") == "user":
                history_text += f"User: {turn.get('content')}\n"
            elif turn.get("role") == "assistant":
                history_text += f"Bot: {turn.get('content')}\n"

        # Tạo prompt mới với lịch sử hội thoại
        template = create_prompt()
        prompt_with_history = (
            f"{template}\n"
            f"Lịch sử hội thoại:\n{history_text}\n"
            f"Câu hỏi của khách hàng: {message}\n"
            "Trả lời:"
        )

        print("=== PROMPT GỬI VÀO AI ===")
        print(prompt_with_history)

        prompt = ChatPromptTemplate.from_template(prompt_with_history)
        chain = prompt | model

        response = chain.invoke({"question": message})
        return jsonify({'message': response})

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000) 