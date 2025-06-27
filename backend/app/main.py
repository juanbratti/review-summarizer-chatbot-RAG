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
from .routers import question_router, upload_router, search_router, get_chat_history
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

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

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Chatbot API"}

# To run with uvicorn:
# uvicorn app.main:app --reload
