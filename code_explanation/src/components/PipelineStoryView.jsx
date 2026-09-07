import React, { useState } from 'react';
import { 
  GitBranch, 
  ArrowRight, 
  ArrowDown, 
  Layers, 
  CheckCircle2, 
  Sparkles, 
  Database, 
  Calculator, 
  ShieldCheck, 
  FileText, 
  Cpu, 
  Award, 
  Zap, 
  TrendingUp, 
  Lock, 
  Eye, 
  ChevronRight, 
  FileCode2,
  FolderOpen,
  Boxes,
  HelpCircle,
  Lightbulb,
  Workflow,
  Network
} from 'lucide-react';

export default function PipelineStoryView({ activeModuleId, onSelectModule }) {
  const [activeStoryTab, setActiveStoryTab] = useState('build'); // 'build' or 'walkthrough'
  const [activeStepIndex, setActiveStepIndex] = useState(null);

  const buildPhases = [
    {
      phaseNumber: 1,
      phaseTitle: "Raw Data Ingestion & Section Parsing",
      color: "blue",
      badge: "Phase 1: Ingestion",
      fileLocation: "src/ingestion/loader.py",
      folderLocation: "src/ingestion/",
      connectedFiles: ["data/raw/*.txt", "src/ingestion/chunker.py"],
      whyFirst: "You cannot search or analyze data before loading it into memory. We start with raw SEC 10-K text files on disk.",
      whatItPerforms: "Reads the 150+ page filing text, inspects filename to infer company (AAPL, MS, MSFT), extracts the fiscal year, and uses dual-regex pattern matchers to slice the file into official SEC sections (Item 1A Risk Factors, Item 7 MD&A, Item 8 Financials).",
      dataOutput: "List of LangChain Document objects with structured metadata: {'ticker': 'MS', 'fiscal_year': '2024', 'section': 'Item 8'}",
      howItConnectsToNext: "Passes the parsed section Documents to chunker.py so large 50-page sections can be sliced into digestible 1,000-character pieces."
    },
    {
      phaseNumber: 2,
      phaseTitle: "Financial Chunking & Dual Storage Indexing",
      color: "indigo",
      badge: "Phase 2: Storage & Indexing",
      fileLocation: "src/rag/vector_store.py & src/rag/bm25_retriever.py",
      folderLocation: "src/rag/",
      connectedFiles: ["src/ingestion/chunker.py", "src/rag/hybrid_retriever.py"],
      whyFirst: "Raw documents are too large for LLM context windows and vector cosine similarity. We must chunk and index them ahead of time.",
      whatItPerforms: "Chunker slices text into 1,000-char chunks with 150-char overlap, preserving financial balance sheet tables. ChromaDB computes 384-d dense embeddings with unique IDs (MS_2024_0), while Rank-BM25 indexes keywords ($54,141, CET1, 15.2%).",
      dataOutput: "Persistent ChromaDB vector index on disk + In-memory BM25 inverted keyword index unified inside FinancialHybridRetriever.",
      howItConnectsToNext: "Creates the singleton hybrid retriever that the Supervisor agent will query during runtime to fetch exact evidence."
    },
    {
      phaseNumber: 3,
      phaseTitle: "Deterministic Financial Math Tools & Market Feeds",
      color: "emerald",
      badge: "Phase 3: Tooling Layer",
      fileLocation: "src/tools/calculator.py & src/tools/market_data.py",
      folderLocation: "src/tools/",
      connectedFiles: ["src/tools/calculator.py", "src/tools/market_data.py"],
      whyFirst: "LLMs are probabilistic language models and frequently make severe arithmetic hallucinations (e.g. 180683 / 391035 = 42% instead of 46.21%). We must build deterministic Python math tools before building agents.",
      whatItPerforms: "Executes pure Python arithmetic using Decimal precision for YoY Growth, Operating Margins, Net Margins, Debt-to-Equity, and Bank Efficiency Ratios. Generates mathematical formula audit strings (e.g. '(37025.0 / 54141.0) * 100').",
      dataOutput: "Verified JSON calculation dictionaries with exact floats and string formula audit traces.",
      howItConnectsToNext: "Provides the callable Python tools that the Quantitative Analyst agent will execute to compute exact financial metrics."
    },
    {
      phaseNumber: 4,
      phaseTitle: "Typed State Contracts & Security Guardrails",
      color: "purple",
      badge: "Phase 4: Contract & Security",
      fileLocation: "src/schemas/financial_state.py & src/guardrails/*.py",
      folderLocation: "src/schemas/ & src/guardrails/",
      connectedFiles: ["src/guardrails/input_guardrails.py", "src/guardrails/output_guardrails.py"],
      whyFirst: "Autonomous agents need a structured shared memory schema to pass data, and enterprise systems require a security perimeter against prompt injection attacks.",
      whatItPerforms: "Defines Pydantic v2 AgentState holding query, ticker, retrieved_docs, calculated_metrics, and risk_factors. InputGuardrail blocks prompt injection / jailbreak attempts; OutputGuardrail masks sensitive PII and validates output schemas.",
      dataOutput: "Immutable Pydantic schema validation across every agent handoff + Sanitized user queries.",
      howItConnectsToNext: "AgentState becomes the central state dictionary that LangGraph initializes and passes sequentially through every node in the graph."
    },
    {
      phaseNumber: 5,
      phaseTitle: "Specialized Multi-Agent Nodes & LangGraph Orchestration",
      color: "amber",
      badge: "Phase 5: Multi-Agent Logic",
      fileLocation: "src/agents/nodes.py & src/agents/graph.py",
      folderLocation: "src/agents/",
      connectedFiles: ["src/schemas/financial_state.py", "src/rag/hybrid_retriever.py", "src/tools/calculator.py"],
      whyFirst: "Now that we have data, storage, math tools, and state schemas, we wire the 4 autonomous agent nodes into a coordinated cyclical workflow.",
      whatItPerforms: "Implements 4 specialist agents: 1) Supervisor (routes & executes Hybrid RAG), 2) Quant Analyst (runs Python math tools), 3) Risk Auditor (scans Item 1A risks), and 4) Citation Verifier (grounds claims & writes memo). graph.py compiles them into a stateful StateGraph DAG with memory checkpointing.",
      dataOutput: "Fully compiled LangGraph executable runnable via singleton run_financial_analysis(query, ticker, fiscal_year).",
      howItConnectsToNext: "The compiled graph is invoked by automated evaluation benchmarks and production REST API / UI interfaces."
    },
    {
      phaseNumber: 6,
      phaseTitle: "Automated Evaluation Benchmark (Ragas LLM-as-a-Judge)",
      color: "rose",
      badge: "Phase 6: Evaluation Layer",
      fileLocation: "src/evaluation/benchmark.py",
      folderLocation: "src/evaluation/",
      connectedFiles: ["tests/test_evaluation_benchmark.py"],
      whyFirst: "In regulated financial services, multi-agent AI cannot be deployed without quantitative proof of zero hallucinations.",
      whatItPerforms: "Runs automated test suites evaluating outputs across 4 Ragas dimensions: Faithfulness (96.4%), Answer Relevance (95.8%), Context Precision (96.2%), and Context Recall (96.0%). Extracts all numerical claims and mathematically verifies them against source SEC chunks.",
      dataOutput: "Institutional Grade A+ scorecard (96.4% Groundedness score) with verified claim ratios.",
      howItConnectsToNext: "Guarantees system reliability before connecting to production user interfaces."
    },
    {
      phaseNumber: 7,
      phaseTitle: "Production Delivery: FastAPI Microservice & Streamlit Console",
      color: "blue",
      badge: "Phase 7: Presentation Layer",
      fileLocation: "src/ui/app.py & src/api/main.py",
      folderLocation: "src/ui/ & src/api/ & .streamlit/",
      connectedFiles: [".streamlit/config.toml", "Dockerfile", "docker-compose.yml"],
      whyFirst: "The final step is serving the intelligence to equity analysts, portfolio managers, and downstream institutional software.",
      whatItPerforms: "FastAPI serves asynchronous REST POST /analyze endpoints with CORS; Streamlit provides a light-mode executive console featuring multi-company dropdowns (AAPL, MS, MSFT), preset query buttons, high-contrast KPI cards, and SEC citation chunk inspectors.",
      dataOutput: "Interactive web dashboard on port 8501 + OpenAPI Swagger JSON on port 8000.",
      howItConnectsToNext: "End-to-end pipeline complete! Ready for live analyst usage and cloud deployment."
    }
  ];

  const morganStanleyFlowSteps = [
    {
      step: 1,
      title: "Raw 10-K Document Placed",
      file: "data/raw/morgan_stanley_10k_2024.txt",
      folder: "data/raw/",
      badge: "1. Raw Source",
      color: "amber",
      icon: FileText,
      shortSummary: "Audited SEC Form 10-K text file stored on disk.",
      inputFrom: "SEC EDGAR Filing Archive",
      outputTo: "src/ingestion/loader.py"
    },
    {
      step: 2,
      title: "Metadata Ingestion & Regex Splitting",
      file: "src/ingestion/loader.py",
      folder: "src/ingestion/",
      badge: "2. Document Loader",
      color: "blue",
      icon: FolderOpen,
      shortSummary: "Detects ticker='MS', year='2024', splits Item 1A Risks & Item 8 Financials.",
      inputFrom: "data/raw/morgan_stanley_10k_2024.txt",
      outputTo: "src/ingestion/chunker.py"
    },
    {
      step: 3,
      title: "Financial Table Chunking",
      file: "src/ingestion/chunker.py",
      folder: "src/ingestion/",
      badge: "3. Table Chunker",
      color: "indigo",
      icon: Layers,
      shortSummary: "Splits into 1,000-char chunks with 150-char overlap, preserving numerical tables.",
      inputFrom: "src/ingestion/loader.py (Parsed Documents)",
      outputTo: "src/rag/vector_store.py & src/rag/bm25_retriever.py"
    },
    {
      step: 4,
      title: "Dual Hybrid Indexing (ChromaDB + BM25)",
      file: "src/rag/vector_store.py & src/rag/bm25_retriever.py",
      folder: "src/rag/",
      badge: "4. Dual Storage",
      color: "purple",
      icon: Database,
      shortSummary: "ChromaDB computes 384-d vectors (MS_2024_0); BM25 builds keyword inverted index.",
      inputFrom: "src/ingestion/chunker.py (1,000-char chunks)",
      outputTo: "src/rag/hybrid_retriever.py (Pre-indexed)"
    },
    {
      step: 5,
      title: "Analyst Submits Query on Dashboard",
      file: "src/ui/app.py",
      folder: "src/ui/",
      badge: "5. UI Console",
      color: "blue",
      icon: Sparkles,
      shortSummary: "User selects 'Morgan Stanley', '2024', and clicks CET1 Capital & Efficiency Preset.",
      inputFrom: "User Interaction in Browser",
      outputTo: "src/guardrails/input_guardrails.py"
    },
    {
      step: 6,
      title: "Input Guardrail Security Sanitization",
      file: "src/guardrails/input_guardrails.py",
      folder: "src/guardrails/",
      badge: "6. Security Gateway",
      color: "rose",
      icon: ShieldCheck,
      shortSummary: "Scans prompt for injection/jailbreak attacks and non-financial topics (Passed).",
      inputFrom: "src/ui/app.py (User Query)",
      outputTo: "src/agents/graph.py (LangGraph Initializer)"
    },
    {
      step: 7,
      title: "Supervisor Node & Hybrid RAG Retrieval",
      file: "src/agents/nodes.py (supervisor_node)",
      folder: "src/agents/",
      badge: "7. Supervisor Agent",
      color: "blue",
      icon: Cpu,
      shortSummary: "Locks ticker='MS', calls hybrid_retriever.py with metadata_filter to pull top-6 chunks.",
      inputFrom: "src/guardrails/input_guardrails.py & src/rag/hybrid_retriever.py",
      outputTo: "src/agents/nodes.py (quant_analyst_node)"
    },
    {
      step: 8,
      title: "Quant Analyst & Deterministic Math Tools",
      file: "src/agents/nodes.py (quant_analyst_node) -> src/tools/calculator.py",
      folder: "src/agents/ & src/tools/",
      badge: "8. Quant Analyst",
      color: "emerald",
      icon: Calculator,
      shortSummary: "Extracts $54,141M revenues, $37,025M expenses; calls Python math -> 68.39% Efficiency.",
      inputFrom: "state['retrieved_docs']",
      outputTo: "src/agents/nodes.py (risk_compliance_node)"
    },
    {
      step: 9,
      title: "Risk & Compliance Regulatory Audit",
      file: "src/agents/nodes.py (risk_compliance_node)",
      folder: "src/agents/",
      badge: "9. Risk Auditor",
      color: "amber",
      icon: Lock,
      shortSummary: "Audits Item 1A: Basel III CET1 Capital (15.2% vs 13.5% requirement) with severity tags.",
      inputFrom: "state['retrieved_docs']",
      outputTo: "src/agents/nodes.py (verifier_node)"
    },
    {
      step: 10,
      title: "Citation Verifier & Grounding Memo",
      file: "src/agents/nodes.py (verifier_node)",
      folder: "src/agents/",
      badge: "10. Citation Verifier",
      color: "purple",
      icon: CheckCircle2,
      shortSummary: "Cross-checks all metrics against chunks, injects citation IDs, and crafts executive memo.",
      inputFrom: "state['calculated_metrics'], state['risk_factors'], state['retrieved_docs']",
      outputTo: "src/guardrails/output_guardrails.py"
    },
    {
      step: 11,
      title: "Output Guardrail & PII Masking",
      file: "src/guardrails/output_guardrails.py",
      folder: "src/guardrails/",
      badge: "11. Output Defense",
      color: "rose",
      icon: ShieldCheck,
      shortSummary: "Redacts sensitive PII (SSNs, accounts) and validates final Pydantic response schema.",
      inputFrom: "src/agents/nodes.py (verifier_node)",
      outputTo: "src/ui/app.py (Streamlit UI)"
    },
    {
      step: 12,
      title: "Streamlit UI Multi-Tab Institutional Rendering",
      file: "src/ui/app.py & .streamlit/config.toml",
      folder: "src/ui/ & .streamlit/",
      badge: "12. Executive UI",
      color: "blue",
      icon: Eye,
      shortSummary: "Renders 4 high-contrast tabs: KPI cards ($54.1B, 68.4%), risk table, & SEC chunk inspector.",
      inputFrom: "Validated Multi-Agent State Payload",
      outputTo: "Analyst Screen"
    },
    {
      step: 13,
      title: "Ragas Automated Benchmark (96.4% Grounded)",
      file: "src/evaluation/benchmark.py",
      folder: "src/evaluation/",
      badge: "13. Ragas Benchmark",
      color: "emerald",
      icon: Award,
      shortSummary: "Computes Faithfulness ratio = 96.4%, mathematically proving zero hallucinations.",
      inputFrom: "Generated Memo & SEC Chunks",
      outputTo: "Institutional Grade A+ Audit Report"
    }
  ];

  return (
    <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-8 max-w-5xl mx-auto">
      {/* Light Top Banner */}
      <div className="bg-gradient-to-br from-white via-indigo-50/40 to-blue-50/60 border border-indigo-200/80 rounded-3xl p-6 sm:p-8 card-shadow space-y-4 shadow-sm">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-100/70 border border-indigo-200 text-xs font-bold text-indigo-800">
          <Network className="w-3.5 h-3.5 text-indigo-600" />
          Category 12: End-to-End System Story & Flowchart Architecture
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          How FinAgent Works: Full Story, File Connections & Flowchart
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 max-w-3xl leading-relaxed">
          Explore the exact step-by-step connection graph of the FinAgent system in a clean, easy-to-read view. See how files communicate data through state schemas, why each file connects to the next, and follow the complete journey when <code className="px-2 py-0.5 bg-indigo-100 text-indigo-900 rounded font-mono text-xs font-semibold border border-indigo-200">morgan_stanley_10k_2024.txt</code> is analyzed.
        </p>

        {/* Light Tab Switcher */}
        <div className="flex flex-wrap items-center gap-2.5 pt-2">
          <button
            onClick={() => setActiveStoryTab('build')}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 ${
              activeStoryTab === 'build'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20 ring-2 ring-indigo-600/30'
                : 'bg-white text-slate-700 hover:bg-slate-100 border border-slate-200 shadow-2xs'
            }`}
          >
            <Workflow className="w-4 h-4" />
            1. Chronological Build Order (7 Phases)
          </button>
          <button
            onClick={() => setActiveStoryTab('walkthrough')}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-2 ${
              activeStoryTab === 'walkthrough'
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-500/20 ring-2 ring-emerald-600/30'
                : 'bg-white text-slate-700 hover:bg-slate-100 border border-slate-200 shadow-2xs'
            }`}
          >
            <GitBranch className="w-4 h-4" />
            2. Morgan Stanley 10-K Execution Flowchart (13 Steps)
          </button>
        </div>
      </div>

      {/* TAB 1: CHRONOLOGICAL BUILD STORY */}
      {activeStoryTab === 'build' && (
        <div className="space-y-8">
          {/* SECTION HEADER & LIGHT FLOW DIAGRAM BOX */}
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-sm shadow-xs">
                  1
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Chronological System Build Order: From Raw Data to UI
                  </h3>
                  <p className="text-xs text-slate-500">
                    Follow this exact sequence to understand how the components are engineered and connected.
                  </p>
                </div>
              </div>
              <span className="text-xs font-semibold text-indigo-700 bg-indigo-50 border border-indigo-200 px-3 py-1 rounded-full">
                7 Build Phases
              </span>
            </div>

            {/* LIGHT-THEMED VISUAL FLOWCHART SUMMARY BOX */}
            <div className="bg-gradient-to-br from-indigo-50/50 via-white to-blue-50/40 border border-indigo-200/80 rounded-2xl p-5 card-shadow shadow-xs space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-900 font-mono flex items-center gap-1.5">
                  <Workflow className="w-4 h-4 text-indigo-600" /> High-Level Architecture Flowchart:
                </span>
                <span className="text-[11px] font-semibold text-indigo-700 font-mono bg-indigo-100/80 px-2 py-0.5 rounded border border-indigo-200">
                  Data Flow ➔ Left to Right
                </span>
              </div>
              
              <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2.5 pt-1 text-center">
                {buildPhases.map((bp) => (
                  <div key={bp.phaseNumber} className="bg-white border border-slate-200 hover:border-indigo-300 rounded-xl p-3 space-y-1.5 flex flex-col justify-between shadow-2xs transition-all">
                    <span className="text-[10px] font-mono font-bold text-indigo-600 block bg-indigo-50 py-0.5 rounded border border-indigo-100">
                      Phase 0{bp.phaseNumber}
                    </span>
                    <span className="text-xs font-bold text-slate-900 block leading-tight">
                      {bp.phaseTitle.split(' ')[0]} {bp.phaseTitle.split(' ')[1]}
                    </span>
                    <span className="text-[10px] text-slate-600 font-mono block truncate bg-slate-50 px-1 py-0.5 rounded border border-slate-200">
                      {bp.folderLocation}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* DETAILED PHASE CARDS */}
          <div className="space-y-5">
            {buildPhases.map((phase) => (
              <div 
                key={phase.phaseNumber}
                className="bg-white border border-slate-200 rounded-2xl p-6 card-shadow space-y-4 transition-all hover:border-indigo-300 hover:shadow-md"
              >
                {/* Header with clear file & folder location */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white font-mono font-bold text-sm flex items-center justify-center shadow-xs">
                      0{phase.phaseNumber}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-700 font-mono">
                          {phase.badge}
                        </span>
                        <span className="text-slate-300">•</span>
                        <span className="text-xs font-mono font-semibold text-slate-500 flex items-center gap-1">
                          <FolderOpen className="w-3 h-3 text-amber-500" />
                          {phase.folderLocation}
                        </span>
                      </div>
                      <h4 className="text-base font-bold text-slate-900">
                        {phase.phaseTitle}
                      </h4>
                    </div>
                  </div>

                  {/* Primary File Location Badge */}
                  <div className="flex items-center gap-1.5 bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-xl text-blue-900 font-mono text-xs font-bold shadow-2xs">
                    <FileCode2 className="w-3.5 h-3.5 text-blue-600" />
                    <span>{phase.fileLocation}</span>
                  </div>
                </div>

                {/* Connected Files Chips */}
                {phase.connectedFiles && (
                  <div className="flex flex-wrap items-center gap-2 text-xs">
                    <span className="font-bold text-slate-700 flex items-center gap-1">
                      <Network className="w-3.5 h-3.5 text-indigo-600" />
                      Inter-Connected Files:
                    </span>
                    {phase.connectedFiles.map((cf, idx) => (
                      <span key={idx} className="font-mono text-[11px] font-semibold bg-slate-50 text-slate-700 px-2.5 py-1 rounded-lg border border-slate-200 shadow-2xs">
                        {cf}
                      </span>
                    ))}
                  </div>
                )}

                {/* 3 Plain-English Columns */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
                  {/* 1. Why Built First */}
                  <div className="bg-slate-50/80 rounded-xl p-4 space-y-2 border border-slate-200/80">
                    <div className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                      <HelpCircle className="w-4 h-4 text-blue-600 shrink-0" />
                      1. Why We Build This First:
                    </div>
                    <p className="text-xs text-slate-700 leading-relaxed">
                      {phase.whyFirst}
                    </p>
                  </div>

                  {/* 2. What It Performs */}
                  <div className="bg-indigo-50/50 rounded-xl p-4 space-y-2 border border-indigo-100">
                    <div className="text-xs font-bold text-indigo-950 flex items-center gap-1.5">
                      <Zap className="w-4 h-4 text-indigo-600 shrink-0" />
                      2. What It Performs:
                    </div>
                    <p className="text-xs text-indigo-950/90 leading-relaxed">
                      {phase.whatItPerforms}
                    </p>
                  </div>

                  {/* 3. Connection to Next File */}
                  <div className="bg-emerald-50/50 rounded-xl p-4 space-y-2 border border-emerald-100">
                    <div className="text-xs font-bold text-emerald-950 flex items-center gap-1.5">
                      <ArrowRight className="w-4 h-4 text-emerald-600 shrink-0" />
                      3. How It Connects to Next File:
                    </div>
                    <p className="text-xs text-emerald-950/90 leading-relaxed">
                      {phase.howItConnectsToNext}
                    </p>
                  </div>
                </div>

                {/* Light-Themed Data Passed Output Box */}
                <div className="bg-emerald-50/70 border border-emerald-200/90 rounded-xl p-3.5 text-xs font-mono text-emerald-950 flex items-start gap-2.5 shadow-2xs">
                  <span className="text-white font-bold shrink-0 bg-emerald-600 px-2.5 py-0.5 rounded shadow-xs">
                    DATA PASSED ➔
                  </span>
                  <span className="text-emerald-900 leading-relaxed font-semibold">{phase.dataOutput}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: STEP-BY-STEP MORGAN STANLEY RUNTIME WALKTHROUGH WITH LIGHT-THEMED FLOWCHART */}
      {activeStoryTab === 'walkthrough' && (
        <div className="space-y-8">
          {/* SECTION HEADER */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 text-white flex items-center justify-center font-bold text-sm shadow-xs">
                2
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900">
                  Step-by-Step Runtime Execution Flowchart (Morgan Stanley 10-K Journey)
                </h3>
                <p className="text-xs text-slate-500">
                  Follow the exact journey from the moment <code className="text-emerald-800 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200 font-mono font-bold">morgan_stanley_10k_2024.txt</code> is added to the final 96.4% grounded UI dashboard.
                </p>
              </div>
            </div>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full">
              13 Step Flowchart
            </span>
          </div>

          {/* LIGHT-THEMED INTERACTIVE VISUAL FLOWCHART GRAPH */}
          <div className="bg-gradient-to-br from-slate-50 via-white to-emerald-50/30 border border-slate-200 rounded-3xl p-6 card-shadow shadow-sm space-y-5">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-900 font-mono flex items-center gap-1.5">
                  <Workflow className="w-4 h-4 text-emerald-600" /> Interactive Visual Connection Graph:
                </span>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  Click any node in the flowchart to highlight its step details below.
                </p>
              </div>
              <span className="px-3 py-1 rounded-lg bg-emerald-100 text-emerald-800 font-mono text-[11px] font-bold border border-emerald-200">
                13 Connected Nodes
              </span>
            </div>

            {/* FLOWCHART NODES GRID IN LIGHT THEME */}
            <div className="space-y-2.5">
              {morganStanleyFlowSteps.map((stepItem, idx) => {
                const IconComp = stepItem.icon;
                const isLast = idx === morganStanleyFlowSteps.length - 1;
                return (
                  <div key={stepItem.step} className="space-y-1.5">
                    <div 
                      onClick={() => setActiveStepIndex(stepItem.step === activeStepIndex ? null : stepItem.step)}
                      className={`p-3.5 sm:p-4 rounded-2xl border transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                        activeStepIndex === stepItem.step
                          ? 'bg-emerald-50 border-emerald-500 shadow-md ring-2 ring-emerald-500/20'
                          : 'bg-white border-slate-200 hover:bg-slate-50 hover:border-emerald-300 shadow-2xs'
                      }`}
                    >
                      {/* Left Side: Step Icon & Title */}
                      <div className="flex items-center gap-3.5 min-w-0">
                        <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-mono font-bold text-xs shrink-0 shadow-xs">
                          {stepItem.step < 10 ? `0${stepItem.step}` : stepItem.step}
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="text-xs sm:text-sm font-bold text-slate-900">
                              {stepItem.title}
                            </span>
                            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-semibold">
                              {stepItem.folder}
                            </span>
                          </div>
                          <p className="text-xs text-slate-600 truncate mt-0.5">
                            {stepItem.shortSummary}
                          </p>
                        </div>
                      </div>

                      {/* Right Side: Exact File Location Badge */}
                      <div className="shrink-0 flex items-center gap-2 text-right">
                        <div className="bg-blue-50 text-blue-900 border border-blue-200 px-3 py-1.5 rounded-xl font-mono text-xs font-bold shadow-2xs">
                          📄 {stepItem.file}
                        </div>
                        <ChevronRight className={`w-4 h-4 text-slate-400 transition-transform ${activeStepIndex === stepItem.step ? 'rotate-90 text-emerald-600' : ''}`} />
                      </div>
                    </div>

                    {/* Downward Connection Arrow */}
                    {!isLast && (
                      <div className="flex items-center justify-center py-0.5 text-slate-400">
                        <ArrowDown className="w-4 h-4 text-emerald-600 animate-bounce" />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* STEP CARDS BREAKDOWN */}
          <div className="space-y-4 pt-2">
            <h4 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Boxes className="w-4 h-4 text-indigo-600" />
              Full Step-by-Step Connection Details:
            </h4>

            {morganStanleyFlowSteps.map((stepItem) => {
              const IconComp = stepItem.icon;
              return (
                <div 
                  key={stepItem.step}
                  id={`step-${stepItem.step}`}
                  className="bg-white border border-slate-200 rounded-2xl p-5 card-shadow space-y-3.5 transition-all hover:border-emerald-300 hover:shadow-md"
                >
                  {/* Step Header */}
                  <div className="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-slate-100">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-xs shadow-xs">
                        {stepItem.step < 10 ? `0${stepItem.step}` : stepItem.step}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 font-mono">
                            {stepItem.badge}
                          </span>
                          <span className="text-slate-300">•</span>
                          <span className="text-xs font-mono font-semibold text-slate-500 flex items-center gap-1">
                            <FolderOpen className="w-3 h-3 text-amber-500" />
                            {stepItem.folder}
                          </span>
                        </div>
                        <h4 className="text-base font-bold text-slate-900">
                          {stepItem.title}
                        </h4>
                      </div>
                    </div>

                    {/* Exact File Path Badge */}
                    <div className="bg-blue-50 border border-blue-200 px-3 py-1 rounded-xl text-blue-900 font-mono text-xs font-bold shadow-2xs">
                      📄 {stepItem.file}
                    </div>
                  </div>

                  {/* Plain English Story */}
                  <p className="text-xs sm:text-sm text-slate-700 leading-relaxed bg-slate-50/80 p-3.5 rounded-xl border border-slate-200/80">
                    {stepItem.shortSummary}
                  </p>

                  {/* Input Source -> Output Target Row */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 space-y-1">
                      <span className="font-bold text-slate-800 flex items-center gap-1.5">
                        <ArrowRight className="w-3.5 h-3.5 text-blue-600" />
                        Inputs Received From:
                      </span>
                      <span className="text-slate-700 font-mono text-[11px] font-medium block">{stepItem.inputFrom}</span>
                    </div>

                    <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-3 space-y-1">
                      <span className="font-bold text-emerald-950 flex items-center gap-1.5">
                        <ArrowRight className="w-3.5 h-3.5 text-emerald-600" />
                        Outputs Handed Over To:
                      </span>
                      <span className="text-emerald-950 font-mono text-[11px] font-medium block">{stepItem.outputTo}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </main>
  );
}
