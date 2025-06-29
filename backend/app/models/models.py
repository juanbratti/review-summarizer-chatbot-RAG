# ===============================================
# DOCS
# ===============================================

"""
Defines request/response models with proper validation.
"""

# ===============================================
# IMPORTS
# ===============================================

from pydantic import BaseModel, Field
from typing import List, Optional

# ===============================================
# REQUEST MODELS
# ===============================================

class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str = Field(..., min_length=1, max_length=500, description="The question to ask")

class SearchRequest(BaseModel):
    """Request model for searching reviews."""
    query: str = Field(..., min_length=1, max_length=500, description="Search query")

class UploadRequest(BaseModel):
    """Request model for uploading reviews."""
    reviews: str = Field(..., min_length=1, description="Reviews to upload")

# ===============================================
# RESPONSE MODELS
# ===============================================

class SearchResult(BaseModel):
    """Individual search result model."""
    document_id: str = Field(..., description="Unique document identifier")
    content_snippet: str = Field(..., description="Preview of the document content")
    similarity_score: float = Field(..., description="Similarity score (lower is more similar)")

class QuestionResponse(BaseModel):
    """Response model for question answers."""
    answer: str = Field(..., description="Generated answer to the question")
    results: List[SearchResult] = Field(default_factory=list, description="Related search results")
    success: bool = Field(default=True, description="Whether the operation was successful")

class SearchResponse(BaseModel):
    """Response model for search results."""
    results: List[SearchResult] = Field(default_factory=list, description="Search results")
    total_results: int = Field(..., ge=0, description="Total number of results found")
    success: bool = Field(default=True, description="Whether the search was successful")

class UploadResponse(BaseModel):
    """Response model for upload operations."""
    message: str = Field(..., description="Upload status message")
    documents_processed: int = Field(..., ge=0, description="Number of documents processed")
    success: bool = Field(default=True, description="Whether the upload was successful")

# ===============================================
# CHAT MODELS
# ===============================================

class ChatMessage(BaseModel):
    """Individual chat message model."""
    role: str = Field(..., pattern="^(user|assistant|system)$", description="Message role")
    content: str = Field(..., min_length=1, description="Message content")

class ChatHistory(BaseModel):
    """Chat history model."""
    history: List[ChatMessage] = Field(default_factory=list, description="List of chat messages")

# ===============================================
# ERROR MODELS
# ===============================================

class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    success: bool = Field(default=False, description="Always false for errors")
