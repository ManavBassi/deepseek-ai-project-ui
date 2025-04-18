import streamlit as st
import requests
import json
# Set the page title and layout
st.set_page_config(page_title="Deepseek chatbot",layout="wide")
# Display the main title at the top of the web app
st.title("DEEPSEEK CHATBOT")

# Text input for the Ollama server host address (default is local machine)
with st.sidebar:
    host=st.sidebar.text_input("Ollama API HOST","http://localhost:11434")

# Loop through each message in the chat history and display it
if "messages" not in st.session_state:
    st.session_state.messages = []
# Loop through each message in the chat history and display it
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder=st.empty()
        full_response=""

# Send a POST request to Ollama's /api/chat endpoint
        try:
            # Send request to local Ollama server
            response = requests.post(
                f"{host}/api/chat",
                json={
                    "model":"deepseek-r1:14b",
                    "messages": st.session_state.messages,
                },
                stream=True,
            )

            # Stream response from Ollama
            for chunk in response.iter_lines():
                if chunk:
                    data = chunk.decode("utf-8")
                    if data.startswith("data: "):
                        data = data[6:]
                    token = json.loads(data).get("message", {}).get("content", "")
                    full_response += token
                    message_placeholder.markdown(full_response + "▌")

        except Exception as e:
            message_placeholder.markdown("Error connecting to Ollama.")
            st.error(str(e))
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})