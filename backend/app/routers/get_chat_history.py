# ===============================================
# DOCS
# ===============================================

"""
Get Chat History Router for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import APIRouter, HTTPException
from ..models.models import ChatHistory, ChatMessage
from ..services.cohere_llm import chat_history

# ===============================================
# ROUTER
# ===============================================

router = APIRouter()

# ===============================================
# GET CHAT HISTORY FUNCTION
# ===============================================

@router.get("/history/", response_model=ChatHistory)
async def get_chat_history():
    """
    Get the chat history from the database.
    """
    history = [ChatMessage(role=msg['role'], content=msg['content']) for msg in chat_history]
    
    return ChatHistory(history=history)