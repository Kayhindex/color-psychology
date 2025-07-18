import streamlit as st
import pandas as pd
import os
import plotly.express as px
from helper import render_sidebar

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="📊 Feedback Dashboard", layout="wide")
render_sidebar()

# -------------------------------
# Load Data
# -------------------------------
data_path = "engagement_data.csv"

if not os.path.exists(data_path):
    st.warning("⚠️ No engagement data found. Submit feedback first.")
    st.stop()

try:
    df = pd.read_csv(data_path, parse_dates=["date"])
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"🚫 Error loading data: {e}")
    st.stop()

if df.empty:
    st.warning("📭 No data to display yet.")
    st.stop()

# -------------------------------
# Sidebar Filters
# -------------------------------
with st.sidebar:
    st.markdown("### 🔎 Filter Data")

    app_types = df["app_type"].unique()
    themes = df["theme_name"].unique()

    app_filter = st.multiselect("Filter by App Type", app_types, default=app_types)
    theme_filter = st.multiselect("Filter by Theme", themes, default=themes)

    date_range = st.date_input(
        "Filter by Date Range",
        value=(df["date"].min().date(), df["date"].max().date()),
        min_value=df["date"].min().date(),
        max_value=df["date"].max().date(),
        key="date_range",
    )

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = df[
    (df["app_type"].isin(app_filter)) &
    (df["theme_name"].isin(theme_filter)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

if filtered_df.empty:
    st.warning("📭 No data matching filters.")
    st.stop()

# -------------------------------
# Summary Metrics
# -------------------------------
st.markdown("## 📊 Engagement Overview")

col1, col2, col3, col4 = st.columns(4)

avg_rating = round(filtered_df["rating"].mean(), 2)
avg_engagement = round(filtered_df["engagement_score"].mean(), 2)
total_users = filtered_df["user_id"].nunique()

# Top Preferred Colors: explode and count
if "preferred_colors" in filtered_df.columns:
    colors_series = filtered_df["preferred_colors"].dropna().str.split(",").explode().str.strip()
    top_color = colors_series.mode()[0] if not colors_series.empty else "N/A"
else:
    top_color = "N/A"

col1.metric("⭐ Avg Rating", avg_rating)
col2.metric("📈 Avg Engagement", avg_engagement)
col3.metric("👥 Total Users", total_users)

if top_color != "N/A":
    col4.markdown("🎨 Most Preferred Color")
    color_html = f"""
    <div style="display:flex; align-items:center; gap:10px">
        <div style="width:25px; height:25px; background-color:{top_color}; border:1px solid #ccc; border-radius:4px;"></div>
        <span style="font-weight:bold;">{top_color}</span>
    </div>
    """
    col4.markdown(color_html, unsafe_allow_html=True)
else:
    col4.metric("🎨 Most Preferred Color", "N/A")

# -------------------------------
# Visualizations
# -------------------------------
st.markdown("## 📈 Data Visualizations")

# Ratings by Theme
rating_chart = px.box(
    filtered_df,
    x="theme_name",
    y="rating",
    color="theme_name",
    title="Theme Ratings Distribution",
    template="plotly_dark",
)
st.plotly_chart(rating_chart, use_container_width=True)

# Engagement by Theme
engagement_theme = (
    filtered_df.groupby("theme_name")["engagement_score"].mean().reset_index()
)
engagement_chart = px.bar(
    engagement_theme,
    x="theme_name",
    y="engagement_score",
    color="theme_name",
    title="Average Engagement by Theme",
    template="plotly_dark",
)
st.plotly_chart(engagement_chart, use_container_width=True)

# Average Rating and Engagement by App Type
app_metrics = (
    filtered_df.groupby("app_type")[["rating", "engagement_score"]]
    .mean()
    .reset_index()
)
app_chart = px.bar(
    app_metrics.melt(id_vars="app_type"),
    x="app_type",
    y="value",
    color="variable",
    barmode="group",
    title="Average Rating and Engagement by App Type",
    labels={"value": "Score", "app_type": "App Type", "variable": "Metric"},
    template="plotly_dark",
)
st.plotly_chart(app_chart, use_container_width=True)

# Section-wise color previews - show average colors per section (convert hex colors to RGB average)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return f"#{''.join(f'{v:02x}' for v in rgb)}"

color_sections = ["landing_color", "header_color", "button_color", "background_color", "text_color"]

section_colors = {}
for section in color_sections:
    if section in filtered_df.columns:
        # Convert hex to RGB tuples and average
        colors = filtered_df[section].dropna().apply(hex_to_rgb)
        if not colors.empty:
            avg_rgb = tuple(
                int(sum(x) / len(x)) for x in zip(*colors)
            )
            section_colors[section] = rgb_to_hex(avg_rgb)

if section_colors:
    st.markdown("## 🎨 Average Section-wise Colors")
    color_cols = st.columns(len(section_colors))
    for i, (section, color_hex) in enumerate(section_colors.items()):
        with color_cols[i]:
            st.markdown(f"**{section.replace('_', ' ').title()}**")
            st.markdown(
                f"<div style='width:80px; height:40px; background-color:{color_hex}; border-radius:6px; border:1px solid #ccc'></div>",
                unsafe_allow_html=True,
            )

# -------------------------------
# Raw Data Table & Export
# -------------------------------
st.markdown("## 📋 Raw Feedback Data")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Data as CSV", csv, file_name="filtered_feedback.csv", mime="text/csv"
)
