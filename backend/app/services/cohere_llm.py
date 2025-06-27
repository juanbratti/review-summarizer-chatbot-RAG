# ===============================================
# DOCS
# ===============================================

"""
Cohere LLM Service for the RAG Chatbot API.
"""

# ===============================================
# IMPORTS
# ===============================================

import cohere
from ..config import settings

# ===============================================
# COHERE CLIENT AND CHAT HISTORY
# ===============================================

co = cohere.ClientV2(settings.cohere_api_key)

chat_history = []

# ===============================================
# SERVICES
# ===============================================

def get_embeddings(textos):
    """
    Get embeddings from Cohere.
    """
    response = co.embed(
        texts=textos,
        model=settings.embedding_model,
        input_type="search_query",
        embedding_types=["float"],
    )
    return response.embeddings.float_ 

def translate_query(query):
    """
    Translate a question to English.
    """
    
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
    
    content = llm(settings.llm_model, intr_system, query, 1)
    
    return content

def llm(modelo, prompt, msje, translation):
    """
    Use Cohere to generate a response from a prompt.
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

def get_llm_response(question: str, reviews: list):
    """
    Use Cohere to generate a response from reviews.
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
    
    

    content = llm(settings.llm_model, prompt, question, 0)

    return content

def translate_llm_answer(answer):
    """
    Translate the LLM answer to Spanish.
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
    
    content = llm(settings.llm_model, intr_system, query, 1)
    
    return content

