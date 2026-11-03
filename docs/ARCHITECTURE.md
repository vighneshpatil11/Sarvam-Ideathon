# SAARTHI — System Architecture

## 1. High-Level Architecture Diagram

```
+-------------------------------------------------------+
|                   Citizen Client                      |
|       Next.js 14 / React / Tailwind / TypeScript       |
|    Routes: /, /services, /eligibility, /docs, /chat   |
+---------------------------+---------------------------+
                            | HTTP / JSON (API v1)
                            v
+-------------------------------------------------------+
|                     FastAPI Backend                   |
|  - API Router (/api/v1/*)                             |
|  - Security & Rate Limiting                           |
|  - Deterministic Eligibility Engine                   |
|  - Knowledge Retrieval & Citation Resolver            |
|  - Admin Auth & Audit Logging                         |
+-------------+-----------------------------+-----------+
              |                             |
              v                             v
+---------------------------+ +-------------------------+
|     PostgreSQL / SQLite   | |     Sarvam AI API       |
| - Departments & Services  | |  - Chat Completions     |
| - Rules & Documents       | |  - Model: sarvam-105b-  |
| - Sources & Citations     | |    conversations        |
| - Knowledge Chunks        | |  - Multilingual LLM     |
+---------------------------+ +-------------------------+
```

## 2. Component Design
- **Frontend**: Next.js App Router providing server-rendered shells and reactive client islands. Internationalization (English, Hindi, Marathi) implemented via declarative dictionary tokens with dynamic RTL/LTR support.
- **Backend**: FastAPI asynchronous application with Pydantic v2 schemas for bidirectional validation and strict OpenAPI compliance.
- **Database Layer**: SQLAlchemy 2.x ORM with declarative models and Alembic version-controlled migrations. Configured for PostgreSQL in production and SQLite for zero-setup local developer velocity.
- **Deterministic Eligibility Engine**: Rule-based evaluation engine executing AST-style boolean/comparison operations against citizen inputs without any LLM intervention in decision making.
- **AI/RAG Pipeline**: Strict retrieval-augmented assistant. Answers are constrained to retrieved government chunks and structured service models with verifiable citations.
- **Security Boundary**: Citizen interactions require zero authentication and zero personal data retention. Admin API routes require cryptographic JWT bearer authorization with audit logging.
