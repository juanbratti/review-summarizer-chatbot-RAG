from fastapi import APIRouter, HTTPException
from ..models.models import QuestionRequest, QuestionResponse
from ..services.chroma_database import search_similar_reviews
from ..services.cohere_llm import get_llm_response, translate_llm_answer, translate_query

router = APIRouter()

@router.post("/questions/", response_model=QuestionResponse)
async def ask_question(question: QuestionRequest):
    """
    Recibe una pregunta, busca reseñas similares usando chroma,
    y utiliza un LLM para responder.
    """
    try:

        question_og = question.question

        # Traducir la pregunta al inglés
        question_en = translate_query(question_og)

        # Buscar reseñas similares en ChromaDB
        similar_reviews, result = search_similar_reviews(question_en)

        # Si no hay reseñas similares, responder con un mensaje
        if not similar_reviews:
            return {"answer": "No reviews found for that question."}

        # Generar respuesta usando el LLM
        llm_answer = get_llm_response(question_en, similar_reviews)
    
        # traduzco respuesta del idioma a español
        llm_answer_translated = translate_llm_answer(llm_answer)

        formatted_results = [
            {
                "document_id": result["ids"][0][i],
                "content_snippet": result["documents"][0][i][:100],
                "similarity_score": result["distances"][0][i]
            } for i in range(len(result["ids"][0]))
        ]

        return {"answer": llm_answer_translated, "results": formatted_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
