import streamlit as st
import asyncio
from playwright.async_api import async_playwright
from google import genai
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Direct API Key Client Setup
API_KEY = "AQ.Ab8RN6JvzmMbVuI5NPkasBWrzNc-xfhXv26m0pwdDWCX1VcxYw"
client = genai.Client(api_key=API_KEY)

# Page Configuration
st.set_page_config(page_title="Competitor War-Room Agent", page_icon="⚔️", layout="wide")

st.title("⚔️ Advanced Competitor War-Room Agent")
st.subheader("Multi-Competitor Scraping, Gemini AI Intelligence & PDF Export")

# Function to Generate PDF
def create_pdf(text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )
    
    story = []
    lines = text_content.split('\n')
    for line in lines:
        clean_line = line.replace('#', '').replace('*', '').strip()
        if clean_line:
            story.append(Paragraph(clean_line, body_style))
            story.append(Spacer(1, 4))
            
    doc.build(story)
    buffer.seek(0)
    return buffer

# Scraper Function
async def scrape_competitor(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            title = await page.title()
            page_text = await page.inner_text("body")
            clean_text = "\n".join([line.strip() for line in page_text.splitlines() if line.strip()])
            return {"url": url, "title": title, "content": clean_text[:2500]}
        except Exception as e:
            st.error(f"Scraping Error ({url}): {e}")
            return None
        finally:
            await browser.close()

# AI Analysis Function
def analyze_with_gemini(scraped_results):
    combined_content = ""
    for idx, item in enumerate(scraped_results, 1):
        combined_content += f"\n--- COMPETITOR {idx}: {item['title']} ({item['url']}) ---\n"
        combined_content += item['content'] + "\n"
        
    prompt = f"""
    You are a Strategic Competitor War-Room AI Agent.
    Analyze the following scraped webpage data from competitor(s) and provide a detailed structured report:
    
    1. Competitor Focus & Market Niche Comparison
    2. Product / Service Portfolio Analysis
    3. Weaknesses or Strategic Gaps Identified
    4. Actionable Competitive Strategies to Win Market Share

    Competitor Scraped Data:
    {combined_content}
    """
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        st.error(f"AI Analysis Error: {e}")
        return None

# User Input Interface (Multi-URL Support)
urls_input = st.text_area(
    "Competitor Website URLs Enter Karein (Har line par ek URL dalein):", 
    value="https://books.toscrape.com/",
    height=100
)

if st.button("Run War-Room Analysis", type="primary"):
    url_list = [u.strip() for u in urls_input.splitlines() if u.strip()]
    
    if url_list:
        scraped_data_list = []
        with st.spinner(f"1. Playwright {len(url_list)} website(s) scrape kar raha hai..."):
            for u in url_list:
                res = asyncio.run(scrape_competitor(u))
                if res:
                    scraped_data_list.append(res)
                    st.success(f"✓ Scraped: **{res['title']}** ({res['url']})")
        
        if scraped_data_list:
            with st.spinner("2. Gemini AI Comparative Strategic Report Generate Kar Raha Hai..."):
                report = analyze_with_gemini(scraped_data_list)
            
            if report:
                st.markdown("---")
                st.header("📊 Strategic Intelligence Report")
                st.markdown(report)
                
                # Feature 1: PDF Export Download Button
                pdf_bytes = create_pdf(report)
                st.download_button(
                    label="📥 Download Strategic Report (PDF)",
                    data=pdf_bytes,
                    file_name="Competitor_WarRoom_Report.pdf",
                    mime="application/pdf"
                )
    else:
        st.warning("Meherbani karke kam se kam ek valid URL enter karein.")