import streamlit as st
import requests


with st.sidebar:
    st.title("Test UI")

    st.divider()

    api = st.text_input(
        label="API URL"
    )
    apiKey = st.text_input(
        label="API Key",
        type="password"
    )

    st.text_input(
        label="Conversation ID",
        value=st.session_state['conversation_id'] if 'conversation_id' in st.session_state else "",
        disabled=True
    )

    st.divider()
    if st.button('RESET', use_container_width=True, type="primary"):
        if 'conversation_id' in st.session_state:
            del st.session_state["conversation_id"]
        st.session_state['messages'] = []
        st.rerun()

input = st.chat_input()

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.write(message['text'])

if input:
    st.session_state['messages'].append({
        "role": "user",
        "text": input,
    })
    with st.chat_message('user'):
        st.write(input)
    try:
        with st.spinner("loading"):
            request_body = {
                "text": input
            }

            if 'conversation_id' in st.session_state:
                request_body['conversationId'] = st.session_state['conversation_id']

            response = requests.post(api, json=request_body, headers={
                "x-api-key": apiKey,
                "Content-Type": "application/json"
            })
            response.raise_for_status()
            body = response.json()
            print(f"body: {body['text']}")
            st.session_state['messages'].append({
                "role": "ai",
                "text": body['text'],
            })
            st.session_state['conversation_id'] = body['conversationId']
            with st.chat_message('ai'):
                st.write(body['text'])
    except requests.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
