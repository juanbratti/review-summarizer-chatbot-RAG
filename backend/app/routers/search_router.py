# ===============================================
# DOCS
# ===============================================

"""
Search Router for the RAG Chatbot API.
Handles search endpoints with proper error handling and validation.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.models import SearchRequest, SearchResponse, SearchResult, ErrorResponse
from ..services.chroma_database import search_similar_reviews
from ..services.cohere_llm import get_llm_service, CohereLLMService
from ..exceptions import RAGChatbotException, convert_to_http_exception

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
    "/search/", 
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def search(
    search_request: SearchRequest,
    llm_service: CohereLLMService = Depends(get_llm_dependency)
):
    """
    Perform a search for similar documents and return multiple results.
    
    This endpoint:
    1. Translates the search query to English if needed
    2. Searches for similar reviews in the database
    3. Returns formatted search results
    
    Args:
        search_request: Search request containing the query
        llm_service: Injected LLM service instance
        
    Returns:
        SearchResponse with search results and metadata
        
    Raises:
        HTTPException: For various error conditions
    """
    try:
        # --- step 1: Translate the query to English --- #
        query_en = llm_service.translate_text(
            search_request.query, 
            target_language="English"
        )
        
        # --- step 2: Search for similar reviews --- #
        docs, result = search_similar_reviews(query_en)
        
        # --- step 3: Format search results --- #
        formatted_results = format_search_results(result)
        
        return SearchResponse(
            results=formatted_results,
            total_results=len(formatted_results),
            success=True
        )
        
    except RAGChatbotException as e:
        raise convert_to_http_exception(e, 500)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "An unexpected error occurred during search",
                "detail": str(e),
                "success": False
            }
        )