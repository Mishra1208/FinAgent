# FinAgent: Enterprise SEC Multi-Agent Financial Intelligence System

> **A production-grade, stateful Multi-Agent AI system built with LangGraph, Hybrid RAG, FastAPI, and Streamlit (Light Mode) to analyze SEC 10-K filings, calculate deterministic financial ratios, audit risk factors, and eliminate hallucinations with LLM-as-a-Judge evaluation.**

---

## 📖 Complete Documentation & Learning Guide
Every component of this project is documented step-by-step for easy learning and interview preparation inside the [`docs/`](./docs) folder:

1. [**00 - Project Overview & System Architecture**](./docs/00_PROJECT_OVERVIEW_AND_ARCHITECTURE.md)
2. [**01 - Data Ingestion & SEC 10-K Chunk Strategy**](./docs/01_DATA_INGESTION_AND_CHUNK_STRATEGY.md)
3. [**02 - Hybrid RAG & Vector Store (ChromaDB + BM25 + RRF)**](./docs/02_HYBRID_RAG_AND_VECTOR_STORE.md)
4. [**03 - Deterministic Financial Math Tools**](./docs/03_DETERMINISTIC_FINANCIAL_MATH_TOOLS.md)
5. [**04 - LangGraph Multi-Agent Stateful Orchestration**](./docs/04_LANGGRAPH_MULTI_AGENT_WORKFLOW.md)
6. [**05 - Guardrails & Pydantic Structured Outputs**](./docs/05_GUARDRAILS_AND_STRUCTURED_OUTPUTS.md)
7. [**06 - Automated Evaluation & LLM-as-a-Judge Benchmark**](./docs/06_EVALUATION_AND_LLM_AS_A_JUDGE.md)
8. [**07 - Full-Stack Deployment & Morgan Stanley Interview Master Guide**](./docs/07_FULLSTACK_DEPLOYMENT_AND_INTERVIEW_GUIDE.md)

---

## 🚀 Quickstart & Verification

### 1. Run Complete Test Suite
```bash
python tests/test_ingestion.py              # Step 1: Ingestion & Chunker
python tests/test_hybrid_rag.py             # Step 2: Hybrid RAG Engine
python tests/test_tools.py                  # Step 3: Financial Math Tools
python tests/test_multi_agent.py            # Step 4: LangGraph Multi-Agent
python tests/test_guardrails.py             # Step 5: Enterprise Guardrails
python tests/test_evaluation_benchmark.py   # Step 6: Ragas LLM-as-a-Judge Benchmark
```

### 2. Launch Interactive Light-Mode Dashboard
```bash
streamlit run src/ui/app.py
```
Open your browser at: `http://localhost:8501`

### 3. Launch FastAPI REST Server
```bash
uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```
Open Swagger Docs at: `http://127.0.0.1:8000/docs`

---

## 🏛️ System Architecture

```
                       [ USER QUERY ]
                             │
                             ▼
                 ┌───────────────────────┐
                 │ 1. INPUT GUARDRAILS   │
                 │   - Prompt Injection  │
                 │   - Scope Filter      │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ 2. SUPERVISOR AGENT   │
                 │   - Hybrid RAG Search │
                 │   - BM25 + ChromaDB   │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ 3. QUANT ANALYST      │
                 │   - Deterministic Math│
                 │   - Margins, YoY, P/E │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ 4. RISK & COMPLIANCE  │
                 │   - Item 1A Risk Audit│
                 │   - Severity Scoring  │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ 5. FACTUAL VERIFIER   │
                 │   - Zero Hallucination│
                 │   - Grounded Citation │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ 6. OUTPUT GUARDRAIL   │
                 │   - PII Redaction     │
                 │   - Pydantic Schema   │
                 └───────────┬───────────┘
                             │
                             ▼
                 [ INSTITUTIONAL DOSSIER ]
```
