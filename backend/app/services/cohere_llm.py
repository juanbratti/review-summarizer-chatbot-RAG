# ===============================================
# DOCS
# ===============================================

"""
Cohere LLM Service for the RAG Chatbot API.
Handles all LLM operations including embeddings, chat, and translation.
"""

# ===============================================
# IMPORTS
# ===============================================

import cohere
from typing import List, Dict, Any
from ..config import settings
from ..exceptions import LLMException, TranslationException

# ===============================================
# COHERE CLIENT
# ===============================================

class CohereLLMService:
    """Service class for Cohere LLM operations."""
    
    def __init__(self):
        """Initialize Cohere client."""
        try:
            self.client = cohere.ClientV2(settings.cohere_api_key)
            self.chat_history: List[Dict[str, str]] = []
        except Exception as e:
            raise LLMException("Failed to initialize LLM service", str(e))
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings from Cohere.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            LLMException: If embedding generation fails
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=settings.embedding_model,
                input_type="search_query",
                embedding_types=["float"],
            )
            return response.embeddings.float_
        except Exception as e:
            raise LLMException("Failed to generate embeddings", str(e))
    
    def _chat_completion(self, messages: List[Dict[str, str]], model: str) -> str:
        """
        Internal method for chat completion.
        
        Args:
            messages: List of messages
            model: Model to use
            
        Returns:
            Generated response text
        """
        try:
            response = self.client.chat(model=model, messages=messages)
            return response.message.content[0].text
        except Exception as e:
            raise LLMException("Chat completion failed", str(e))
    
    def translate_text(self, text: str, target_language: str = "English") -> str:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language for translation
            
        Returns:
            Translated text
            
        Raises:
            TranslationException: If translation fails
        """
        try:
            system_prompt = f"""
            You are an expert translator who can translate texts from any language to another.
            You always maintain the exact meaning and coherence of the original text.
            Your task is to translate a text to {target_language}.
            """
            
            user_message = f"""
            You must translate the following text to {target_language}:
            
            {text}
            
            Your answer should be only the translated text.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            translated_text = self._chat_completion(messages, settings.llm_model)
            return translated_text.strip()
            
        except Exception as e:
            raise TranslationException("Translation failed", str(e))
    
    def generate_answer(self, question: str, context_reviews: List[str]) -> str:
        """
        Generate answer based on question and context reviews.
        
        Args:
            question: User question
            context_reviews: List of relevant reviews
            
        Returns:
            Generated answer
            
        Raises:
            LLMException: If answer generation fails
        """
        try:
            context = "\n".join(context_reviews)
            
            system_prompt = f"""
            You are a specialized system for answering questions about product reviews.
            You must answer the user's question using ONLY the reviews provided below.

            Reviews:
            {context}

            Rules:
            - Answer ONLY based on the information in the reviews
            - If you cannot answer based on the reviews, say "I can't answer that based on the available reviews."
            - Do not use emojis or emoticons
            - Be concise and factual
            - If the question is unrelated to product reviews, say "This question is not related to product reviews."
            """
            
            # Add to chat history for context
            self.chat_history.append({"role": "user", "content": question})
            
            messages = [{"role": "system", "content": system_prompt}] + self.chat_history
            
            answer = self._chat_completion(messages, settings.llm_model)
            
            # Add response to chat history
            self.chat_history.append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            raise LLMException("Failed to generate answer", str(e))
    
    def clear_chat_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get current chat history."""
        return self.chat_history.copy()

# ===============================================
# SERVICE INSTANCE
# ===============================================

# Create a singleton instance
_llm_service = None

def get_llm_service() -> CohereLLMService:
    """Get or create LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = CohereLLMService()
    return _llm_service

