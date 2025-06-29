# ===============================================
# DOCS
# ===============================================

"""
Custom exceptions for the RAG Chatbot API.
Provides specific error types for better error handling.
"""

# ===============================================
# IMPORTS
# ===============================================

from fastapi import HTTPException
from typing import Optional

# ===============================================
# CUSTOM EXCEPTIONS
# ===============================================

class RAGChatbotException(Exception):
    """Base exception for RAG Chatbot application."""
    def __init__(self, message: str, detail: Optional[str] = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)

class DatabaseException(RAGChatbotException):
    """Exception raised for database-related errors."""
    pass

class LLMException(RAGChatbotException):
    """Exception raised for LLM-related errors."""
    pass

class TranslationException(RAGChatbotException):
    """Exception raised for translation-related errors."""
    pass

class ValidationException(RAGChatbotException):
    """Exception raised for validation errors."""
    pass

class NoResultsException(RAGChatbotException):
    """Exception raised when no results are found."""
    pass

# ===============================================
# HTTP EXCEPTION CONVERTERS
# ===============================================

def convert_to_http_exception(exc: RAGChatbotException, status_code: int = 500) -> HTTPException:
    """Convert custom exception to FastAPI HTTPException."""
    return HTTPException(
        status_code=status_code,
        detail={
            "error": exc.message,
            "detail": exc.detail,
            "success": False
        }
    ) 