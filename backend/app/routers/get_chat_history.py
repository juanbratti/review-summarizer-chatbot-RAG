from fastapi import APIRouter, HTTPException
from ..models.models import ChatHistory, ChatMessage
from ..services.cohere_llm import chat_history

router = APIRouter()

@router.get("/history/", response_model=ChatHistory)
async def get_chat_history():
    history = [ChatMessage(role=msg['role'], content=msg['content']) for msg in chat_history]
    
    return ChatHistory(history=history)