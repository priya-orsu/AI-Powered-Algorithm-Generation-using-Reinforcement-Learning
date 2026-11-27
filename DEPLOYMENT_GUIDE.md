# AlgoGen Studio — Application Deployment & Desktop App Guide

This guide details how to run, package, and deploy **AlgoGen Studio** as a Desktop Application or a Cloud Web App.

---

## 1. Run as a Native Desktop App (One-Click Launcher)

We have created one-click launcher scripts in your root directory:

### Files Created:
- [`AlgoGenStudio.vbs`](file:///c:/Users/likhi/Downloads/AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main%20%281%29/AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main/AlgoGenStudio.vbs) — Silent background launcher (no terminal windows).
- [`launch_app.bat`](file:///c:/Users/likhi/Downloads/AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main%20%281%29/AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main/launch_app.bat) — Automatic launcher script.

### How to use:
1. Double-click [`AlgoGenStudio.vbs`](file:///c:/Users/likhi/Downloads/AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main%20%281%29/AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main/AlgoGenStudio.vbs) in File Explorer.
2. It automatically starts the FastAPI backend, boots the Vite frontend, and opens **AlgoGen Studio in Standalone App Window Mode** (without browser address bars or tabs).
3. **Optional**: Right-click `AlgoGenStudio.vbs` -> **Send to Desktop (create shortcut)** to place an icon on your desktop!

---

## 2. Progressive Web App (PWA) Mode

We configured PWA support inside your frontend (`manifest.json` + `sw.js` + meta tags).

### How to install on Desktop / Mobile:
1. Open **`http://localhost:3000`** in Chrome, Edge, or Brave.
2. Click the **"Install AlgoGen Studio"** button in the top address bar.
3. The app will install directly into your Windows/Mac Applications menu and Start Menu as a native application.

---

## 3. Public Cloud Web Deployment (Free Hosting)

To make your project accessible to anyone on the internet:

### Step A: Deploy Database (MongoDB Atlas)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create a free database cluster.
2. Copy your connection string (`mongodb+srv://<user>:<password>@cluster0...`).

### Step B: Deploy Backend (Render / Railway)
1. Push your repository to GitHub.
2. Sign up on [Render.com](https://render.com) or [Railway.app](https://railway.app).
3. Create a **Web Service**, select your repo root directory.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variable: `MONGO_URI` = `<your MongoDB Atlas URI>`.

### Step C: Deploy Frontend (Vercel)
1. Sign up on [Vercel](https://vercel.com).
2. Connect your GitHub repository and select the `frontend/` folder as the root directory.
3. Set Build Command: `npm run build`
4. Set Output Directory: `dist`
5. In `frontend/src/services/api.js`, update `API_BASE_URL` to your production backend URL (e.g. `https://algogen-backend.onrender.com`).

---

## 4. Containerized Deployment (Docker)

To run the complete stack with Docker Compose:

```bash
docker-compose up --build -d
```

This starts:
- **MongoDB**: Port 27017
- **FastAPI Backend**: Port 8000
