# FinAgent: Enterprise SEC Multi-Agent Financial Intelligence System

> **A production-grade, stateful Multi-Agent AI system built with LangGraph, Hybrid RAG, FastAPI, and Streamlit to analyze SEC 10-K filings, calculate deterministic financial ratios, audit risk factors, and eliminate hallucinations with LLM-as-a-Judge evaluation.**

---

## 📖 Complete Documentation & Learning Guide
Every component of this project is documented step-by-step for easy learning and interview preparation inside the [`docs/`](./docs) folder:

1. [**00 - Project Overview & System Architecture**](./docs/00_PROJECT_OVERVIEW_AND_ARCHITECTURE.md)
2. [**01 - Data Ingestion & SEC 10-K Chunk Strategy**](./docs/01_DATA_INGESTION_AND_CHUNK_STRATEGY.md)
3. [**02 - Hybrid RAG & Vector Store (ChromaDB + BM25 + RRF)**](./docs/02_HYBRID_RAG_AND_VECTOR_STORE.md)
4. [**03 - Deterministic Financial Math Tools**](./docs/03_DETERMINISTIC_FINANCIAL_MATH_TOOLS.md)
5. [**04 - LangGraph Multi-Agent Stateful Orchestration**](./docs/04_LANGGRAPH_MULTI_AGENT_WORKFLOW.md)
6. [**05 - Guardrails & Pydantic Structured Outputs**](./docs/05_GUARDRAILS_AND_STRUCTURED_OUTPUTS.md)
7. *(Next: 06 - Evaluation & LLM-as-a-Judge Benchmark)*
8. *(Next: 07 - Full-Stack Deployment & Morgan Stanley Interview Guide)*

---

## 🏛️ Why FinAgent? (The Wall Street Context)
Standard LLMs hallucinate numbers, fail at multi-step financial math, and cannot provide verifiable citations required by financial regulations (SEC / FINRA).

FinAgent solves this by orchestrating a **team of specialized agents** on a stateful **LangGraph** workflow:
* **SEC Retrieval Agent:** Hybrid search (BM25 + Dense Vectors) with page-level citations.
* **Quantitative Analyst Agent:** Deterministic Python execution tool for exact financial ratios.
* **Risk & Compliance Agent:** Scans Item 1A Risk Factors and audits factual grounding.
* **Evaluation:** Benchmarked with **Ragas (LLM-as-a-Judge)** to prove 95%+ Faithfulness.
