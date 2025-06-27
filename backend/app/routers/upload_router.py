from fastapi import APIRouter, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..models.models import Input
from ..services.chroma_database import save_documents

router = APIRouter()

@router.post("/upload/")
async def upload_reviews(reviews : Input):
    """
    Endpoint que recibe un string con reseñas, las procesa, las vectoriza y las almacena en ChromaDB.
    """
    if not reviews.reviews:
        raise HTTPException(status_code=400, detail="String can't be empty.")

    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        chunks = text_splitter.split_text(reviews.reviews)
        # almacenamiento de los documentos en ChromaDB
        save_documents(chunks)
        return {"message": "Docs loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

