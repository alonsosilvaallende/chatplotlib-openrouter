import openai
import streamlit as st
from streamlit_chat import message
from components.Sidebar import sidebar
import json
from shared import constants

api_key, selected_model = sidebar(constants.OPENROUTER_DEFAULT_CHAT_MODEL)

st.sidebar.title("Chatplotlib")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    openai.api_key = api_key
    openai.api_base = constants.OPENROUTER_API_BASE
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=selected_model,
            headers={"HTTP-Referer": constants.OPENROUTER_REFERRER},
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=0,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
