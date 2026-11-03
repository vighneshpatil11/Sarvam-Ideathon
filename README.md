<div align="center">

<img src="frontend/public/logo.svg" width="72" alt="SAARTHI Logo"/>

# 🇮🇳 SAARTHI — सारथी

### *Multilingual AI Voice Assistant for Maharashtra Government Services*

**Built for the Sarvam AI Ideathon 2026**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://sarvam-ideathon.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-Sarvam--Ideathon-181717?style=for-the-badge&logo=github)](https://github.com/vighneshpatil11/Sarvam-Ideathon)
[![Sarvam AI](https://img.shields.io/badge/Powered%20By-Sarvam%20AI-6C63FF?style=for-the-badge)](https://sarvam.ai)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

</div>

---

## 🎯 Problem Statement

More than **3 crore citizens** interact with the Maharashtra Government's **Aaple Sarkar** portal annually — seeking certificates, ration cards, land records, and welfare schemes. Yet most of them:

- ❌ Don't know **which documents** to bring
- ❌ Don't know the **exact fee** (and overpay agents)
- ❌ Can't read government websites in **their native Marathi**
- ❌ Have **no voice-first option** for illiterate or elderly citizens

**SAARTHI** solves all of this — with a single voice conversation.

---

## 💡 What is SAARTHI?

SAARTHI (*सारथी* — Hindi/Marathi for "guide") is an **AI-powered voice and chat assistant** that helps any Maharashtra citizen navigate government services in **English, Marathi, or Hindi** — just by speaking.

```
🎙️  Citizen says: "उत्पन्नाच्या दाखल्यासाठी किती शुल्क लागते?"
🤖  SAARTHI says: "उत्पन्न प्रमाणपत्रासाठी अधिकृत शासकीय शुल्क ₹३३.६० आहे.
                   हा दाखला आपले सरकार पोर्टलवर अर्ज केल्यानंतर
                   RTS कायद्यानुसार १५ कामकाजाच्या दिवसांत मिळतो."
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎙️ **Voice Input (STT)** | Speak naturally in Marathi, Hindi, or English via **Sarvam Saaras v3** |
| 🔊 **Voice Output (TTS)** | AI replies read aloud in natural Marathi voice via **Sarvam Bulbul v3** |
| 🤖 **AI Brain** | **Sarvam 105B Conversations** model with grounded, verified government knowledge |
| 🧠 **Conversation Memory** | Remembers the last 6 turns — ask follow-up questions naturally |
| 📋 **30 Government Services** | Complete database of Aaple Sarkar submission services with verified RTS Act fees & timelines |
| 🌐 **Trilingual** | Full English / मराठी / हिन्दी support across UI and AI responses |
| ⚡ **Rate-Limited Audio** | Visual loading bar prevents duplicate TTS requests |
| 📱 **Mobile-First Design** | Responsive UI built with Tailwind CSS |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Vercel (Production)                   │
│                                                             │
│  ┌──────────────────────┐     ┌──────────────────────────┐  │
│  │   Frontend Service   │────▶│    Backend Service       │  │
│  │   Next.js 15 / React │     │    FastAPI + SQLite       │  │
│  │                      │     │                          │  │
│  │  /api/stt  ──────────┼─────┼──▶ Sarvam Saaras v3 STT │  │
│  │  /api/tts  ──────────┼─────┼──▶ Sarvam Bulbul v3 TTS │  │
│  │  /         (UI)      │     │                          │  │
│  └──────────────────────┘     └──────────────────────────┘  │
│           │                              │                   │
│           │     BACKEND_SERVICE_URL      │                   │
│           └──────── (binding) ───────────┘                   │
└─────────────────────────────────────────────────────────────┘
                              │
               ┌──────────────▼──────────────┐
               │       Sarvam AI APIs         │
               │  • sarvam-105b-conversations │
               │  • saaras:v3  (STT)          │
               │  • bulbul:v3  (TTS)          │
               └─────────────────────────────┘
```

### Backend Flow (per question)

```
User Question
    │
    ▼
Keyword Retriever ──▶ Matches service in SQLite DB (30 services)
    │
    ▼
Context Builder ──▶ Extracts: fee, days, documents, steps
    │
    ▼
Prompt Builder ──▶ System prompt + verified facts + chat history (last 6 turns)
    │
    ▼
Sarvam 105B ──▶ Generates grounded, language-appropriate answer
    │
    ▼
JSON Response ──▶ { answer, session_id, sources, related_services }
```

---

## 📂 Project Structure

```
saarthi/
├── 📁 backend/                   # FastAPI Python backend
│   ├── main.py                   # Vercel entrypoint
│   └── app/
│       ├── api/                  # Route handlers (assistant, services, search…)
│       ├── ai/                   # Sarvam 105B provider + local fallback
│       ├── knowledge/            # Keyword-based context retriever
│       ├── prompts/              # System prompt builder
│       ├── models/               # SQLAlchemy ORM models
│       ├── schemas/              # Pydantic request/response schemas
│       └── seed.py               # Auto-seeds 30 Aaple Sarkar services on boot
│
├── 📁 frontend/                  # Next.js 15 / React 19 frontend
│   └── src/
│       ├── app/                  # App Router pages (/, /services, /assistant…)
│       ├── components/           # AssistantWidget, Header, ServiceCard…
│       ├── lib/api/              # Typed API client (assistant, STT, TTS…)
│       └── i18n/                 # Translations (en / mr / hi)
│
├── 📁 database/seeds/            # Seed scripts for 30 services
├── vercel.json                   # Multi-service Vercel deployment config
└── docker-compose.yml            # Local dev (optional)
```

---

## 🗂️ Government Services Database

SAARTHI includes **30 core Maharashtra Aaple Sarkar services** with verified data from the Maharashtra RTS Act:

<details>
<summary>Click to expand all 30 services</summary>

| # | Service | Fee (₹) | RTS Days |
|---|---------|---------|----------|
| 1 | Income Certificate | ₹33.60 | 15 days |
| 2 | Caste Certificate | ₹40.00 | 21 days |
| 3 | Non-Creamy Layer Certificate | ₹50.00 | 21 days |
| 4 | Domicile Certificate | ₹33.60 | 15 days |
| 5 | Age, Nationality & Domicile Certificate | ₹33.60 | 15 days |
| 6 | Birth Certificate | ₹25.00 | 7 days |
| 7 | Death Certificate | ₹25.00 | 7 days |
| 8 | Marriage Certificate | ₹100.00 | 15 days |
| 9 | Senior Citizen Certificate | ₹0.00 | 15 days |
| 10 | Disability Certificate | ₹0.00 | 30 days |
| 11 | Residence Certificate | ₹33.60 | 15 days |
| 12 | Character Certificate | ₹0.00 | 21 days |
| 13 | Solvency Certificate | ₹100.00 | 30 days |
| 14 | Agriculturist Certificate | ₹33.60 | 15 days |
| 15 | Landless Labourer Certificate | ₹33.60 | 15 days |
| 16 | Below Poverty Line (BPL) Certificate | ₹0.00 | 30 days |
| 17 | Ration Card – New Application | ₹2.00 | 30 days |
| 18 | Ration Card – Name Addition | ₹2.00 | 15 days |
| 19 | Ration Card – Name Deletion | ₹0.00 | 15 days |
| 20 | Ration Card – Address Change | ₹2.00 | 15 days |
| 21 | Shop & Establishment Registration | ₹100.00 | 3 days |
| 22 | Temporary Residence Certificate | ₹33.60 | 7 days |
| 23 | Small Landholder Certificate | ₹33.60 | 15 days |
| 24 | Widow Certificate | ₹0.00 | 15 days |
| 25 | Legal Heir Certificate | ₹33.60 | 30 days |
| 26 | Duplicate Birth Certificate | ₹50.00 | 7 days |
| 27 | Duplicate Death Certificate | ₹50.00 | 7 days |
| 28 | Nationality Certificate | ₹33.60 | 15 days |
| 29 | Permission for Tree Cutting | ₹200.00 | 30 days |
| 30 | Land Record Certified Copy (7/12) | ₹15.00 | 7 days |

</details>

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Sarvam AI API Key → [Get one at sarvam.ai](https://sarvam.ai)

### 1. Clone the repository

```bash
git clone https://github.com/vighneshpatil11/Sarvam-Ideathon.git
cd Sarvam-Ideathon
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set SARVAM_API_KEY=your_key_here

# Run the server (auto-seeds database on first start)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be live at: `http://localhost:8000`
API Docs (Swagger): `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Configure environment
cp .env.example .env.local
# Edit .env.local:
#   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
#   NEXT_PUBLIC_DEMO_MODE=false

# Start dev server
npm run dev
```

Frontend will be live at: `http://localhost:3000`

---

## 🌐 Deployment (Vercel)

This project is configured for **Vercel multi-service deployment** out of the box.

### Environment Variables to set in Vercel Dashboard

| Variable | Value |
|---|---|
| `SARVAM_API_KEY` | Your Sarvam API key |
| `NEXT_PUBLIC_DEMO_MODE` | `false` |

The `vercel.json` handles everything else — routing, bindings, and build commands automatically.

---

## 🎙️ Sarvam AI Integration

| Capability | Model | Usage |
|---|---|---|
| **Chat / AI Brain** | `sarvam-105b-conversations` | Answers questions about government services with grounded context |
| **Speech-to-Text** | `saaras:v3` | Transcribes citizen's voice in Marathi / Hindi / English |
| **Text-to-Speech** | `bulbul:v3` | Reads AI responses aloud (speaker: `rupali` for Marathi) |

### How the AI stays accurate

1. **Keyword Retriever** matches the query against 30 known services using English + Marathi keywords
2. **Verified Facts** (fee, days, documents, steps) are extracted from the SQLite database and injected into the prompt
3. **Sarvam 105B** generates a natural, complete answer grounded in these facts
4. **Conversation History** (last 6 turns) is sent with every request so citizens can ask follow-up questions naturally

---

## 💬 Example Conversations

**English:**
> 🧑 *"What documents do I need for a Caste Certificate?"*
> 🤖 *"For a Caste Certificate in Maharashtra, you need: Proof of Identity (Aadhaar/Voter ID), Proof of Address, Old school leaving certificate or family records proving caste, and a Self-declaration affidavit. The official fee is ₹40.00 and delivery is guaranteed within 21 working days under the RTS Act."*

**Marathi:**
> 🧑 *"रेशन कार्डसाठी किती दिवस लागतात?"*
> 🤖 *"नवीन रेशन कार्ड अर्जासाठी महाराष्ट्र लोकसेवा हमी कायद्यानुसार विहित मुदत ३० कामकाजाचे दिवस आहे. अधिकृत शुल्क केवळ ₹२.०० आहे."*

**Follow-up (Memory Demo):**
> 🧑 *"What is the fee?"* → 🤖 answers about Caste Certificate (remembers context)
> 🧑 *"And the documents?"* → 🤖 still answers about Caste Certificate ✅

---

## 🛡️ Security & Privacy

- ✅ No `.env` or API keys committed to Git (`.gitignore` enforced)
- ✅ SQLite database file excluded from repository
- ✅ Voice audio is processed in-memory and never stored
- ✅ CORS properly configured for production domain

---

## 👥 Team

**Vighnesh Patil** — Full-Stack Developer  
Maharashtra, India  
GitHub: [@vighneshpatil11](https://github.com/vighneshpatil11)

---

## 📄 License

MIT License — open for educational and civic use.

---

<div align="center">

**Made with ❤️ for the citizens of Maharashtra**

*"Every citizen deserves a guide — SAARTHI is that guide."*

</div>
