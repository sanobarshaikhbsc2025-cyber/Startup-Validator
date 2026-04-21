import streamlit as st
import google.generativeai as genai
import json

# 1. Configuration
st.set_page_config(page_title="Startup Battle-Bot", page_icon="📈", layout="wide")
genai.configure(api_key="AIzaSyCyAKlibuvXiMfvuCF82LofbY4GV1DWGso")

# 2. The "Winner" System Prompt
SYSTEM_PROMPT = """
You are a brutal but brilliant Venture Capitalist from Shark Tank. 
Your goal is to interview the user about their startup idea.
1. Be skeptical and witty.
2. Ask one sharp question at a time to dig deeper.
3. If the user asks for a 'Final Verdict', provide a JSON report.
"""

# 3. Initialize Session State (This gives the AI "Memory")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat_session = model.start_chat(history=[])

# 4. UI Design
st.title("📈 Startup Battle-Bot")
st.markdown("---")

# Sidebar for the "Final Report"
with st.sidebar:
    st.header("Project Controls")
    if st.button("Generate Final Scorecard"):
        # Low temperature for the serious report
        res = st.session_state.chat_session.send_message("Summarize our talk into a JSON: Market_Fit (0-100), Risk_Level, and Final_Verdict.")
        try:
            clean_json = res.text.replace("```json", "").replace("```", "").strip()
            stats = json.loads(clean_json)
            st.metric("Market Fit", f"{stats['Market_Fit']}%")
            st.warning(f"Risk: {stats['Risk_Level']}")
            st.success(f"Verdict: {stats['Verdict']}")
        except:
            st.write("Keep chatting to build more data first!")

# 5. The Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Explain your idea to the Shark..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})