# ===============================================
# DOCS
# ===============================================

"""
Chroma Database Service for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings
from .cohere_llm import get_embeddings
from ..config import settings
import json

# ===============================================
# EMBEDDING FUNCTION CLASS
# ===============================================

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Llama a la función de Cohere para obtener las embeddings
        return get_embeddings(input)  
    
# ===============================================
# CHROMA CLIENT AND COLLECTION
# ===============================================

# --- Initialize ChromaDB client using centralized configuration --- #
chroma_client = chromadb.PersistentClient(path=settings.chroma_db_path)
collection = chroma_client.get_or_create_collection(
    name=settings.collection_name,
    embedding_function=MyEmbeddingFunction(),
)

# ===============================================
# SEARCH SIMILAR REVIEWS FUNCTION
# ===============================================

def search_similar_reviews(question: str):
    """
    Search for similar reviews in Chroma.
    """
    result = collection.query(
        query_texts=[question],
        n_results=settings.similarity_results
    )

    docs = result["documents"][0]
    return docs, result

# ===============================================
# SAVE DOCUMENTS FUNCTION
# ===============================================

def save_documents(docs):
    """
    Store documents in ChromaDB.
    """
    try:
        # --- divide the documents into batches of 96 --- #
        batch_size = 96
        for i in range(0, len(docs), batch_size):
            batch_docs = docs[i:i + batch_size]
            batch_ids = [f"chunk_{i+j}_doc_id{i+j}" for j in range(len(batch_docs))]
            
            # --- store the batch of documents --- #
            collection.add(
                documents=batch_docs,
                ids=batch_ids
            )
            
            print(f"Batch {i // batch_size + 1} de {len(docs) // batch_size + 1} guardado.")
    except Exception as e:
        raise Exception(f"Error when saving docs in chroma: {str(e)}")
