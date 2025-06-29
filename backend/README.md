# Review Summarizer RAG Chatbot - Backend

A FastAPI-based backend service that uses Retrieval-Augmented Generation (RAG) to answer questions about product reviews using ChromaDB and Cohere AI.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Project Structure](#project-structure)
- [Code Patterns & Best Practices](#code-patterns--best-practices)
- [Troubleshooting](#troubleshooting)

## Features

- **Question Answering**: Ask questions about product reviews in any language
- **Semantic Search**: Find similar reviews using vector embeddings
- **Multi-language Support**: Automatic translation between Spanish and English
- **Review Upload**: Process and store review documents
- **Chat History**: Maintain conversation context
- **Error Handling**: Comprehensive error management with detailed responses

## Architecture

### Design Patterns Used

1. **Dependency Injection**: Clean service management with FastAPI's `Depends()`
2. **Service Layer Pattern**: Business logic separated from HTTP handling
3. **Repository Pattern**: Data access abstraction through ChromaDB service
4. **Exception Hierarchy**: Custom exceptions for different error types
5. **Singleton Pattern**: Single instance of services across requests
6. **Model Validation**: Pydantic models for request/response validation

## 📦 Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Cohere API key

### Setup

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Required
COHERE_API_KEY=your_cohere_api_key_here

# Optional (with defaults)
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Database
CHROMA_DB_PATH=./.chromadb
COLLECTION_NAME=reviewsdb

# RAG Configuration
CHUNK_SIZE=2000
CHUNK_OVERLAP=0
SIMILARITY_RESULTS=10

# LLM Configuration
LLM_MODEL=command-r-plus-04-2024
EMBEDDING_MODEL=embed-english-v3.0

# CORS
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
LOG_FILE=
```

### Configuration Class

The app uses Pydantic Settings for configuration management:

```python
class Settings(BaseSettings):
    # Automatically loads from environment variables
    cohere_api_key: str = Field(..., env="COHERE_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

## API Documentation

### Running the Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs

### API Endpoints

#### Questions
- `POST /app/questions/` - Ask a question about reviews
- `POST /app/questions/clear-history/` - Clear chat history

#### Search
- `POST /app/search/` - Search for similar reviews

#### Upload
- `POST /app/upload/` - Upload and process reviews

#### Chat History
- `GET /app/history/` - Get current chat history

## 🛠️ Development

### Running in Development Mode

```bash
python -m uvicorn app.main:app --reload
```

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── exceptions.py          # Custom exceptions
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── question_router.py  # Question handling
│   │   ├── search_router.py    # Search endpoints
│   │   ├── upload_router.py    # File upload
│   │   └── get_chat_history.py # Chat history
│   └── services/
│       ├── __init__.py
│       ├── cohere_llm.py      # LLM service
│       └── chroma_database.py  # Database service
├── requirements.txt
├── .env                       # Environment variables
└── README.md
```

## Code Patterns & Best Practices

### 1. Dependency Injection

**Why**: Better testability, cleaner code, single responsibility

```python
# Instead of creating services inside endpoints
async def ask_question(
    question_request: QuestionRequest,
    llm_service: CohereLLMService = Depends(get_llm_dependency)
):
    # Use injected service
    answer = llm_service.generate_answer(...)
```

### 2. Service Layer Architecture

**Why**: Separation of concerns, reusable business logic

```python
class CohereLLMService:
    """Handles all LLM operations"""
    
    def translate_text(self, text: str) -> str:
        # Business logic here
        
    def generate_answer(self, question: str, context: List[str]) -> str:
        # Business logic here
```

### 3. Custom Exception Hierarchy

**Why**: Better error handling, consistent error responses

```python
class RAGChatbotException(Exception):
    """Base exception"""
    
class LLMException(RAGChatbotException):
    """Specific to LLM operations"""
    
class DatabaseException(RAGChatbotException):
    """Specific to database operations"""
```

### 4. Pydantic Models with Validation

**Why**: Type safety, automatic validation, better documentation

```python
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    
class QuestionResponse(BaseModel):
    answer: str
    results: List[SearchResult]
    success: bool = True
```

### 5. Response Model Consistency

**Why**: Predictable API responses, better client integration

```python
# All responses include success field
{
    "answer": "Generated answer",
    "results": [...],
    "success": true
}

# Error responses follow same pattern
{
    "error": "Error message",
    "detail": "Detailed information", 
    "success": false
}
```

### 6. Type Hints

**Why**: Better IDE support, catch errors early, self-documenting code

```python
def format_search_results(result: dict) -> List[SearchResult]:
    """Clear input/output types"""
    
async def ask_question(
    question_request: QuestionRequest,
    llm_service: CohereLLMService = Depends(get_llm_dependency)
) -> QuestionResponse:
```
