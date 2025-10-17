import solara
import solara.lab as lab

from app.components import (
    show_chat,
)

from langchain_core.prompts import ChatPromptTemplate 
from langchain_ollama.llms import OllamaLLM

template = """Question: {question} 
 
Answer: Let's think step by step."""

promt = ChatPromptTemplate.from_template(template)

# Sử dụng model phiên bản nhỏ hơn và phổ biến hơn
model = OllamaLLM(
    model='mistral',
    temperature=0.7,
    num_ctx=2048,
    num_thread=4
)

message = solara.reactive('')
list_messages_user = solara.reactive([])
list_messages_chatbox = solara.reactive([])

def send_message(mess: str):
    if mess.strip():  # Chỉ xử lý tin nhắn không rỗng
        message.set(mess)
        list_messages_user.set(list_messages_user.get() + [mess])

@solara.component
def home_page():
    with solara.Div(
        style={
            'height': '100vh',
            'padding': '20px',
            'max-width': '1200px',
            'margin': '0 auto',
        }
    ) as container:
        solara.Text('Build Chatbot Ollama Model With 8 Sync Dev', 
                   style={'font-size': '2rem', 'margin-bottom': '20px', 'text-align': 'center'})
        
        with solara.Div(
            style={
                'height': '60%',
                'border': '1px solid #ccc',
                'border-radius': '8px',
                'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                'overflow-y': 'auto',
                'padding': '20px',
                'margin-bottom': '20px',
                'background-color': '#f9f9f9',
            }
        ) as showchat:
            show_chat(
                mess_reactive=message,
                config_model={
                    'model': model,
                    'prompt': promt,
                },
            )
            
        with solara.Div(
            style={
                'padding': '10px',
                'background-color': '#fff',
                'border-radius': '8px',
                'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
            }
        ) as chat_box:
            lab.ChatInput(send_callback=send_message)