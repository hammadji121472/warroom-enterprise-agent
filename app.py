import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Page Configuration
st.set_page_config(
    page_title="War-Room AI | Enterprise Competitor Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Modern Enterprise UI CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .status-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(96, 165, 250, 0.4);
        color: #60a5fa;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2.5rem;
    }

    .card-box {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .card-value {
        font-size: 2rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .card-label {
        font-size: 0.8rem;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-top: 4px;
    }

    .stTextInput label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #475569 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }

    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
        color: #ffffff;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 1rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        transition: all 0.2s ease;
        margin-top: 1.8rem;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5);
    }

    .stTextArea textarea {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div style="text-align: center;"><span class="status-badge">⚡ ENTERPRISE AI AGENT</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Competitor War-Room Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Automated Web Extraction & Strategic Counter-Attack Engine</div>', unsafe_allow_html=True)

# 4. Highlight Cards
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div class="card-box"><div class="card-value">10s</div><div class="card-label">Analysis Speed</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card-box"><div class="card-value">Gemini AI</div><div class="card-label">Intelligence Engine</div></div>', unsafe_allow_html=True)
with col_c:
    st.markdown('<div class="card-box"><div class="card-value">PDF Ready</div><div class="card-label">Executive Export</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Inputs
input_col, btn_col = st.columns([3, 1])

with input_col:
    target_url = st.text_input("🎯 Target Competitor Website URL", placeholder="https://www.webfx.com")

with btn_col:
    analyze_btn = st.button("🚀 Run Analysis")

# Helper Functions
def clean_input_url(url_str):
    match = re.search(r'https?://[^\s\)\]]+', url_str)
    if match:
        return match.group(0)
    return url_str.strip()

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
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=15
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    story.append(Paragraph("<b>EXECUTIVE COMPETITOR WAR-ROOM REPORT</b>", title_style))
    story.append(Spacer(1, 10))

    lines = report_text.split('\n')
    for line in lines:
        if line.strip():
            clean_line = line.replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(clean_line, body_style))
            story.append(Spacer(1, 4))

    doc.build(story)
    return filename

# 6. Execution Logic
if analyze_btn:
    if not target_url:
        st.warning("⚠️ Please enter a valid URL first.")
    else:
        valid_url = clean_input_url(target_url)
        
        with st.spinner(f"⚡ Extracting Data from {valid_url} & Generating Counter-Strategy..."):
            scraped_data = scrape_website(valid_url)
            api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                st.error("❌ Gemini API Key missing in Streamlit secrets!")
            else:
                try:
                    client = genai.Client(api_key=api_key)

                    prompt = f"""
                    You are an Elite Executive Growth Strategist & Competitor Intelligence Analyst.
                    Analyze the following scraped competitor website text:
                    {scraped_data}

                    Provide a structured Executive War-Room Report:
                    1. EXECUTIVE SUMMARY & VALUE PROPOSITION
                    2. COMPETITOR CORE STRENGTHS & OFFERINGS
                    3. IDENTIFIED VULNERABILITIES & WEAKNESSES
                    4. TACTICAL COUNTER-ATTACK STRATEGY FOR OUR BRAND
                    5. RECOMMENDED QUICK WINS (NEXT 30 DAYS)
                    """

                    # Explicit single model targeting standard endpoint
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )

                    report_output = response.text
                    pdf_file = generate_pdf(report_output)

                    st.success("🎯 Intelligence Analysis Successfully Completed!")

                    st.markdown("### 📊 Executive Intelligence Summary")
                    st.text_area("Analysis Output", report_output, height=380)

                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="📄 Download Official PDF Report",
                            data=f,
                            file_name="Competitor_War_Room_Report.pdf",
                            mime="application/pdf"
                        )
                except Exception as err:
                    st.error(f"❌ AI Generation Failed: {str(err)}")
