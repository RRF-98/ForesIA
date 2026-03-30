# ForensIA

> **Detecção Multimodal de Conteúdo Gerado por Inteligência Artificial**  
> TCC — Detecção de conteúdo sintético baseada em Transformers e arquitetura de microserviços

![Java](https://img.shields.io/badge/Java-21-007396?style=flat-square&logo=openjdk)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.3.5-6DB33F?style=flat-square&logo=springboot)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Stack Tecnológica](#stack-tecnológica)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Endpoints da API](#endpoints-da-api)
- [Regras de Negócio](#regras-de-negócio)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Conformidade Legal](#conformidade-legal)
- [Equipe](#equipe)

---

## Visão Geral

O **ForensIA** é um sistema de detecção de conteúdo gerado por Inteligência Artificial. Analisa **texto, áudio, imagem e vídeo**, retornando:

- **Probabilidade** (0–100%) de o conteúdo ter sido gerado por IA
- **Classificação**: `Humano` · `Híbrido` · `IA`

O sistema expõe uma API RESTful autenticada via JWT e processa as mídias por meio de um microserviço Python dedicado, baseado em modelos HuggingFace e PyTorch.

---

## Funcionalidades

| Funcionalidade | Status |
|---|---|
| Análise de texto (PT/EN) | ✅ |
| Análise de áudio (MP3, WAV, AAC) | ✅ |
| Análise de imagem (PNG, JPG, WEBP) | ✅ |
| Análise de vídeo (MP4, AVI, MOV) | ✅ |
| Autenticação JWT | ✅ |
| Histórico de análises por usuário | ✅ |
| Cache Redis (evita rechamadas ao motor de IA) | ✅ |
| Documentação interativa Swagger | ✅ |
| Health check para Docker | ✅ |
| Exportação em PDF e CSV | 🔄 Planejado |
| Painel administrativo | 🔄 Planejado |

---

## Arquitetura

```
┌─────────────────────────────────────┐
│         CLIENTE (Frontend)          │
│      Web ou Desktop — a definir     │
└──────────────────┬──────────────────┘
                   │ HTTP (JSON + multipart)
                   │ Authorization: Bearer <token>
┌──────────────────▼──────────────────┐
│    API REST — Java (Spring Boot)    │  :8080
│  • Autenticação JWT                 │
│  • AnalysisController               │
│  • HistoryService                   │
│  • Cache Redis                      │
└────────┬─────────────────┬──────────┘
         │ JDBC            │ HTTP interno
┌────────▼──────┐  ┌───────▼──────────────────┐
│  PostgreSQL   │  │  Motor IA — Python/FastAPI │  :8001
│   :5432       │  │  /analyze/text  → HuggingFace │
│  users        │  │  /analyze/audio → librosa  │
│  analyses     │  │  /analyze/image → torchvision │
└───────────────┘  │  /analyze/video → OpenCV   │
┌───────────────┐  └──────────────────────────┘
│  Redis :6379  │
│  cache análises│
└───────────────┘
```

### Fluxo de uma análise

```
1. POST /auth/login          → recebe token JWT
2. POST /api/v1/analysis/text com Bearer token
3. JwtFilter valida o token
4. AnalysisService verifica Redis:
     → HIT:  retorna resultado sem chamar Python
     → MISS: POST http://ai-engine:8001/analyze/text
5. Python processa com HuggingFace → { probability, classification }
6. Java salva no PostgreSQL
7. Java armazena no Redis (TTL: 1h)
8. Resultado retornado em JSON padronizado
```

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| **API Backend** | Java 21 + Spring Boot 3.3.5 + Maven |
| **Motor de IA** | Python 3.11 + FastAPI + HuggingFace Transformers + PyTorch |
| **Banco de Dados** | PostgreSQL 15 (JPA/Hibernate) |
| **Cache** | Redis 7 |
| **Autenticação** | JWT (JJWT 0.12.6) + BCrypt |
| **Documentação API** | SpringDoc OpenAPI 2.5.0 (Swagger UI) |
| **Containerização** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- Git

> **Para desenvolvimento local (sem Docker):**
> - Java 21 (Eclipse Temurin)
> - Maven 3.9+
> - Python 3.11+
> - PostgreSQL 15
> - Redis 7

---

## Instalação e Execução

### Via Docker Compose (recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/forensia.git
cd forensia

# 2. Suba todos os serviços (primeira execução — faz o build)
docker-compose up --build

# Aguarde a mensagem: Started ForensiaApplication in X seconds

# 3. Acesse
# Swagger UI → http://localhost:8080/swagger-ui.html
# Health      → http://localhost:8080/actuator/health
# Motor IA    → http://localhost:8001/health
```

```bash
# Parar os serviços
docker-compose down

# Parar e apagar o banco de dados
docker-compose down -v

# Rebuild de um serviço após mudança no código
docker-compose up -d --build api
```

### Desenvolvimento local (IntelliJ)

```bash
# Configure a variável de ambiente antes de rodar:
SPRING_PROFILES_ACTIVE=dev

# Inicie o PostgreSQL e Redis localmente, depois rode:
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

---

## Endpoints da API

| Método | Endpoint | Auth | Descrição |
|---|---|---|---|
| `POST` | `/auth/register` | Pública | Cadastro de novo usuário |
| `POST` | `/auth/login` | Pública | Login — retorna token JWT |
| `POST` | `/api/v1/analysis/text` | JWT | Análise de texto |
| `POST` | `/api/v1/analysis/file?type={audio\|image\|video}` | JWT | Análise de arquivo |
| `GET` | `/api/v1/history` | JWT | Histórico de análises do usuário |
| `DELETE` | `/api/v1/history/{id}` | JWT | Remove análise do histórico |
| `GET` | `/actuator/health` | Pública | Health check para Docker |
| `GET` | `/swagger-ui.html` | Pública | Documentação interativa |

### Formato de resposta padrão

```json
{
  "success": true,
  "data": {
    "probability": 87.43,
    "classification": "IA",
    "mediaType": "TEXT",
    "warning": null,
    "analyzedAt": "2026-03-30T14:32:00"
  },
  "error": null,
  "timestamp": "2026-03-30T14:32:00"
}
```

### Exemplo de uso (cURL)

```bash
# Login
curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","password":"senha123"}'

# Análise de texto
curl -X POST http://localhost:8080/api/v1/analysis/text \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Texto a ser analisado..."}'

# Análise de imagem
curl -X POST "http://localhost:8080/api/v1/analysis/file?type=image" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@imagem.jpg"
```

---

## Regras de Negócio

### Classificação por probabilidade

| Faixa | Classificação |
|---|---|
| 0% – 30% | **Humano** |
| 31% – 69% | **Híbrido** |
| 70% – 100% | **IA** |

### Limites de arquivo por mídia

| Tipo | Formatos aceitos | Tamanho máximo | Duração máxima |
|---|---|---|---|
| Áudio | MP3, WAV, AAC | 50 MB | 10 minutos |
| Imagem | PNG, JPG, WEBP | 20 MB | — |
| Vídeo | MP4, AVI, MOV | 200 MB | 5 minutos |

### Avisos automáticos

- Textos com **menos de 50 palavras** geram alerta de acurácia reduzida
- Imagens abaixo de **256×256 px** geram alerta de possível redução de acurácia
- Áudios abaixo de **8 kHz** geram alerta informativo
- Detecções com **confiança < 70%** em vídeo geram alerta

---

## Estrutura do Projeto

```
forensia/                          ← raiz do workspace
├── docker-compose.yml             ← orquestra todos os serviços
├── forensia/                      ← módulo Java
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/main/java/com/forensia/
│       ├── config/                ← SecurityConfig, RestTemplate, OpenApi
│       ├── controller/            ← AuthController, AnalysisController, HistoryController
│       ├── service/               ← AuthService, AnalysisService, HistoryService
│       ├── repository/            ← UserRepository, AnalysisRepository
│       ├── model/                 ← User.java, Analysis.java
│       ├── dto/                   ← request/ e response/
│       ├── security/              ← JwtUtil.java, JwtFilter.java
│       └── exception/             ← GlobalExceptionHandler.java
└── forensia-ai-engine/            ← módulo Python
    ├── requirements.txt
    ├── Dockerfile
    └── app/
        ├── main.py
        ├── routers/               ← text.py, audio.py, image.py, video.py
        └── services/              ← text_service.py, audio_service.py, ...
```

---

## Testes

```bash
# Testes Java
cd forensia
mvn test -Dspring.profiles.active=dev

# Testes Python
cd forensia-ai-engine
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

### Métricas de qualidade do modelo

| Métrica | Meta |
|---|---|
| Acurácia global | ≥ 85% |
| Precisão (classe IA) | ≥ 80% |
| Recall (classe IA) | ≥ 80% |
| F1-Score | ≥ 0,82 |
| Falsos positivos | ≤ 10% |
| Latência da API (texto ≤ 5k palavras) | ≤ 2 segundos |

---

## Conformidade Legal

O ForensIA foi desenvolvido em conformidade com:

- **LGPD** — Lei nº 13.709/2018 (dados pessoais, consentimento, retenção mínima)
- **Marco Civil da Internet** — Lei nº 12.965/2014 (guarda de logs por no mínimo 6 meses)
- **GDPR** — Regulamento UE 2016/679 (caso haja processamento de dados de cidadãos europeus)
- **AI Act** — Regulamento UE 2024/1689 (transparência sobre uso de IA)

> Arquivos submetidos **não são armazenados** após o processamento, salvo mediante consentimento explícito do usuário. O histórico armazena apenas metadados e resultados, nunca o conteúdo original.

---

## Equipe

Desenvolvido como Trabalho de Conclusão de Curso (TCC) — 2026.

| Papel | Responsabilidades |
|---|---|
| **Líder / Backend** | API REST (Java/Spring Boot), banco de dados, infraestrutura Docker |
| **Motor de IA** | Microserviço Python (FastAPI), modelos HuggingFace/PyTorch |
| **Interface / Testes** | Interface do usuário, testes (JUnit 5, pytest), documentação |

---

> **Código do Projeto:** PP_2026_001_FORENSIA  
> **Período:** Fevereiro – Novembro 2026