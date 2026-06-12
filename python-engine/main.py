from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import text_analyzer

app = FastAPI(
    title="ForensIA Engine",
    description="Motor de analise de conteudo gerado por IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(text_analyzer.router, prefix="/analyze", tags=["text"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "ForensIA Engine"}
