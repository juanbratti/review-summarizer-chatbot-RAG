# ===============================================
# DOCS
# ===============================================

"""
Chroma Database Service for the RAG Chatbot API.
Handles ChromaDB operations with improved error handling.
"""

# ===============================================
# IMPORTS
# ===============================================

import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings
from .cohere_llm import get_llm_service
from ..config import settings
from ..exceptions import DatabaseException

# ===============================================
# EMBEDDING FUNCTION CLASS
# ===============================================

class MyEmbeddingFunction(EmbeddingFunction):
    """Custom embedding function using Cohere LLM service."""
    
    def __init__(self):
        """Initialize the embedding function with LLM service."""
        self.llm_service = get_llm_service()
    
    def __call__(self, input: Documents) -> Embeddings:
        """Generate embeddings for the input documents."""
        try:
            return self.llm_service.get_embeddings(input)
        except Exception as e:
            raise DatabaseException("Failed to generate embeddings for documents", str(e))

# ===============================================
# CHROMA CLIENT AND COLLECTION
# ===============================================

def get_chroma_collection():
    """
    Get or create ChromaDB collection with error handling.
    
    Returns:
        ChromaDB collection instance
        
    Raises:
        DatabaseException: If collection initialization fails
    """
    try:
        chroma_client = chromadb.PersistentClient(path=settings.chroma_db_path)
        collection = chroma_client.get_or_create_collection(
            name=settings.collection_name,
            embedding_function=MyEmbeddingFunction(),
        )
        return collection
    except Exception as e:
        raise DatabaseException("Failed to initialize ChromaDB collection", str(e))

# --- Global collection instance --- #
_collection = None

def get_collection():
    """Get or create collection instance (singleton pattern)."""
    global _collection
    if _collection is None:
        _collection = get_chroma_collection()
    return _collection

# ===============================================
# DATABASE OPERATIONS
# ===============================================

def search_similar_reviews(question: str):
    """
    Search for similar reviews in ChromaDB.
    
    Args:
        question: The search query
        
    Returns:
        Tuple of (documents, raw_result)
        
    Raises:
        DatabaseException: If search fails
    """
    try:
        collection = get_collection()
        result = collection.query(
            query_texts=[question],
            n_results=settings.similarity_results
        )
        
        docs = result["documents"][0] if result["documents"] and result["documents"][0] else []
        return docs, result
        
    except Exception as e:
        raise DatabaseException("Failed to search similar reviews", str(e))

def save_documents(docs):
    """
    Store documents in ChromaDB with batch processing.
    
    Args:
        docs: List of documents to store
        
    Raises:
        DatabaseException: If saving fails
    """
    try:
        collection = get_collection()
        
        # --- Divide documents into batches to avoid memory issues --- #
        batch_size = 96
        total_batches = (len(docs) + batch_size - 1) // batch_size
        
        for i in range(0, len(docs), batch_size):
            batch_docs = docs[i:i + batch_size]
            batch_ids = [f"chunk_{i+j}_doc_id{i+j}" for j in range(len(batch_docs))]
            
            # --- Store the batch of documents --- #
            collection.add(
                documents=batch_docs,
                ids=batch_ids
            )
            
            batch_num = i // batch_size + 1
            print(f"Batch {batch_num} of {total_batches} saved successfully.")
            
    except Exception as e:
        raise DatabaseException("Failed to save documents to ChromaDB", str(e))

def get_collection_stats():
    """
    Get collection statistics.
    
    Returns:
        Dictionary with collection stats
    """
    try:
        collection = get_collection()
        count = collection.count()
        return {
            "document_count": count,
            "collection_name": settings.collection_name,
            "status": "healthy" if count > 0 else "empty"
        }
    except Exception as e:
        raise DatabaseException("Failed to get collection statistics", str(e))
