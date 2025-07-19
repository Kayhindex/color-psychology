import streamlit as st
from helper import render_sidebar

# Page setup
st.set_page_config(page_title="About This Project", layout="wide")
render_sidebar()

# Custom CSS
st.markdown("""
<style>
  /* Outer app background */
  .stApp, .reportview-container {
    background-color: #f9fafb !important;  /* Light neutral background */
  }

  /* Main content container */
  .main .block-container {
    padding: 4rem 6rem;
    background: linear-gradient(145deg, #e0f2fe, #dbeafe);
    border-radius: 15px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    min-height: 100vh;
    color: #0f172a; /* Dark blue text */
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  /* Page title */
  .about-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 2.5rem;
    text-align: center;
    text-shadow: none;
  }

  /* Section titles */
  .about-section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2563eb;
    margin-top: 3rem;
    margin-bottom: 1.25rem;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 0.4rem;
  }

  /* Body text */
  .about-text {
    font-size: 1.1rem;
    line-height: 1.75;
    color: #1e293b;
  }

  /* Lists inside body */
  .about-text ul {
    margin-left: 1.8rem;
    margin-bottom: 1rem;
  }

  /* Contact block */
  .contact-block {
    margin-top: 2.5rem;
    font-size: 1.1rem;
    color: #1e293b;
  }

  /* Links */
  .contact-block a {
    color: #2563eb;
    text-decoration: none;
    transition: all 0.3s ease;
  }
  .contact-block a:hover {
    text-decoration: underline;
    color: #3b82f6;
  }

  /* Responsive styles */
  @media screen and (max-width: 768px) {
    .main .block-container {
      padding: 2rem 1.5rem;
      border-radius: 14px;
    }
    .about-title {
      font-size: 2.2rem;
    }
    .about-section-title {
      font-size: 1.3rem;
      margin-top: 2rem;
    }
    .about-text {
      font-size: 1rem;
    }
    .contact-block {
      font-size: 1rem;
    }
  }
</style>
""", unsafe_allow_html=True)

# Page content
st.markdown("""
<div class="about-container">
  <div class="about-title">📘 About This Project</div>
  <div class="about-text">
    The <strong>Color Psychology System for Mobile UI Engagement</strong> is an AI-powered assistant designed to help designers and developers create emotionally intelligent app interfaces.
    It leverages color psychology theories and generative AI to provide meaningful insights into how colors influence user engagement and decision-making.
  </div>
  
  <div class="about-section-title">🎯 Project Purpose</div>
  <div class="about-text">
    This system was built to:
    <ul>
      <li>Analyze the emotional impact of UI color schemes</li>
      <li>Guide designers in selecting optimal color palettes</li>
      <li>Improve user engagement and visual consistency</li>
    </ul>
  </div>
  
  <div class="about-section-title">🧠 Key Features</div>
  <div class="about-text">
    <ul>
      <li><strong>🤖 Ask HueBot:</strong> Interact with an AI expert for color advice</li>
      <li><strong>📊 Analyze Screenshots:</strong> Upload a UI and get instant emotional feedback</li>
      <li><strong>📈 Dashboard:</strong> View trends and compare engagement insights</li>
      <li><strong>💬 Color Theme Feedback:</strong> Collect feedback from UI/UX designers to improve design insight</li>
    </ul>
  </div>
  
  <div class="about-section-title">🛠️ Technologies Used</div>
  <div class="about-text">
    Python • Streamlit • Google Gemini API • OpenCV • KMeans Clustering • dotenv
  </div>
  
  <div class="about-section-title">👨‍💻 Developer</div>
  <div class="about-text">
    <strong>Abdulsalam Mufliat Adenike</strong><br>
    Python Programmer<br>
    Ogbomoso, Oyo State, Nigeria<br>
    Passionate about mathematics, AI, and user-centric technology.
  </div>
  
  <div class="about-section-title">📌 Acknowledgement</div>
  <div class="about-text">
    This project bridges machine learning, user psychology, and UI design — enhancing tech experiences in African mobile markets and beyond.
  </div>
  
  <div class="about-section-title">📫 Contact</div>
  <div class="contact-block">
    Email: <a href="mailto:abdulsalammufliah@gmail.com.">abdulsalammufliah@gmail.com</a><br>
    LinkedIn: <a href="https://linkedin.com/in/MufliahA.Abdulsalam" target="_blank">linkedin.com/in/MufliahA.Abdulsalam"</a>
  </div>
</div>
""", unsafe_allow_html=True)
