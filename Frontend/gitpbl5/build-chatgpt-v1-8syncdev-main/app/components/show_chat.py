import solara
from solara.tasks import use_task, Task
import solara.lab as lab
from langchain_ollama.llms import OllamaLLM
from asgiref.sync import sync_to_async


manager = solara.reactive([])

@solara.component
def get_ai_chat(chain: OllamaLLM, current_mess: str):
    if not current_mess or current_mess.strip() == '':
        return lab.ChatMessage(children=[solara.Markdown(md_text='Please enter a message')], user=False)
    
    try:
        ai_mess = chain.invoke(current_mess)
        return lab.ChatMessage(children=[
            solara.Markdown(md_text=ai_mess),
        ], user=False)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return lab.ChatMessage(children=[
            solara.Markdown(md_text=error_message),
        ], user=False)

# async def async_get_ai_chat(chain: OllamaLLM, current_mess: str):
#     return await sync_to_async(get_ai_chat)(chain, current_mess)

def get_old_mess():
    old_mess = []
    for mess in manager.get():
        if mess['user']:  # Chỉ hiển thị tin nhắn người dùng không rỗng
            user_chat = lab.ChatMessage(
                children=[
                    solara.Markdown(md_text=mess['user']),
                ],
                user=True,
            )
            old_mess.append(user_chat)
            
        if mess['ai']:  # Chỉ hiển thị tin nhắn AI không rỗng
            ai_chat = lab.ChatMessage(
                children=[
                    solara.Markdown(md_text=mess['ai']),
                ],
                user=False,
            )
            old_mess.append(ai_chat)
    return old_mess

@solara.component
def show_chat(
    mess_reactive: solara.Reactive,
    config_model: dict,
    list_messages_user_reactive: solara.Reactive = None,
    list_messages_chatbox_reactive: solara.Reactive = None,
):
    chain = config_model['prompt'] | config_model['model']
    
    # Chỉ tạo task khi có tin nhắn mới
    get_ai_chat_response: Task = use_task(
        lambda: get_ai_chat(chain=chain, current_mess=mess_reactive.value),
        dependencies=[mess_reactive.value] if mess_reactive.value else []
    )

    if get_ai_chat_response.finished and mess_reactive.value:
        # Chỉ cập nhật manager khi có tin nhắn mới và response đã hoàn thành
        if not manager.get() or manager.get()[-1]['user'] != mess_reactive.value:
            try:
                ai_response = chain.invoke(mess_reactive.value)
                manager.set(manager.get() + [{
                    'user': mess_reactive.value,
                    'ai': ai_response,
                }])
            except Exception as e:
                manager.set(manager.get() + [{
                    'user': mess_reactive.value,
                    'ai': f"Error: {str(e)}",
                }])
        
        old_mess = get_old_mess()
        return lab.ChatBox(children=[
            *old_mess,
            get_ai_chat_response.result.value,
        ])
    else:
        old_mess = get_old_mess()
        return lab.ChatBox(children=[
            *old_mess,
            lab.ChatMessage(children=[mess_reactive.value], user=True) if mess_reactive.value else None,
            solara.ProgressLinear(value=get_ai_chat_response.progress) if not get_ai_chat_response.finished else None,
        ])


            
        

        


