from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.algorithms import router as algorithm_router
from app.routes.admin import router as admin_router
from app.routes.dashboard import router as dashboard_router
from app.routes.health import router as health_router
from app.routes.garl import router as garl_router
from app.routes.auth import router as auth_router

from app.middleware.logger import log_requests

# Create FastAPI App
app = FastAPI(
    title="Algorithm Generator Backend",
    version="1.0.0"
)

# -------------------- CORS --------------------

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-powered-algorithm-generation-usi.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Middleware --------------------

app.middleware("http")(log_requests)

# -------------------- Routers --------------------

app.include_router(algorithm_router)
app.include_router(admin_router)
app.include_router(dashboard_router)
app.include_router(health_router)
app.include_router(garl_router)
app.include_router(auth_router)

# -------------------- Home --------------------

@app.get("/")
def home():
    return {
        "message": "Backend Running"
    }