import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# Page Config
st.set_page_config(page_title="Competitor War-Room Agent", page_icon="⚔️", layout="wide")

st.title("⚔️ Advanced Competitor War-Room Agent")
st.subheader("Multi-Competitor Scraping, Gemini AI Intelligence & PDF Export")

# Get API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

# PDF Generator Function
def generate_pdf(analysis_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=15
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=8
    )
    
    story = [Paragraph("Competitor Intelligence & War-Room Report", title_style), Spacer(1, 10)]
    
    for paragraph in analysis_text.split('\n'):
        if paragraph.strip():
            clean_p = paragraph.replace('*', '').strip()
            story.append(Paragraph(clean_p, body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer

# Scraper Function
def scrape_competitor(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title and text
        title = soup.title.string.strip() if soup.title and soup.title.string else url
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        # Limit text length for Gemini
        return f"URL: {url}\nTitle: {title}\nContent Snippet: {text[:4000]}"
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# Input Area
urls_input = st.text_area(
    "Competitor Website URLs Enter Karein (Har line par ek URL dalein):",
    value="https://books.toscrape.com/",
    height=120
)

if st.button("Run War-Room Analysis", type="primary"):
    if not api_key:
        st.error("GEMINI_API_KEY Streamlit Secrets mein nahi mili! Baraye meherbani Advanced Settings mein API Key add karein.")
    elif not urls_input.strip():
        st.warning("Baraye meherbani kam az kam ek URL daalain.")
    else:
        urls = [u.strip() for u in urls_input.split('\n') if u.strip()]
        
        with st.spinner("Competitor websites scrape ki ja rahi hain..."):
            scraped_results = []
            for url in urls:
                data = scrape_competitor(url)
                scraped_results.append(data)
                
            combined_context = "\n\n--- COMPETITOR DATA ---\n\n".join(scraped_results)

        with st.spinner("Gemini AI se Strategic War-Room Analysis generate ho raha hai..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                Aap ek Senior Business Intelligence Analyst aur Growth Strategist hain.
                Neeche diye gaye competitor data ka deep strategic analysis karein:
                
                {combined_context}
                
                Mujhe ek detailed War-Room Report bana kar dein jisme yeh sections hoon:
                1. Executive Summary & Value Proposition
                2. Competitor Strengths & Product Offerings
                3. Market Gaps & Weaknesses Identified
                4. Strategic Counter-Attack Strategy & Monetization Recommendations
                
                Report ko clear, professional aur actionable format mein likhein.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                analysis_result = response.text
                
                st.success("War-Room Analysis Complete!")
                st.markdown("---")
                st.markdown(analysis_result)
                
                # PDF Download Button
                pdf_data = generate_pdf(analysis_result)
                st.download_button(
                    label="📄 Download Executive War-Room PDF Report",
                    data=pdf_data,
                    file_name="Competitor_WarRoom_Analysis.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Gemini AI Analysis mein error aaya: {str(e)}")
