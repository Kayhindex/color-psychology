import streamlit as st
import time
from helper import get_gemini_chat_session, ask_gemini, render_sidebar

# --- Page Config ---
st.set_page_config(page_title="🎨 HueBot - Color Psychology Chatbot", layout="wide")
render_sidebar()

# --- Initialize Session State ---
defaults = {
    "chat_session": get_gemini_chat_session(),
    "chat_history": [],
    "is_generating": False,
    "stop_generation": False,
    "clear_input": False,
    "interrupted": False,
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

# --- Custom CSS ---
st.markdown("""
<style>
.stApp, .reportview-container {
    background-color: #f9fafb !important;  /* Light neutral background */
  }
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #0b111e;
    color: #ffffff !important;
}
footer { visibility: hidden; height: 0; }
.chat-container {
    padding: 2rem;
    padding-bottom: 10rem;
    max-height: 70vh;
    overflow-y: auto;
}
.message {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 10px;
    max-width: 80%;
}
.user {
   background-color:#e0e7ff;
color: #0f172a;
    margin-left: auto;
    text-align: right;
}
.bot {
        # background: linear-gradient(135deg, #4f46e5, #5a52e9);
    background:#4f46e5;
    color: #ffffff;
    margin-right: auto;
}
.input-area {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #0b111e;
    padding: 1rem 2rem 2rem 2rem;
    border-top: 1px solid #00f7ff33;
    z-index: -1000 !important;
}
textarea {
    background-color: #1a2537;
    color: #ffffff;
    border: 1px solid #1a2537;
    border-radius: 8px;
    padding: 0.75rem;
    width: 100%;
    resize: none;
}
.ask-btn {
    background-color: #00f7ff;
    color: #0b111e;
    border: none;
    border-radius: 6px;
    padding: 0.7rem 1.2rem;
    font-weight: bold;
}
.ask-btn:hover {
    background-color: #5efbfb;
}
.blink {
    animation: blink 1s infinite;
    font-weight: bold;
}
@keyframes blink { 50% { opacity: 0; } }
.interrupt-box {
    color: white;
    font-weight: bold;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-top: 1rem;
    max-width: 80%;
}
@media screen and (max-width: 768px) {
    .chat-container { max-height: 60vh; padding: 1rem; }
    .input-area { padding: 0.5rem 1rem; }
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    '<div style="text-align:center; font-size:2.5rem; color:#a78bfa; font-weight:700; padding:1rem;">🎨 HueBot - Color Psychology Chatbot</div>',
    unsafe_allow_html=True
)

# --- Chat History ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    st.markdown(f'<div class="message user">{chat["question"]}</div>', unsafe_allow_html=True)
    if chat["answer"].strip():
        st.markdown(f'<div class="message bot">{chat["answer"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Typing Placeholder ---
typing_placeholder = st.empty()

# --- Input Area ---
st.markdown('<div class="input-area">', unsafe_allow_html=True)
chat_input_default = "" if st.session_state.clear_input else st.session_state.get("chat_input", "")
with st.form("chat_form", clear_on_submit=False):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Type your message...",
            height=100,
            label_visibility="collapsed",
            key="chat_input",
            value=chat_input_default,
            placeholder="Ask about color psychology..."
        )
    with col2:
        button_label = "⏹️ Stop" if st.session_state.is_generating else "Ask"
        button_clicked = st.form_submit_button(button_label, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Button Logic ---
if button_clicked:
    if st.session_state.is_generating:
        st.session_state.stop_generation = True
        st.session_state.interrupted = True
        st.session_state.is_generating = False
        if st.session_state.chat_history:
            st.session_state.chat_history[-1]["answer"] = (
                '<div class="interrupt-box">🤖 HueBot was stopped — let’s try another question!</div>'
            )
        st.rerun()
    elif user_input.strip():
        st.session_state.chat_history.append({"question": user_input.strip(), "answer": ""})
        st.session_state.clear_input = True
        st.session_state.is_generating = True
        st.session_state.interrupted = False
        st.rerun()

# --- Generate Response ---
if (
    st.session_state.chat_history and
    st.session_state.chat_history[-1]["answer"] == "" and
    st.session_state.is_generating
):
    question = st.session_state.chat_history[-1]["question"]
    full_response = ""
    st.session_state.stop_generation = False

    with st.spinner("🎨 HueBot is thinking..."):
        typing_placeholder.markdown('<div class="message bot"><i>🎨 HueBot is typing...</i></div>', unsafe_allow_html=True)
        response = ask_gemini(question, st.session_state.chat_session)

        for char in response:
            if st.session_state.stop_generation:
                st.session_state.interrupted = True
                break
            full_response += char
            typing_placeholder.markdown(
                f'<div class="message bot">{full_response}<span class="blink">▌</span></div>',
                unsafe_allow_html=True
            )
            time.sleep(0.015)

    # Final message output
    if st.session_state.interrupted:
        msg = '<div class="interrupt-box">✋ You stopped HueBot’s response. Please rephrase or ask something else!</div>'
    else:
        msg = full_response

    typing_placeholder.markdown(f'<div class="message bot">{msg}</div>', unsafe_allow_html=True)
    st.session_state.chat_history[-1]["answer"] = msg
    st.session_state.clear_input = False
    st.session_state.is_generating = False
    st.rerun()
