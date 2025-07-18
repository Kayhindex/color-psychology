import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime
from helper import render_sidebar

# Page setup
st.set_page_config(page_title="📝 Submit Feedback", layout="wide")
render_sidebar()

st.markdown("## 📝 User Engagement Feedback")
st.markdown("Please provide feedback on your experience with the app interface.")

# -------------------------------
# Form Input
# -------------------------------
with st.form("feedback_form"):
    col1, col2 = st.columns(2)

    with col1:
        app_type = st.selectbox(
            "App Type",
            [
                "Education", "E-commerce", "Health", "Gaming", "News", "Finance",
                "Productivity", "Travel", "Social Media", "Music", "Utility", "Fitness"
            ],
            index=0
        )

        theme_name = st.selectbox(
            "Theme Name",
            ["Dark Blue", "Soft Green", "Vibrant Orange", "Minimal Gray", "Neon Pink"],
            index=0
        )

        st.markdown("#### 🎨 Preferred Colors (Suggest up to 5)")
        preferred_color_1 = st.color_picker("Preferred Color 1", "#0b111e")
        preferred_color_2 = st.color_picker("Preferred Color 2", "#00f7ff")
        preferred_color_3 = st.color_picker("Preferred Color 3", "#ffffff")
        preferred_color_4 = st.color_picker("Preferred Color 4", "#000000")
        preferred_color_5 = st.color_picker("Preferred Color 5", "#ff0000")

        preferred_colors = [
            preferred_color_1,
            preferred_color_2,
            preferred_color_3,
            preferred_color_4,
            preferred_color_5
        ]

        st.markdown("#### 🎨 Section-wise Color Preferences")
        color_landing = st.color_picker("Landing Page Color", "#0b111e")
        color_header = st.color_picker("Header Color", "#00f7ff")
        color_button = st.color_picker("Button Color", "#00ff00")
        color_background = st.color_picker("Background Color", "#ffffff")
        color_text = st.color_picker("Text Color", "#000000")

    with col2:
        dominant_color = st.color_picker("Dominant Color", "#00f7ff")
        rating = st.slider("Rate the Theme", 1, 5, 3)
        engagement_score = st.slider("Engagement Score (0-100)", 0, 100, 50)
        comments = st.text_area("Any additional feedback? (Optional)", height=150)

    submitted = st.form_submit_button("Submit Feedback")

# -------------------------------
# Handle Submission
# -------------------------------
if submitted:
    cleaned_colors = [color for color in preferred_colors if color]  # remove empty values

    if len(cleaned_colors) == 0:
        st.warning("⚠️ Please suggest at least one preferred color.")
    else:
        feedback_data = {
            "user_id": str(uuid.uuid4()),
            "app_type": app_type,
            "theme_name": theme_name,
            "preferred_colors": ", ".join(cleaned_colors),
            "dominant_color": dominant_color,
            "rating": rating,
            "engagement_score": engagement_score,
            "comments": comments,
            "landing_color": color_landing,
            "header_color": color_header,
            "button_color": color_button,
            "background_color": color_background,
            "text_color": color_text,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

        df = pd.DataFrame([feedback_data])
        file_path = "engagement_data.csv"

        try:
            if os.path.exists(file_path):
                df.to_csv(file_path, mode="a", index=False, header=False)
            else:
                df.to_csv(file_path, index=False)
            st.success("✅ Feedback submitted successfully!")
        except Exception as e:
            st.error(f"❌ Failed to save feedback: {e}")
