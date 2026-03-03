import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Phase 1: Environment Setup
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_ID = 'gemini-3-flash-preview'

# Phase 2: Knowledge Base Design
KNOWLEDGE_BASE = [
    {
        "id": "kb-001",
        "title": "Password Reset Guide",
        "keywords": ["password", "reset", "login", "access", "forgot", "account"],
        "content": "To reset your password, navigate to the login page and click 'Forgot Password'. Enter your registered email address, and we will send you a secure link to create a new password."
    },
    {
        "id": "kb-002",
        "title": "Refund Policy",
        "keywords": ["refund", "money", "return", "charge", "billing", "cancel"],
        "content": "Our refund policy allows for full refunds within 30 days of the original purchase date. To request a refund, go to your Billing Dashboard, select the transaction, and click 'Request Refund'."
    },
    {
        "id": "kb-003",
        "title": "API Rate Limits",
        "keywords": ["api", "rate", "limit", "429", "developer", "throttle", "requests"],
        "content": "The standard API rate limit is 1,000 requests per minute per IP address. If you exceed this limit, you will receive a 429 Too Many Requests response."
    }
]

# Phase 3: Persona Detector Schema
class PersonaInsights(BaseModel):
    persona: str = Field(description="The user persona, e.g., Technical, Beginner, Frustrated, Neutral, Urgent")
    sentiment: str = Field(description="The user sentiment, e.g., Positive, Negative, Neutral, Angry")
    requiresEscalation: bool = Field(description="True if the message requires immediate human escalation")
    reasoning: str = Field(description="Brief reasoning for the classification")

def detect_persona(message: str) -> PersonaInsights:
    prompt = f'Analyze the following customer message. Determine their persona, sentiment, and if it requires immediate human escalation (e.g., threats, extreme anger, or explicit requests for a human).\n\nMessage: "{message}"'
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PersonaInsights,
            temperature=0.1
        ),
    )
    # Parse the JSON string back into our Pydantic model
    return PersonaInsights.model_validate_json(response.text)

# Phase 4: KB Retriever
def retrieve_kb(message: str):
    lower_msg = message.lower()
    best_match = None
    highest_score = 0
    
    for article in KNOWLEDGE_BASE:
        score = sum(1 for kw in article["keywords"] if kw in lower_msg)
        if score > highest_score:
            highest_score = score
            best_match = article
            
    return best_match if highest_score > 0 else None

# Phase 5 & 6: Response Generator & Escalation Logic
def generate_response(message: str, insights: PersonaInsights, kb_article: dict, chat_history: list) -> str:
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history])
    
    kb_context = f"Title: {kb_article['title']}\nContent: {kb_article['content']}" if kb_article else "No relevant knowledge base articles found."
    escalation_note = "IMPORTANT: This user requires human escalation. Acknowledge their frustration and inform them you are transferring them to a human agent immediately." if insights.requiresEscalation else ""

    system_instruction = f"""You are a helpful customer support agent. 
Your current customer has the following persona: {insights.persona} and sentiment: {insights.sentiment}.
Adapt your tone to match their persona.
If they are technical, use technical terms. If beginner, avoid jargon. If frustrated, be empathetic.

Use the following knowledge base article to answer their question:
{kb_context}

{escalation_note}

Chat History for context:
{history_text}
"""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )
    )
    return response.text

def generate_escalation_summary(chat_history: list) -> str:
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history])
    prompt = f"Summarize this chat log for a human support agent who is taking over. Include the user's main issue, emotional state, and what has been discussed.\n\nChat Log:\n{history_text}"
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

# Phase 7: Streamlit UI
st.set_page_config(page_title="AI Support Agent", page_icon="🤖", layout="wide")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your Support Agent. How can I help you today?"}]
if "insights" not in st.session_state:
    st.session_state.insights = None
if "kb_match" not in st.session_state:
    st.session_state.kb_match = None
if "summary" not in st.session_state:
    st.session_state.summary = None

# UI Layout: Main Chat (Left) and Agent Insights (Right Sidebar)
st.title("🤖 Adaptive Support Agent")

# Sidebar: Agent Insights
with st.sidebar:
    st.header("🧠 Agent Insights")
    st.divider()
    
    if st.session_state.insights:
        st.subheader("👤 Persona Detector")
        st.info(f"**Persona:** {st.session_state.insights.persona}\n\n**Sentiment:** {st.session_state.insights.sentiment}")
        st.caption(f"**Reasoning:** {st.session_state.insights.reasoning}")
        
        st.divider()
        st.subheader("📚 KB Retriever")
        if st.session_state.kb_match:
            st.success(f"**Matched Article:** {st.session_state.kb_match['title']}")
            st.caption(st.session_state.kb_match['content'])
        else:
            st.warning("No relevant KB article found.")
            
        st.divider()
        st.subheader("⚠️ Escalation Logic")
        if st.session_state.insights.requiresEscalation:
            st.error("🚨 STATUS: ESCALATION TRIGGERED")
            if st.session_state.summary:
                st.markdown("**Handoff Summary Generated:**")
                st.write(st.session_state.summary)
        else:
            st.success("✅ STATUS: NORMAL")
    else:
        st.write("Waiting for user input...")

# Main Chat Interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message here..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Agent is thinking..."):
        # 1. Detect Persona
        insights = detect_persona(prompt)
        st.session_state.insights = insights
        
        # 2. Retrieve KB
        kb_match = retrieve_kb(prompt)
        st.session_state.kb_match = kb_match
        
        # 3. Generate Response
        response_text = generate_response(prompt, insights, kb_match, st.session_state.messages)
        
        # 4. Handle Escalation
        if insights.requiresEscalation:
            st.session_state.summary = generate_escalation_summary(st.session_state.messages)
        else:
            st.session_state.summary = None

    # Add assistant response to state and display
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)
    
    # Force a rerun to update the sidebar immediately
    st.rerun()