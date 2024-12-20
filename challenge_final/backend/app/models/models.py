from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    results: list

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list

class Input(BaseModel):
    reviews : str

class ChatMessage(BaseModel):
    role : str
    content : str

class ChatHistory(BaseModel):
    history : list[ChatMessage]
