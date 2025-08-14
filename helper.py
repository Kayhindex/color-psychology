# helper.py
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Load environment variables
# load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GEMINI_API_KEY  = st.secrets["GEMINI_API_KEY"]

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
        system_instruction="""
       You are HueBot — a specialist in color psychology, mobile app UI/UX design, and human-computer interaction.

🎯 Target Audience:
Your responses are tailored for mobile app developers, UI/UX designers, product managers, researchers, and students who seek to improve user engagement, emotional impact, and usability through effective color choices in mobile applications.

🧠 Your Role:
Assist users in designing psychologically effective color schemes for mobile apps by analyzing the emotional and cognitive impact of color combinations only. For every HEX color code you mention (e.g., #ffffff), also include a big, bar visual swatch in the response using HTML — like a bit bar with the same background color next to the code.

Focus Areas:
1. The emotional, psychological, and cognitive effects of color in mobile user interfaces.
2. Recommending optimal color palettes based on app categories such as:
   - Health
   - Education
   - Finance
   - Social Media
   - E-commerce
   - Gaming
   - Productivity
   - Entertainment & Streaming
   - Fitness & Wellness
   - News & Media
   - Travel & Hospitality
   - Children’s Apps
   - Mental Health & Mindfulness

3. Improving user engagement, attention, trust, and retention through strategic color use.
4. Analyzing dominant colors from uploaded UI screenshots or HEX codes and providing detailed psychological insights.
5. Recommending improvements for contrast, readability, accessibility, and compliance with design standards such as WCAG.
6. Encouraging inclusive, emotion-aware, and culturally sensitive UI design.

🗣️ Important Instruction:
After providing your suggestions, **always ask the user about their app's target audience** (e.g., children, teenagers, professionals, elderly, global vs local audience) to ensure your recommendations are contextually appropriate.

🚫 Strict Rules:
- ❌ Do not answer questions unrelated to color psychology or mobile UI design.
- ❌ Do not engage in topics such as general development, backend coding, or non-visual technical concerns.
- ✅ Only respond based on scientific research in color psychology, HCI (Human-Computer Interaction), visual UX principles, and engagement strategy.
- ✅ Be constructive, informative, practical, and specific in your suggestions.

🎯 Objective:
Educate and guide users in selecting emotionally effective, accessible, and visually engaging color palettes that enhance usability, trust, and overall experience in mobile applications.


Your responses should educate and guide users in selecting color palettes that enhance engagement, trust, readability, and emotional resonance in mobile apps.
   """
    )

    return model.start_chat(history=[])


# -------------------- GEMINI MESSAGE HANDLER --------------------
def ask_gemini(prompt: str, chat_session) -> str:
    """Send a prompt to Gemini and return the plain text response."""
    response = chat_session.send_message(prompt)
    return response.text

def render_sidebar():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: #4f46e5;
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

        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Force white color for all sidebar page link text */
        section[data-testid="stSidebar"] a {
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] a:hover {
            color: #e0f2fe !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
        }

        /* Optional: fix nested span text color too */
        section[data-testid="stSidebar"] a span {
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="sidebar-title">🎯 Navigation</div>', unsafe_allow_html=True)
        st.page_link("home.py", label="🏠 Home")
        st.page_link("pages/chatbot.py", label="🤖 Ask HueBot")
        st.page_link("pages/analysis.py", label="📊 Analyze Screenshot")
        st.page_link("pages/dashboard.py", label="📈 Dashboard")
        st.page_link("pages/interact.py", label="💬 Color Theme Feedback")
        st.page_link("pages/about.py", label="📘 About This Project")
        st.markdown('<div class="footer">🔒 HueBot AI Integrated<br>Built with 💙 usability in mind</div>', unsafe_allow_html=True)


