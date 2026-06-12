# ForensIA — Arquitetura Técnica

## Visão Geral

Sistema distribuído de dois microserviços para detecção forense de conteúdo gerado por IA:

```
┌─────────────────────────────────────┐     HTTP POST      ┌──────────────────────────────┐
│         Spring Boot :8080           │ ─────────────────► │       FastAPI :8001           │
│                                     │                     │                              │
│  AuthController    /auth/**         │                     │  GET  /health                │
│  AnalysisController /api/v1/**      │ ◄───────────────── │  POST /analyze/text          │
│  GlobalExceptionHandler             │   { probability }   │                              │
│  JwtFilter (Spring Security)        │                     │  TextAnalyzerService         │
│  PostgreSQL + Redis                 │                     │  (RoBERTa | heurísticas)     │
└─────────────────────────────────────┘                     └──────────────────────────────┘
```

---

## Fluxo de Análise

```
1. Cliente envia POST /api/v1/analysis/text com JWT no header
2. JwtFilter valida token → extrai username do contexto Spring Security
3. AnalysisController recebe requisição → chama AnalysisService.analyzeText(username, request)
4. AnalysisService monta payload { "text": "..." }
5. AnalysisService faz HTTP POST para http://localhost:8001/analyze/text via RestTemplate
6. FastAPI recebe → TextAnalyzerService.analyze(text)
7. TextAnalyzerService tenta modelo RoBERTa, cai em heurísticas se indisponível
8. FastAPI retorna { probability: 0.87, model_used: "...", method: "..." }
9. AnalysisService classifica: <0.30=HUMANO, 0.30-0.69=HIBRIDO, ≥0.70=IA_GERADO
10. AnalysisService persiste Analysis no PostgreSQL
11. AnalysisService retorna ApiResponse<AnalysisResult> ao controller
12. Controller retorna HTTP 200 com JSON padronizado
```

---

## Camadas do Backend Java

### Config
| Classe | Responsabilidade |
|--------|-----------------|
| `SecurityConfig` | Configura Spring Security — rotas públicas (`/auth/**`) e protegidas (`/api/v1/**`) |
| `RestTemplateConfig` | Bean `RestTemplate` + bean `String aiEngineBaseUrl` para injeção no `AnalysisService` |

### Segurança
| Classe | Responsabilidade |
|--------|-----------------|
| `JwtFilter` | Intercepta todas as requisições, valida JWT do header `Authorization: Bearer` |
| `JwtUtil` | Geração e validação de tokens JWT |
| `UserDetailsServiceImpl` | Implementa `UserDetailsService` — carrega `User` do banco para Spring Security |

### Controllers
| Classe | Endpoints |
|--------|----------|
| `AuthController` | `POST /auth/register`, `POST /auth/login` |
| `AnalysisController` | `POST /api/v1/analysis/text` (protegido por JWT) |

### Services
| Classe | Responsabilidade |
|--------|-----------------|
| `AuthService` | Registro com BCrypt, login com geração de JWT, checagem de unicidade |
| `AnalysisService` | Orquestra chamada HTTP ao motor Python, classifica e persiste resultado |

### Modelos de Dados
| Entidade | Campos relevantes |
|----------|------------------|
| `User` | `username`, `email_user`, `password_user` (BCrypt), `role` |
| `Analysis` | `username`, `probability` (double), `file_type`, `role`, timestamps |

### DTOs
| DTO | Uso |
|-----|-----|
| `RegisterRequest` | `Username`, `Email_user`, `Password_user` (validado com regex) |
| `LoginsRequest` | `Username`, `Password_user` |
| `TextRequest` | `Text` (campo para análise) |
| `AnalysisResult` | `Probability`, `Classification`, `File_Type`, `Created_at`, `Warning` |
| `ApiResponse<T>` | Envelope padronizado `{ sucess: bool, data: T }` |

### Tratamento de Erros
`GlobalExceptionHandler` captura:
- `MethodArgumentNotValidException` → 400 Bad Request (erros de validação de campos)
- `ResourceAccessException` → 503 Service Unavailable (motor Python inacessível)
- `BadCredentialsException` → 401 Unauthorized
- `AccessDeniedException` → 403 Forbidden
- `Exception` genérico → 500 Internal Server Error

---

## Motor Python (FastAPI)

### Estrutura
```
python-engine/
├── main.py                    # App FastAPI, CORS, roteamento
├── requirements.txt           # Dependências pinadas
├── Dockerfile                 # Python 3.11-slim, porta 8001
├── routers/
│   └── text_analyzer.py       # Router POST /analyze/text, validação Pydantic
└── services/
    └── text_service.py        # TextAnalyzerService — lógica de análise
```

### TextAnalyzerService — Dois Modos

**Modo Transformer (primário)**
```
Modelo: openai-community/roberta-base-openai-detector
Pipeline: text-classification, truncation=True, max_length=512
Label "Fake" → IA gerado; Label "Real" → humano
probability = score se "Fake", senão 1.0 - score
```

**Modo Heurístico (fallback)**

Pesos e features:

```python
weights = {
    "low_burstiness":        0.30,  # variância < 8.0 no tamanho das frases
    "many_transitions":      0.25,  # conectivos formais / total palavras
    "high_ttr":              0.20,  # type-token ratio > 0.65
    "long_sentences":        0.15,  # média > 18 palavras/frase
    "no_personal_pronouns":  0.10,  # ausência de eu/nós/my/our etc.
}
probability = Σ (feature_value × weight)
```

### Singleton Pattern
`_service = TextAnalyzerService()` — modelo carregado uma única vez na inicialização do processo. Requisições subsequentes reutilizam o pipeline já em memória.

### CORS
Configurado para aceitar apenas `http://localhost:8080` (backend Java).

---

## Dependências Python

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
transformers==4.46.3
torch==2.6.0
pydantic==2.9.0
httpx==0.27.2
```

---

## Infraestrutura

### Portas
| Serviço | Porta |
|---------|-------|
| Spring Boot | 8080 |
| FastAPI | 8001 |
| PostgreSQL | 5432 (padrão) |
| Redis | 6379 (padrão) |

### Docker (motor Python)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Cache HuggingFace
Modelo baixado automaticamente na primeira execução. Cache em `~/.cache/huggingface` (~500MB). Execuções subsequentes usam cache local.
