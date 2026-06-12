# ForensIA

Sistema forense para detecção de conteúdo gerado por Inteligência Artificial em textos.

Arquitetura de dois serviços: backend Java (Spring Boot) + motor de análise Python (FastAPI) comunicando via HTTP.

---

## Visão Geral

```
Cliente → POST /api/v1/analysis/text (JWT)
              ↓
         Spring Boot :8080
         AnalysisController
              ↓
         AnalysisService
              ↓  HTTP POST
         FastAPI :8001
         /analyze/text
              ↓
         TextAnalyzerService
         (RoBERTa ou heurísticas)
              ↓
         { probability: 0.87, classification: "IA_GERADO" }
```

---

## Estrutura do Repositório

```
Claude_Forencia/
├── java-fixes/          ← Correções para arquivos existentes no projeto Java
│   ├── config/
│   │   ├── SecurityConfig.java       (fix: typo /autho/** → /auth/**)
│   │   └── RestTemplateConfig.java   (substitui RestTemplate.java vazio)
│   ├── model/
│   │   ├── Analysis.java             (fix: unique + @Enumerated removidos)
│   │   └── User.java                 (fix: import javax.swing + @Enumerated removidos)
│   ├── dto/request/
│   │   ├── RegisterRequest.java      (fix: regex de senha corrigida)
│   │   └── LoginsRequest.java        (fix: regex de senha corrigida)
│   ├── security/
│   │   └── JwtFilter.java            (fix: lógica null check invertida)
│   └── repository/
│       └── UserRepository.java       (fix: existBy → existsBy)
│
├── java-src/            ← Novos arquivos a criar no projeto Java
│   ├── service/
│   │   ├── UserDetailsServiceImpl.java
│   │   ├── AuthService.java
│   │   └── AnalysisService.java
│   ├── controller/
│   │   ├── AuthController.java
│   │   └── AnalysisController.java
│   └── exception/
│       └── GlobalExceptionHandler.java
│
├── python-engine/       ← Microserviço Python separado
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── routers/
│   │   └── text_analyzer.py
│   └── services/
│       └── text_service.py
│
├── docs/                ← Documentação e especificação do projeto
│   └── f3f06d27-62a2-4862-9d32-ce95539bb8fd/
│       ├── FORENSIA_PROJETO.xlsx
│       ├── FORENSIA_PROJETO_v2.pdf
│       ├── ARQUITETURA.md
│       ├── API_REFERENCE.md
│       └── GUIA_INTEGRACAO.md
│
├── INSTRUCOES.md        ← Guia de integração passo a passo
└── body.json            ← Payload de exemplo para testes
```

---

## Stack Tecnológica

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Backend API | Spring Boot | 3.x |
| Segurança | Spring Security + JWT | — |
| Banco de dados | PostgreSQL | — |
| Cache | Redis | — |
| Motor de IA | FastAPI | — |
| Modelo ML | roberta-base-openai-detector | HuggingFace |
| Framework ML | PyTorch + Transformers | 2.6 / 4.46 |

---

## Pré-requisitos

- Java 17+
- Maven (ou wrapper `./mvnw`)
- Python 3.11+
- PostgreSQL rodando
- Redis rodando
- ~500MB de espaço livre (download do modelo HuggingFace na primeira execução)

---

## Setup

### 1. Aplicar correções no projeto Java

```
forensia/src/main/java/com/forensia/
├── config/     DELETAR RestTemplate.java
│               SUBSTITUIR SecurityConfig.java     ← java-fixes/config/
│               COPIAR    RestTemplateConfig.java  ← java-fixes/config/
├── model/      SUBSTITUIR Analysis.java           ← java-fixes/model/
│               SUBSTITUIR User.java               ← java-fixes/model/
├── dto/request/ SUBSTITUIR RegisterRequest.java   ← java-fixes/dto/request/
│               SUBSTITUIR LoginsRequest.java      ← java-fixes/dto/request/
├── security/   SUBSTITUIR JwtFilter.java          ← java-fixes/security/
└── repository/ SUBSTITUIR UserRepository.java     ← java-fixes/repository/
```

### 2. Adicionar novos arquivos ao projeto Java

```
forensia/src/main/java/com/forensia/
├── service/    CRIAR UserDetailsServiceImpl.java  ← java-src/service/
│               CRIAR AuthService.java             ← java-src/service/
│               CRIAR AnalysisService.java         ← java-src/service/
├── controller/ CRIAR AuthController.java          ← java-src/controller/
│               CRIAR AnalysisController.java      ← java-src/controller/
└── exception/  CRIAR GlobalExceptionHandler.java  ← java-src/exception/
```

### 3. Iniciar motor Python

```bash
cd python-engine
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Via Docker:
```bash
docker build -t forensia-engine .
docker run -p 8001:8001 forensia-engine
```

### 4. Iniciar backend Java

```bash
cd forensia
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

PostgreSQL e Redis devem estar rodando conforme configurado em `application-dev.yml`.

---

## Endpoints da API

### Autenticação

#### `POST /auth/register`
Registra novo usuário.

```json
{
  "Username": "usuario01",
  "Email_user": "usuario@email.com",
  "Password_user": "Senha123"
}
```

#### `POST /auth/login`
Autentica e retorna JWT.

```json
{
  "Username": "usuario01",
  "Password_user": "Senha123"
}
```

Resposta:
```json
{
  "token": "eyJ...",
  "type": "Bearer",
  "username": "usuario01"
}
```

### Análise

#### `POST /api/v1/analysis/text`
Analisa texto quanto à probabilidade de ser gerado por IA.

**Header:** `Authorization: Bearer <token>`

```json
{ "Text": "conteúdo a analisar" }
```

Resposta:
```json
{
  "sucess": true,
  "data": {
    "probability": 0.87,
    "classification": "IA_GERADO",
    "file_Type": "TEXT",
    "warning": "Alta probabilidade de conteudo gerado por IA",
    "created_at": "2026-05-29T10:00:00"
  }
}
```

**Classificações:**
| Faixa | Classificação |
|-------|--------------|
| < 0.30 | `HUMANO` |
| 0.30 – 0.69 | `HIBRIDO` |
| ≥ 0.70 | `IA_GERADO` |

### Motor Python (direto, sem JWT)

#### `POST http://localhost:8001/analyze/text`
```json
{ "text": "texto para analisar" }
```

#### `GET http://localhost:8001/health`
```json
{ "status": "ok", "service": "ForensIA Engine" }
```

Swagger: `http://localhost:8001/docs`

---

## Motor de Análise

`TextAnalyzerService` opera em dois modos:

**Modo primário — Transformer:**
Usa `openai-community/roberta-base-openai-detector` (HuggingFace).
Download automático na primeira execução (~500MB, cache em `~/.cache/huggingface`).
Retorna: `{ probability, model_used, method: "transformer", label, confidence }`

**Modo fallback — Heurísticas estatísticas:**
Ativado quando o modelo transformer não está disponível.

| Feature | Peso | Indicador IA |
|---------|------|-------------|
| `low_burstiness` | 30% | Variância baixa no tamanho das frases |
| `many_transitions` | 25% | Conectivos formais (furthermore, portanto…) |
| `high_ttr` | 20% | Type-Token Ratio alto (vocabulário diverso) |
| `long_sentences` | 15% | Média > 18 palavras por frase |
| `no_personal_pronouns` | 10% | Ausência de pronomes pessoais |

Retorna: `{ probability, model_used: "statistical-heuristics", method: "statistical", features }`

---

## Bugs Corrigidos

| Arquivo | Problema | Correção |
|---------|----------|---------|
| `SecurityConfig.java` | Path `/autho/**` (typo) | `/auth/**` |
| `JwtFilter.java` | `username == null` (lógica invertida) | `username != null` |
| `RegisterRequest.java` | Regex `[?=.*\\d]` (classe de char incorreta) | `(?=.*\\d)` (lookahead) |
| `LoginsRequest.java` | Mesmo regex inválido | Idem |
| `Analysis.java` | `unique=true` em campo username | Removido |
| `Analysis.java` + `User.java` | `@Enumerated` em campo String | Removido |
| `User.java` | `import javax.swing.*` (import errado) | Removido |
| `UserRepository.java` | `existByUsername` (sem 's') | `existsByUsername` |
| `RestTemplate.java` | Classe vazia conflitando com bean Spring | Substituída por `RestTemplateConfig` |

---

## Novos Componentes Implementados

| Arquivo | Responsabilidade |
|---------|-----------------|
| `UserDetailsServiceImpl.java` | Integração Spring Security — carrega usuário do banco |
| `AuthService.java` | Registro (BCrypt) e login (JWT) com verificação de duplicatas |
| `AnalysisService.java` | Orquestra chamada ao motor Python e persiste resultado |
| `AuthController.java` | Endpoints `POST /auth/register` e `POST /auth/login` |
| `AnalysisController.java` | Endpoint `POST /api/v1/analysis/text` (requer JWT) |
| `GlobalExceptionHandler.java` | Tratamento centralizado de exceções com respostas padronizadas |

---

## Exemplos de Teste

```bash
# 1. Registrar
curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"Username":"usuario01","Email_user":"user@email.com","Password_user":"Senha123"}'

# 2. Login
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"Username":"usuario01","Password_user":"Senha123"}'

# 3. Analisar texto (substituir TOKEN pelo JWT retornado no login)
curl -X POST http://localhost:8080/api/v1/analysis/text \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"Text":"Furthermore, it is worth noting that the implementation of such systems requires careful consideration."}'

# 4. Testar motor Python diretamente
curl -X POST http://localhost:8001/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text":"Furthermore, it is worth noting that the implementation requires careful consideration."}'
```
