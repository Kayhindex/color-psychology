import streamlit as st
from helper import render_sidebar

# Page Configuration
st.set_page_config(page_title="🎨Color Psychology System", layout="wide")
render_sidebar()

# --- Custom CSS Styling (Full width & Pleasant theme) ---
st.markdown("""
    <style>
    /* Make main container full width with minimal side padding */
    .main .block-container {
        max-width: 100% !important;
        padding: 2rem 2rem 3rem 2rem !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #4f46e5, #38bdf8);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 2rem;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .hero p {
        color: #f0f9ff;
        font-size: 1.15rem;
        max-width: 100%;
        line-height: 1.6;
    }

    .hero img {
        max-width: 160px;
        border-radius: 12px;
    }

    /* Feature Cards Grid */
    .feature-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        margin-top: 3rem;
        justify-content: center;
    }

    /* Individual Card */
    .card {
        flex: 0 1 calc(48% - 1rem);
        background: linear-gradient(145deg, #e0f2fe, #dbeafe);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
    }

    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 8px 20px rgba(56, 189, 248, 0.3);
        cursor: pointer;
    }

    .card h3 {
        color: #0f172a;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .card p {
        color: #334155;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    .card a {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 5;
        text-decoration: none;
    }

    /* Responsive Design */
    @media screen and (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem 1rem 2rem 1rem !important;
        }

        .hero {
            flex-direction: column;
            text-align: center;
            padding: 2rem 1rem;
        }

        .hero h1 {
            font-size: 2rem;
        }

        .hero p {
            font-size: 1rem;
        }

        .hero img {
            max-width: 100px;
        }

        .card {
            flex: 1 1 100%;
        }

        .feature-grid {
            flex-direction: column;
            align-items: center;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
    <div class="hero">
        <div style="flex: 1;">
            <h1>🎨 Color Psychology System</h1>
            <p>
                Welcome to your intelligent color assistant for mobile UI. This system helps you design emotionally resonant, high-engagement apps by applying color psychology principles.
            </p>
        </div>
        <div>
            <img src="https://cdn-icons-png.flaticon.com/512/1087/1087815.png" alt="Color Icon" />
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Feature Cards Section ---
st.markdown("""
    <div class="feature-grid">
        <div class="card">
            <a href="/dashboard" target="_self"></a>
            <h3>📈 Dashboard</h3>
            <p>Explore color engagement analytics and visual breakdowns from your previous tests and uploads.</p>
        </div>
        <div class="card">
            <a href="/chatbot" target="_self"></a>
            <h3>🤖 Ask HueBot</h3>
            <p>Chat with HueBot about color choices, emotional response, and optimal color combinations for your app type.</p>
        </div>
        <div class="card">
            <a href="/analysis" target="_self"></a>
            <h3>📊 Analyze Screenshot</h3>
            <p>Upload your mobile UI design to extract the dominant colors and receive real-time psychological insights.</p>
        </div>
        <div class="card">
            <a href="/interact" target="_self"></a>
            <h3>💬 Color Feedback</h3>
            <p>Share your expert UI/UX feedback with us to improve design insights.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
