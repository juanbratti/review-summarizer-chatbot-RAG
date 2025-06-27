from fastapi import FastAPI
from .routers import question_router, upload_router, search_router, get_chat_history
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Reseñas Q&A",
              description="API para responder preguntas sobre reseñas usando ChromaDB y un LLM.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Incluimos los routers, incluimos el de upload y el de preguntas
app.include_router(upload_router.router, prefix="/app", tags=["upload"])
app.include_router(question_router.router, prefix="/app", tags=["questions"])
app.include_router(search_router.router, prefix="/app", tags=["search"])
app.include_router(get_chat_history.router, prefix="/app", tags=["chat_history"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Reseñas QA"}

# Para ejecutar con uvicorn:
# uvicorn app.main:app --reload
