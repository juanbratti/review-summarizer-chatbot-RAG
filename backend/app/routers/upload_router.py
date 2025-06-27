# ===============================================
# DOCS
# ===============================================

"""
Upload Router for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..models.models import Input
from ..services.chroma_database import save_documents
from ..config import settings

# ===============================================
# ROUTER
# ===============================================

router = APIRouter()

# ===============================================
# UPLOAD REVIEWS FUNCTION
# ===============================================

@router.post("/upload/")
async def upload_reviews(reviews : Input):
    """
    Endpoint that receives a string with reviews, processes them, vectorizes them and stores them in ChromaDB.
    """
    if not reviews.reviews:
        raise HTTPException(status_code=400, detail="String can't be empty.")

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size, 
            chunk_overlap=settings.chunk_overlap
        )
        chunks = text_splitter.split_text(reviews.reviews)
        # --- store the documents in ChromaDB --- #
        save_documents(chunks)
        return {"message": "Docs loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

