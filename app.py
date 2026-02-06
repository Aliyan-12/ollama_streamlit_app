import streamlit as st
import requests
# from ollama import chat, ChatResponse

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "phi3"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Ollama Chat UI", layout="wide")
st.title("💬 Local LLM Chat (Ollama)")

st.sidebar.header("Conversation History")
if st.session_state.messages:
    for msg in st.session_state.messages:
        speaker = "🧑 You" if msg["role"] == "user" else "🤖 AI"
        st.sidebar.markdown(f"**{speaker}:** {msg['content']}")
else:
    st.sidebar.write("No conversation yet.")

if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.messages = []
    st.rerun()

st.write("### Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 AI:** {msg['content']}")

# st.write("### Ask something to your locally running LLM:")
user_input = st.text_input("Ask Anything", "", key="user_input")

def query_ollama(messages):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json().get("message")

if st.button("Send") and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        ai_response = query_ollama(st.session_state.messages)
        print(ai_response['content'])
        st.session_state.messages.append({"role": "assistant", "content": ai_response['content']})
        # user_input = ""

    except Exception as e:
        st.error(f"Error communicating with Ollama: {e}")

    st.rerun()
