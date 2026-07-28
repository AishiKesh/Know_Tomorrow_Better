import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from astronomy_engine import calculate_astronomy_engine 
from ai_services import run_astrological_chat, generate_astrology_pdf
load_dotenv()

st.set_page_config(page_title="Know Tomorrow Better", page_icon="logo.png", layout="wide")
st.markdown("""
<style>
    /* Main App Background & Default Text */
    .stApp {
        background: linear-gradient(135deg, #0d0f18 0%, #131726 50%, #0a0c14 100%);
        color: #ffffff !important;
    }

    /* Fix Sidebar Title & Label Visibility */
    section[data-testid="stSidebar"] {
        background-color: #111422 !important;
        border-right: 1px solid rgba(147, 51, 234, 0.3);
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Fix Input Box Labels */
    .stTextInput > label, .stDateInput > label, .stTimeInput > label {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* Card Containers for Metric Info */
    .astro-card {
        background: rgba(22, 27, 46, 0.85);
        border: 1px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    
    .astro-card-title {
        color: #c084fc !important;
        font-size: 0.85rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .astro-card-value {
        color: #ffffff !important;
        font-size: 1.3rem;
        font-weight: 800;
    }

    /* Custom Header Banner */
    .hero-header {
        background: linear-gradient(90deg, rgba(147, 51, 234, 0.25) 0%, rgba(59, 130, 246, 0.25) 100%);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff !important;
        margin: 0;
    }

    .hero-subtitle {
        color: #cbd5e1 !important;
        font-size: 0.95rem;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Chat Message Bubbles & Text Visibility Fix */
    div[data-testid="stChatMessage"] {
        background-color: rgba(22, 27, 46, 0.85) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }

    /* Chat Message Paragraph Text */
    div[data-testid="stChatMessage"] p {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }

    /* FIX FOR HEADINGS INSIDE CHATBOT MESSAGES */
    div[data-testid="stChatMessage"] h1,
    div[data-testid="stChatMessage"] h2,
    div[data-testid="stChatMessage"] h3,
    div[data-testid="stChatMessage"] h4 {
        color: #c084fc !important;
        font-weight: 800 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        margin-top: 14px !important;
        margin-bottom: 8px !important;
        font-size: 1.25rem !important;
    }

    /* FIX FOR BOLD TEXT INSIDE CHAT MESSAGES */
    div[data-testid="stChatMessage"] strong,
    div[data-testid="stChatMessage"] b {
        color: #60a5fa !important;
        font-weight: 800 !important;
    }

    /* Chat Input Bar Accent */
    .stChatInputContainer {
        border-radius: 14px !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        background-color: #111422 !important;
    }

    /* Download Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #7e22ce 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(126, 34, 206, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

api_key = os.getenv("GROQ_API_KEY")

st.sidebar.title("Fill in the details")
name = st.sidebar.text_input("Full Name", value="Alex Doe")
birth_date = st.sidebar.date_input("Birth Date", value=datetime.date(2001, 4, 12))
birth_time = st.sidebar.time_input("Birth Time", value=datetime.time(14, 30))
birth_loc = st.sidebar.text_input("Birth Location", value="New York, NY")

st.sidebar.markdown("---")
st.sidebar.subheader(" Calculated Coordinates")

# Run calculation engine
calculated_data = calculate_astronomy_engine(birth_date, birth_time)

# Render Sun & Moon signs inside styled high-contrast dark cards
sun_sign = calculated_data.get('sun_sign', 'N/A')
moon_sign = calculated_data.get('moon_sign', 'N/A')

st.sidebar.markdown(f"""
<div class="astro-card">
    <div class="astro-card-title"> Sun Sign</div>
    <div class="astro-card-value">{sun_sign}</div>
</div>
<div class="astro-card">
    <div class="astro-card-title"> Moon Sign</div>
    <div class="astro-card-value">{moon_sign}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader(" Active Cosmic Transits")

# Render active transits grouped by category
if 'transits' in calculated_data and calculated_data['transits']:
    for transit in calculated_data['transits']:
        t_lower = transit.lower()
        if "financial" in t_lower or "expansion" in t_lower or "house" in t_lower:
            st.sidebar.markdown(f" **Finance:** `{transit}`")
        elif "health" in t_lower or "vitality" in t_lower or "scorpio" in t_lower:
            st.sidebar.markdown(f" **Health & Energy:** `{transit}`")
        elif "education" in t_lower or "intellectual" in t_lower or "focus" in t_lower:
            st.sidebar.markdown(f" **Education & Focus:** `{transit}`")
        else:
            st.sidebar.markdown(f"- `{transit}`")



tracking_key = f"{name}_{birth_date}_{birth_time}"
if "user_tracking_key" not in st.session_state or st.session_state.user_tracking_key != tracking_key:
    st.session_state.user_tracking_key = tracking_key
    st.session_state.chat_history = [] 


# 3. CHAT INTERFACE & HERO HEADER
st.markdown(f"""
<div class="hero-header">
    <div class="hero-title"> Know Tomorrow Better</div>
    <div class="hero-subtitle">Interactive Celestial Intelligence & Natal Analysis</div>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.chat_history) == 0:
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": f"**Hello {name}!** I have mapped your cosmic coordinates. What aspect of your health transitions, education, relationships, or financial expansions shall we look into today?"
    })

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if current_user_prompt := st.chat_input("Ask about your health vitality, exam preparation focus, or financial expansions..."):
    if not api_key or not api_key.strip():
        st.error("⚠️ Environment Error: GROQ_API_KEY is missing from your .env file.")
    else:
        with st.chat_message("user"):
            st.markdown(current_user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": current_user_prompt})
            
        with st.chat_message("assistant"):
            with st.spinner("Processing deep cosmic vectors via Groq Cloud API..."):
                try:
                    bot_reply = run_astrological_chat(
                        user_name=name,
                        user_query=current_user_prompt,
                        history_list=st.session_state.chat_history[:-1], 
                        natal_metrics=calculated_data
                    )
                    st.markdown(bot_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
                    
                    # Dynamic PDF export generation
                    pdf_bytes = generate_astrology_pdf(name, calculated_data, bot_reply)
                    st.download_button(
                        label=" Download Reading as PDF",
                        data=pdf_bytes,
                        file_name=f"AstroInsight_{name.replace(' ', '_')}_Report.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as error_msg:
                    st.error(f"Execution Error Encountered: {error_msg}")