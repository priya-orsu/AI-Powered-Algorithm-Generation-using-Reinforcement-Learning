<<<<<<< HEAD
# 🚀 Algorithm Generator Backend

**Version:** 1.0.0

An AI-powered backend system developed using **FastAPI**, **MongoDB**, and **OpenRouter AI** that intelligently retrieves algorithm information from the database or automatically generates new algorithm documentation using AI.

---

# 📌 Overview

The Algorithm Generator Backend is designed to provide an efficient and intelligent algorithm search system.

Whenever a user searches for an algorithm:

- The backend first searches the MongoDB database.
- If the algorithm exists, it is returned instantly.
- If not found, OpenRouter AI generates complete algorithm documentation.
- The generated algorithm is automatically stored in MongoDB for future requests.

This reduces repeated AI calls and continuously expands the local algorithm database.

---

# ✨ Features

## 🔍 Intelligent Algorithm Search

- Search Algorithm by Name
- Search by Category
- Search by Keyword
- Search by Application
- Get All Algorithms

---

## 🤖 AI Integration

Uses **OpenRouter AI** to automatically generate:

- Algorithm Description
- Problem Statement
- Working Steps
- Time Complexity
- Space Complexity
- Resource Usage
- Advantages
- Disadvantages
- Applications
- Keywords
- Sample Interview Questions

Generated algorithms are automatically saved into MongoDB.

---

## 🗄 Database

MongoDB Collections:

- algorithms
- query_history
- generation_logs
- api_logs
- performance_metrics

---

## 📊 Dashboard Analytics

Provides backend analytics such as:

- Total Algorithms
- Total Queries
- MongoDB Hits
- AI Generated Results
- Successful Requests
- Failed Requests
- Average Response Time
- Fastest API
- Slowest API
- Most Frequently Searched Algorithms
- Recent Searches

---

## 📈 Performance Monitoring

Tracks:

- Response Time
- Search Source
- Endpoint Performance
- Timestamp

---

## 📝 API Logging

Automatically stores:

- Endpoint
- HTTP Method
- Status Code
- Response Time
- Timestamp

---

## ❤️ Health Monitoring

Health endpoint verifies:

- Backend Status
- MongoDB Connection
- Database Availability

---

## 🔐 JWT Authentication

Secure Admin APIs using JWT Authentication.

Supports:

- Admin Login
- Token Generation
- Token Verification
- Protected CRUD Operations

---

# 🏗 System Architecture

```
                Client
                   │
                   ▼
            FastAPI Backend
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 Authentication  Dashboard   Health Check
      │            │            │
      ▼            ▼            ▼
     JWT       Analytics   Monitoring
                   │
                   ▼
          Algorithm Search
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
      MongoDB           OpenRouter AI
        │                     │
        └──────────┬──────────┘
                   ▼
           Store Generated Data
                   │
                   ▼
             Return Response
```

---

# 🛠 Technology Stack

### Backend

- Python 3.13
- FastAPI
- Uvicorn

### Database

- MongoDB
- PyMongo

### AI

- OpenRouter AI
- OpenAI Python SDK

### Authentication

- JWT
- Python-JOSE

### Configuration

- python-dotenv

---

# 📂 Project Structure

```
Algorithm-Generator-Backend/

│
├── app/
│   ├── database/
│   │     └── connection.py
│   │
│   ├── middleware/
│   │     └── logger.py
│   │
│   ├── routes/
│   │     ├── algorithms.py
│   │     ├── admin.py
│   │     ├── dashboard.py
│   │     └── health.py
│   │
│   ├── services/
│   │     └── ai_generator.py
│   │
│   ├── security/
│   │     ├── auth.py
│   │     └── dependencies.py
│   │
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# 📡 API Endpoints

## Public APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home |
| GET | /algorithm/{algorithm_name} | Search Algorithm |
| GET | /category/{category_name} | Search by Category |
| GET | /keyword/{keyword} | Search by Keyword |
| GET | /application/{application} | Search by Application |
| GET | /algorithms | Get All Algorithms |
| GET | /statistics | Backend Statistics |
| GET | /dashboard | Dashboard Analytics |
| GET | /health | Health Status |

---

## Admin APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /admin/login | Admin Login |
| GET | /admin/algorithms | View Algorithms |
| POST | /admin/algorithm | Add Algorithm |
| PUT | /admin/algorithm/{name} | Update Algorithm |
| DELETE | /admin/algorithm/{name} | Delete Algorithm |

---

# 🤖 AI Workflow

```
User Search
     │
     ▼
Search MongoDB
     │
 ┌───┴────┐
 │        │
Found   Not Found
 │        │
 ▼        ▼
Return  OpenRouter AI
             │
             ▼
    Generate Algorithm
             │
             ▼
    Save into MongoDB
             │
             ▼
      Return Response
```

---

# 📊 Database Collections

### algorithms

Stores complete algorithm information.

### query_history

Stores:

- Search Query
- Search Type
- Search Status
- Timestamp

### generation_logs

Stores:

- Algorithm Name
- Generation Status
- AI Source
- Timestamp

### api_logs

Stores:

- Endpoint
- HTTP Method
- Status Code
- Response Time
- Timestamp

### performance_metrics

Stores:

- Endpoint
- Search Source
- Response Time
- Timestamp

---

# 🔐 Security

- JWT Authentication
- Protected Admin Routes
- Secure Token Verification
- Environment Variable Configuration

---

# ⚙ Installation

## Clone Repository

```bash
git clone <repository-url>
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn app.main:app --reload
```

---

# 🌐 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

OpenAPI JSON

```
http://127.0.0.1:8000/openapi.json
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
MONGO_URI=your_mongodb_connection_string

DATABASE_NAME=AlgorithmGenerator

COLLECTION_NAME=algorithms

OPENROUTER_API_KEY=your_openrouter_api_key

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# ✅ Completed Modules

- FastAPI Backend
- MongoDB Integration
- CRUD Operations
- JWT Authentication
- OpenRouter AI Integration
- Automatic AI Algorithm Generation
- MongoDB Storage
- Query History
- Generation Logs
- API Logs Middleware
- Performance Metrics
- Dashboard Analytics
- Health Monitoring
- Swagger Documentation

---

# 🚀 Future Enhancements

- Intelligent Spell Correction
- AI Query Suggestions
- Bulk Algorithm Dataset (500+ Algorithms)
- Redis Caching
- Docker Deployment
- Unit Testing
- Role-Based Access Control
- AI Model Fallback
- Advanced Analytics Dashboard

---

# 👨‍💻 Developer

**PRATHIPATI GOWTHAM SAI**

**Role:** Backend & Database Developer

**Capstone Project:** AI-Powered Algorithm Generation System
=======
# AI-Powered-Algorithm-Generation-using-Reinforcement-Learning
Introducing a hybrid approach integrating genetic algorithms and reinforcement learning. This enables dynamic learning, real-time adaptability, and improved performance across multiple problem domains, making it more efficient and scalable.
>>>>>>> 4a4ca23e44bb724b8b1c4cde19130aa8e8fdf921
