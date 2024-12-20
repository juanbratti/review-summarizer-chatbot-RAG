from fastapi import APIRouter, HTTPException
from models.models import SearchRequest, SearchResponse
from services.chroma_database import search_similar_reviews
from services.cohere_llm import get_llm_response, translate_llm_answer, translate_query

router = APIRouter()

@router.post("/search", status_code=200, response_model=SearchResponse)
async def search(to_search: SearchRequest):
    """
    Endpoint que realiza una búsqueda de documentos similares y devuelve múltiples resultados.
    """
    # traucir la pregunta al inglés
    question_en = translate_query(to_search.query)

    docs, result = search_similar_reviews(question_en)

    formatted_results = [
        {
            "document_id": result["ids"][0][i],
            "content_snippet": result["documents"][0][i][:100],
            "similarity_score": result["distances"][0][i]
        } for i in range(len(result["ids"][0]))
    ]

    return {"results": formatted_results}