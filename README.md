
# 🤖 Adaptive AI Support Agent

### LLM-Powered Customer Support Automation with Persona Detection & Smart Escalation

An intelligent, production-style customer support assistant built using **Google Gemini + Streamlit** that goes beyond basic chatbots.

This system dynamically:

* Detects user persona & sentiment
* Retrieves contextual knowledge base articles
* Adapts tone based on user type
* Automatically escalates high-risk conversations to human agents
* Generates structured handoff summaries

Designed to demonstrate **LLM orchestration, structured output validation, and human-in-the-loop AI systems**.

---

## 🚀 Why This Project Matters

Traditional chatbots:

* Give static responses
* Ignore emotional context
* Fail at safe escalation

This system solves that by introducing:

* **Persona-aware response adaptation**
* **Structured LLM outputs using Pydantic**
* **Escalation detection with automated handoff summaries**
* **Real-time agent insight dashboard**

It simulates a real-world AI support system used in SaaS companies.

---

## 🏗️ System Architecture

```
User Input
   ↓
Persona & Sentiment Detection (Gemini + JSON Schema)
   ↓
Knowledge Base Retrieval (Keyword Scoring)
   ↓
Adaptive Response Generator (Context + Tone Control)
   ↓
Escalation Decision Engine
   ↓
Human Handoff Summary (if required)
   ↓
Streamlit UI (Chat + Live Agent Insights)
```

---

## 🧠 Core Capabilities

### 1️⃣ Persona & Sentiment Detection

* Structured JSON output using **Pydantic schema**
* Classifies:

  * Persona (Technical, Beginner, Frustrated, Urgent, etc.)
  * Sentiment (Positive, Neutral, Angry)
  * Escalation necessity
* Low temperature inference for classification reliability

---

### 2️⃣ Adaptive Tone Engineering

* Dynamically modifies system instructions
* Technical users → detailed explanation
* Beginners → simplified language
* Frustrated users → empathetic tone

Demonstrates advanced **prompt conditioning techniques**.

---

### 3️⃣ Knowledge Base Retrieval Engine

* Lightweight keyword scoring algorithm
* Returns most relevant article
* Clean modular retriever design (easy to upgrade to RAG)

---

### 4️⃣ Smart Escalation System

Triggers escalation when:

* Explicit request for human agent
* Extreme anger or frustration
* Urgent or high-risk queries

When triggered:

* Flags conversation
* Generates structured handoff summary
* Displays escalation status in UI

Simulates real-world **AI + Human hybrid workflows**.

---

## 🛠 Tech Stack

| Component         | Technology                             |
| ----------------- | -------------------------------------- |
| LLM               | Google Gemini (gemini-3-flash-preview) |
| UI                | Streamlit                              |
| Schema Validation | Pydantic                               |
| Environment       | python-dotenv                          |
| Language          | Python 3                               |

---

## 📊 Engineering Highlights

* Structured LLM output validation
* Deterministic classification (temperature=0.1)
* Context-aware multi-turn conversation handling
* Session state management
* Clean modular architecture
* Production-style environment variable handling

---

## 🧪 Example Scenarios

### ✅ Normal Query

**Input:**

> "How do I reset my password?"

**System Behavior:**

* Persona: Beginner
* Sentiment: Neutral
* KB Retrieved: Password Reset Guide
* Escalation: No

---

### 🚨 Escalation Scenario

**Input:**

> "This is ridiculous. I want to speak to a human right now."

**System Behavior:**

* Sentiment: Angry
* Escalation: TRUE
* Handoff summary auto-generated
* Sidebar status: 🚨 Escalation Triggered

---

## 📈 Scalability Potential

Can be upgraded with:

* Vector DB (Pinecone/FAISS)
* Semantic embeddings
* CRM integration
* Real-time analytics dashboard
* Multi-language support
* Fine-tuned sentiment model

---

## ⚙️ Installation & Usage
### 1️⃣ Clone the Repository
git clone https://github.com/yourusername/adaptive-support-agent.git
cd adaptive-support-agent
### 2️⃣ Install Dependencies
pip install -r requirements.txt
### 3️⃣ Configure Environment Variables

Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here
### 4️⃣ Run the Application
streamlit run app.py

The app will start locally at:

http://localhost:8501
🏃 One-Line Quick Start (For Reviewers)
pip install -r requirements.txt && streamlit run app.py

---


* 🧠 Turn this into a strong LinkedIn project showcase post
* 📄 Convert it into a portfolio case study format
