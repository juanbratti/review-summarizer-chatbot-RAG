import chromadb
from chromadb import EmbeddingFunction, Documents, Embeddings
from .cohere_llm import get_embeddings
import json
# Inicializamos ChromaDB client. tiene que ser persistente 

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Llama a la función de Cohere para obtener las embeddings
        return get_embeddings(input)  

chroma_client = chromadb.PersistentClient(path="./.chromadb")
collection = chroma_client.get_or_create_collection(name="reviewsdb",
                                      embedding_function=MyEmbeddingFunction(),
                                     )


# Modelo de embeddings
def search_similar_reviews(question: str):
    """
    Busca reseñas similares a la pregunta en Chroma.
    """
    result = collection.query(
        query_texts = [question],
        n_results = 10
    )

    docs = result["documents"][0]
    return docs, result

def save_documents(docs):
    """
    Almacena documentos en ChromaDB.
    """
    # Almacenar los chunks en ChromaDB

    try:
        # Dividir los documentos en lotes de 96
        batch_size = 96
        for i in range(0, len(docs), batch_size):
            batch_docs = docs[i:i + batch_size]
            batch_ids = [f"chunk_{i+j}_doc_id{i+j}" for j in range(len(batch_docs))]
            
            # Guardar el lote de documentos
            collection.add(
                documents=batch_docs,
                ids=batch_ids
            )
            
            print(f"Batch {i // batch_size + 1} de {len(docs) // batch_size + 1} guardado.")
    except Exception as e:
        raise Exception(f"Error when saving docs in chroma: {str(e)}")
