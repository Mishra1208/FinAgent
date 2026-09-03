# FinAgent: Enterprise SEC Multi-Agent Financial Intelligence System

> **A production-grade, stateful Multi-Agent AI system built with LangGraph, Hybrid RAG, FastAPI, and Streamlit to analyze SEC 10-K filings, calculate deterministic financial ratios, audit risk factors, and eliminate hallucinations with LLM-as-a-Judge evaluation.**

---

## 📖 Complete Documentation & Learning Guide
Every component of this project is documented step-by-step for easy learning and interview preparation inside the [`docs/`](./docs) folder:

1. [**00 - Project Overview & System Architecture**](./docs/00_PROJECT_OVERVIEW_AND_ARCHITECTURE.md)
2. *(Next: 01 - Data Ingestion & SEC 10-K Chunk Strategy)*
3. *(Next: 02 - Hybrid RAG & Vector Store)*
4. *(Next: 03 - Deterministic Financial Math Tools)*
5. *(Next: 04 - LangGraph Multi-Agent Workflow)*
6. *(Next: 05 - Guardrails & Pydantic Structured Outputs)*
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
