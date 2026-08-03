# Algorithm Generator Portal - Frontend Suite

This is the production-grade, highly responsive, dark-theme-first frontend for the AI-Powered Algorithm Generation & Search System. It is built using HTML5, Tailwind CSS, Alpine.js, and Chart.js, running entirely on vanilla JavaScript without complex build tools or compilers.

---

## 📂 Folder Structure

```
frontend/
├── index.html            # Main search portal and system landing page
├── css/
│   └── styles.css        # Premium custom animations, glassmorphism, and scrollbars
├── js/
│   ├── api.js            # Central API Fetch wrapper (bearer tokens, handles 401s, endpoints mappings)
│   └── app.js            # Global state manager, route protection guards, local history tracking
└── pages/
    ├── login.html        # Portal authentication panel (Admin login & user registration simulator)
    ├── dashboard.html    # Normal client user area (bookmarks, personal history, settings)
    └── admin-dashboard.html    # Root administration panel (Chart.js dashboard analytics)
    └── admin-algorithms.html   # Root CRUD database console (insert, update, delete modal)
```

---

## ⚡ Setup & Run Instructions

### Step 1: Start the Backend
The FastAPI backend MUST be running on **`http://localhost:8000`** as configured in `api.js`.
Ensure your Python virtual environment is activated and start the server:
```bash
# In the root repository folder:
$env:PYTHONIOENCODING="utf-8"
.\venv\Scripts\python -m uvicorn app.main:app --reload
```

### Step 2: Serve the Frontend
Due to strict backend CORS configuration in `app/main.py`, the frontend **MUST** run on port **`3000`** (`http://localhost:3000` or `http://127.0.0.1:3000`).

You can easily serve the frontend using any lightweight server. Below are two simple ways:

#### Option A: Using Python (Recommended, no installation required)
Open a new terminal window inside the `frontend/` directory and run:
```bash
python -m http.server 3000
```
This instantly boots up a static web server. Navigate to [http://localhost:3000](http://localhost:3000).

#### Option B: Using Node.js (If installed)
Install a simple static runner and boot the folder:
```bash
npm install -g serve
serve -l 3000
```
Navigate to [http://localhost:3000](http://localhost:3000).

---

## 🔐 Credentials & Authentication Flows

| Role | Username | Password | Flow Type | Functionality |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | **Real Endpoint Auth** | Sends credentials to `POST /admin/login`. Receives and stores a JWT Bearer Token in `localStorage`. Grants access to Admin Analytics (`/pages/admin-dashboard.html`) and secure database CRUD operations (`/pages/admin-algorithms.html`). |
| **Normal User** | *Any Name* | *Any Pass* | **Client-Side Simulation** | Simulates authentication client-side. Saves a user object in `localStorage`. Generates a personal dashboard showing search logs, bookmarks, and account profiles. |

---

## 🚀 Key Highlights & Polish

1. **AI Generation States Tracker**: When querying an algorithm not present in the database, the OpenRouter AI generation can take 3 to 10 seconds. The landing page search box displays a multi-step loader notifying users of database scanning, AI initialization, and model outputs compilation.
2. **Schema Divergence Resilience**: The frontend automatically checks if time complexity/working steps are returned as strings (manual data entry) or structured arrays/objects (AI-generated output) and renders them elegantly using adaptive layouts.
3. **Interactive Charting**: Integrates **Chart.js** via CDN to feed admin dashboard analytics (API call grouping counts and generation success ratios) and user metrics (search count aggregates) on demand.
