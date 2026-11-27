# VS Code Implementation Guide

This project is pre-configured for **Visual Studio Code** with one-click running, debugging, tasks, and recommended extensions.

---

## 1. Quick Launch (How to Open in VS Code)

You can open this project in VS Code anytime by doing either of the following:

### Option A: From Terminal / Command Prompt
```bash
code "C:\Users\HP 840 G6\Desktop\AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main (2)"
```

### Option B: From VS Code UI
1. Open VS Code.
2. Click **File** > **Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select `AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main (2)` and click **Select Folder**.

---

## 2. One-Click Running in VS Code

### Method 1: Keyboard Shortcut (Easiest)
Press **`Ctrl + Shift + B`** (Run Build Task).
- VS Code automatically runs **"Start Full Stack App (Backend + Frontend)"**.
- It spawns both servers side-by-side in integrated terminal panels:
  - **FastAPI Backend:** `http://127.0.0.1:8000`
  - **Vite Frontend:** `http://127.0.0.1:3000`

### Method 2: VS Code Menu
1. Press `Ctrl + Shift + P` (or `F1`) to open the Command Palette.
2. Type **`Tasks: Run Task`** and press Enter.
3. Choose:
   - **`Start Full Stack App (Backend + Frontend)`** (starts both)
   - **`Start FastAPI Backend`** (only backend)
   - **`Start Vite Frontend`** (only frontend)
   - **`Seed MongoDB Database`** (populates initial algorithm DB)
   - **`Install Dependencies (Python + Node)`**

---

## 3. Debugging with Breakpoints (F5)

1. Open the **Run and Debug** view (`Ctrl + Shift + D` or click the bug icon on the left sidebar).
2. In the top dropdown, select one of the pre-configured debug profiles:
   - **`⚡ Run FastAPI Backend (Debug)`**: Launches FastAPI with Python `debugpy`. You can set breakpoints inside `app/services/problem_solver.py`, `app/main.py`, etc.
   - **`🚀 Full Stack: Debug Backend + Run Frontend`**: Launches Vite dev server and debugs FastAPI simultaneously.
   - **`🌟 Complete Full Stack (Debug Backend + Frontend + Edge)`**: Launches backend, starts frontend, and automatically opens Microsoft Edge at `http://127.0.0.1:3000`.
3. Press **`F5`** to start debugging.

---

## 4. Recommended Extensions (Auto-Prompted)

When you open this folder, VS Code will suggest installing recommended extensions (`.vscode/extensions.json`):
- **Python** (`ms-python.python`)
- **Pylance** (`ms-python.vscode-pylance`)
- **Python Debugger** (`ms-python.debugpy`)
- **Tailwind CSS IntelliSense** (`bradlc.vscode-tailwindcss`)
- **Prettier Code Formatter** (`esbenp.prettier-vscode`)
- **MongoDB for VS Code** (`mongodb.mongodb-vscode`)

---

## 5. Directory Structure in VS Code

```
📁 AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main (2)/
├── 📁 .vscode/                 # Pre-configured VS Code settings, tasks, and debug profiles
│   ├── launch.json            # F5 Debugger configs
│   ├── tasks.json             # Ctrl+Shift+B Build & Dev tasks
│   ├── settings.json          # Formatter, Python path, Tailwind configs
│   └── extensions.json        # Recommended VS Code plugins
├── 📁 app/                     # FastAPI Python Backend
│   ├── main.py                # Server entrypoint (Port 8000)
│   ├── services/
│   │   ├── problem_solver.py  # 10-stage AI solver with math models & code runner
│   │   └── ...
├── 📁 frontend/                # React + Vite + Tailwind CSS Frontend
│   ├── src/
│   │   ├── pages/StudioPage.jsx # Main 10-stage studio workbench
│   │   └── ...
│   ├── package.json           # Port 3000
│   └── vite.config.js
├── requirements.txt           # Python dependencies
└── seed_database.py           # Database seeding script
```
