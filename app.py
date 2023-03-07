import streamlit as st
import openai
import time

from utils import *


# Page configuration
# NOTE: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script.
st.set_page_config(
    page_title='A demo of ChatGPT',
    page_icon='🦖',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://github.com/gukt/streamlit-chatgpt',
        'Report a bug': "https://github.com/gukt/streamlit-chatgpt/issues",
        'About': about
    }
)


def ensure_conversation() -> None:
    """确保会话状态中有 conversation 字段
    """
    if 'conversation' not in st.session_state:
        # https://platform.openai.com/docs/guides/chat/introduction
        st.session_state.conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
        ]

    return st.session_state.conversation


def display_message(role: str, content: str):
    """输出指定角色的聊天消息
    """
    # We don't want to display the system messages
    if role == 'system':
        return

    # Display the message in the message box
    col1, col2 = st.columns([1, 15])
    with col1:
        st.markdown('You' if role == 'user' else icons['openai'],
                    unsafe_allow_html=True)
    with col2:
        st.write(content)
        # st.info(content, icon="ℹ️")
    st.markdown('---')


def display_messages():
    """输出对话历史消息
    """
    messages = ensure_conversation()
    with box:
        for message in messages:
            role = message['role']
            content = message['content']
            display_message(role, content)


def ask_gpt(prompt, temperature=0.5):
    """调用 OpenAI API 生成回答

    See also:
    - https://platform.openai.com/docs/api-reference/completions/create?lang=python
    """
    # Check if prompt is empty
    if not prompt:
        with input_error.container():
            st.write('请输入您的问题')
        return

    messages = ensure_conversation()
    messages.append({'role': 'user', 'content': prompt})

    # For testing only
    # answer = '我是 GPT-3.5 人工智能助手。'

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        # max_tokens=4096,
        stop=None,
        temperature=temperature,
    )
    answer = response.choices[0].message.content

    # 如果得到了回复，保存此次会话上下文记录
    if answer:
        messages.append({'role': 'assistant', 'content': answer})
        # display_message('assistant', answer)


def ensure_conversation():
    """
    确保会话状态中有 conversation 字段
    """
    if 'conversation' not in st.session_state:
        # https://platform.openai.com/docs/guides/chat/introduction
        st.session_state.conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
        ]

    return st.session_state.conversation


def handle_generate():
    """处理生成按钮点击事件
    """
    # time.sleep(3)
    # 将 st.session_state 中的 prompt, temperature 字段赋值给同名变量
    prompt = st.session_state.prompt
    temperature = st.session_state.temperature
    ask_gpt(prompt, temperature)
    # 清空输入框
    st.session_state.prompt = ''


# Your OpenAI API key here (required)
api_key = '<Your OpenAI API key here>'
init_prompt = '请用中文给 6 周岁小孩解释一下什么是量子力学。'

# Initializing the sidebar
with st.sidebar:
    st.write(f"""
        # 🚀 开始吧！
        
        请在右边的输入框中输入一条指令或选择一个预设，然后点击“生成”按钮，就可以愉快地和 ChatGPT 进行交谈了。
        """)

    st.info('''**注意：** 使用之前，请先设置好您的 OpenAI API Key。👇🏻 ''', icon='ℹ️')

    '---'

    # st.markdown('## :gear: 设置')
    '# 设置 '

    st.text_input('**OpenAI API Key**', api_key, key='api_key',
                  help='在开始之前，请先设置好您的 OpenAI API Key。否则程序不会执行。')
    st.caption("""
        👉🏻 如果你还没有注册 OpenAI 账户，点击这里 [注册 OpenAI](https://platform.openai.com/) ；如果你已经有了账户，请点击 [这里](https://platform.openai.com/account/api-keys) 获取 API Key。
        """)

    st.slider('**温度**', key='temperature', min_value=0.0,
              max_value=1.0, value=0.5, step=0.1, format="%f", help='用来调整 ChatGPT 生成的回复的多样性。')
    st.caption('''
            🔥 温度用来调整 ChatGPT 生成的回复的多样性，数值越大多样性越丰富 :sparkles:。详见 [OpenAI API](https://platform.openai.com/docs/introduction) 文档： [调整你的设置](https://platform.openai.com/docs/quickstart/adjust-your-settings)
            ''')

    '---'

    '# 联系我'
    'Github: [Gu kaitong](https://github.com/gukt) '
    'Email: gukaitong@gmail.com'

    'Source code: [Github](https//github.com/gukt/chatgpt)'
    # TODO 输出一个使用 icons['github'] 图标的链接，连接地址是 https//github.com/gukt/streamlit-chatgpt
    # github_icon = icons['github']
    # '[![]()](https://github.com/gukt/streamlit-chatgpt)'

# 检查是否设置了 API Key，如果程序停止
if 'api_key' not in st.session_state:
    st.error('Please set your OpenAPI key in the sidebar.')
    st.stop()

# Set the api key for OpenAI API
openai.api_key = st.session_state.get('api_key')

# =================================================
# Initializing the main page
# =================================================

box = st.container()

messages = ensure_conversation()
# messages

if len(messages) > 1:
    box.write('# 对话历史')
    box.markdown('---')
    display_messages()

# 显示 prompt 输入框和生成按钮
col1, col2 = st.columns([9, 1])
with col1:
    st.text_input(
        'Prompt',
        init_prompt or '',
        key='prompt',
        placeholder='输入您的问题，然后点击`生成`按钮',
        # on_change=handle_generate,
        label_visibility='collapsed'
    )
with col2:
    st.button(
        '生成',
        on_click=handle_generate,
        use_container_width=True,
    )
input_error = st.empty()
