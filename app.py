import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Page Config
st.set_page_config(
    page_title="War-Room Agent | Enterprise AI Competitor Intelligence",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS - Silicon Valley Dark Glassmorphism UI
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1f2937 100%);
        color: #f3f4f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Title Styling */
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #9ca3af;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2.5rem;
    }

    /* Input Fields */
    .stTextInput input {
        background-color: rgba(17, 24, 39, 0.8) !important;
        color: #f9fafb !important;
        border-radius: 12px !important;
        border: 1px solid #374151 !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
    }
    .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 15px rgba(129, 140, 248, 0.3) !important;
    }

    /* Primary Action Button */
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 14px 24px;
        font-size: 1.1rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
        transition: all 0.3s ease;
        margin-top: 1.8rem;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(124, 58, 237, 0.6);
        background: linear-gradient(90deg, #4338ca 0%, #6d28d9 100%);
    }

    /* Feature Score Cards */
    .card-box {
        background: rgba(31, 41, 55, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
    }
    .card-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #60a5fa;
    }
    .card-label {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Output Box Styling */
    .stTextArea textarea {
        background-color: rgba(17, 24, 39, 0.9) !important;
        color: #e5e7eb !important;
        border-radius: 12px !important;
        border: 1px solid #374151 !important;
        font-family: 'Menlo', 'Monaco', monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. App Header
st.markdown('<div class="hero-title">⚔️ COMPETITOR WAR-ROOM AGENT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Autonomous AI Intelligence & Strategic Counter-Attack Engine</div>', unsafe_allow_html=True)

# 4. Metric Highlights Header
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div class="card-box"><div class="card-value">10s</div><div class="card-label">Analysis Speed</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card-box"><div class="card-value">Gemini 2.5</div><div class="card-label">AI Engine</div></div>', unsafe_allow_html=True)
with col_c:
    st.markdown('<div class="card-box"><div class="card-value">PDF Exec</div><div class="card-label">Export Ready</div></div>', unsafe_allow_html=True)

st.markdown("---")

# 5. Input Form Area
input_col, btn_col = st.columns([3, 1])

with input_col:
    target_url = st.text_input("🎯 Enter Competitor Website URL", placeholder="https://competitor-domain.com")

with btn_col:
    analyze_btn = st.button("🚀 Analyze Competitor")

# Scraping & Helper Functions
def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
        return text[:4500] if len(text) > 100 else "Scraped content is too brief."
    except Exception as e:
        return f"Scraping Error: {str(e)}"

def generate_pdf(report_text, filename="Competitor_War_Room_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1E2
