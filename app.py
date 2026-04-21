import streamlit as st
import google.generativeai as genai
import json

# 1. Configuration
st.set_page_config(page_title="Startup Battle-Bot", page_icon="🚀", layout="wide")

# IMPORTANT: Get key from Streamlit Secrets or paste it here
api_key = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)

# 2. The Winner System Prompt
SYSTEM_PROMPT = """
You are a brilliant Venture Capitalist. Your goal is to help users build their startup.
1. Be sharp and professional.
2. Ask one question at a time to improve their idea.
3. If the user asks for Competitors, Branding, or a Pitch, be very detailed.
"""

# 3. Initialize Session State (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(model_name="gemini-pro", system_instruction=SYSTEM_PROMPT)
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Sidebar: The "Pro" Tools
with st.sidebar:
    st.header("🛠️ Startup Tool-Kit")
    st.write("Use these after chatting with the AI")
    
    # Feature 1: Competitor Research
    if st.button("🔍 Find My Rivals"):
        with st.spinner("Analyzing market..."):
            res = st.session_state.chat_session.send_message("Identify 3 potential real-world competitors for this business idea and explain their strength.")
            st.subheader("Competitor Analysis")
            st.info(res.text)

    # Feature 2: Brand Identity
    if st.button("🎨 Design My Brand"):
        with st.spinner("Creating brand board..."):
            res = st.session_state.chat_session.send_message("Suggest a professional Brand Name, a Color Palette (with Hex codes), and a catchy Tagline for this startup.")
            st.subheader("Brand Identity")
            st.success(res.text)

    # Feature 3: Pitch Deck Exporter
    if st.button("📊 Export Pitch Deck"):
        with st.spinner("Synthesizing data..."):
            res = st.session_state.chat_session.send_message("Convert our entire chat into a 5-point Investor Pitch Deck: 1. Problem, 2. Solution, 3. Market Size, 4. Revenue Model, 5. The Ask.")
            st.subheader("Final Pitch Deck")
            st.warning(res.text)

# 5. Main Chat Interface
st.title("🚀 Startup Battle-Bot")
st.caption("The AI that builds your business while it roasts it.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Explain your soap business or cat cafe..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
