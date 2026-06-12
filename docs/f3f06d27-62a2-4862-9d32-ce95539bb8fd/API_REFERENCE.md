# ForensIA — Referência de API

Base URL Java: `http://localhost:8080`
Base URL Python: `http://localhost:8001`

---

## Autenticação

### POST /auth/register

Registra novo usuário no sistema.

**Não requer autenticação.**

**Request Body:**
```json
{
  "Username": "string",
  "Email_user": "string",
  "Password_user": "string"
}
```

**Validações:**
- `Password_user`: deve conter letras maiúsculas, minúsculas e dígitos (regex: `(?=.*\d)(?=.*[a-z])(?=.*[A-Z])`)
- `Username`: deve ser único no banco
- `Email_user`: deve ser único no banco

**Resposta 200 — Sucesso:**
```json
{
  "sucess": true,
  "data": {
    "message": "Usuario registrado com sucesso"
  }
}
```

**Resposta 200 — Erro de negócio:**
```json
{
  "sucess": false,
  "data": "Nome de usuario ja esta em uso"
}
```

**Resposta 400 — Validação:**
```json
{
  "sucess": false,
  "data": "Password_user: deve conter maiuscula, minuscula e digito"
}
```

---

### POST /auth/login

Autentica usuário e retorna token JWT.

**Não requer autenticação.**

**Request Body:**
```json
{
  "Username": "string",
  "Password_user": "string"
}
```

**Resposta 200 — Sucesso:**
```json
{
  "sucess": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiJ9...",
    "type": "Bearer",
    "username": "usuario01"
  }
}
```

**Resposta 200 — Credenciais inválidas:**
```json
{
  "sucess": false,
  "data": "Credenciais invalidas"
}
```

---

## Análise

### POST /api/v1/analysis/text

Analisa texto e retorna probabilidade de ser gerado por IA.

**Requer autenticação JWT.**

**Header:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "Text": "string (texto a ser analisado)"
}
```

**Resposta 200 — Sucesso:**
```json
{
  "sucess": true,
  "data": {
    "probability": 0.87,
    "classification": "IA_GERADO",
    "file_Type": "TEXT",
    "warning": "Alta probabilidade de conteudo gerado por IA",
    "created_at": "2026-05-29T10:30:00"
  }
}
```

**Campo `classification`:**
| Valor | Condição |
|-------|----------|
| `HUMANO` | probability < 0.30 |
| `HIBRIDO` | 0.30 ≤ probability < 0.70 |
| `IA_GERADO` | probability ≥ 0.70 |

**Campo `warning`:** presente apenas quando `probability ≥ 0.70`.

**Resposta 503 — Motor Python indisponível:**
```json
{
  "sucess": false,
  "data": "Motor de IA indisponivel: ..."
}
```

**Resposta 401 — Token inválido/ausente:**
```json
{
  "sucess": false,
  "data": "Credenciais invalidas"
}
```

---

## Motor Python (direto)

### POST /analyze/text

Analisa texto sem passar pelo backend Java. Útil para testes diretos.

**Não requer autenticação.**

**Request Body:**
```json
{
  "text": "string (mínimo 5 caracteres)"
}
```

**Resposta 200 — Modo Transformer:**
```json
{
  "probability": 0.87,
  "model_used": "openai-community/roberta-base-openai-detector",
  "method": "transformer",
  "label": "Fake",
  "confidence": 0.87
}
```

**Resposta 200 — Modo Heurístico (fallback):**
```json
{
  "probability": 0.75,
  "model_used": "statistical-heuristics",
  "method": "statistical",
  "features": {
    "low_burstiness": 1.0,
    "high_ttr": 1.0,
    "long_sentences": 0.0,
    "many_transitions": 0.6666,
    "no_personal_pronouns": 1.0
  }
}
```

**Resposta 422 — Validação:**
```json
{
  "detail": [
    {
      "msg": "Texto deve ter no minimo 5 caracteres"
    }
  ]
}
```

**Resposta 500 — Erro interno:**
```json
{
  "detail": "Erro na analise: ..."
}
```

---

### GET /health

Health check do motor Python.

**Resposta 200:**
```json
{
  "status": "ok",
  "service": "ForensIA Engine"
}
```

---

## Swagger / OpenAPI

Documentação interativa disponível em: `http://localhost:8001/docs`

---

## Exemplos cURL

```bash
# Registro
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"Username":"usuario01","Email_user":"user@email.com","Password_user":"Senha123"}'

# Login
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"Username":"usuario01","Password_user":"Senha123"}'

# Análise (substituir TOKEN)
curl -X POST http://localhost:8080/api/v1/analysis/text \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Text":"Furthermore, it is worth noting that the implementation of such systems requires careful consideration of multiple factors."}'

# Motor Python direto
curl -X POST http://localhost:8001/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text":"Furthermore, it is worth noting that the implementation requires careful consideration."}'

# Health check
curl http://localhost:8001/health
```
