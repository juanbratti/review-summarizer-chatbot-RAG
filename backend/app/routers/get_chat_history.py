# ===============================================
# DOCS
# ===============================================

"""
Get Chat History Router for the RAG Chatbot API.
Handles chat history endpoints with proper error handling.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException, Depends
from ..models.models import ChatHistory, ChatMessage, ErrorResponse
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
# ENDPOINTS
# ===============================================

@router.get(
    "/history/", 
    response_model=ChatHistory,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def get_chat_history(llm_service: CohereLLMService = Depends(get_llm_dependency)):
    """
    Get the current chat history from the LLM service.
    
    Args:
        llm_service: Injected LLM service instance
        
    Returns:
        ChatHistory with all chat messages
        
    Raises:
        HTTPException: If retrieving chat history fails
    """
    try:
        # Get chat history from LLM service
        history_data = llm_service.get_chat_history()
        
        # Convert to ChatMessage objects
        history = [
            ChatMessage(role=msg['role'], content=msg['content']) 
            for msg in history_data
        ]
        
        return ChatHistory(history=history)
        
    except RAGChatbotException as e:
        raise convert_to_http_exception(e, 500)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to retrieve chat history",
                "detail": str(e),
                "success": False
            }
        )