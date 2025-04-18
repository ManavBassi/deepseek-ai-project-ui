import streamlit as st
import requests
import json

# --- Streamlit Page Setup ---45
st.set_page_config(page_title="DeepSeek Chatbot", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'> DeepSeek R1 Chatbot</h1>", unsafe_allow_html=True)

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    host = st.text_input("Ollama API Host", "http://localhost:11434")
    model = st.text_input("Model Name", "deepseek-r1:14b")
    st.markdown("Make sure your Ollama server is running.")

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# --- User Input ---
prompt = st.chat_input("Type your message here...")

# --- Handle User Input ---
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)

    # Add assistant message placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Send request to Ollama
            response = requests.post(
                f"{host}/api/chat",
                json={
                    "model": model,
                    "messages": st.session_state.messages,
                },
                stream=True,
            )

            # Stream and display response
            for chunk in response.iter_lines():
                if chunk:
                    data = chunk.decode("utf-8")
                    if data.startswith("data: "):
                        data = data[6:]
                    token = json.loads(data).get("message", {}).get("content", "")
                    full_response += token
                    message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

        except Exception as e:
            error_msg = f"❌ Error connecting to Ollama server at `{host}`.\n\n**Details:** {str(e)}"
            message_placeholder.markdown(error_msg)
            st.stop()

        message_placeholder.markdown(full_response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
