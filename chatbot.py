import streamlit as st
import time
from helper import get_gemini_chat_session, ask_gemini, render_sidebar

# Page config
st.set_page_config(page_title="🎨 HueBot - Color Psychology Chatbot", layout="wide")
render_sidebar()

# --- Session State Init ---
def init_session_state():
    defaults = {
        "chat_session": get_gemini_chat_session(),
        "chat_history": [],
        "is_generating": False,
        "stop_generation": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# --- Custom CSS ---
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #0b111e;
    color: #e2e8f0;
}

/* Hide Streamlit default header and footer */
header, footer {
    visibility: hidden;
    height: 0;
    margin: 0;
    padding: 0;
    overflow: hidden;
    border: none !important;
}

/* Remove any border/shadow on main container */
.css-18e3th9 {
    border: none !important;
    box-shadow: none !important;
}

.header {
    text-align: center;
    font-size: 1.8rem;
    padding: 1.2rem;
    color: #00f7ff;
    font-weight: bold;
    border-bottom: 1px solid #00f7ff44;
}
.chat-container {
    padding: 2rem;
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
    background-color: #00f7ff;
    color: #0b111e;
    margin-left: auto;
    text-align: right;
}
.bot {
    background-color: #172033;
    color: #e2e8f0;
    margin-right: auto;
}
.input-area {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #0b111e;
    padding: 1rem 2rem;
    border-top: 1px solid #00f7ff33;
    box-shadow: none !important;  /* Remove shadow if any */
}
textarea {
    background-color: #1a2537;
    color: #e2e8f0;
    border: 1px solid #1a2537;
    border-radius: 8px;
    padding: 0.75rem;
    resize: none;
    width: 100%;
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
@keyframes blink {
    50% { opacity: 0; }
}

/* Responsive */
@media screen and (max-width: 768px) {
    .chat-container {
        max-height: 60vh;
        padding: 1rem;
    }
    .input-area {
        padding: 0.5rem 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header">🎨 HueBot - Color Psychology Chatbot</div>', unsafe_allow_html=True)

# --- Chat Display ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, chat in enumerate(st.session_state.chat_history):
    st.markdown(f'<div class="message user"><b>You:</b><br>{chat["question"]}</div>', unsafe_allow_html=True)

    if chat["answer"] == "..." and i == len(st.session_state.chat_history) - 1:
        placeholder = st.empty()
        response = ask_gemini(chat["question"], st.session_state.chat_session)

        full_response = ""
        st.session_state.is_generating = True
        st.session_state.stop_generation = False

        for char in response:
            if st.session_state.stop_generation:
                full_response += " ❌ *Response stopped by user.*"
                break
            full_response += char
            placeholder.markdown(
                f'<div class="message bot"><b>HueBot:</b><br>{full_response}<span class="blink">▌</span></div>', 
                unsafe_allow_html=True)
            time.sleep(0.015)

        placeholder.markdown(
            f'<div class="message bot"><b>HueBot:</b><br>{full_response}</div>', 
            unsafe_allow_html=True)
        st.session_state.chat_history[i]["answer"] = full_response
        st.session_state.is_generating = False
    else:
        st.markdown(f'<div class="message bot"><b>HueBot:</b><br>{chat["answer"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Input Section ---
st.markdown('<div class="input-area">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=not st.session_state.is_generating):
    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_area(
            "Type your message...", 
            height=100, 
            label_visibility="collapsed", 
            key="chat_input", 
            placeholder="Ask about color psychology..."
        )

    with col2:
        button_label = "⏹️ Stop" if st.session_state.is_generating else "Ask"
        button_clicked = st.form_submit_button(button_label, use_container_width=True)

    if button_clicked:
        if st.session_state.is_generating:
            st.session_state.stop_generation = True
        elif user_input.strip():
            st.session_state.chat_history.append({"question": user_input.strip(), "answer": "..."})
            st.stop()

st.markdown('</div>', unsafe_allow_html=True)
