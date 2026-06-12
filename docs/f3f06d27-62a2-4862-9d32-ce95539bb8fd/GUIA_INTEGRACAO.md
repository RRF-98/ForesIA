# ForensIA — Guia de Integração

Passo a passo completo para aplicar as implementações ao projeto Java existente e subir o motor Python.

---

## O que foi entregue

### Correções (java-fixes/) — aplicar ao projeto Java existente
8 arquivos com bugs corrigidos para substituir nos locais correspondentes.

### Novos arquivos (java-src/) — adicionar ao projeto Java
6 arquivos novos de serviços, controllers e tratamento de exceções.

### Motor Python (python-engine/) — serviço separado
Microserviço FastAPI independente para análise de texto com IA.

---

## Passo 1 — Aplicar correções no projeto Java

Localizar o diretório base: `forensia/src/main/java/com/forensia/`

### config/
```
DELETAR:     RestTemplate.java
SUBSTITUIR:  SecurityConfig.java      ← java-fixes/config/SecurityConfig.java
COPIAR:      RestTemplateConfig.java  ← java-fixes/config/RestTemplateConfig.java
```

### model/
```
SUBSTITUIR:  Analysis.java  ← java-fixes/model/Analysis.java
SUBSTITUIR:  User.java      ← java-fixes/model/User.java
```

### dto/request/
```
SUBSTITUIR:  RegisterRequest.java  ← java-fixes/dto/request/RegisterRequest.java
SUBSTITUIR:  LoginsRequest.java    ← java-fixes/dto/request/LoginsRequest.java
```

### security/
```
SUBSTITUIR:  JwtFilter.java  ← java-fixes/security/JwtFilter.java
```

### repository/
```
SUBSTITUIR:  UserRepository.java  ← java-fixes/repository/UserRepository.java
```

---

## Passo 2 — Adicionar novos arquivos ao projeto Java

Localizar o diretório base: `forensia/src/main/java/com/forensia/`

### service/ (criar diretório se não existir)
```
CRIAR:  UserDetailsServiceImpl.java  ← java-src/service/UserDetailsServiceImpl.java
CRIAR:  AuthService.java             ← java-src/service/AuthService.java
CRIAR:  AnalysisService.java         ← java-src/service/AnalysisService.java
```

### controller/ (criar diretório se não existir)
```
CRIAR:  AuthController.java      ← java-src/controller/AuthController.java
CRIAR:  AnalysisController.java  ← java-src/controller/AnalysisController.java
```

### exception/ (criar diretório se não existir)
```
CRIAR:  GlobalExceptionHandler.java  ← java-src/exception/GlobalExceptionHandler.java
```

---

## Passo 3 — Iniciar motor Python

```bash
cd python-engine

# Instalar dependências (primeira execução — baixa modelo ~500MB)
pip install -r requirements.txt

# Iniciar servidor na porta 8001
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Via Docker:**
```bash
docker build -t forensia-engine .
docker run -p 8001:8001 forensia-engine
```

**Verificar:**
```
GET http://localhost:8001/health
→ {"status": "ok", "service": "ForensIA Engine"}
```

---

## Passo 4 — Iniciar backend Java

PostgreSQL e Redis devem estar rodando antes.

```bash
cd forensia
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

---

## Passo 5 — Validar integração

### 5.1 Registrar usuário
```http
POST http://localhost:8080/auth/register
Content-Type: application/json

{
  "Username": "usuario01",
  "Email_user": "usuario@email.com",
  "Password_user": "Senha123"
}
```

Esperado: `{ "sucess": true, "data": { "message": "Usuario registrado com sucesso" } }`

### 5.2 Fazer login
```http
POST http://localhost:8080/auth/login
Content-Type: application/json

{
  "Username": "usuario01",
  "Password_user": "Senha123"
}
```

Esperado: `{ "sucess": true, "data": { "token": "eyJ...", "type": "Bearer", "username": "usuario01" } }`

Copiar o valor de `token`.

### 5.3 Analisar texto
```http
POST http://localhost:8080/api/v1/analysis/text
Authorization: Bearer eyJ...
Content-Type: application/json

{
  "Text": "Furthermore it is worth noting that the implementation of such systems requires careful consideration."
}
```

Esperado:
```json
{
  "sucess": true,
  "data": {
    "probability": 0.87,
    "classification": "IA_GERADO",
    "file_Type": "TEXT",
    "warning": "Alta probabilidade de conteudo gerado por IA",
    "created_at": "..."
  }
}
```

---

## Diagnóstico de Problemas

### Motor Python não inicia
```
ModuleNotFoundError: No module named 'fastapi'
```
→ Rodar `pip install -r requirements.txt` dentro de `python-engine/`

### Java não conecta ao motor Python
```
503 Service Unavailable: Motor de IA indisponivel
```
→ Verificar se `uvicorn` está rodando em `:8001`
→ Verificar CORS em `main.py`: `allow_origins=["http://localhost:8080"]`

### Erro de compilação Java: `RestTemplate` bean duplicado
→ Confirmar que `RestTemplate.java` foi **deletado** e `RestTemplateConfig.java` foi copiado

### JWT inválido / 401 em análise
→ Confirmar header: `Authorization: Bearer <token>` (sem aspas, com espaço após Bearer)
→ Token expira — fazer login novamente

### Modelo HuggingFace não baixa
→ Verificar conexão com internet na primeira execução
→ O serviço funciona em modo heurístico mesmo sem o modelo — `method: "statistical"` na resposta confirma fallback

---

## Arquivos de Referência

| Arquivo | Descrição |
|---------|-----------|
| `INSTRUCOES.md` | Guia rápido de integração (raiz do projeto) |
| `ARQUITETURA.md` | Diagrama completo e detalhes técnicos |
| `API_REFERENCE.md` | Endpoints, payloads e respostas documentados |
| `body.json` | Payload de exemplo para teste do motor Python |
| `FORENSIA_PROJETO_v2.pdf` | Especificação completa do projeto |
| `FORENSIA_PROJETO.xlsx` | Planilha de acompanhamento do projeto |
