# ===============================================
# DOCS
# ===============================================

"""
Question Router for the RAG Chatbot API.
Handles question-answering endpoints with proper error handling and validation.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.models import QuestionRequest, QuestionResponse, SearchResult, ErrorResponse
from ..services.chroma_database import search_similar_reviews
from ..services.cohere_llm import get_llm_service, CohereLLMService
from ..exceptions import (
    RAGChatbotException, 
    NoResultsException, 
    convert_to_http_exception
)

# ===============================================
# ROUTER
# ===============================================

router = APIRouter()

# ===============================================
# DEPENDENCY INJECTION
# ===============================================

def get_llm_dependency() -> CohereLLMService:
    """Dependency injection for LLM service."""
    return get_llm_service()

# ===============================================
# HELPER FUNCTIONS
# ===============================================

def format_search_results(result: dict) -> List[SearchResult]:
    """
    Format ChromaDB search results into SearchResult models.
    
    Args:
        result: Raw ChromaDB search result
        
    Returns:
        List of formatted SearchResult objects
    """
    if not result.get("ids") or not result["ids"][0]:
        return []
    
    formatted_results = []
    for i in range(len(result["ids"][0])):
        # ChromaDB returns distances (lower is more similar)
        distance = result["distances"][0][i]
        
        search_result = SearchResult(
            document_id=result["ids"][0][i],
            content_snippet=result["documents"][0][i][:100] + "..." if len(result["documents"][0][i]) > 100 else result["documents"][0][i],
            similarity_score=round(distance, 3)  # Keep distance as-is (lower means more similar)
        )
        formatted_results.append(search_result)
    
    return formatted_results

# ===============================================
# ENDPOINTS
# ===============================================

@router.post(
    "/questions/", 
    response_model=QuestionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "No Results Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def ask_question(
    question_request: QuestionRequest,
    llm_service: CohereLLMService = Depends(get_llm_dependency)
):
    """
    Process a question and return an AI-generated answer based on similar reviews.
    
    This endpoint:
    1. Translates the question to English if needed
    2. Searches for similar reviews in the database
    3. Generates an answer using the LLM
    4. Translates the answer back to Spanish if needed
    
    Args:
        question_request: Question request containing the user's question
        llm_service: Injected LLM service instance
        
    Returns:
        QuestionResponse with answer and related search results
        
    Raises:
        HTTPException: For various error conditions
    """
    try:
        # --- step 1: Translate question to English if needed --- #
        question_en = llm_service.translate_text(
            question_request.question, 
            target_language="English"
        )
        
        # --- step 2: Search for similar reviews --- #
        similar_reviews, search_result = search_similar_reviews(question_en)
        
        # --- step 3: Check if we found any results --- #
        if not similar_reviews:
            raise NoResultsException(
                "No reviews found for that question",
                "The database might be empty or the question might not be related to available reviews"
            )
        
        # --- step 4: Generate answer using LLM --- #
        llm_answer = llm_service.generate_answer(question_en, similar_reviews)
        
        # --- step 5: Translate answer back to Spanish --- #
        llm_answer_translated = llm_service.translate_text(
            llm_answer,
            target_language="Spanish"
        )
        
        # --- step 6: Format search results --- #
        formatted_results = format_search_results(search_result)
        
        return QuestionResponse(
            answer=llm_answer_translated,
            results=formatted_results,
            success=True
        )
        
    except NoResultsException as e:
        raise convert_to_http_exception(e, 404)
        
    except RAGChatbotException as e:
        raise convert_to_http_exception(e, 500)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "An unexpected error occurred",
                "detail": str(e),
                "success": False
            }
        )

@router.post("/questions/clear-history/")
async def clear_chat_history(llm_service: CohereLLMService = Depends(get_llm_dependency)):
    """
    Clear the chat history.
    
    Args:
        llm_service: Injected LLM service instance
        
    Returns:
        Success message
    """
    try:
        llm_service.clear_chat_history()
        return {"message": "Chat history cleared successfully", "success": True}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to clear chat history",
                "detail": str(e),
                "success": False
            }
        )
