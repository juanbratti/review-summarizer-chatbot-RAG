# ===============================================
# DOCS
# ===============================================

"""
Upload Router for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException, UploadFile, File
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..models.models import UploadRequest, UploadResponse
from ..services.chroma_database import save_documents
from ..config import settings
import io

# ===============================================
# ROUTER
# ===============================================

router = APIRouter()

# ===============================================
# UPLOAD REVIEWS FUNCTION
# ===============================================

@router.post("/upload/", response_model=UploadResponse)
async def upload_reviews(reviews: UploadRequest):
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
        
        return UploadResponse(
            message="Reviews uploaded and processed successfully.",
            documents_processed=len(chunks),
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

