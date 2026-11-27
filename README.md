# 🚀 AlgoGen Studio — AI-Powered Algorithm Generation & Optimization Platform

**Version:** 1.0.0  
**Capstone Project:** AI-Powered Algorithm Generation using Reinforcement Learning  

**AlgoGen Studio** is a full-stack AI algorithm generation, problem-solving, and optimization platform built with **FastAPI**, **React 18 (Vite)**, **MongoDB**, and a custom **Hybrid GA-RL Engine (Genetic Algorithm + Q-Learning Reinforcement Learning)**. It retrieves cached algorithm documentation from MongoDB, dynamically synthesizes missing algorithms via **OpenAI**, **OpenRouter**, or the local **Hybrid GA-RL Engine**, and provides an interactive **10-Stage Problem-to-Algorithm Solver Pipeline** with live training telemetry, benchmarking, LeetCode problem mapping, interview Q&A, and Python code execution.

---

## 📌 Overview

AlgoGen Studio supports two primary workflows:

1. **Algorithm Search & Dynamic Synthesis**
   - **Prompt Validation**: Validates and normalizes user queries via the NLP prompt parser (`app/services/prompt_parser.py`).
   - **MongoDB Cache Lookup**: Searches `algorithms` by name, category, keyword, or application for instant retrieval.
   - **Multi-Tier AI & GA-RL Fallback**: On a cache miss (or placeholder record), `app/services/ai_generator.py` generates full algorithm documentation using **OpenAI** → **OpenRouter** → **Hybrid GA-RL Metaheuristic Engine**, then persists the result to MongoDB.
   - **Rich Enrichment**: Every retrieved or generated algorithm is enriched with curated **LeetCode practice problems**, a structured **overview breakdown**, and **technical interview Q&A** (plus custom interactive question answering).

2. **10-Stage Problem-to-Algorithm Solver Pipeline**
   - Accepts real-world engineering or computational problems (routing, healthcare, aviation, cloud scheduling, traffic, robotics, warehousing, job-shop, EV charging, portfolio optimization, graph/sorting, and custom domains) via `POST /problem/solve`.
   - Walks through 10 interactive stages in the Studio UI:
     1. **Problem Analyzer** — Extracts entities, scale, objectives, and bounds
     2. **Classification** — Determines computational class & complexity profile
     3. **Candidate Generator** — Synthesizes 7 candidate algorithms
     4. **RL Utility & MDP Formulation** — Defines states, actions, and rewards
     5. **Classical vs RL Trade-off Matrix** — Compares approaches
     6. **Simulation Environment** — Interactive sandbox parameters
     7. **Training & Evaluation** — Dynamic convergence telemetry (`POST /problem/train`, `POST /problem/evaluate`)
     8. **Benchmarking Matrix** — Ranks all 7 candidates
     9. **Best Algorithm** — Explains the winning selection rationale
     10. **Visuals & Source Code** — Architecture blueprints and live Python execution (`POST /problem/run-code` & browser Pyodide)

---

## ✨ Core Features

### 🔍 Intelligent Algorithm Search & Enrichment
- Search by **Algorithm Name**, **Category**, **Keyword**, or **Application**.
- Automatic persistence of newly generated algorithms into MongoDB.
- Outputs include problem statement, working steps, pseudocode, executable Python code, time/space complexity, resource usage, advantages/disadvantages, real-world applications, keywords, LeetCode problems, and interview Q&A.

### 🤖 Hybrid GA-RL Engine
- **Genetic Algorithm (GA)**: Encodes algorithm strategy parameters as chromosomes and evolves populations across generations using multi-objective fitness, crossover, and mutation.
- **Reinforcement Learning (RL)**: Uses Q-Learning state-action policies to select and optimize algorithmic strategies.
- **Automated Benchmarking**: `/garl/benchmark` evaluates standard categories (Sorting, Graph, Dynamic Programming, String Matching) against a $\ge 98.0\%$ accuracy target.

### 🔐 Authentication, Admin Console & OTP Recovery
- **User Authentication**: Registration (`POST /auth/register`) and login (`POST /auth/login`), with demo user fallback (`user` / `password123`).
- **Admin JWT Console**: Protected admin login (`POST /admin/login`, default `admin` / `admin123`) issuing HS256 JWT Bearer tokens for algorithm CRUD (`GET/POST/PUT/DELETE /admin/...`) and analytics.
- **Forgot-Password OTP Flow**: 6-digit time-limited (10 min) OTP generation, verification, and password reset via `/auth/forgot-password/*`.
- **Multi-Provider Email Delivery**: Supports **Brevo HTTP REST API**, **Resend HTTP REST API**, and **SMTP** (with server-console fallback when unconfigured).

### 📊 Analytics, Logging & Health Monitoring
- **Middleware Request Logger**: Non-blocking HTTP request logging (`endpoint`, `method`, `status_code`, `response_time_ms`) stored in `api_logs`.
- **Dashboard & Telemetry Endpoints**: Tracks total algorithms, query history, DB hits vs. AI generations, top searched algorithms, API usage counts, and average response latency.
- **Health Check**: `GET /health` verifies backend status and MongoDB connectivity via `ping`.

### 📱 Multi-Platform Delivery
- **Web App**: React 18 + Vite (`http://localhost:3000`) with Tailwind CSS and Pyodide WebAssembly Python runner.
- **PWA**: Configured with `frontend/public/manifest.json` and `frontend/public/sw.js`.
- **Windows Desktop Launcher**: One-click app mode via `AlgoGenStudio.vbs` and `launch_app.bat`.
- **Android Wrapper**: Capacitor configuration (`frontend/capacitor.config.json`, `com.algogen.studio`) and Android project in `frontend/android/`.

---

## 🏗 System Architecture

```text
                           ┌──────────────────────────────────┐
                           │   React 18 + Vite Frontend       │
                           │   (Studio, Dashboards, Admin UI) │
                           └────────────────┬─────────────────┘
                                            │ HTTP REST / JSON
                                            ▼
                           ┌──────────────────────────────────┐
                           │     FastAPI Backend Server       │
                           │   + Request Logging Middleware   │
                           └────────────────┬─────────────────┘
                                            │
    ┌──────────────────┬────────────────────┼────────────────────┬──────────────────┐
    ▼                  ▼                    ▼                    ▼                  ▼
┌─────────┐    ┌───────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│Auth/JWT │    │Algorithm API  │    │10-Stage      │    │Hybrid GA-RL  │    │Dashboard &   │
│& OTP    │    │& Enrichment   │    │Problem Solver│    │Engine & Q-Tbl│    │Health Check  │
└────┬────┘    └───────┬───────┘    └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
     │                 │                   │                   │                   │
     │                 ▼                   │                   │                   │
     │         ┌───────────────┐           │                   │                   │
     │         │ MongoDB Cache │           │                   │                   │
     │         └───────┬───────┘           │                   │                   │
     │                 │ Cache Miss        │                   │                   │
     │                 ▼                   │                   │                   │
     │         ┌───────────────────────────┴───────┐           │                   │
     │         │ OpenAI -> OpenRouter ->           │           │                   │
     │         │ Hybrid GA-RL Metaheuristic Engine │◄──────────┘                   │
     │         └───────────────┬───────────────────┘                               │
     │                         │ Persist & Log                                     │
     ▼                         ▼                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                       MongoDB                                           │
│  algorithms | users | otp_requests | query_history | generation_logs | api_logs         │
│  performance_metrics | garl_logs | garl_qtable | garl_benchmarks                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

### Frontend
- **Framework**: React 18.3 + Vite 5.4
- **Routing**: React Router DOM v6 (`/`, `/login`, `/dashboard`, `/admin`, `/admin/algorithms`)
- **UI & Icons**: Tailwind CSS (CDN), Lucide React
- **In-Browser Execution**: Pyodide (`v0.25.0` WebAssembly Python runtime)
- **Mobile / PWA**: Capacitor Android (`com.algogen.studio`), Service Worker & Web Manifest

### Backend
- **Framework**: Python + FastAPI (`0.115.0`), Uvicorn (`0.30.6`), Starlette
- **Validation**: Pydantic v2
- **Authentication**: PyJWT / `python-jose` + `passlib` / `bcrypt`
- **Email Service**: Brevo HTTP API, Resend HTTP API, and Python `smtplib`

### AI & Optimization Engine
- **Hybrid Engine**: Custom Genetic Algorithm + Q-Learning Reinforcement Learning (`app/services/hybrid_garl.py`) & Metaheuristic Engine (`app/services/metaheuristic_engine.py`)
- **LLM Integrations**: OpenAI SDK (`openai`) & OpenRouter API

### Database (`pymongo`)
- **MongoDB Collections** (`app/database/connection.py`):
  - `algorithms` (configurable via `COLLECTION_NAME`)
  - `users`
  - `otp_requests` (with TTL expiration index on `expires_at`)
  - `query_history`
  - `generation_logs`
  - `api_logs`
  - `performance_metrics`
  - `garl_logs`, `garl_qtable`, `garl_benchmarks`

---

## 📂 Project Structure

```text
AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main/
├── app/
│   ├── auth/                   # JWT creation & verification dependencies
│   ├── database/               # MongoDB client, collections, and index setup
│   ├── middleware/             # HTTP request logging middleware (api_logs)
│   ├── models/                 # Data models (algorithm, user)
│   ├── routes/
│   │   ├── admin.py            # Admin login & JWT-protected CRUD endpoints
│   │   ├── algorithms.py       # Search, LeetCode, interview Q&A, problem solver & code runner
│   │   ├── auth.py             # User register, login, and OTP password reset
│   │   ├── dashboard.py        # Dashboard summary, top algorithms, recent searches, API usage
│   │   ├── garl.py             # Hybrid GA-RL generation, metrics, benchmark, Q-table
│   │   └── health.py           # /health MongoDB connectivity check
│   ├── schemas/                # Pydantic request/response schemas
│   ├── services/               # AI generator, Hybrid GA-RL, 10-stage solver, catalogs, email
│   ├── utils/                  # Logger & security helpers
│   └── main.py                 # FastAPI app initialization, CORS & router registration
├── frontend/
│   ├── android/                # Capacitor Android native project
│   ├── public/                 # PWA manifest, service worker, icons, presentations
│   ├── src/
│   │   ├── components/         # Navbar, SidebarNav, visualizers & UI components
│   │   ├── context/            # AuthContext, ToastContext, UserHistoryContext
│   │   ├── pages/              # StudioPage, LoginPage, UserDashboardPage, Admin pages
│   │   ├── services/api.js     # Backend REST client
│   │   └── App.jsx             # Protected & admin route definitions
│   ├── capacitor.config.json   # Capacitor configuration (com.algogen.studio)
│   ├── index.html              # Tailwind CDN + Pyodide + root mount
│   ├── package.json            # Frontend scripts & dependencies
│   ├── vercel.json             # Vercel SPA routing config
│   └── vite.config.js          # Vite dev server config (port 3000)
├── scripts/                    # Database seeding & migration scripts
├── tests/                      # Pytest & email verification tests
├── .env.example                # Environment variables template
├── Dockerfile                  # Backend container image (Python 3.11-slim)
├── docker-compose.yml          # MongoDB + FastAPI multi-container stack
├── requirements.txt            # Python dependencies
├── launch_app.bat              # Windows standalone app launcher
├── AlgoGenStudio.vbs           # Silent Windows desktop launcher
├── start_servers.ps1           # PowerShell dual-server launcher
├── DEPLOYMENT_GUIDE.md         # Desktop, PWA, Docker & cloud deployment guide
└── VS_CODE_GUIDE.md            # VS Code tasks, extensions & F5 debug profiles
```

---

## 📡 API Endpoints Reference

### 🌐 Public & Algorithm Routes (`app/routes/algorithms.py`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Backend status greeting (`{"message": "Backend Running"}`) |
| `GET` | `/algorithms` | List all stored algorithms |
| `GET` | `/algorithm/{algorithm_name}` | Search algorithm by name (DB → OpenAI/OpenRouter/GA-RL → MongoDB) |
| `GET` | `/algorithm/{algorithm_name}/leetcode` | Retrieve matching LeetCode practice problems |
| `POST` | `/algorithm/{algorithm_name}/ask-interview` | Ask a custom technical interview question |
| `GET` | `/category/{category_name}` | Search algorithms by category |
| `GET` | `/keyword/{keyword}` | Search algorithms by keyword |
| `GET` | `/application/{application}` | Search algorithms by application |
| `GET` | `/statistics` | Aggregate query, generation, and algorithm counts |
| `GET` | `/performance` | Retrieve all algorithm performance metrics |
| `GET` | `/performance/top` | Retrieve top 5 most searched algorithms |

### 🧩 10-Stage Problem Solver & Runner (`app/routes/algorithms.py`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/problem/solve` | Run the 10-stage problem-to-algorithm pipeline |
| `GET` | `/problem/{problem_text}` | Solve a problem prompt via URL parameter |
| `POST` | `/problem/train` | Simulate dynamic RL/GA-RL training telemetry |
| `POST` | `/problem/evaluate` | Run test-episode evaluation metrics |
| `POST` | `/problem/run-code` | Execute submitted Python code in a timed subprocess (max 15s) |

### 🤖 Hybrid GA-RL Engine Routes (`app/routes/garl.py`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/garl/generate` | Run GA evolution + RL Q-Learning optimization and store result |
| `GET` | `/garl/metrics` | Get GA-RL accuracy metrics, strategy distribution, and logs |
| `POST` | `/garl/benchmark` | Run benchmark suite across standard categories ($\ge 98.0\%$ target) |
| `GET` | `/garl/qtable` | Retrieve current RL Q-Learning table entries |

### 🔐 Authentication & OTP Routes (`app/routes/auth.py`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user account |
| `POST` | `/auth/login` | Authenticate user credentials |
| `POST` | `/auth/forgot-password/request-otp` | Generate and email a 6-digit OTP (10-minute expiry) |
| `POST` | `/auth/forgot-password/verify-otp` | Verify OTP code validity |
| `POST` | `/auth/forgot-password/reset-password` | Reset user password using a verified OTP |

### 🔑 Admin Routes (`app/routes/admin.py`, JWT Protected)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/admin/login` | Admin login returning JWT Bearer token |
| `GET` | `/admin/algorithms` | Fetch all algorithms for the admin console |
| `POST` | `/admin/algorithm` | Insert a new algorithm record |
| `PUT` | `/admin/algorithm/{algorithm_name}` | Update an existing algorithm's description |
| `DELETE` | `/admin/algorithm/{algorithm_name}` | Delete an algorithm record |

### 📊 Dashboard & Health Routes (`app/routes/dashboard.py`, `app/routes/health.py`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/dashboard` | Overall analytics (totals, top search, latest query, avg latency) |
| `GET` | `/dashboard/top-algorithms` | Top 3 most searched algorithms |
| `GET` | `/dashboard/recent-searches` | Latest 10 user search queries |
| `GET` | `/dashboard/api-usage` | Aggregated request counts grouped by endpoint |
| `GET` | `/dashboard/generation-analytics` | Counts of `generated`, `retrieved`, and `failed` logs |
| `GET` | `/health` | Backend and MongoDB connection health status |

---

## ⚙️ Installation & Local Setup

### Prerequisites
- **Python**: `3.10+`
- **Node.js**: `v18+` and `npm`
- **MongoDB**: Local MongoDB instance (`mongodb://localhost:27017`) or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### 1. Clone & Configure Environment
```bash
git clone <repository-url>
cd AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main
```

Copy `.env.example` to `.env` and fill in your values:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=algogen_db
COLLECTION_NAME=algorithms
SECRET_KEY=your_super_secret_jwt_key_here

# Optional LLM Providers (falls back to local Hybrid GA-RL Engine if omitted)
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Email / OTP Delivery (Brevo REST API, Resend REST API, or SMTP)
BREVO_API_KEY=your_brevo_api_key_here
BREVO_SENDER_EMAIL=your_verified_sender_email@gmail.com
BREVO_SENDER_NAME=AlgoGen Studio
```

### 2. Backend Setup
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

*(Optional)* Seed initial algorithm records into MongoDB:
```bash
python update_db.py
```

Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Backend API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- Frontend Studio: `http://localhost:3000`

### 4. Quick Launchers & Docker
- **PowerShell (both servers)**: `.\start_servers.ps1`
- **Windows Desktop App Mode**: Double-click `AlgoGenStudio.vbs` or run `launch_app.bat`
- **Docker Compose (MongoDB + Backend)**:
  ```bash
  docker-compose up --build -d
  ```
- **Tests**:
  ```bash
  pytest
  ```

For cloud hosting (Render, Railway, Vercel) and PWA instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md). For VS Code tasks and debugging profiles, see [VS_CODE_GUIDE.md](VS_CODE_GUIDE.md).

---

## 👨‍💻 Authors & Project Info

**Developers**: ORSU LIKHITA PRIYA, PRATHIPATI GOWTHAM SAI, ANSAR KHAN, MODUGULA YASASWINI  
**Capstone Project**: AI-Powered Algorithm Generation using Reinforcement Learning
