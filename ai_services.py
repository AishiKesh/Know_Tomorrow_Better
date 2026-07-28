import os
import io
import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from market_trends import extract_market_context
from system_prompts import build_system_instruction


def run_astrological_chat(user_name: str, user_query: str, history_list: list, natal_metrics: dict) -> str:
    """Handles conversation payloads and interacts with Groq API using key from .env."""
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or not api_key.strip():
        raise ValueError("API Key missing! Please ensure GROQ_API_KEY is correctly defined in your .env file.")

    tool_context = extract_market_context(user_query)

    system_instruction = build_system_instruction(user_name, natal_metrics)

    llm = ChatGroq(
        groq_api_key=api_key.strip(),
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )

    messages = [
        SystemMessage(content=system_instruction)
    ]

    for msg in history_list:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    # Append current incoming user query along with market analytics context
    full_prompt = f"{user_query}\n\n[Market Analytics Context]:\n{tool_context}" if tool_context else user_query
    messages.append(HumanMessage(content=full_prompt))

    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"


def generate_astrology_pdf(user_name: str, natal_data: dict, chat_response: str) -> bytes:
    """Generates a styled PDF document in memory and returns raw bytes for Streamlit download."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1E1E2F"), spaceAfter=12)
    meta_style = ParagraphStyle('MetaText', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor("#555555"), spaceAfter=8)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=8)

    story = [
        Paragraph("<b> AstroGraph AI Advisory Report</b>", title_style),
        Paragraph(f"<b>Client Name:</b> {user_name} | <b>Date:</b> {datetime.date.today().strftime('%B %d, %Y')}", meta_style),
        Paragraph(f"<b>Sun Sign:</b> {natal_data.get('sun_sign', 'N/A')} | <b>Moon Sign:</b> {natal_data.get('moon_sign', 'N/A')}", meta_style),
        Spacer(1, 15)
    ]

    formatted_text = chat_response.replace("\n", "<br/>")
    story.append(Paragraph(formatted_text, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()