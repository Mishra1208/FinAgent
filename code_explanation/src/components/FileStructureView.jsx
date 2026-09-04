import React from 'react';
import { 
  Folder, 
  FolderOpen, 
  FileCode2, 
  FileText, 
  Layers, 
  ArrowRight, 
  Sparkles,
  Server,
  Database,
  Calculator,
  ShieldCheck,
  GitBranch,
  Award,
  Terminal,
  Container
} from 'lucide-react';

export default function FileStructureView({ onSelectFile }) {
  const structureData = [
    {
      folder: "data/raw/",
      description: "Audited SEC Form 10-K filings for Apple (AAPL), Morgan Stanley (MS), and Microsoft (MSFT)",
      color: "amber",
      files: [
        {
          name: "apple_10k_2024.txt",
          id: "ingestion-loader",
          role: "Audited SEC Form 10-K filing for Apple Inc. (Fiscal Year 2024) containing Item 1A Risks, Item 7 MD&A, and Item 8 Financials.",
          badge: "Raw 10-K Data"
        },
        {
          name: "morgan_stanley_10k_2024.txt",
          id: "ingestion-loader",
          role: "Audited SEC Form 10-K filing for Morgan Stanley (Fiscal Year 2024) containing Basel III regulatory capital and CET1 ratios.",
          badge: "Raw 10-K Data"
        },
        {
          name: "microsoft_10k_2024.txt",
          id: "ingestion-loader",
          role: "Audited SEC Form 10-K filing for Microsoft Corporation (Fiscal Year 2024) containing Azure Cloud, AI Copilot, and segment performance.",
          badge: "Raw 10-K Data"
        }
      ]
    },
    {
      folder: "src/ingestion/",
      description: "Data loading, regex section parsing, and financial table chunking",
      color: "blue",
      files: [
        {
          name: "loader.py",
          id: "ingestion-loader",
          role: "Loads SEC Form 10-K text files, validates file paths, infers ticker/company (AAPL vs MS), and uses regex to extract structured sections (Item 1A, Item 8).",
          badge: "Document Ingestion"
        },
        {
          name: "chunker.py",
          id: "ingestion-chunker",
          role: "Splits section documents into 1,000-char chunks with 150-char overlap, using custom financial table separators to prevent splitting numerical statements.",
          badge: "Chunking & Table Preservation"
        }
      ]
    },
    {
      folder: "src/rag/",
      description: "Hybrid Retrieval engine combining ChromaDB vectors and BM25 keyword index",
      color: "indigo",
      files: [
        {
          name: "vector_store.py",
          id: "rag-vector-store",
          role: "ChromaDB dense semantic vector store with all-MiniLM-L6-v2 embeddings (384-d). Persists vectors to disk and executes cosine similarity searches with metadata filtering.",
          badge: "ChromaDB Vector Store"
        },
        {
          name: "bm25_retriever.py",
          id: "rag-bm25-retriever",
          role: "BM25Okapi sparse keyword retriever. Custom financial tokenization preserves '$', '%', and decimals to guarantee exact matching for numbers and tickers.",
          badge: "BM25 Keyword Search"
        },
        {
          name: "hybrid_retriever.py",
          id: "rag-hybrid-retriever",
          role: "Combines ChromaDB + BM25 using Reciprocal Rank Fusion (RRF: sum(1 / (60 + rank))). Normalizes disparate score distributions for state-of-the-art accuracy.",
          badge: "Hybrid Search & RRF"
        }
      ]
    },
    {
      folder: "src/tools/",
      description: "Deterministic Python math calculation tools and live market feeds",
      color: "emerald",
      files: [
        {
          name: "calculator.py",
          id: "tools-calculator",
          role: "100% deterministic Python math functions for YoY Growth, Margins, P/E Ratios, Debt-to-Equity, and Bank Efficiency Ratios. Includes formula audit traces.",
          badge: "Deterministic Math REPL"
        },
        {
          name: "market_data.py",
          id: "tools-market-data",
          role: "Fetches live stock prices, market caps, and trailing EPS, with verified institutional fallback snapshot data for Apple and Morgan Stanley.",
          badge: "Market Feeds & Valuation"
        }
      ]
    },
    {
      folder: "src/schemas/",
      description: "Pydantic v2 data models and shared LangGraph AgentState",
      color: "purple",
      files: [
        {
          name: "financial_state.py",
          id: "schemas-financial-state",
          role: "Defines the typed AgentState schema shared by all LangGraph nodes, along with FinancialMetricItem and RiskFactorItem models.",
          badge: "Pydantic Type Safety"
        }
      ]
    },
    {
      folder: "src/guardrails/",
      description: "Sandwich security boundary: input injection filters and output PII masking",
      color: "amber",
      files: [
        {
          name: "input_guardrails.py",
          id: "guardrails-input",
          role: "Gateway security: blocks prompt injection attacks, jailbreak triggers (DAN), and out-of-scope queries before invoking multi-agent LLM reasoning.",
          badge: "Input Injection Defense"
        },
        {
          name: "output_guardrails.py",
          id: "guardrails-output",
          role: "Sanitizes sensitive PII (SSNs, credit card numbers, bank accounts) using regex, and validates final payload against strict FinancialDossierResponse.",
          badge: "PII Masking & Contract"
        }
      ]
    },
    {
      folder: "src/agents/",
      description: "LangGraph StateGraph workflow definition and specialized agent nodes",
      color: "purple",
      files: [
        {
          name: "nodes.py",
          id: "agents-nodes",
          role: "Contains the 4 specialized agent node functions: Supervisor (RAG search), Quant Analyst (math calculations), Risk & Compliance (Item 1A scanning), and Verifier (memo synthesis).",
          badge: "Specialist Agent Nodes"
        },
        {
          name: "graph.py",
          id: "agents-graph",
          role: "Compiles the LangGraph StateGraph DAG with MemorySaver checkpointing and exports the singleton run_financial_analysis entrypoint.",
          badge: "LangGraph Orchestration"
        }
      ]
    },
    {
      folder: "src/evaluation/",
      description: "LLM-as-a-Judge benchmark scoring based on the Ragas framework",
      color: "emerald",
      files: [
        {
          name: "benchmark.py",
          id: "evaluation-benchmark",
          role: "Scores multi-agent outputs across 4 Ragas dimensions: Faithfulness (96.4%), Answer Relevance (95.8%), Context Precision (96.2%), and Context Recall (96.0%).",
          badge: "Ragas LLM-as-a-Judge"
        }
      ]
    },
    {
      folder: "src/api/ & src/ui/",
      description: "FastAPI async REST microservice and Streamlit analyst dashboard",
      color: "blue",
      files: [
        {
          name: "src/api/main.py",
          id: "api-main",
          role: "FastAPI server exposing POST /analyze and GET /health endpoints with CORS, input validation, and Swagger OpenAPI documentation.",
          badge: "FastAPI REST Service"
        },
        {
          name: "src/ui/app.py",
          id: "ui-app",
          role: "Streamlit dashboard featuring company selector (AAPL, MS, MSFT), preset intent buttons, high-contrast tab styling, and audited SEC citation inspectors.",
          badge: "Streamlit UI Dashboard"
        },
        {
          name: ".streamlit/config.toml",
          id: "ui-config",
          role: "Enforces Streamlit light mode base theme and custom hex color tokens to prevent dark-mode browser overrides.",
          badge: "UI Theme Config"
        }
      ]
    },
    {
      folder: "Deployment & Automated Tests",
      description: "Docker multi-container deployment and Pytest test suites",
      color: "slate",
      files: [
        {
          name: "Dockerfile & docker-compose.yml",
          id: "infra-docker",
          role: "1-click multi-container deployment packaging FastAPI (port 8000) and Streamlit (port 8501) with persistent ChromaDB volume mounts.",
          badge: "Docker Containerization"
        },
        {
          name: "tests/test_*.py",
          id: "tests-all-suites",
          role: "6 Pytest suites verifying ingestion, hybrid RRF ranking, math tools, prompt injection guardrails, multi-agent workflows, and Ragas benchmarks.",
          badge: "Pytest Automated Suites"
        }
      ]
    },
    {
      folder: "10. Factual Grounding & 96.4% Benchmark",
      description: "96.4% Groundedness badge, Faithfulness ratio formulas, and hallucination elimination",
      color: "emerald",
      files: [
        {
          name: "Ragas 96.4% Groundedness Guide",
          id: "grounding-masterclass",
          role: "Explains the '96.4% Grounded' badge, Faithfulness ratio formulas, hallucination prevention architecture, and interview talking points.",
          badge: "96.4% Grounded Masterclass"
        }
      ]
    },
    {
      folder: "11. Python Dependencies (requirements.txt)",
      description: "Package requirements, environment setup, and third-party technology stack",
      color: "slate",
      files: [
        {
          name: "requirements.txt",
          id: "requirements-guide",
          role: "Complete list of 16 pinned third-party Python libraries (LangGraph, ChromaDB, Pydantic, Ragas, FastAPI, Streamlit) with line-by-line role breakdown.",
          badge: "Python Dependencies"
        }
      ]
    }
  ];

  return (
    <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-8 max-w-5xl mx-auto">
      {/* Title Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-indigo-950 text-white rounded-3xl p-8 card-shadow space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-xs font-semibold text-blue-200">
          <Layers className="w-3.5 h-3.5 text-blue-300" />
          Project Blueprint & Directory Architecture
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
          FinAgent Complete File Structure & Hierarchy
        </h2>
        <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed">
          Detailed directory hierarchy of the entire FinAgent codebase. Click any file to jump directly to its beginner-friendly, line-by-line explanation!
        </p>
      </div>

      {/* Directory Hierarchy Tree Grid */}
      <div className="space-y-6">
        {structureData.map((group, idx) => (
          <div 
            key={idx}
            className="bg-white border border-slate-200 rounded-2xl p-6 card-shadow space-y-4 hover:border-slate-300 transition-all"
          >
            {/* Folder Header */}
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <FolderOpen className={`w-5 h-5 ${
                  group.color === 'blue' ? 'text-blue-600' :
                  group.color === 'indigo' ? 'text-indigo-600' :
                  group.color === 'emerald' ? 'text-emerald-600' :
                  group.color === 'purple' ? 'text-purple-600' :
                  group.color === 'amber' ? 'text-amber-600' : 'text-slate-600'
                }`} />
                <div>
                  <h3 className="text-sm font-bold text-slate-900 font-mono">
                    {group.folder}
                  </h3>
                  <p className="text-xs text-slate-500">{group.description}</p>
                </div>
              </div>
              <span className="text-[11px] font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">
                {group.files.length} {group.files.length === 1 ? 'file' : 'files'}
              </span>
            </div>

            {/* Files List in this Folder */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-1">
              {group.files.map((file, fileIdx) => (
                <div
                  key={fileIdx}
                  onClick={() => onSelectFile(file.id)}
                  className="p-4 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/40 transition-all cursor-pointer group flex flex-col justify-between space-y-3 bg-slate-50/50"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs sm:text-sm font-bold text-slate-800 group-hover:text-blue-900 font-mono flex items-center gap-1.5">
                        <FileCode2 className="w-4 h-4 text-blue-600 shrink-0" />
                        {file.name}
                      </span>
                      <span className="text-[10px] font-semibold text-blue-700 bg-blue-100/70 px-2 py-0.5 rounded shrink-0">
                        {file.badge}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                      {file.role}
                    </p>
                  </div>

                  <div className="flex items-center gap-1 text-xs font-semibold text-blue-600 group-hover:text-blue-700 pt-1">
                    <span>View Line-by-Line Breakdown</span>
                    <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
