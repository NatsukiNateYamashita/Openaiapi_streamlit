from langchain.chat_models import ChatOpenAI
from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)

import streamlit as st
from streamlit_chat import message

# loading the OpenAI api key from .env (OPENAI_API_KEY="sk-********")
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title='日本語教師用日本語添削君',
    page_icon='🤖'
)
st.subheader('日本語教師用日本語添削君 🤖')

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

default_system_message = '''
中国語母語話者の誤った日本語を添削してください。

まず、文法と語法における誤りを指摘、誤りの理由を説明、正しい答えを教えてください。誤りがない場合には、”文法語法に誤りはありません”と回答してください。

次に、語用的における不自然さを指摘、不自然な理由を説明、より良い表現を教えてください。不自然さがない場合には、"語用に不自然さはありません"と回答してください。

最後に、上記の正しい答え、より良い表現を踏まえて、回答を提示してください。
'''

# creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.insert(0, SystemMessage(content=default_system_message))

# creating the sidebar
with st.sidebar:
    # text_input for the OpenAI API key (alternative to python-dotenv and .env)
    api_key = st.text_input('OpenAI API Key:', type='password')
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role', placeholder='please input your custom instruction')
    # streamlit text input widget for the user message
    # user_prompt = st.text_input(label='send sentences')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
                )
    st.write(st.session_state.messages)
    # if the user entered a question
    # if user_prompt:
    #     st.session_state.messages.append(
    #         HumanMessage(content=user_prompt)
    #     )

        # with st.spinner('Working on your request ...'):
        #     # creating the ChatGPT response
        #     response = chat(st.session_state.messages)

        # adding the response's content to the session state
        # st.session_state.messages.append(AIMessage(content=response.content))

# st.session_state.messages
message('Please send the sentences that you would like to correct', is_user=False)
# message('this is the user', is_user=True)


user_msg = st.chat_input('Input sentences that you would like to correct')
if user_msg:
    st.session_state.messages.append(
        HumanMessage(content=user_msg)
    )

    with st.spinner('Working on your request ...'):
        # creating the ChatGPT response
        response = chat(st.session_state.messages)


    # adding the response's content to the session state
    st.session_state.messages.append(AIMessage(content=response.content))

# adding a default SystemMessage if the user didn't entered one
# if len(st.session_state.messages) >= 1:
#     if not isinstance(st.session_state.messages[0], SystemMessage):
        # st.session_state.messages.insert(0, SystemMessage(content=default_system_message))

# displaying the messages (chat history)
for i, msg in enumerate(st.session_state.messages[1:]):
    if i % 2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 🤓') # user's question
    else:
        message(msg.content, is_user=False, key=f'{i} +  🤖') # ChatGPT response

# run the app: streamlit run ./project_streamlit_custom_chatgpt.py