<u></u># FinAgent: Enterprise SEC Multi-Agent Financial Intelligence System
## System Architecture & Project Blueprint

---

## 1. What is FinAgent?
**FinAgent** is an enterprise-grade, stateful multi-agent system designed for investment banks and asset managers (like Morgan Stanley). 

It autonomously parses, analyzes, and audits complex **SEC 10-K and 10-Q annual reports** to answer high-stakes financial queries, calculate verifiable valuation metrics, audit business risk disclosures, and produce cited executive investment memos.

---

## 2. Why We Built It (The Problem We Are Solving)
At major financial institutions, equity analysts and compliance officers read hundreds of 150-300 page SEC filings every month. 

When analysts try using standard generative AI models (like ChatGPT), they encounter three fatal flaws:
1. **Hallucination of Numerical Data:** Generic LLMs frequently misquote balance sheet figures or confuse fiscal years (e.g., mixing up Q3 2023 vs Q3 2024).
2. **Mathematical Inaccuracy:** LLMs predict tokens probabilistically; they cannot execute reliable multi-step math (like P/E ratios, operating margins, or debt ratios).
3. **Lack of Auditable Citations:** Financial compliance regulations (SEC / FINRA) require that any stated claim must trace back to an exact page number and financial table.

**FinAgent solves all three problems** by combining **Hybrid RAG**, **deterministic Python calculation tools**, and a **LangGraph cyclical multi-agent graph**.

---

## 3. High-Level Architecture

```
                                 [ FINANCIAL ANALYST ]
                                          │
                                          ▼
                            ┌───────────────────────────┐
                            │      STREAMLIT UI         │
                            │ (Interactive Dashboard)   │
                            └─────────────┬─────────────┘
                                          │ (HTTP / SSE)
                                          ▼
                            ┌───────────────────────────┐
                            │      FASTAPI SERVER       │
                            │   (Async Microservice)    │
                            └─────────────┬─────────────┘
                                          │
                                          ▼
                            ┌───────────────────────────┐
                            │  SUPERVISOR AGENT (Graph) │
                            │ Formulates execution plan │
                            └──────┬──────┬──────┬──────┘
                                   │      │      │
            ┌──────────────────────┘      │      └──────────────────────┐
            ▼                             ▼                             ▼
   [ SEC RETRIEVAL AGENT ]      [ QUANT RATIO AGENT ]       [ RISK & COMPLIANCE AGENT ]
   * Hybrid Search (BM25+Dense) * Executes Python REPL      * Scans Item 1A Risks
   * Ingests 10-K filings       * Computes P/E, EBITDA      * Eliminates hallucinations
   * Attaches Page Citations    * 100% deterministic math   * Enforces compliance rules
            │                             │                             │
            └──────────────────────┬──────┴─────────────────────────────┘
                                   │
                                   ▼
                      [ CITATION & VERIFIER AGENT ]
                      Cross-checks facts against raw text
                                   │
                                   ▼
                      [ STRUCTURED PYDANTIC OUTPUT ]
                      Strict JSON (Summary, Ratios, Risks, Citations)
                                   │
                                   ▼
                      [ LLM-AS-A-JUDGE BENCHMARK ]
                      Automated Ragas scoring (Faithfulness >= 95%)
```

---

## 4. Project Folder Structure Explained

```
FinAgent/
├── docs/                     <-- YOUR STUDY GUIDE (Updated at every single step)
│   ├── 00_PROJECT_OVERVIEW_AND_ARCHITECTURE.md
│   ├── 01_DATA_INGESTION_AND_CHUNK_STRATEGY.md
│   ├── 02_HYBRID_RAG_AND_VECTOR_STORE.md
│   └── ...
│
├── data/                     <-- RAW & PROCESSED SEC FILINGS
│   ├── raw/                  <-- Real SEC 10-K PDFs (e.g., Apple, Morgan Stanley)
│   └── vector_store/         <-- Persistent Chroma/Qdrant vector indices
│
├── src/                      <-- SOURCE CODE (Modular & Clean)
│   ├── ingestion/            <-- Document loading, table cleaning, chunking
│   ├── rag/                  <-- Hybrid search (BM25 + OpenAI/HuggingFace vectors)
│   ├── tools/                <-- Python calculation tools (Financial math REPL)
│   ├── agents/               <-- LangGraph nodes, state definitions, supervisor
│   ├── schemas/              <-- Pydantic data validation models
│   ├── api/                  <-- FastAPI async endpoints
│   └── ui/                   <-- Streamlit interactive dashboard
│
├── tests/                    <-- EVALUATION & BENCHMARKS
│   ├── test_rag.py           <-- Retrieval accuracy tests
│   └── evaluate_ragas.py     <-- LLM-as-a-Judge benchmark (Faithfulness & Relevance)
│
├── requirements.txt          <-- Project dependencies
└── docker-compose.yml        <-- 1-click enterprise deployment
```

---

## 5. Our Step-by-Step Implementation Roadmap

We will build FinAgent in clear, digestible milestones. You will never see massive blocks of unexplained code:

* **Step 1: Document Ingestion & SEC 10-K Chunking**
  * *What:* Ingest real 10-K filings, preserve table structures, and implement `RecursiveCharacterTextSplitter`.
  * *Docs:* `docs/01_DATA_INGESTION_AND_CHUNK_STRATEGY.md`
* **Step 2: Hybrid Retrieval (BM25 + Dense Vectors)**
  * *What:* Combine exact keyword matching with semantic embeddings and metadata filtering.
  * *Docs:* `docs/02_HYBRID_RAG_AND_VECTOR_STORE.md`
* **Step 3: Deterministic Financial Math Tool**
  * *What:* A Python calculation sandbox that calculates ratios without letting the LLM guess numbers.
  * *Docs:* `docs/03_FINANCIAL_MATH_TOOLS.md`
* **Step 4: LangGraph Multi-Agent Orchestration**
  * *What:* Supervisor, Analyst, and Compliance agents communicating over a shared typed `State`.
  * *Docs:* `docs/04_LANGGRAPH_MULTI_AGENT_WORKFLOW.md`
* **Step 5: Pydantic Structured Output & Guardrails**
  * *What:* Type-safe JSON responses and prompt injection defenses.
  * *Docs:* `docs/05_GUARDRAILS_AND_STRUCTURED_OUTPUTS.md`
* **Step 6: Automated Evaluation with LLM-as-a-Judge (Ragas)**
  * *What:* Automated script proving 95%+ Faithfulness and low hallucination.
  * *Docs:* `docs/06_EVALUATION_AND_LLM_AS_A_JUDGE.md`
* **Step 7: Full-Stack App (FastAPI + Streamlit + Docker)**
  * *What:* Live interactive dashboard ready to demonstrate in interviews.
  * *Docs:* `docs/07_DEPLOYMENT_AND_INTERVIEW_GUIDE.md`
