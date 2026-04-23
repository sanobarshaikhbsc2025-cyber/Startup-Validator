import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Startup Battle-Bot", page_icon="🚀", layout="wide")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY is missing in Streamlit Secrets.")
    st.stop()

client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"],
    http_options=types.HttpOptions(api_version="v1")
)

SYSTEM_PROMPT = """
You are a brilliant Venture Capitalist. Your goal is to help users build their startup.
1. Be sharp and professional.
2. Ask one question at a time to improve their idea.
3. If the user asks for Competitors, Branding, or a Pitch, be very detailed.
"""

def get_reply(user_text):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    return response.text

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🚀 Startup Battle-Bot")
st.caption("The AI that builds your business while it roasts it.")

with st.sidebar:
    st.header("🛠️ Startup Tool-Kit")
    st.write("Use these after chatting with the AI")

    if st.button("🔍 Find My Rivals"):
        with st.spinner("Analyzing market..."):
            text = get_reply(
                "Identify 3 potential real-world competitors for this business idea and explain their strengths and weaknesses."
            )
            st.subheader("Competitor Analysis")
            st.info(text)

    if st.button("🎨 Design My Brand"):
        with st.spinner("Creating brand board..."):
            text = get_reply(
                "Suggest a professional Brand Name, a Color Palette with hex codes, a logo concept, and a catchy tagline for this startup."
            )
            st.subheader("Brand Identity")
            st.success(text)

    if st.button("📊 Export Pitch Deck"):
        with st.spinner("Synthesizing data..."):
            text = get_reply(
                "Convert our entire chat into a 5-point investor pitch deck: 1. Problem, 2. Solution, 3. Market Size, 4. Revenue Model, 5. The Ask. Format as markdown."
            )
            st.subheader("Final Pitch Deck")
            st.warning(text)

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
            answer = get_reply(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
