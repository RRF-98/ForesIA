from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from services.text_service import TextAnalyzerService

router = APIRouter()
_service = TextAnalyzerService()  # singleton — modelo carregado uma vez na inicializacao


class TextRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_have_min_length(cls, v: str) -> str:
        if len(v.strip()) < 5:
            raise ValueError("Texto deve ter no minimo 5 caracteres")
        return v.strip()


class TextAnalysisResponse(BaseModel):
    probability: float
    model_used: str
    method: str


@router.post("/text", response_model=dict)
def analyze_text(request: TextRequest):
    """
    Recebe texto e retorna probabilidade de ser gerado por IA.
    probability: 0.0 (humano) a 1.0 (IA)
    """
    try:
        result = _service.analyze(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na analise: {str(e)}")
