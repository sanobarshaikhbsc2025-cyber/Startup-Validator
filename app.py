import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Startup Battle-Bot", page_icon="🚀", layout="wide")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY is missing in Streamlit Secrets.")
    st.stop()

SYSTEM_PROMPT = """
You are a brilliant Venture Capitalist. Your goal is to help users build their startup.
1. Be sharp and professional.
2. Ask one question at a time to improve their idea.
3. If the user asks for Competitors, Branding, or a Pitch, be very detailed.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"],
    http_options=types.HttpOptions(api_version="v1")
)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
)

st.title("🚀 Startup Battle-Bot")
st.caption("The AI that builds your business while it roasts it.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Explain your soap business or cat cafe...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
