# ===============================================
# DOCS
# ===============================================

"""
Configuration management for the RAG Chatbot API.
Handles environment variables, API keys, and application settings.
"""

# ===============================================
# IMPORTS
# ===============================================

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache

# ===============================================
# SETTINGS CLASS
# ===============================================

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # --- Application Settings --- #
    app_name: str = "Review Summarizer RAG Chatbot"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # --- Server Configuration --- #
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=True, env="RELOAD")
    
    # --- API Keys --- #
    cohere_api_key: str = Field(..., env="COHERE_API_KEY")
    
    # --- Database Configuration --- #
    chroma_db_path: str = Field(default="./.chromadb", env="CHROMA_DB_PATH")
    collection_name: str = Field(default="reviewsdb", env="COLLECTION_NAME")
    
    # --- RAG Configuration --- #
    chunk_size: int = Field(default=2000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=0, env="CHUNK_OVERLAP")
    similarity_results: int = Field(default=10, env="SIMILARITY_RESULTS")
    
    # --- LLM Configuration --- #
    llm_model: str = Field(default="command-r-plus-04-2024", env="LLM_MODEL")
    embedding_model: str = Field(default="embed-english-v3.0", env="EMBEDDING_MODEL")
    
    # --- CORS Configuration (simplified) --- #
    cors_origins: str = Field(default="*", env="CORS_ORIGINS")
    
    # --- Logging Configuration --- #
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# ===============================================
# GET SETTINGS FUNCTION
# ===============================================

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    Using lru_cache to ensure settings are loaded only once.
    """
    return Settings()
settings = get_settings() 