# ===============================================
# DOCS
# ===============================================

"""
Main file for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import question_router, upload_router, search_router, get_chat_history
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
import os

# ===============================================
# APP
# ===============================================

app = FastAPI(
    title=settings.app_name,
    description="API to answer questions about reviews using ChromaDB and an LLM.",
    version=settings.app_version,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins] if settings.cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include the routers, including the upload and questions routers --- #
app.include_router(upload_router.router, prefix="/app", tags=["upload"])
app.include_router(question_router.router, prefix="/app", tags=["questions"])
app.include_router(search_router.router, prefix="/app", tags=["search"])
app.include_router(get_chat_history.router, prefix="/app", tags=["chat_history"])

# Serve static files (React build) in production
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "REVI.AI API is running"}

@app.get("/api/")
async def api_root():
    return {"message": "Welcome to the REVI.AI API"}

# To run with uvicorn:
# uvicorn app.main:app --reload
