import streamlit as st
import openai
import time

from utils import *


# Configuring the page for the app.
# 
# set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script.
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
    """Ensure that there is a conversation in the session state.
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
    """Display a message in the message box.
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
    """Displays history messages for current conversation.
    """
    messages = ensure_conversation()
    with box:
        for message in messages:
            role = message['role']
            content = message['content']
            display_message(role, content)


def ask_gpt(prompt, temperature=0.5):
    """Generates an answer using OpenAI API.

    See also:
    - https://platform.openai.com/docs/api-reference/completions/create?lang=python
    """
    # Check if api_key is empty
    if not st.session_state.get('api_key'):
        st.error('Please set your OpenAI API key in the sidebar.')
        return
    
    # Check if prompt is empty
    if not prompt:
        st.error('Please enter your question.')
        # TODO: Fix: It doesn't work
        # with error_placeholder.container():
        #     st.write('Please enter your question')
        return

    messages = ensure_conversation()
    messages.append({'role': 'user', 'content': prompt})

    # For testing only
    answer = 'I am GPT-3.5 artificial intelligence assistant.'

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
    """Ensure that there is a conversation in the session state.
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
    """Handles the click event of the generate button.
    """
    prompt = st.session_state.prompt
    temperature = st.session_state.temperature
    ask_gpt(prompt, temperature)
    # 清空输入框
    st.session_state.prompt = ''


# Your OpenAI API key here (required)
api_key = ''
init_prompt = 'Please explain quantum mechanics to a 6-year-old child.'

# Initializing the sidebar
with st.sidebar:
    st.write(f"""
        # 🚀 Get Started
        
        You can enter an instruction, then click the "Generate" button to start chatting with ChatGPT on the right 👉🏻.
        """)
    st.info('''Note: Please set your OpenAI API Key before using. 👇🏻 ''', icon='ℹ️')

    '---'

    '# Settings '
    st.text_input('**OpenAI API Key**', api_key, key='api_key',
                  help='The API key for OpenAI API. You can get it from [here](https://beta.openai.com/account/api-keys).')
    st.caption(api_key_caption)

    st.slider('**Temperature**', key='temperature', min_value=0.0,
              max_value=1.0, value=0.5, step=0.1, format="%f", help=temperature_help)
    st.caption(temperature_caption)    

    '---'

    '# Contact'
    'Github: [Gu kaitong](https://github.com/gukt) '
    'Email: gukaitong@gmail.com'

    'Source code: [Github](https//github.com/gukt/chatgpt)'

# Check if the API key is set, otherwise stop the program
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
    box.write('# Conversation messages')
    box.markdown('---')
    display_messages()

# Input field and generate button
col1, col2 = st.columns([8, 1])
with col1:
    st.text_input(
        'Prompt',
        init_prompt or '',
        key='prompt',
        placeholder='Enter your question, then click the `Generate` button',
        # on_change=handle_generate,
        label_visibility='collapsed'
    )
with col2:
    st.button(
        'Generate',
        on_click=handle_generate,
        use_container_width=True,
    )
error_placeholder = st.empty()
