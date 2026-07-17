<div align="center">

# 🧠 Market Intelligence Engine

### A Generative AI–Powered Industry Research & Outreach Platform

[![GenAI](https://img.shields.io/badge/Generative_AI-Project-ff6f61?style=for-the-badge&logo=sparkles&logoColor=white)](#-genai-techniques)
[![Gemini](https://img.shields.io/badge/Gemini_2.0-Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Google Search](https://img.shields.io/badge/Google_Search-Grounding-34A853?style=for-the-badge&logo=google&logoColor=white)](#-genai-techniques)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org)
[![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A multi-stage LLM pipeline that takes a single industry name and autonomously discovers 10 prospects, maps decision-makers, and generates personalized outreach — all grounded in live web data via Gemini 2.0 Flash.**

[GenAI Techniques](#-genai-techniques) · [Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Demo](#-live-demo-flow)

---

</div>

## 🎯 The Problem

Marketing and branding agencies spend **5-8 hours manually researching** each new industry vertical — Googling companies, stalking LinkedIn profiles, building spreadsheets, and writing cold emails that feel generic. By the time research is compiled, half the data is already stale.

**MIE replaces this entire workflow with a 6-stage Generative AI pipeline** — using Gemini 2.0 Flash with Google Search Grounding to autonomously discover prospects, find decision-makers, and generate hyper-personalized outreach, all from a single text input.

---

## 🤖 GenAI Techniques

This project demonstrates several advanced Generative AI patterns:

| Technique | How It's Used |
|-----------|---------------|
| **🔍 Search-Grounded Generation** | Every data-fetching LLM call uses Gemini's Google Search Grounding — the model searches the live web before generating, eliminating hallucination of company names, contacts, and events |
| **🔗 Multi-Stage LLM Pipeline** | 6 chained stages where each stage's output feeds the next — brands → events → contacts → activity → personalization → outreach. This is an agentic orchestration pattern. |
| **📋 Structured Output Prompting** | Every prompt enforces a strict JSON schema with field-level instructions. Responses are validated, cleaned, and parsed with fallback handling for malformed LLM output. |
| **🎯 Role-Based Prompt Engineering** | Each stage uses a specialized system persona — *"senior market research analyst"*, *"B2B sales researcher"*, *"outreach copywriter"* — to optimize output quality per task. |
| **🌡️ Temperature Tuning** | Data-fetching calls use `temperature: 0.2` for factual accuracy; creative outreach generation uses `temperature: 0.4` for natural, engaging copy. |
| **⚡ Parallel LLM Execution** | Stages 2-4 (events, contacts, activity) fire 3 Gemini calls simultaneously via `ThreadPoolExecutor` — cutting pipeline time by ~40%. |
| **🔄 Iterative Refinement** | Brand discovery validates count (must be ≥10); stale caches with fewer entries are auto-busted and the LLM is re-queried. |
| **🧩 LLM Output Chaining** | Contact emails discovered in Stage 3 are injected into Stage 5's outreach generation — so `mailto:` links have real `To:` addresses. |
| **🛡️ Graceful Degradation** | If any LLM call fails: retry with backoff → fall back to cache → fall back to demo data → return empty state. The pipeline never crashes. |
| **📡 Real-Time Streaming (SSE)** | LLM results stream to the frontend as each stage completes via Server-Sent Events — users see live progress instead of waiting 90s for a full response. |

## ✨ Features

### 🏢 10-Company Prospect Discovery
- **Live web search** via Gemini + Google Search Grounding — no stale training data
- Exactly **10 verified companies** per industry with multi-axis scoring
- Strategic rationale for each: *"Why StepOne?"* + *"Why Now?"*
- Clickable source URLs to the company's official homepage

### 📅 Industry Event Mapping
- Real, **upcoming conferences and trade shows** discovered via live search
- Cross-referenced with discovered prospects — *"Which brands will be there?"*
- Official event URLs, dates, locations, and strategic attendance recommendations
- Confidence scoring (HIGH / MEDIUM / LOW) with source attribution

### 👤 Decision-Maker & Contact Intelligence
- **2-3 senior stakeholders per brand** — CMO, VP Marketing, Head of Brand, CEO
- Real **LinkedIn profile URLs** (`linkedin.com/in/...`) from live search
- **Email addresses** from company press pages, newsrooms, and contact pages
- One-click **"Search on LinkedIn"** button (searches `Name + Company`) as fallback
- One-click **"Send Email"** button — opens mail client with `To:` pre-filled

### 📨 Personalized Outreach
- **LinkedIn connection messages** — under 300 characters, pitch-hook driven
- **Cold emails** — subject + body + CTA, 120-150 words, zero placeholders
- 3-layer personalization engine:
  - `Layer 1` — Brand context (why StepOne fits)
  - `Layer 2` — Recent activity (what the brand just did)
  - `Layer 3` — Opportunity angle (specific service + pitch hook)
- **`mailto:` deep links** — pre-fills To, Subject, and Body in one click
- **LinkedIn compose links** — message auto-copied to clipboard on click

### 📊 Confidence Scoring & Ranking
- Multi-axis scoring: strategic fit, growth signals, event presence, recent activity
- Prospects ranked by composite score with trust percentage metrics
- Exportable as **JSON**, **CSV**, or **TXT** reports

### 🖥️ Premium UI
- Dark-mode, glassmorphism-inspired interface
- Real-time **SSE streaming** — results appear as each stage completes
- **Presentation Mode** — full-screen view with auto-scroll for live demos
- Responsive sidebar with progress tracking and navigation dots

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React 18 + Vite)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Research  │  │ Settings │  │ Tracking │  │ Presentation  │   │
│  │   Page    │  │   Page   │  │Dashboard │  │    Mode       │   │
│  └────┬─────┘  └──────────┘  └──────────┘  └───────────────┘   │
│       │ SSE Stream                                               │
├───────┼─────────────────────────────────────────────────────────┤
│       ▼           BACKEND (Flask + Python 3.10+)                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Industry Orchestrator                       │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │  Brand   │  │  Event   │  │ Contact  │  ← Parallel  │    │
│  │  │Discovery │  │Discovery │  │Discovery │    Execution  │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │    │
│  │       │              │              │                    │    │
│  │  ┌────▼──────────────▼──────────────▼─────┐             │    │
│  │  │         Recent Activity Service         │             │    │
│  │  └────────────────┬───────────────────────┘             │    │
│  │                   ▼                                      │    │
│  │  ┌─────────────────────────────────────┐                │    │
│  │  │    Personalization + Outreach Gen    │                │    │
│  │  └────────────────┬────────────────────┘                │    │
│  │                   ▼                                      │    │
│  │  ┌─────────────────────────────────────┐                │    │
│  │  │   Confidence Scoring & Ranking      │                │    │
│  │  └─────────────────────────────────────┘                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
├──────────────────────────────┼───────────────────────────────────┤
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │       Gemini 2.0 Flash + Google Search Grounding        │    │
│  │       (Live web search • Low temperature 0.2)           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline Stages

| Stage | Service | Execution | Time |
|:-----:|---------|:---------:|:----:|
| **1** | `BrandDiscoveryService` — 10 companies with scoring | Sequential | ~20s |
| **2** | `EventDiscoveryService` — upcoming industry events | ┐ | |
| **3** | `ContactDiscoveryService` — stakeholders + LinkedIn/email | ├ Parallel | ~30s |
| **4** | `RecentActivityService` — latest news per brand | ┘ | |
| **5** | `OutreachGeneratorService` — LinkedIn + email drafts | Sequential | ~15s |
| **6** | `ConfidenceScoringService` — rank & score all prospects | Local | <1s |

**Total pipeline time: ~60-90 seconds** depending on API response times.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Gemini API Key](https://aistudio.google.com/app/apikey) (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/market-intelligence-engine.git
cd market-intelligence-engine
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

```env
GEMINI_API_KEY=your_key_here
SECRET_KEY=change-this-in-production
PORT=4000
FLASK_ENV=development
```

```bash
python app.py
# ✅ Backend running at http://localhost:4000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# ✅ Frontend running at http://localhost:3000
```

### 4. Open the App

Navigate to **http://localhost:3000** → Go to **Settings** → Enter your Gemini API key → Switch to **Industry Mode** → Type any industry → Click **Run Pipeline ↗**

---

## 📁 Project Structure

```
mie_project/
├── backend/
│   ├── app.py                          # Flask entry point
│   ├── .env                            # Environment variables
│   ├── requirements.txt                # Python dependencies
│   ├── routes/
│   │   ├── intelligence.py             # /api/intelligence/* endpoints
│   │   ├── outreach.py                 # /api/outreach/* endpoints
│   │   └── tracking.py                 # /api/tracking/* endpoints
│   └── services/
│       ├── industry_orchestrator.py    # 🎯 Core pipeline orchestrator
│       ├── gemini.py                   # Gemini API wrapper + prompts
│       ├── brand_discovery.py          # Stage 1: 10-brand discovery
│       ├── event_discovery.py          # Stage 2: Event mapping
│       ├── contact_discovery.py        # Stage 3: Contact intelligence
│       ├── recent_activity.py          # Stage 4: Brand news/signals
│       ├── outreach_generator.py       # Stage 5: Outreach generation
│       ├── personalization.py          # Opportunity angle synthesis
│       ├── confidence_scoring.py       # Stage 6: Scoring & ranking
│       ├── cache_service.py            # In-memory cache (6hr TTL)
│       ├── store.py                    # Session & campaign storage
│       ├── json_utils.py              # LLM JSON response cleaning
│       └── demo_mode.py               # Demo safe mode fallback data
├── frontend/
│   ├── src/
│   │   ├── App.jsx                     # Root component + routing
│   │   ├── pages/
│   │   │   ├── Research.jsx            # 🎯 Main research interface
│   │   │   ├── Settings.jsx            # API key + agency config
│   │   │   └── Tracking.jsx            # Campaign tracking dashboard
│   │   └── styles/
│   │       └── global.css              # Design system + animations
│   ├── package.json
│   └── vite.config.js
├── presentation.html                   # HTML slide deck for demos
└── README.md
```

---

## 📡 API Reference

### Intelligence

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `POST` | `/api/intelligence/run` | Company deep-dive (11-section SSE stream) |
| `POST` | `/api/intelligence/run_industry` | **Industry discovery** (6-stage SSE stream) |
| `POST` | `/api/intelligence/section` | Re-run a single section |
| `GET` | `/api/intelligence/sessions` | List recent research sessions |
| `GET` | `/api/intelligence/sessions/:id` | Get session details + results |

#### `POST /api/intelligence/run_industry`

```json
{
  "industry": "Electric Vehicles",
  "agency": "brand strategy, digital experience",
  "apiKey": "AIza...",
  "demoMode": false
}
```

**Response:** SSE stream with events: `session`, `section_start`, `section_done`, `section_error`, `complete`

### Outreach

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `POST` | `/api/outreach/generate` | Generate outreach drafts for brands |
| `POST` | `/api/outreach/personalize` | Contact-specific personalized outreach |

### Tracking

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/tracking/campaigns` | List all campaigns |
| `POST` | `/api/tracking/campaigns` | Create a new campaign |
| `GET` | `/api/tracking/campaigns/:id` | Get campaign + leads |
| `POST` | `/api/tracking/campaigns/:id/leads` | Log an outreach contact |
| `PATCH` | `/api/tracking/leads/:id` | Update lead status |
| `GET` | `/api/tracking/campaigns/:id/stats` | Campaign analytics |

---

## 🎬 Live Demo Flow

1. **Open the app** → `http://localhost:3000`
2. **Select Industry Mode** (default)
3. **Type any industry** — e.g., *"Electric Vehicles"*, *"FinTech"*, *"Sustainable Fashion"*
4. **Click "Run Pipeline ↗"** and watch 6 stages stream live:

| What You'll See | Checkpoint |
|----------------|:----------:|
| 10 company cards with scores, rationale, and source links | ✅ Prospect List |
| Event cards with dates, locations, and attending brands | ✅ Event Mapping |
| Contact cards with LinkedIn profiles, emails, and action buttons | ✅ Contact Intelligence |
| LinkedIn + Email tabs with pre-filled outreach per brand | ✅ Personalized Outreach |

5. **Click "Search on LinkedIn"** on any contact → opens LinkedIn people search
6. **Click "Send Email"** → opens mail client with `To:` pre-filled
7. **Click "Open in Mail ↗"** in outreach tab → full email with To, Subject, Body ready
8. **Export** results as JSON, CSV, or TXT

---

## 🔧 Technical Highlights

| Feature | Implementation |
|---------|---------------|
| **Live Data** | Gemini 2.0 Flash with Google Search Grounding — every call searches the live web |
| **No Fabrication** | Low temperature (0.2), source attribution on every data point, confidence labels |
| **Streaming UX** | Server-Sent Events (SSE) — results appear in real-time as each stage completes |
| **Parallel Execution** | Stages 2-4 run concurrently via `ThreadPoolExecutor` — 40% faster pipeline |
| **Smart Caching** | 6-hour TTL cache; auto-busts stale entries with < 10 brands |
| **Graceful Fallbacks** | Live → Cache → Demo Safe Mode → Empty state (never crashes) |
| **Rate Limit Handling** | Exponential backoff with 3 retries on 429/quota errors |
| **One-Click Outreach** | `mailto:` links pre-fill To + Subject + Body; LinkedIn compose auto-copies message |
| **Presentation Mode** | Full-screen view with auto-scroll for live client demos |

---

## 🚢 Production Deployment

```bash
# Build frontend
cd frontend && npm run build

# Run backend with gunicorn
cd backend && gunicorn app:app -w 4 -b 0.0.0.0:4000
```

**For production, consider:**
- Replace in-memory store (`store.py`) with SQLite or PostgreSQL
- Serve frontend build with Nginx or deploy to Vercel/Netlify
- Add authentication and rate limiting
- Set `FLASK_ENV=production`

---

⭐ Don't forget to star the repositories if you find them useful!
<div align="center">
<sub>Built by <a href="https://github.com/vishnu-murukan">Vishnu Murukan</a></sub>
</div>
