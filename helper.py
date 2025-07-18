# helper.py
import streamlit as st
import google.generativeai as genai
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Load Gemini API key from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure Gemini once
genai.configure(api_key=GEMINI_API_KEY)

# -------------------- COLOR EXTRACTION --------------------
def extract_dominant_colors(image_file, k=5):
    """Extract k dominant colors from an image using KMeans clustering."""
    image = Image.open(image_file)
    image = image.resize((150, 150))  # Reduce size for speed
    img_np = np.array(image)

    # Remove transparency if it exists
    if img_np.shape[-1] == 4:
        img_np = img_np[:, :, :3]

    img_np = img_np.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(img_np)

    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

# -------------------- GEMINI SESSION SETUP --------------------
def get_gemini_chat_session():
    """Start a new Gemini chat session with system instructions."""
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction="""..."""  # Keep the full system instructions here
    )

    return model.start_chat(history=[])

# -------------------- GEMINI MESSAGE HANDLER --------------------
def ask_gemini(prompt: str, chat_session) -> str:
    """Send a prompt to Gemini and return the plain text response."""
    response = chat_session.send_message(prompt)
    return response.text

# -------------------- SIDEBAR --------------------
def render_sidebar():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(160deg, #4f46e5 0%, #38bdf8 100%);
            padding: 2rem 1rem;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-title {
            color: #ffffff;
            font-size: 1.6rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0 0 6px rgba(255, 255, 255, 0.3);
        }

        .footer {
            text-align: center;
            color: #e0f2fe;
            font-size: 0.85rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Hide default sidebar nav */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Force link text to white */
        section[data-testid="stSidebar"] a {
            color: #ffffff !important;
            font-weight: 500;
            text-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
        }

        section[data-testid="stSidebar"] a:hover {
            color: #ffffff !important;
            text-decoration: none;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="sidebar-title">🎯 Navigation</div>', unsafe_allow_html=True)

        # ✅ Corrected page references (no .py extension)
        st.page_link("Home", label="🏠 Home")
        st.page_link("pages/Chatbot", label="🤖 Ask HueBot")
        st.page_link("pages/Analysis", label="📊 Analyze Screenshot")
        st.page_link("pages/Dashboard", label="📈 Dashboard")
        st.page_link("pages/Interact", label="💬 Color Theme Feedback")
        st.page_link("pages/About", label="📘 About This Project")

        st.markdown('<div class="footer">🔒 HueBot AI Integrated<br>Built with 💙 usability in mind</div>', unsafe_allow_html=True)
