# Documentación Proyecto: Sistema de Preguntas y Respuestas con Reseñas


# Descripción General

Este proyecto está diseñado para proporcionar una interfaz de preguntas y respuestas sobre productos, basada en reseñas. Utiliza ChromaDB para almacenar y consultar reseñas similares a las preguntas, y Cohere LLM (Large Language Model) para generar respuestas basadas en estas reseñas. El sistema es capaz de traducir las preguntas y respuestas entre varios idiomas.

# Endpoints de la API

## 1. `/history/` (Método: `GET`)

### Descripción:

Este endpoint devuelve el historial de mensajes de chat. El historial es generado en función de las interacciones previas realizadas por el usuario con el sistema.

### Respuesta:

- **Código de respuesta:** `200 OK`
- **Cuerpo de la respuesta:** Un objeto `ChatHistory` que contiene una lista de mensajes del chat. Cada mensaje incluye un rol (por ejemplo, `user`, `assistant`) y el contenido del mensaje.

### Ejemplo de respuesta:

```json

{
  "history": [
    {
      "role": "user",
      "content": "¿Cuál es la mejor característica del producto?"
    },
    {
      "role": "assistant",
      "content": "La mejor característica es su durabilidad."
    }
  ]
}

```

### Código

```jsx
@router.get("/history/", response_model=ChatHistory)
async def get_chat_history():
    history = [ChatMessage(role=msg['role'], content=msg['content']) for msg in chat_history]
    
    return ChatHistory(history=history)
```

## 2. `/questions/` (Método: `POST`)

### Descripción:

Este endpoint recibe una pregunta del usuario, busca reseñas similares utilizando ChromaDB, y utiliza Cohere LLM para generar una respuesta. La respuesta es traducida al español.

### Parámetros:

- **Cuerpo de la solicitud:** Un objeto `QuestionRequest` con el siguiente formato:
    
    ```json
    
    {
      "question": "¿Es este producto fácil de usar?"
    }
    
    ```
    

### Respuesta:

- **Código de respuesta:** `200 OK`
- **Cuerpo de la respuesta:** Un objeto `QuestionResponse` que contiene la respuesta generada por el LLM y una lista de reseñas similares.

### Ejemplo de respuesta:

```python

{
  "answer": "Sí, el producto es muy fácil de usar.",
  "results": [
    {
      "document_id": "chunk_0_doc_id1",
      "content_snippet": "Este producto tiene una interfaz amigable...",
      "similarity_score": 0.95
    },
    {
      "document_id": "chunk_0_doc_id2",
      "content_snippet": "La facilidad de uso es una de las principales ventajas...",
      "similarity_score": 0.92
    }
  ]
}

```

### Código

```python
@router.post("/questions/", response_model=QuestionResponse)
async def ask_question(question: QuestionRequest):
    """
    Recibe una pregunta, busca reseñas similares usando chroma,
    y utiliza un LLM para responder.
    """
    try:

        question_og = question.question

        # Traducir la pregunta al inglés
        question_en = translate_query(question_og)

        # Buscar reseñas similares en ChromaDB
        similar_reviews, result = search_similar_reviews(question_en)

        # Si no hay reseñas similares, responder con un mensaje
        if not similar_reviews:
            return {"answer": "No reviews found for that question."}

        # Generar respuesta usando el LLM
        llm_answer = get_llm_response(question_en, similar_reviews)
    
        # traduzco respuesta del idioma a español
        llm_answer_translated = translate_llm_answer(llm_answer)

        formatted_results = [
            {
                "document_id": result["ids"][0][i],
                "content_snippet": result["documents"][0][i][:100],
                "similarity_score": result["distances"][0][i]
            } for i in range(len(result["ids"][0]))
        ]

        return {"answer": llm_answer_translated, "results": formatted_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

## 3. `/search` (Método: `POST`)

### Descripción:

Este endpoint realiza una búsqueda de documentos similares basados en una consulta. Utiliza ChromaDB para encontrar reseñas relacionadas.

### Parámetros:

- **Cuerpo de la solicitud:** Un objeto `SearchRequest` con el siguiente formato:
    
    ```json
    
    {
      "query": "¿Cómo se compara este producto con otros en términos de calidad?"
    }
    
    ```
    

### Respuesta:

- **Código de respuesta:** `200 OK`
- **Cuerpo de la respuesta:** Un objeto `SearchResponse` que contiene una lista de documentos similares encontrados.

### Ejemplo de respuesta:

```json

{
  "results": [
    {
      "document_id": "chunk_0_doc_id1",
      "content_snippet": "Este producto ofrece una calidad superior...",
      "similarity_score": 0.93
    },
    {
      "document_id": "chunk_0_doc_id2",
      "content_snippet": "Comparado con otros productos, su calidad es impresionante...",
      "similarity_score": 0.91
    }
  ]
}

```

### Código

```python
@router.post("/search", status_code=200, response_model=SearchResponse)
async def search(to_search: SearchRequest):
    """
    Endpoint que realiza una búsqueda de documentos similares y devuelve múltiples resultados.
    """
    # traucir la pregunta al inglés
    question_en = translate_query(to_search.query)

    docs, result = search_similar_reviews(question_en)

    formatted_results = [
        {
            "document_id": result["ids"][0][i],
            "content_snippet": result["documents"][0][i][:100],
            "similarity_score": result["distances"][0][i]
        } for i in range(len(result["ids"][0]))
    ]

    return {"results": formatted_results}
```

## 4. `/upload/` (Método: `POST`)

### Descripción:

Este endpoint recibe un conjunto de reseñas en formato de texto, las procesa, las divide en fragmentos/chunks y las almacena en ChromaDB.

### Parámetros:

- **Cuerpo de la solicitud:** Un objeto `Input` que contiene una cadena de texto con las reseñas:
    
    ```json
    json
    Copiar código
    {
      "reviews": "Este producto es excelente. Me encanta su diseño..."
    }
    
    ```
    

### Respuesta:

- **Código de respuesta:** `200 OK`
- **Cuerpo de la respuesta:** Un mensaje indicando que los documentos fueron cargados correctamente.

### Ejemplo de respuesta:

```json

{
  "message": "Docs loaded successfully."
}

```

### Código

```python
@router.post("/upload/")
async def upload_reviews(reviews : Input):
    """
    Endpoint que recibe un string con reseñas, las procesa, las vectoriza y las almacena en ChromaDB.
    """
    if not reviews.reviews:
        raise HTTPException(status_code=400, detail="String can't be empty.")

    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        chunks = text_splitter.split_text(reviews.reviews)
        # almacenamiento de los documentos en ChromaDB
        save_documents(chunks)
        return {"message": "Docs loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
```

## Servicios

## 1. `search_similar_reviews(question: str)` | Chroma

### Descripción:

Este servicio consulta ChromaDB para buscar reseñas que sean similares a la pregunta proporcionada.

### Parámetros:

- **question:** La pregunta que se desea buscar en las reseñas.

### Respuesta:

- **docs:** Las reseñas similares encontradas.
- **result:** El resultado de la consulta con detalles de los documentos y su similitud.

```python
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
```

## 2. `save_documents(docs)` | Chroma

### Descripción:

Este servicio guarda los documentos procesados en ChromaDB. En este servicio, tuve el problema de que no podía guardar todos los documentos de una en Chroma, ya que tiene un límite de 96 documentos en cada subida. Por lo que decidí subirlo por lotes.

### Parámetros:

- **docs:** Una lista de documentos (chunks de reseñas) que se almacenarán.

```python
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
```

## 3. `get_embeddings(textos)` | Cohere

### Descripción:

Este servicio utiliza Cohere para generar embeddings (representaciones vectoriales) de los textos proporcionados.

### Parámetros:

- **textos:** La lista de textos de los cuales se generarán los embeddings.

### Respuesta:

- **Embeddings:** Representaciones vectoriales de los textos proporcionados.

```python
def get_embeddings(textos):
    """Función para obtener embeddings de Cohere."""
    response = co.embed(
        texts=textos,
        model="embed-english-v3.0",
        input_type="search_query",
        embedding_types=["float"],
    )
    return response.embeddings.float_ 
```

## 4. `translate_query(query)` | Cohere

### Descripción:

Este servicio traduce una consulta del usuario a inglés utilizando el modelo LLM de Cohere.

### Parámetros:

- **query:** La consulta en cualquier idioma.

### Respuesta:

- **query_en:** La consulta traducida al inglés.

```python
def translate_query(query):
    """Función para traducir una pregunta al inglés."""
    
    intr_system = """
        You are an expert translator who can translate texts from any language to another.
        You always maintain the exact meaning and coherence of the original text.
        Your task is to translate a text to English.
        """
    
    query = f"""
        You must translate the following text to English:
        \n
        {query}
        \n
        Your answer should be only the translated text.
        """
    
    content = llm('command-r-plus-04-2024', intr_system, query, 1)
    
    return content
```

## 5. `get_llm_response(question, reviews)` | Cohere

### Descripción:

Este servicio utiliza Cohere para generar una respuesta a una pregunta, utilizando un conjunto de reseñas como contexto.

### Parámetros:

- **question:** La pregunta que se desea responder.
- **reviews:** Las reseñas que proporcionan el contexto para la respuesta.

### Respuesta:

- **Respuesta generada:** Una respuesta basada en el contexto proporcionado.

```python
def get_llm_response(question: str, reviews: list):
    """
    Utiliza Cohere para generar una respuesta a partir de reseñas.
    """

    context = "\n".join(reviews)

    prompt = f"""
                You are a specialized system in answering questions about product reviews.
                You must answer the user's question about a product using the reviews given:

                Reviews:
                {context}

                You must obey the following rules:
                - You must not answer with information that is not in the context.
                - If you cannot answer the question, or the question is not related to the reviews, you must answer with "I can't answer that."
                - Do not use emojis or emoticons in your answer.
                - If the question has already been made, you must answer with the previous answer.
                """
    
    

    content = llm('command-r-plus-04-2024', prompt, question, 0)

    return content

```

## 6. `translate_llm_answer(answer)`

### Descripción:

Este servicio traduce la respuesta generada por el LLM de Cohere al español.

### Parámetros:

- **answer:** La respuesta generada por el LLM en inglés.

### Respuesta:

- **answer_es:** La respuesta traducida al español.

```python
def translate_llm_answer(answer):
    """
    Traduce la respuesta del LLM al Español.
    """

    intr_system = """
        You are an expert translator who can translate texts from any language to another.
        You always maintain the exact meaning and coherence of the original text.
        Your task is to translate a text to spanish.
        """
    
    query = f"""
        Text to translate: {answer}

        You must not answer with anything other than the translated text. Make sure the text to translate is in spanish.
        """
    
    content = llm('command-r-plus-04-2024', intr_system, query, 1)
    
    return content
```

## 7. `llm(modelo, prompt, msje, translation)`

### Descripción:

Esta función utiliza el modelo de lenguaje de Cohere para generar una respuesta basada en un prompt y un mensaje proporcionado. La función mantiene un historial de conversaciones para generar respuestas más contextuales y coherentes, especialmente en interacciones consecutivas.

Es usada por las funciones de traducción.

### **Parámetros:**

- `modelo` (str): El nombre del modelo de Cohere que se utilizará para generar la respuesta. Ejemplo: `'command-r-plus-04-2024'`.
- `prompt` (str): El texto que se envía como indicación o contexto al modelo de Cohere. Este parámetro debe proporcionar la información necesaria para que el modelo genere una respuesta relevante.
- `msje` (str): El mensaje del usuario o la consulta que se desea responder. Este mensaje es utilizado por el modelo para generar una respuesta adecuada en base al `prompt` y el historial de conversación (si aplica).
- `translation` (bool): Un valor booleano que indica si la respuesta debe ser traducida. Si es `False`, la función mantiene un historial de conversación y genera la respuesta en el contexto de esa conversación. Si es `True`, la respuesta se genera sin historial previo y se traduce al español.

### Respuesta:

Devuelve una cadena de texto (`str`) que es la respuesta generada por el modelo de Cohere en función del `prompt` y `msje`. Si `translation` es `True`, solo se hace la tarea de traducción. Si `translation` es `False`, la respuesta será generada utilizando el historial de conversación.

```python
def llm(modelo, prompt, msje, translation):
    """
    Utiliza Cohere para generar una respuesta a partir de un prompt.
    """
    if not translation:
        chat_history.append({"role": "user", "content": msje})

        response = co.chat(
            model=modelo,
            messages=[{"role": "system", "content": prompt}] + chat_history,
        )

        content=(response.message).content[0].text

        chat_history.append({"role": "assistant", "content": content})
        return content
    else:
        response = co.chat(
            model=modelo,
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": msje}]
        )

        content=(response.message).content[0].text
        
        return content
```

---

## Modelos

## 1. `QuestionRequest`

### Descripción:

Modelo de entrada que representa una pregunta hecha por el usuario.

### Campos:

- **question:** La pregunta del usuario.

## 2. `QuestionResponse`

### Descripción:

Modelo de salida que representa la respuesta generada y los resultados de las reseñas similares.

### Campos:

- **answer:** La respuesta generada por el LLM.
- **results:** Una lista de reseñas similares encontradas.

## 3. `SearchRequest`

### Descripción:

Modelo de entrada que representa una consulta de búsqueda de reseñas similares.

### Campos:

- **query:** La consulta que el usuario desea buscar.

## 4. `SearchResponse`

### Descripción:

Modelo de salida que representa los resultados de una búsqueda de reseñas similares.

### Campos:

- **results:** Una lista de documentos similares.

## 5. `Input`

### Descripción:

Modelo de entrada que contiene las reseñas a ser cargadas en ChromaDB.

### Campos:

- **reviews:** Un string que contiene las reseñas a ser procesadas.

## 6. `ChatMessage`

### Descripción:

Modelo que representa un mensaje del chat (usuario o asistente).

### Campos:

- **role:** El rol del mensaje (usuario o asistente).
- **content:** El contenido del mensaje.

## 7. `ChatHistory`

### Descripción:

Modelo que representa el historial de mensajes del chat.

### Campos:

- **history:** Una lista de objetos `ChatMessage`.