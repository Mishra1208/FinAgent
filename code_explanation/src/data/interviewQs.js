export const INTERVIEW_QUESTIONS = [
  {
    category: "Architecture & System Design",
    items: [
      {
        id: "arch-1",
        question: "Can you give an elevator pitch of your FinAgent project for an executive interviewer?",
        answer: "FinAgent is an enterprise-grade multi-agent financial intelligence system designed for investment banks. It autonomously parses and audits complex 150-page SEC 10-K filings to generate institutional-quality investment memos. It overcomes the three fatal flaws of generic LLMs—hallucination of numbers, bad math, and missing citations—by combining Hybrid RAG (BM25 + ChromaDB with Reciprocal Rank Fusion), deterministic Python calculation tools, and a LangGraph stateful multi-agent workflow.",
        keyPoints: ["Target audience: Wall Street analysts / compliance officers", "3 Solved Flaws: Hallucinations, Math inaccuracies, Missing citations", "Tech stack: LangGraph, ChromaDB, BM25, RRF, FastAPI, Streamlit, Ragas"]
      },
      {
        id: "arch-2",
        question: "Why did you use LangGraph instead of LangChain or AutoGen?",
        answer: "Standard LangChain SequentialChain is rigid and struggles with state mutations or cyclical loops. AutoGen can easily get stuck in unpredictable conversational loops. LangGraph gives us deterministic StateGraph DAGs, typed Pydantic state transitions across nodes, and built-in checkpointing with MemorySaver for session persistence and time-travel debugging.",
        keyPoints: ["Deterministic execution order", "Typed Pydantic state", "MemorySaver checkpointing", "Time-travel debugging"]
      },
      {
        id: "arch-3",
        question: "How do you handle cross-company or cross-year data pollution during RAG retrieval?",
        answer: "We use metadata extraction during SEC 10-K loading. Every chunk is tagged with ticker (AAPL vs MS), fiscal year (2024 vs 2023), and section name (Item 1A vs Item 8). During retrieval, the Supervisor node applies metadata pre-filtering (`metadata_filter={'ticker': ticker}`), restricting search to the exact company and eliminating cross-company contamination.",
        keyPoints: ["Metadata pre-filtering vs post-filtering", "Chunk tagging during ingestion", "Eliminating false positives"]
      }
    ]
  },
  {
    category: "Retrieval-Augmented Generation (RAG)",
    items: [
      {
        id: "rag-1",
        question: "What is Reciprocal Rank Fusion (RRF) and why is it preferred over linear score weighting?",
        answer: "Dense cosine similarity scores (scaled between -1 and 1) and sparse BM25 scores (unbounded positive floats) have fundamentally incompatible statistical distributions. Linearly combining them requires brittle alpha/beta hyperparameter tuning. RRF ranks items purely by position: RRF_Score(d) = sum(1 / (60 + rank_i(d))). It is scale-invariant, robust to outliers, and requires zero manual score calibration.",
        keyPoints: ["Scale invariance", "Formula: sum(1 / (60 + rank))", "Empirical constant k=60", "Robust to score distribution differences"]
      },
      {
        id: "rag-2",
        question: "What chunking strategy did you use and why?",
        answer: "We implemented a custom FinancialChunker using RecursiveCharacterTextSplitter with a 1,000-character chunk size and 150-character overlap. Crucially, our separator hierarchy prioritizes section headers, double newlines, bullet points, and single newlines over arbitrary token counts, keeping financial tables and risk disclosures cohesive without orphan rows.",
        keyPoints: ["1000 char size / 150 char overlap", "Table-aware separator hierarchy", "Unique chunk ID injection for auditability"]
      },
      {
        id: "rag-3",
        question: "Why did you choose all-MiniLM-L6-v2 embeddings?",
        answer: "all-MiniLM-L6-v2 produces high-quality 384-dimensional embeddings with ultra-fast inference (~15ms on CPU) and zero external API dependencies. Combined with BM25 keyword search, it achieves enterprise-grade semantic accuracy without recurring OpenAI embedding costs.",
        keyPoints: ["384 dimensions", "Fast CPU inference (~15ms)", "Zero API costs / offline capable"]
      }
    ]
  },
  {
    category: "Math & Deterministic Tool Calling",
    items: [
      {
        id: "tool-1",
        question: "Why can't we trust Large Language Models with arithmetic calculations?",
        answer: "LLMs predict the next most likely token based on probability weights from training corpora; they do not perform arithmetic logic. When computing YoY growth `(391035 - 383285) / 383285 * 100`, an LLM might generate 2.15% instead of the exact 2.02%. In regulated finance, arithmetic errors destroy credibility. We decouple extraction from calculation by passing numbers to verified Python tools.",
        keyPoints: ["Probabilistic token prediction vs arithmetic logic", "Deterministic Python REPL tools", "Exact formula audit trail"]
      },
      {
        id: "tool-2",
        question: "How do your tools ensure mathematical auditability?",
        answer: "Every calculation tool returns a structured dictionary containing the metric name, raw inputs, exact formula string, absolute difference, and formatted percentage. This allows the Citation Verifier agent to embed the exact mathematical formula directly into the research memo table.",
        keyPoints: ["Structured calculation response", "Formula citation in Markdown tables", "Zero division guards"]
      }
    ]
  },
  {
    category: "Guardrails, Security & Evaluation",
    items: [
      {
        id: "sec-1",
        question: "What is your defense against prompt injections and jailbreak attacks?",
        answer: "We use an Input Guardrail gateway that scans incoming queries against compiled regex patterns for jailbreak triggers ('ignore previous instructions', 'system override', 'act as DAN', SQL injection). Queries failing validation are rejected immediately with HTTP 400 before invoking any LLM or multi-agent nodes.",
        keyPoints: ["Gateway regex pattern defense", "Domain scope verification", "Cost saving & security boundary"]
      },
      {
        id: "sec-2",
        question: "How do you systematically benchmark and evaluate your RAG system?",
        answer: "We built an evaluation engine inspired by the Ragas framework that scores 4 metrics: Faithfulness (factual consistency against source chunks), Answer Relevance (query alignment), Context Precision (ground-truth in rank #1 chunk), and Context Recall (full fact retrieval). Our benchmark achieves an overall score of >96%, earning an institutional A+ grade.",
        keyPoints: ["4 Ragas dimensions: Faithfulness, Relevance, Precision, Recall", ">96% overall benchmark score", "Automated regression testing in CI/CD"]
      }
    ]
  }
];
