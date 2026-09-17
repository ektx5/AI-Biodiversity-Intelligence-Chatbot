import streamlit as st
import json
import os
from dotenv import load_dotenv
from src.chatbot import EnvironmentScientistBot

load_dotenv()

st.set_page_config(page_title='AI Biodiversity Intelligence', layout='wide')
st.title('Darukaa.Earth: AI Environmental Scientist')

if not os.getenv('GEMINI_API_KEY'):
    st.error('GEMINI_API_KEY is missing. Add it to a .env file in the project root and restart Streamlit.')
    st.stop()

if 'messages' not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def get_bot():
    return EnvironmentScientistBot()

bot = get_bot()

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

with st.sidebar:
    st.header('Structured Input (Optional)')
    st.write('You can provide variables in JSON format.')
    json_input = st.text_area('JSON Input', value='{\n  "Soil organic carbon": "0.3%",\n  "Rainfall": "low",\n  "Crop": "monoculture wheat"\n}')
    if st.button('Submit JSON'):
        try:
            variables = json.loads(json_input)
        except json.JSONDecodeError as error:
            st.error(f'Invalid JSON: {error.msg}')
            variables = None

        if not isinstance(variables, dict):
            if variables is not None:
                st.error('Structured input must be a JSON object of environmental variables.')
        else:
            normalized_json = json.dumps(variables, indent=2)
            user_message = f'Variables provided via JSON:\n{normalized_json}'
            st.session_state.messages.append({'role': 'user', 'content': user_message})
            with st.chat_message('user'):
                st.markdown(f'Variables provided via JSON:\n```json\n{normalized_json}\n```')
            with st.chat_message('assistant'):
                response = bot.generate_response(user_message, st.session_state.messages[:-1])
                st.markdown(response)
            st.session_state.messages.append({'role': 'assistant', 'content': response})

if prompt := st.chat_input('Describe the environmental situation on your land...'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    
    with st.chat_message('assistant'):
        response = bot.generate_response(prompt, st.session_state.messages[:-1])
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
