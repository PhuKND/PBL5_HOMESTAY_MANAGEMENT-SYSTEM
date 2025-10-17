import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Thiết lập trang
st.set_page_config(
    page_title="Hotel Booking Assistant",
    page_icon="🏨",
    layout="wide"
)

# Tạo tiêu đề và mô tả
st.title("🏨 Hotel Booking Assistant")
st.markdown("""
Chào mừng bạn đến với hệ thống hỗ trợ đặt phòng khách sạn! Tôi có thể giúp bạn:
- 📋 Giới thiệu các loại phòng và tiện ích
- 🔍 Tìm kiếm phòng theo yêu cầu
- 💰 Tư vấn đặt phòng (giá, thời gian, vị trí)
- ❓ Trả lời câu hỏi thường gặp
- 🛠️ Hỗ trợ kỹ thuật và khiếu nại
""")

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tạo template cho câu hỏi và câu trả lời
template = """Bạn là một trợ lý đặt phòng khách sạn chuyên nghiệp. Hãy trả lời câu hỏi của khách hàng một cách thân thiện và hữu ích.

Context: Khách sạn có các loại phòng sau:
- Phòng Deluxe: 2 triệu/đêm, 35m2, giường King, view thành phố
- Phòng Suite: 3 triệu/đêm, 50m2, giường King, view biển
- Phòng Family: 4 triệu/đêm, 70m2, 2 giường Queen, view biển

Tiện ích khách sạn:
- Hồ bơi vô cực
- Phòng gym 24/7
- Nhà hàng 5 sao
- Spa & Massage
- Dịch vụ đưa đón sân bay

Câu hỏi của khách hàng: {question}

Hãy trả lời theo các nguyên tắc:
1. Luôn thân thiện và chuyên nghiệp
2. Cung cấp thông tin chính xác về giá và tiện ích
3. Nếu không biết câu trả lời, hãy chuyển đến bộ phận hỗ trợ
4. Đề xuất các lựa chọn phù hợp với nhu cầu của khách hàng
5. Trả lời bằng tiếng Việt

Trả lời:"""

# Tạo prompt template
prompt = ChatPromptTemplate.from_template(template)

# Khởi tạo model
model = OllamaLLM(
    model="mistral",
    temperature=0.7,
    num_ctx=2048,
    num_thread=4
)

# Kết hợp prompt và model
chain = prompt | model

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Tạo input cho người dùng
if question := st.chat_input("Bạn cần tôi giúp gì?"):
    # Thêm câu hỏi vào lịch sử
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Hiển thị câu hỏi
    with st.chat_message("user"):
        st.markdown(question)
    
    # Tạo câu trả lời
    with st.chat_message("assistant"):
        with st.spinner("Đang tìm thông tin..."):
            response = chain.invoke({"question": question})
            st.markdown(response)
            
            # Thêm câu trả lời vào lịch sử
            st.session_state.messages.append({"role": "assistant", "content": response})

# Thêm sidebar với thông tin bổ sung
with st.sidebar:
    st.header("📞 Liên hệ hỗ trợ")
    st.markdown("""
    - Hotline: 1900 1234
    - Email: support@hotel.com
    - Giờ làm việc: 24/7
    """)
    
    st.header("🏷️ Khuyến mãi")
    st.markdown("""
    - Giảm 20% cho đặt phòng trước 7 ngày
    - Miễn phí bữa sáng cho khách VIP
    - Gói spa 50% cho khách đặt phòng Suite
    """) 