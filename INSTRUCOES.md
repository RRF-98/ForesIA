# ForensIA — Instruções de Integração

## O que foi feito

### Comunicação Java ↔ Python
Java (Spring Boot :8080) chama Python (FastAPI :8001) via HTTP POST.
Fluxo: `AnalysisController → AnalysisService → RestTemplate → /analyze/text → TextAnalyzerService`

---

## Estrutura dos arquivos

```
Claude_Forencia/
├── java-fixes/          ← SUBSTITUIR arquivos existentes no projeto
│   ├── config/
│   │   ├── SecurityConfig.java      (fix: /autho/** → /auth/**)
│   │   └── RestTemplateConfig.java  (NOVO — deletar RestTemplate.java original)
│   ├── model/
│   │   ├── Analysis.java            (fix: unique removido, @Enumerated removido)
│   │   └── User.java                (fix: import javax.swing removido, @Enumerated removido)
│   ├── dto/request/
│   │   ├── RegisterRequest.java     (fix: regex de senha corrigida)
│   │   └── LoginsRequest.java       (fix: regex de senha corrigida)
│   ├── security/
│   │   └── JwtFilter.java           (fix: logica null check invertida na linha 49)
│   └── repository/
│       └── UserRepository.java      (fix: existBy → existsBy)
│
├── java-src/            ← COPIAR para o projeto nos pacotes corretos
│   ├── service/
│   │   ├── UserDetailsServiceImpl.java  → src/.../service/
│   │   ├── AuthService.java             → src/.../service/
│   │   └── AnalysisService.java         → src/.../service/
│   ├── controller/
│   │   ├── AuthController.java          → src/.../controller/
│   │   └── AnalysisController.java      → src/.../controller/
│   └── exception/
│       └── GlobalExceptionHandler.java  → src/.../exception/
│
└── python-engine/       ← PASTA SEPARADA — criar fora do projeto Java
    ├── main.py
    ├── requirements.txt
    ├── Dockerfile
    ├── routers/text_analyzer.py
    └── services/text_service.py
```

---

## Passo a passo

### 1. Aplicar fixes no projeto Java

```
forensia/src/main/java/com/forensia/
├── config/
│   ├── DELETAR: RestTemplate.java
│   ├── SUBSTITUIR: SecurityConfig.java      ← java-fixes/config/SecurityConfig.java
│   └── COPIAR:    RestTemplateConfig.java   ← java-fixes/config/RestTemplateConfig.java
├── model/
│   ├── SUBSTITUIR: Analysis.java            ← java-fixes/model/Analysis.java
│   └── SUBSTITUIR: User.java               ← java-fixes/model/User.java
├── dto/request/
│   ├── SUBSTITUIR: RegisterRequest.java     ← java-fixes/dto/request/RegisterRequest.java
│   └── SUBSTITUIR: LoginsRequest.java       ← java-fixes/dto/request/LoginsRequest.java
├── security/
│   └── SUBSTITUIR: JwtFilter.java          ← java-fixes/security/JwtFilter.java
└── repository/
    └── SUBSTITUIR: UserRepository.java     ← java-fixes/repository/UserRepository.java
```

### 2. Adicionar arquivos novos ao projeto Java

```
forensia/src/main/java/com/forensia/
├── service/
│   ├── CRIAR: UserDetailsServiceImpl.java  ← java-src/service/UserDetailsServiceImpl.java
│   ├── CRIAR: AuthService.java             ← java-src/service/AuthService.java
│   └── CRIAR: AnalysisService.java         ← java-src/service/AnalysisService.java
├── controller/
│   ├── CRIAR: AuthController.java          ← java-src/controller/AuthController.java
│   └── CRIAR: AnalysisController.java      ← java-src/controller/AnalysisController.java
└── exception/
    └── CRIAR: GlobalExceptionHandler.java  ← java-src/exception/GlobalExceptionHandler.java
```

### 3. Iniciar motor Python

```bash
cd python-engine

# Instalar dependencias (primeira vez — baixa modelo ~500MB)
pip install -r requirements.txt

# Iniciar servidor (porta 8001)
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Ou via Docker:
```bash
docker build -t forensia-engine .
docker run -p 8001:8001 forensia-engine
```

### 4. Iniciar Java

```bash
cd forensia
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

PostgreSQL e Redis devem estar rodando (ver application-dev.yml).

---

## Como testar a comunicação Java ↔ Python

### 1. Registrar usuario
```http
POST http://localhost:8080/auth/register
Content-Type: application/json

{
  "Username": "usuario01",
  "Email_user": "usuario@email.com",
  "Password_user": "Senha123"
}
```

### 2. Login (obtém JWT)
```http
POST http://localhost:8080/auth/login
Content-Type: application/json

{
  "Username": "usuario01",
  "Password_user": "Senha123"
}
```
Resposta: `{ "token": "eyJ...", "type": "Bearer" }`

### 3. Analisar texto (requer JWT)
```http
POST http://localhost:8080/api/v1/analysis/text
Authorization: Bearer eyJ...
Content-Type: application/json

{
  "Text": "Furthermore, it is worth noting that the implementation of such systems..."
}
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
    "created_at": "2026-05-29T..."
  }
}
```

### Testar Python diretamente (sem JWT)
```http
POST http://localhost:8001/analyze/text
Content-Type: application/json

{ "text": "texto para analisar aqui" }
```

Swagger do Python: http://localhost:8001/docs

---

## Bugs corrigidos

| Arquivo | Bug | Fix |
|---------|-----|-----|
| `SecurityConfig.java` | `/autho/**` (typo) | `/auth/**` |
| `JwtFilter.java` | `username == null` (logica invertida) | `username != null` |
| `RegisterRequest.java` | regex `[?=.*\\d]` (classe de char incorreta) | `(?=.*\\d)` (lookahead) |
| `LoginsRequest.java` | mesmo regex errado | idem |
| `Analysis.java` | `unique=true` no username | removido |
| `Analysis.java` + `User.java` | `@Enumerated` em campo String | removido |
| `User.java` | `import javax.swing.*` (import errado) | removido |
| `UserRepository.java` | `existByUsername` (sem 's') | `existsByUsername` |
| `RestTemplate.java` | classe vazia conflitando com Spring | substituido por RestTemplateConfig |

---

## Motor Python — como funciona

`TextAnalyzerService` tenta carregar `openai-community/roberta-base-openai-detector` (HuggingFace).
- Se modelo disponivel: usa transformer para classificar (mais preciso)
- Se modelo indisponivel: usa heuristicas estatisticas (burstiness, TTR, transicoes, pronomes)

O modelo faz download automatico na primeira execucao (~500MB, armazenado em ~/.cache/huggingface).
