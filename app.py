import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Page Configuration
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
        font-size: 2.8rem;
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
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
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
        padding: 18px;
        text-align: center;
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
    }
    .card-value {
        font-size: 2rem;
        font-weight: 800;
        color: #60a5fa;
    }
    .card-label {
        font-size: 0.85rem;
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

# 3. Header
st.markdown('<div class="hero-title">⚔️ COMPETITOR WAR-ROOM AGENT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Autonomous AI Intelligence & Strategic Counter-Attack Engine</div>', unsafe_allow_html=True)

# 4. Metric Highlights
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div class="card-box"><div class="card-value">10s</div><div class="card-label">Analysis Speed</div></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card-box"><div class="card-value">Gemini 2.5</div><div class="card-label">AI Engine</div></div>', unsafe_allow_html=True)
with col_c:
    st.markdown('<div class="card-box"><div class="card-value">PDF Exec</div><div class="card-label">Export Ready</div></div>', unsafe_allow_html=True)

st.markdown("---")

# 5. Inputs
input_col, btn_col = st.columns([3, 1])

with input_col:
    target_url = st.text_input("🎯 Enter Competitor Website URL", placeholder="https://competitor-domain.com")

with btn_col:
    analyze_btn = st.button("🚀 Analyze Competitor")

# 6. Functions
def scrape_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
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
        textColor=colors.HexColor('#111827'),
        spaceAfter=15
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#374151')
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

# 7. Logic Execution
if analyze_btn:
    if not target_url:
        st.warning("⚠️ Please enter a valid URL first.")
    else:
        with st.spinner("⚡ Extracting Website Content & Generating Counter-Strategy..."):
            scraped_data = scrape_website(target_url)
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

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )

                    report_output = response.text
                    pdf_file = generate_pdf(report_output)

                    st.success("🎯 Intelligence Analysis Successfully Completed!")

                    st.markdown("### 📊 Executive War-Room Briefing")
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
