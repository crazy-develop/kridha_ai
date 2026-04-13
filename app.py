import streamlit as st
import uuid
from hindsight_client import Hindsight
from groq import Groq

# Configure Page
st.set_page_config(page_title="Kridha Workspace", page_icon="🏢", layout="centered")

# Custom CSS for Premium Professional Look
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* Elegant Dark Background */
.stApp {
    background: #0f1115;
    background-image: radial-gradient(circle at 50% 0%, #1e222d 0%, #0f1115 70%);
}

/* Professional Typography Title */
h1 {
    text-align: center;
    font-size: 2.2rem !important;
    color: #f8fafc !important;
    margin-bottom: 2rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.5px;
    animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Smooth Fade-in Messages */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    animation: fadeInMessage 0.4s ease-out forwards;
    background: #191c24;
    border: 1px solid #2a2f3a;
    line-height: 1.6;
    font-size: 0.95rem;
    color: #e2e8f0;
    box-shadow: none !important;
}

@keyframes fadeInMessage {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Input field */
[data-testid="stChatInput"] {
    background: #191c24 !important;
    border-radius: 8px !important;
    border: 1px solid #333947 !important;
    padding: 2px !important;
    transition: all 0.2s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 1px #6366f1 !important;
}

/* Custom Sleek Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: #333947;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: #4b5563; }

[data-testid="stHeader"] { background: transparent !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Keys
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BANK_NAME = "hacathon"

# Clients
client = Hindsight(api_key=HINDSIGHT_API_KEY, base_url="https://api.hindsight.vectorize.io")
groq_client = Groq(api_key=GROQ_API_KEY)

st.title("🏢 Kridha Workspace")

# Chat History State Management
if "chats" not in st.session_state:
    st.session_state.chats = {"Session 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Session 1"

def create_new_chat():
    new_chat_name = f"Session {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat_name] = []
    st.session_state.current_chat = new_chat_name

# --- Sidebar Features ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #f8fafc; font-weight: 500;'>Workspace Menu</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("➕ New Chat", use_container_width=True):
        create_new_chat()
        st.rerun()
        
    st.markdown("### 🗂️ Chat History")
    for chat_name in list(st.session_state.chats.keys()):
        if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown("---")
    
    current_messages = st.session_state.chats[st.session_state.current_chat]
    
    # Feature 2: Download Chat
    if current_messages:
        chat_text = "\n\n".join(
            [f"User: {m['content']}" if m['role'] == 'user' else f"Kridha: {m['content']}" for m in current_messages]
        )
        st.download_button(
            label="📥 Export Chat",
            data=chat_text,
            file_name=f"{st.session_state.current_chat.replace(' ', '_')}_history.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("<h3 style='text-align: center; font-size: 1rem; color: #94a3b8;'>Quick Inquiries</h3>", unsafe_allow_html=True)
    
    # Feature 3: Quick Prompts based on FAQ data
    faq_1 = st.button("📦 Return policy details?", use_container_width=True)
    faq_2 = st.button("📞 Support team contact?", use_container_width=True)
    faq_3 = st.button("💳 Allowed payment methods?", use_container_width=True)

# Main Chat Rendering
for message in st.session_state.chats[st.session_state.current_chat]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main Input
prompt = st.chat_input("How can I assist you today?")

# Override prompt if a quick FAQ button was clicked
if faq_1: prompt = "What is your return policy?"
if faq_2: prompt = "How can I contact support?"
if faq_3: prompt = "What payment methods do you accept?"

if prompt:
    st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Analyzing..."):
        recall_results = client.recall(query=prompt, bank_id=BANK_NAME)
        
        context = ""
        if recall_results:
            context = "\n".join([r.text for r in recall_results])

        # Professional prompt
        system_prompt = (
            "You are Kridha Assistant, a highly professional corporate AI. "
            "Communicate in a refined, courteous, and efficient manner. "
            "Use minimal but appropriate professional emojis (like ✅, 📊, 📝). "
            "Ensure formatting is structured, use bullet points where necessary. "
            "Provide brief, accurate answers without unnecessary conversational filler. "
            "If greeted, respond formally: 'Hello. How may I assist you today?' "
            f"\n\nContext Database Matches: {context}"
        )

        llm_messages = [{"role": "system", "content": system_prompt}] + st.session_state.chats[st.session_state.current_chat]
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=llm_messages
        )
        answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": answer})