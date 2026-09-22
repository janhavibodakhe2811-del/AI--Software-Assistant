"""
AI Software Engineer Assistant — FastAPI Backend
College Project | 2025-2026
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import analyze, results, chat, filetree

# ── App initialization ────────────────────────────────────────────

app = FastAPI(
    title="AI Software Engineer Assistant",
    description="Analyzes GitHub repositories using AI — architecture, security, docs, and more.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── CORS (allow React dev server) ────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────

app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(results.router, prefix="/api", tags=["Results"])
app.include_router(chat.router,    prefix="/api", tags=["Chat"])
app.include_router(filetree.router, prefix="/api", tags=["File Tree"])


# ── Health check ──────────────────────────────────────────────────

@app.get("/api/health", tags=["Health"])
async def health_check():
    from app.config import GEMINI_API_KEY
    return {
        "status": "ok",
        "ai_configured": bool(GEMINI_API_KEY),
        "version": "1.0.0",
    }


@app.get("/", include_in_schema=False)
async def root():
    return JSONResponse({
        "message": "AI Software Engineer Assistant API",
        "docs": "/api/docs",
        "health": "/api/health",
    })
