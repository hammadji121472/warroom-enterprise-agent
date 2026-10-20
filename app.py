import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Page Configuration
st.set_page_config(
    page_title="WAR-ROOM AI | Enterprise Intelligence Platform",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Silicon Valley Enterprise SaaS CSS Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #090d16;
        color: #f1f5f9;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Top Navigation Banner */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background: rgba(15, 23, 42, 0.6);
        border-bottom: 1px solid rgba(255, 255, 250, 0.08);
        border-radius: 12px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .nav-brand {
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-status {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Hero Title Header */
    .hero-container {
        text-align: center;
        max-width: 900px;
        margin: 0 auto 2.5rem auto;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
        line-height: 1.15;
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 1.15rem;
        font-weight: 500;
        line-height: 1.6;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        text-align: left;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #38bdf8;
    }

    /* Input Section */
    .stTextInput > div > div {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 4px 8px !important;
    }
    .stTextInput > div > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.25) !important;
    }
    
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 14px 24px;
        font-size: 1rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
        transition: all 0.2s ease;
        margin-top: 1.8rem;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 24px rgba(37, 99, 235, 0.6);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        border: 1px solid #334155;
        color: #94a3b8;
        font-weight: 600;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }

    /* Section Output Box */
    .output-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 28px;
        margin-top: 1rem;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Navigation Bar
st.markdown("""
    <div class="top-nav">
        <div class="nav-brand">⚔️ WAR-ROOM PLATFORM <span style="color:#64748b; font-weight:400; font-size:0.85rem;">| Enterprise Edition</span></div>
        <div class="nav-status">● SYSTEM ACTIVE</div>
    </div>
""", unsafe_allow_html=True)

# 4. Hero Header
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Competitor Intelligence & Counter-Strategy Engine</div>
        <div class="hero-subtitle">Real-time web extraction and AI-driven tactical analysis tailored for high-growth enterprise brands.</div>
    </div>
""", unsafe_allow_html=True)

# 5. Enterprise Metrics Dashboard
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><div class="metric-title">Engine Speed</div><div class="metric-value">~8.5s</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="metric-title">Model Core</div><div class="metric-value">Gemini 3.8</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-title">Analysis Depth</div><div class="metric-value">360° Matrix</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><div class="metric-title">Export Format</div><div class="metric-value">PDF Ready</div></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 6. User Inputs
input_col, btn_col = st.columns([3, 1])

with input_col:
    target_url = st.text_input("🎯 Enter Competitor Domain / Website URL", placeholder="https://www.notion.so")

with btn_col:
    analyze_btn = st.button("🚀 Run Deep Analysis")

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
        return text[:5000] if len(text) > 100 else "Content extraction limited, utilizing fallback site information."
    except Exception as e:
        return f"Scraping Notice: {str(e)}"

def generate_pdf(report_text, filename="Competitor_War_Room_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=15,
        fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )

    story.append(Paragraph("<b>EXECUTIVE WAR-ROOM COMPETITOR REPORT</b>", title_style))
    story.append(Spacer(1, 10))

    lines = report_text.split('\n')
    for line in lines:
        if line.strip():
            clean_line = line.replace('<', '&lt;').replace('>', '&gt;').replace('*', '')
            story.append(Paragraph(clean_line, body_style))
            story.append(Spacer(1, 5))

    doc.build(story)
    return filename

# 7. Processing & Tabbed Output
if analyze_btn:
    if not target_url:
        st.warning("⚠️ Please provide a competitor URL to analyze.")
    else:
        valid_url = clean_input_url(target_url)
        
        with st.spinner(f"⚡ Extracting Data from {valid_url} & Running Strategic Synthesis..."):
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

                    Provide a structured Executive War-Room Report with these exact section headers:
                    
                    ### 1. EXECUTIVE SUMMARY & VALUE PROPOSITION
                    Provide positioning summary, core target audience, and unique selling points.

                    ### 2. COMPETITOR CORE STRENGTHS & VULNERABILITIES
                    Detailed analysis of what they do best and key market weaknesses we can exploit.

                    ### 3. TACTICAL COUNTER-ATTACK STRATEGY
                    Specific growth plays, acquisition angles, and messaging hooks to outmaneuver them.

                    ### 4. 30-DAY ACTION PLAN
                    4 concrete quick wins to implement immediately.
                    """

                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )

                    report_output = response.text
                    pdf_file = generate_pdf(report_output)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.success("🎯 Strategic Analysis Completed Successfully!")

                    # Professional Tabbed Interface
                    tab1, tab2, tab3 = st.tabs([
                        "📊 Strategic Intelligence Brief", 
                        "⚔️ Vulnerabilities & Counter-Attack", 
                        "📥 Executive PDF Export"
                    ])

                    with tab1:
                        st.markdown('<div class="output-card">', unsafe_allow_html=True)
                        st.markdown(report_output)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab2:
                        st.markdown('<div class="output-card">', unsafe_allow_html=True)
                        st.markdown("### 🎯 Key Tactical Takeaways for Our Brand")
                        st.info("Direct Counter-Play: Position our solution as faster, more streamlined, and tailored with dedicated enterprise support.")
                        st.markdown("---")
                        st.markdown(report_output)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab3:
                        st.markdown('<div class="output-card" style="text-align: center;">', unsafe_allow_html=True)
                        st.markdown("### 📄 Official Executive Briefing Document")
                        st.write("Click below to download the fully styled, client-ready PDF report.")
                        
                        with open(pdf_file, "rb") as f:
                            st.download_button(
                                label="📥 Download Official Executive PDF Report",
                                data=f,
                                file_name="Competitor_War_Room_Report.pdf",
                                mime="application/pdf"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as err:
                    st.error(f"❌ AI Generation Failed: {str(err)}")
