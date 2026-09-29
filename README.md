# 🚀 AI-Powered Algorithm Generation & Optimization Platform

**Version:** 1.0.0  
**Capstone Project:** AI-Powered Algorithm Generation using Reinforcement Learning  

An intelligent, full-stack AI platform developed using **FastAPI**, **React (Vite)**, **MongoDB**, and a custom **Hybrid GA-RL Engine (Genetic Algorithm + Reinforcement Learning)**. The system intelligently retrieves algorithm documentation from a local MongoDB database or automatically generates and optimizes complete, benchmarked algorithm specifications using GA-RL evolutionary strategy and Q-Learning policies, with **OpenRouter AI** as an optional fallback.

---

# 📌 Overview

Whenever a user searches for an algorithm:

1. **MongoDB Database Check**: The system first searches local MongoDB collections. If the algorithm exists, it is served instantly (< 15ms).
2. **Hybrid GA-RL Engine / AI Fallback**: If missing, the **Hybrid GA-RL Engine** evolves population strategies via Genetic Algorithms, evaluates optimal parameters using Reinforcement Learning Q-tables, and synthesizes complete algorithm documentation with **98%+ benchmarked accuracy**.
3. **Automated Data Persistence**: Newly generated algorithms are validated, benchmarked, and stored in MongoDB so subsequent requests benefit from zero-latency caching.
4. **Interactive Frontend Portal**: A responsive, dark-mode React application powered by Vite that allows seamless searching, admin management, interactive charting, and real-time performance analytics.

---

# ✨ Core Features

## 🔍 Intelligent Algorithm Search & Retrieval
- **Search Capabilities**: Search by Algorithm Name, Category, Keyword, or Application.
- **Auto-Caching**: Generated outputs are saved directly into MongoDB for persistent, instant retrieval.
- **Detailed Outputs**: Generates Problem Statements, Working Steps, Time/Space Complexity, Pseudo Code, Advantages/Disadvantages, Applications, Keywords, and Sample Interview Questions.

## 🤖 Hybrid GA-RL AI Engine
- **Genetic Algorithm (GA)**: Evolves candidate algorithm strategy populations across generations to maximize structural accuracy and performance.
- **Reinforcement Learning (RL)**: Uses Q-Learning policy tables to dynamically optimize algorithmic parameters and selection strategies.
- **Accuracy Benchmarking**: Integrated `/garl/benchmark` endpoint verifying performance metrics against a target target threshold ($\ge 98.0\%$).

## 🔐 Authentication & Security
- **JWT Admin Authentication**: Secure token-based admin access for full database CRUD operations.
- **User Authentication**: User registration, login, and profile management.
- **SMTP Email & OTP Verification**: One-Time Password (OTP) verification for secure user registration and password resets.

## 📊 Analytics & Performance Monitoring
- **Dashboard Analytics**: Tracks MongoDB hits, AI generations, request success ratios, average latency, and search frequencies.
- **API Middleware Logging**: Automatic request-level logging (endpoint, HTTP method, status codes, and execution time).
- **Health Checks**: System health endpoints monitoring database state and engine availability.

---

# 🏗 System Architecture

```
                               ┌───────────────────────────┐
                               │   React Frontend (Vite)   │
                               └─────────────┬─────────────┘
                                             │ HTTP REST / JSON
                                             ▼
                               ┌───────────────────────────┐
                               │  FastAPI Backend Server   │
                               └─────────────┬─────────────┘
                                             │
      ┌────────────────────┬─────────────────┼───────────────────┬───────────────────┐
      ▼                    ▼                 ▼                   ▼                   ▼
┌───────────┐      ┌───────────────┐  ┌──────────────┐   ┌───────────────┐   ┌───────────────┐
│ Auth & JWT│      │ Algorithm Search│ │ Dashboard    │   │  Health Check │   │ API Logging   │
└─────┬─────┘      └───────┬───────┘  └──────┬───────┘   └───────┬───────┘   └───────┬───────┘
      │                    │                 │                   │                   │
      ▼                    ▼                 ▼                   ▼                   ▼
┌───────────┐      ┌───────────────┐  ┌──────────────┐   ┌───────────────┐   ┌───────────────┐
│ User Auth │      │ MongoDB Cache │  │ Analytics    │   │ DB Health     │   │ Request Logs  │
└───────────┘      └───────┬───────┘  └──────────────┘   └───────────────┘   └───────────────┘
                           │ Miss
                           ▼
             ┌───────────────────────────┐
             │ Hybrid GA-RL AI Engine    │
             │ (GA Evolution + RL Q-Table│
             │  / OpenRouter Fallback)   │
             └─────────────┬─────────────┘
                           │ Synthesized & Benchmark Data
                           ▼
             ┌───────────────────────────┐
             │ Store into MongoDB Cache  │
             └───────────────────────────┘
```

---

# 🛠 Technology Stack

### Frontend
- **Framework**: React 18 + Vite
- **Routing**: React Router DOM v6
- **Icons**: Lucide React
- **Styling**: Modern CSS3 / Glassmorphic UI design

### Backend
- **Framework**: Python 3.13 + FastAPI
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic v2
- **Authentication**: PyJWT + Passlib (Bcrypt)
- **Email Service**: Python SMTP (Email OTP Verification & Password Reset)

### Machine Learning & AI Engine
- **Core Engine**: Custom Hybrid GA-RL Engine (Genetic Algorithm + Q-Learning Reinforcement Learning)
- **AI Fallback**: OpenRouter AI API / OpenAI SDK

### Database & Storage
- **Database**: MongoDB (PyMongo Driver)
- **Collections**:
  - `algorithms`: Complete algorithm documentation records
  - `users`: Registered user accounts and authentication credentials
  - `otp_requests`: Email OTP verification records
  - `query_history`: User query search history
  - `generation_logs`: AI generation audit logs
  - `api_logs`: HTTP request performance logs
  - `performance_metrics`: Endpoint response latency benchmarks
  - `garl_logs` / `garl_qtable` / `garl_benchmark`: GA-RL training, Q-table state, and benchmark validation records

---

# 📂 Project Structure

```
AI-Powered-Algorithm-Generation-using-Reinforcement-Learning/
│
├── backend/                    # FastAPI Backend Application
│   ├── app/                    # Backend application package
│   │   ├── auth/                # Security utilities & token generators
│   │   ├── database/            # MongoDB connection setup
│   │   ├── middleware/          # HTTP logging middleware
│   │   ├── models/              # PyMongo & Pydantic data models
│   │   ├── routes/              # API Endpoint Routers
│   │   ├── admin.py            # Admin CRUD endpoints
│   │   ├── algorithms.py       # Public algorithm search & retrieval routes
│   │   ├── auth.py             # User signup, login, OTP verification & password reset
│   │   ├── dashboard.py        # Analytics & performance monitoring routes
│   │   ├── garl.py             # Hybrid GA-RL engine routes & benchmarks
│   │   └── health.py           # Backend health status routes
│   │   ├── schemas/              # API Request & Response schemas
│   │   ├── services/             # Core Business Logic
│   │   ├── ai_generator.py     # OpenRouter AI fallback integration
│   │   ├── email_service.py    # SMTP email OTP delivery service
│   │   └── hybrid_garl.py      # GA-RL Evolutionary Strategy & Q-Learning Engine
│   │   ├── utils/                # Helper utilities
│   │   └── main.py               # FastAPI application entry point & CORS configuration
│   ├── scripts/                 # Backend data and maintenance scripts
│   ├── tests/                   # Backend tests
│   └── requirements.txt         # Backend Python dependencies
│
├── frontend/                   # React + Vite Frontend Application
│   ├── src/                    # React components, pages, and API hooks
│   ├── index.html              # HTML5 entry point
│   ├── vite.config.js          # Vite server & build configurations
│   ├── package.json            # Node.js dependencies
│   └── README.md               # Frontend documentation
│
├── .env                        # Production environment configuration file
├── requirements.txt            # Python dependencies manifest
├── update_db.py                # Database seed & migration script
├── test_smtp.py                # SMTP email configuration tester
└── README.md                   # Main project documentation
```

---

# 📡 Complete API Endpoints Reference

### 🌐 Public Algorithm Routes
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Backend health check greeting |
| `GET` | `/algorithm/{name}` | Search algorithm by name (Checks DB -> GA-RL -> AI) |
| `GET` | `/category/{category_name}` | Search algorithms by category |
| `GET` | `/keyword/{keyword}` | Search algorithms by keyword |
| `GET` | `/application/{application}` | Search algorithms by application |
| `GET` | `/algorithms` | Get all stored algorithms |
| `GET` | `/statistics` | Get basic backend execution statistics |

### 🤖 Hybrid GA-RL Engine Routes
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/garl/generate` | Trigger Hybrid GA-RL optimization & algorithm generation |
| `GET` | `/garl/metrics` | Retrieve global GA-RL accuracy, improvement & strategy distribution |
| `POST` | `/garl/benchmark` | Run automated accuracy benchmark tests ($\ge 98.0\%$ target) |
| `GET` | `/garl/qtable` | View current RL Q-Learning state-action values |

### 🔐 User & Authentication Routes
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register new user account |
| `POST` | `/auth/login` | User login authentication |
| `POST` | `/auth/request-otp` | Request OTP code for email verification or password reset |
| `POST` | `/auth/verify-otp` | Verify OTP code validity |
| `POST` | `/auth/reset-password` | Reset password using verified OTP |

### 🔑 Admin Routes (JWT Protected)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/admin/login` | Admin login & JWT token issuance |
| `GET` | `/admin/algorithms` | Fetch all algorithms for admin console |
| `POST` | `/admin/algorithm` | Manually insert new algorithm document |
| `PUT` | `/admin/algorithm/{name}` | Update existing algorithm document |
| `DELETE` | `/admin/algorithm/{name}`| Delete algorithm document from database |

### 📊 Dashboard & Monitoring Routes
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/dashboard` | Retrieve full analytics (hits, source split, latency, logs) |
| `GET` | `/health` | Check backend & MongoDB database connection health |

---

# ⚙ Installation & Local Setup

### Prerequisites
- **Python**: `3.10+` (Python 3.13 recommended)
- **Node.js**: `v18+` & `npm`
- **Database**: Local MongoDB instance or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) connection string

---

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AI-Powered-Algorithm-Generation-using-Reinforcement-Learning
```

---

### Step 2: Set Up Backend

1. **Create and Activate Virtual Environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory (refer to `.env.example`):
   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=AlgorithmGenerator
   COLLECTION_NAME=algorithms

   SECRET_KEY=your_super_secret_jwt_key_change_in_production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60

   OPENROUTER_API_KEY=your_openrouter_api_key

   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

4. **Seed Database (Optional)**:
   ```bash
   python update_db.py
   ```

5. **Start FastAPI Backend Server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The backend API will be live at `http://localhost:8000` with interactive Swagger docs at `http://localhost:8000/docs`.

---

### Step 3: Set Up Frontend

1. **Navigate to Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Node Dependencies**:
   ```bash
   npm install
   ```

3. **Start Development Server**:
   ```bash
   npm run dev
   ```
   The frontend app will be running at `http://localhost:3000` (or `http://localhost:5173`).

---

# 🚀 Deployment Platforms

Here are recommended platform configurations for deploying this full-stack project:

### 1. **Render (Easiest All-in-One)**
- **Backend (FastAPI)**: Deploy as a **Web Service**.
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Frontend (React)**: Deploy as a **Static Site**.
  - Build Command: `npm install && npm run build`
  - Publish Directory: `frontend/dist`
- **Database**: Connect via `MONGO_URI` environment variable to **MongoDB Atlas**.

### 2. **Vercel / Netlify (Frontend) + Railway / Fly.io (Backend)**
- Deploy `frontend/` to **Vercel** or **Netlify** for global CDN static asset hosting.
- Deploy `app/` backend container to **Railway** or **Fly.io** for low-latency ASGI API serving.

### 3. **Google Cloud Platform (GCP)**
- **Backend**: Deploy containerized FastAPI application on **Cloud Run** (serverless, auto-scaling).
- **Frontend**: Host static Vite build output on **Firebase Hosting** or **Cloud Storage + Cloud CDN**.

---

# 👨‍💻 Author & Project Info

**Developer**: ORSU LIKHITA PRIYA, PRATHIPATI GOWTHAM SAI,  ANSAR KHAN, MODUGULA YASASWINI
**Role**: Full-Stack & AI Systems Developer  
**Capstone Project**: AI-Powered Algorithm Generation using Reinforcement Learning  

---


