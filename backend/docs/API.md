# API Documentation

Complete reference for the Review Summarizer RAG Chatbot API.

## Base URL

```
http://localhost:8000
```

## Authentication

This API requires a Cohere API key configured in the environment variables. No authentication headers are needed for client requests.

## Common Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Endpoints

### 1. Ask Question

Ask a question about the uploaded reviews and get an AI-generated answer.

**Endpoint:** `POST /app/questions/`

**Request Body:**
```json
{
  "question": "What do customers think about the product quality?"
}
```

**Request Model:**
- `question`: string (1-500 characters) - The question to ask

**Response:**
```json
{
  "answer": "Based on the reviews, customers generally appreciate the product quality...",
  "results": [
    {
      "document_id": "chunk_0_doc_id0",
      "content_snippet": "The quality is excellent and the product works as expected...",
      "similarity_score": 0.234
    }
  ],
  "success": true
}
```

**Response Model:**
- `answer`: string - AI-generated answer based on reviews
- `results`: array of SearchResult objects - Related review chunks
- `success`: boolean - Operation success status

**Status Codes:**
- `200`: Success
- `404`: No relevant reviews found
- `500`: Server error

**Example Usage:**
```bash
curl -X POST "http://localhost:8000/app/questions/" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Is the machine affordable?"
     }'
```

---

### 2. Search Reviews

Search for reviews similar to a query without generating an answer.

**Endpoint:** `POST /app/search/`

**Request Body:**
```json
{
  "query": "price affordability"
}
```

**Request Model:**
- `query`: string (1-500 characters) - Search query

**Response:**
```json
{
  "results": [
    {
      "document_id": "chunk_5_doc_id5",
      "content_snippet": "Most reviews say the machine is affordable and ...",
      "similarity_score": 0.156
    }
  ],
  "total_results": 5,
  "success": true
}
```

**Response Model:**
- `results`: array of SearchResult objects
- `total_results`: integer - Number of results found
- `success`: boolean - Operation success status

**Status Codes:**
- `200`: Success
- `500`: Server error

---

### 3. Upload Reviews

Upload and process review documents for the knowledge base.

**Endpoint:** `POST /app/upload/`

**Request Body:**
```json
{
  "reviews": "This product is amazing! The quality is top-notch and delivery was fast.\n\nAnother review: Great value for money..."
}
```

**Request Model:**
- `reviews`: string (minimum 1 character) - Reviews text to upload

**Response:**
```json
{
  "message": "Reviews uploaded and processed successfully.",
  "documents_processed": 15,
  "success": true
}
```

**Response Model:**
- `message`: string - Success message
- `documents_processed`: integer - Number of document chunks created
- `success`: boolean - Operation success status

**Status Codes:**
- `200`: Success
- `400`: Bad request (empty reviews)
- `500`: Server error

**Notes:**
- Reviews are automatically split into chunks for better processing
- Default chunk size is 2000 characters
- Processing happens in batches of 96 documents

---

### 4. Get Chat History

Retrieve the current conversation history.

**Endpoint:** `GET /app/history/`

**Request:** No body required

**Response:**
```json
{
  "history": [
    {
      "role": "user",
      "content": "How is the product quality?"
    },
    {
      "role": "assistant", 
      "content": "Based on the reviews, the product quality is highly rated..."
    }
  ]
}
```

**Response Model:**
- `history`: array of ChatMessage objects
  - `role`: string - "user", "assistant", or "system"
  - `content`: string - Message content

**Status Codes:**
- `200`: Success
- `500`: Server error

---

### 5. Clear Chat History

Clear the conversation history.

**Endpoint:** `POST /app/questions/clear-history/`

**Request:** No body required

**Response:**
```json
{
  "message": "Chat history cleared successfully",
  "success": true
}
```

**Status Codes:**
- `200`: Success
- `500`: Server error

---

## Data Models

### SearchResult

```json
{
  "document_id": "string",
  "content_snippet": "string", 
  "similarity_score": "number"
}
```

- `document_id`: Unique identifier for the document chunk
- `content_snippet`: Preview of the document content (truncated)
- `similarity_score`: Distance score (lower = more similar)

### ChatMessage

```json
{
  "role": "user|assistant|system",
  "content": "string"
}
```

- `role`: Message sender type
- `content`: Message text content

## Error Handling

### Error Response Format

```json
{
  "error": "Brief error description",
  "detail": "Detailed error information",
  "success": false
}
```

### Common Error Codes

| Status | Error | Description |
|--------|-------|-------------|
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | No relevant results found |
| 422 | Validation Error | Request body validation failed |
| 500 | Internal Server Error | Server-side error |

### Error Types

1. **ValidationException**: Invalid input format
2. **LLMException**: AI service errors
3. **DatabaseException**: Database operation errors
4. **TranslationException**: Translation service errors
5. **NoResultsException**: No matching results found

## Rate Limiting

Currently no rate limiting is implemented.

## Interactive Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: http://localhost:8000/docs

These interfaces allow you to:
- Test endpoints directly
- View request/response schemas
- See example payloads
- Understand validation rules
