# ===============================================
# DOCS
# ===============================================

"""
Question Router for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException
from ..models.models import QuestionRequest, QuestionResponse
from ..services.chroma_database import search_similar_reviews
from ..services.cohere_llm import get_llm_response, translate_llm_answer, translate_query

# ===============================================
# ROUTER
# ===============================================

router = APIRouter()

# ===============================================
# ASK QUESTION FUNCTION
# ===============================================

@router.post("/questions/", response_model=QuestionResponse)
async def ask_question(question: QuestionRequest):
    """
    Receives a question, searches for similar reviews using chroma,
    and uses an LLM to answer.
    """
    try:

        question_og = question.question

        # --- translate the question to English --- #
        question_en = translate_query(question_og)

        # --- Search for similar reviews in ChromaDB --- #
        similar_reviews, result = search_similar_reviews(question_en)

        # --- if no similar reviews, respond with a message --- #
        if not similar_reviews:
            return {"answer": "No reviews found for that question.", "results": []}

        # --- generate answer using the LLM --- #
        llm_answer = get_llm_response(question_en, similar_reviews)
    
        # --- translate answer to Spanish --- #
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
