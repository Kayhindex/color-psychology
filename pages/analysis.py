import streamlit as st
from helper import extract_dominant_colors, get_gemini_chat_session, ask_gemini, render_sidebar

# -------------------------------
# Page Config & Sidebar
# -------------------------------
st.set_page_config(page_title="🎨 UI Color Psychology Analyzer", layout="wide")
render_sidebar()

# -------------------------------
# Global CSS Styling + Mobile
# -------------------------------
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            background-color: #0f172a;
            color: #e2e8f0;
        }

        .title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: #a78bfa;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
            color: #cbd5e1;
        }

        .color-card {
            background-color: #1e293b;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #334155;
            transition: transform 0.2s ease;
            margin-bottom: 1rem;
        }

        .color-card:hover {
            transform: scale(1.03);
        }

        .huebot-response {
            background-color: #e0e7ff;
            # border-left: 4px solid #a78bfa;
            padding: 1.2rem;
            margin-top: 1.5rem;
            border-radius: 10px;
            line-height: 1.65;
            font-size: 1.05rem;
        }

        .analyze-btn {
            background-color: #a78bfa;
            color: #0f172a;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6rem 1.4rem;
            font-size: 1rem;
            border: none;
            margin-top: 1rem;
        }

        .analyze-btn:hover {
            background-color: #c084fc;
            cursor: pointer;
        }

        /* 📱 Mobile Responsive Adjustments */
        @media screen and (max-width: 768px) {
            .title {
                font-size: 2rem;
            }
            .subtitle {
                font-size: 0.95rem;
                margin-bottom: 1.5rem;
            }
            .color-card {
                font-size: 0.9rem;
                padding: 0.8rem;
            }
            .huebot-response {
                font-size: 0.95rem;
            }
            .analyze-btn {
                width: 100%;
                padding: 0.8rem;
                font-size: 1rem;
                margin-top: 1.2rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Page Header
# -------------------------------
st.markdown('<div class="title">🎨 HueBot: Color Psychology Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a mobile UI screenshot and get an emotional color analysis.</div>', unsafe_allow_html=True)

# -------------------------------
# Upload Image
# -------------------------------
uploaded_image = st.file_uploader("📤 Drop your mobile UI design (PNG or JPG)", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="📱 Uploaded Screenshot", use_container_width=True)
    st.markdown("### 🎨 Top 5 Dominant Colors")

    # -------------------------------
    # Extract & Display Dominant Colors
    # -------------------------------
    colors = extract_dominant_colors(uploaded_image, k=5)
    hex_colors = ['#%02x%02x%02x' % tuple(map(int, c)) for c in colors]

    # Display color cards responsively
    for i, (rgb, hex_code) in enumerate(zip(colors, hex_colors)):
        rgb_clean = tuple(int(v) for v in rgb)
        st.markdown(f"""
            <div class="color-card">
                <div style='background-color:{hex_code}; height:60px; border-radius:6px;'></div>
                <div style='margin-top:0.5rem; font-size:0.9rem; color: white;' >HEX: `{hex_code}`</div>
                <div style='font-size:0.8rem; color: white'>RGB: {rgb_clean}</div>
            </div>
        """, unsafe_allow_html=True)

    # -------------------------------
    # Gemini Prompt Generation
    # -------------------------------
    prompt = (
        f"The dominant UI colors (in HEX) are: {', '.join(hex_colors)}. "
        f"Analyze the psychological and emotional impact of this palette on mobile app users. "
        f"Also suggest ideal app categories this palette fits (e.g. finance, health, social, games)."
    )

    # -------------------------------
    # Gemini Chat Session & Analysis
    # -------------------------------
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = get_gemini_chat_session()

    if st.button("🧠 Analyze With HueBot", key="analyze_btn"):
        with st.spinner("HueBot is analyzing your color palette..."):
            try:
                response = ask_gemini(prompt, st.session_state.chat_session)
                st.markdown("#### 💬 HueBot Says:")
                st.markdown(f'<div class="huebot-response">{response}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"🚫 HueBot Error: {str(e)}")

else:
    st.info("Upload your UI screenshot above to begin analysis.")
