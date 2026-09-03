import React from 'react';
import { 
  GitBranch, 
  Database, 
  Calculator, 
  ShieldCheck, 
  CheckCircle2, 
  Sparkles,
  ArrowRight,
  TrendingUp,
  Cpu,
  Layers,
  Award,
  FileCode2,
  ExternalLink,
  Zap,
  ArrowDown
} from 'lucide-react';
import { ARCHITECTURE_DATA } from '../data/architecture';

export default function ArchitectureView({ onSelectFile }) {
  const agentNodes = [
    {
      step: 1,
      name: "Supervisor Node",
      badge: "Router & Retriever",
      color: "blue",
      mainFile: "src/agents/nodes.py (Lines 54–107)",
      supportingFiles: [
        { name: "hybrid_retriever.py", id: "rag-hybrid-retriever", role: "Runs dense + sparse RRF fusion" },
        { name: "vector_store.py", id: "rag-vector-store", role: "ChromaDB cosine similarity" },
        { name: "bm25_retriever.py", id: "rag-bm25-retriever", role: "BM25 keyword search" },
        { name: "loader.py", id: "ingestion-loader", role: "Extracts ticker & section metadata" }
      ],
      stateRead: "state.query, state.ticker, state.fiscal_year",
      stateWrite: "ticker, company_name, retrieved_docs, next_node='quant_analyst'",
      whatItDoes: "Analyzes user intent, identifies company ticker (AAPL vs MS), executes Hybrid RAG with metadata pre-filtering, and serializes top-6 SEC 10-K chunks into state."
    },
    {
      step: 2,
      name: "Quant Analyst Node",
      badge: "Deterministic Math",
      color: "emerald",
      mainFile: "src/agents/nodes.py (Lines 108–280)",
      supportingFiles: [
        { name: "calculator.py", id: "tools-calculator", role: "Deterministic Python math tools (Margins, YoY, P/E)" },
        { name: "market_data.py", id: "tools-market-data", role: "Live prices, market cap, diluted EPS" },
        { name: "financial_state.py", id: "schemas-financial-state", role: "FinancialMetricItem schema" }
      ],
      stateRead: "state.ticker, state.fiscal_year, state.retrieved_docs",
      stateWrite: "calculated_metrics (list of FinancialMetricItem), next_node='risk_compliance'",
      whatItDoes: "Extracts raw reported numbers from SEC balance sheets/income statements and invokes verified Python math tools. Produces 100% accurate metrics with exact formulas."
    },
    {
      step: 3,
      name: "Risk & Compliance Node",
      badge: "Item 1A Risk Audit",
      color: "amber",
      mainFile: "src/agents/nodes.py (Lines 281–410)",
      supportingFiles: [
        { name: "financial_state.py", id: "schemas-financial-state", role: "RiskFactorItem Pydantic schema" },
        { name: "loader.py", id: "ingestion-loader", role: "Item 1A section text extraction" }
      ],
      stateRead: "state.ticker, state.retrieved_docs",
      stateWrite: "risk_factors (list of RiskFactorItem), next_node='verifier'",
      whatItDoes: "Scans SEC Item 1A disclosures for supply chain, regulatory/antitrust, and AI competition risks. Categorizes risks and assigns institutional severity levels (CRITICAL, HIGH, MEDIUM)."
    },
    {
      step: 4,
      name: "Citation Verifier Node",
      badge: "Audit & Synthesis",
      color: "indigo",
      mainFile: "src/agents/nodes.py (Lines 411–523)",
      supportingFiles: [
        { name: "output_guardrails.py", id: "guardrails-output", role: "PII masking & schema validation" },
        { name: "benchmark.py", id: "evaluation-benchmark", role: "Ragas Faithfulness grounding check" },
        { name: "graph.py", id: "agents-graph", role: "StateGraph workflow compilation & END state" }
      ],
      stateRead: "calculated_metrics, risk_factors, retrieved_docs, ticker, company_name",
      stateWrite: "final_report (Markdown Memo), compliance_audit_passed=True, hallucination_score=0.0",
      whatItDoes: "Cross-checks every numerical claim against raw source SEC chunks, verifies citations (e.g. Item 8), scrubs any PII, and formats the executive investment research dossier."
    }
  ];

  return (
    <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-8 max-w-5xl mx-auto">
      {/* Title Card */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white rounded-3xl p-8 card-shadow space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-xs font-semibold text-blue-200">
          <Sparkles className="w-3.5 h-3.5 text-amber-300" />
          Enterprise System Blueprint
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
          {ARCHITECTURE_DATA.title}
        </h2>
        <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed">
          {ARCHITECTURE_DATA.description}
        </p>
      </div>

      {/* Enhanced Multi-Agent LangGraph Workflow Flowchart */}
      <div className="bg-white border border-slate-200 rounded-3xl p-6 md:p-8 card-shadow space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100">
          <div>
            <h3 className="text-base sm:text-lg font-extrabold text-slate-900 flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-purple-600" />
              LangGraph Multi-Agent Cyclical Workflow & Supporting Files
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Visual pipeline showing which Python files execute and support each agent node.
            </p>
          </div>
          <span className="text-xs font-mono font-bold text-purple-700 bg-purple-50 border border-purple-200 px-3 py-1 rounded-lg">
            Compiled in src/agents/graph.py
          </span>
        </div>

        {/* Start / End Banner */}
        <div className="flex items-center justify-between px-2 text-xs font-bold text-slate-400 font-mono">
          <span className="flex items-center gap-1.5 text-emerald-600 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            START (User Query)
          </span>
          <span className="hidden sm:inline text-slate-300">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</span>
          <span className="flex items-center gap-1.5 text-purple-600 bg-purple-50 border border-purple-200 px-2.5 py-1 rounded-full">
            END (Executive Memo) &check;
          </span>
        </div>

        {/* 4 Connected Agent Cards */}
        <div className="space-y-4">
          {agentNodes.map((node, idx) => (
            <div key={idx} className="relative">
              {/* Node Card */}
              <div className={`border rounded-2xl p-5 md:p-6 card-shadow transition-all bg-white hover:border-slate-300 ${
                node.color === 'blue' ? 'border-blue-200/80 bg-gradient-to-r from-blue-50/40 via-white to-white' :
                node.color === 'emerald' ? 'border-emerald-200/80 bg-gradient-to-r from-emerald-50/40 via-white to-white' :
                node.color === 'amber' ? 'border-amber-200/80 bg-gradient-to-r from-amber-50/40 via-white to-white' :
                'border-indigo-200/80 bg-gradient-to-r from-indigo-50/40 via-white to-white'
              }`}>
                {/* Node Top Bar */}
                <div className="flex flex-wrap items-start justify-between gap-3 pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-3">
                    <span className={`w-8 h-8 rounded-xl flex items-center justify-center font-bold text-sm text-white shadow-xs ${
                      node.color === 'blue' ? 'bg-blue-600' :
                      node.color === 'emerald' ? 'bg-emerald-600' :
                      node.color === 'amber' ? 'bg-amber-600' : 'bg-indigo-600'
                    }`}>
                      {node.step}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="text-sm sm:text-base font-bold text-slate-900">
                          {node.name}
                        </h4>
                        <span className="text-[10px] font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full">
                          {node.badge}
                        </span>
                      </div>
                      <div className="text-[11px] font-mono text-slate-500 mt-0.5">
                        Main Implementation: <span className="text-blue-700 font-semibold">{node.mainFile}</span>
                      </div>
                    </div>
                  </div>

                  <span className="text-[11px] font-mono font-semibold text-slate-400 bg-slate-50 border border-slate-200 px-2 py-1 rounded">
                    Node {node.step} of 4
                  </span>
                </div>

                {/* Node Explanation */}
                <p className="text-xs sm:text-sm text-slate-700 leading-relaxed pt-3">
                  {node.whatItDoes}
                </p>

                {/* Supporting Files Breakdown (Clickable) */}
                <div className="pt-3 space-y-2">
                  <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                    Supporting Files & Underlying Architecture:
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {node.supportingFiles.map((sf, sfIdx) => (
                      <div
                        key={sfIdx}
                        onClick={() => onSelectFile && onSelectFile(sf.id)}
                        className="p-2.5 rounded-lg border border-slate-200/80 bg-white hover:border-blue-300 hover:bg-blue-50/50 transition-all cursor-pointer group flex items-start gap-2 text-xs shadow-2xs"
                      >
                        <FileCode2 className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
                        <div className="min-w-0 flex-1">
                          <div className="font-mono font-bold text-slate-800 group-hover:text-blue-700 flex items-center justify-between">
                            <span>{sf.name}</span>
                            <ArrowRight className="w-3 h-3 text-slate-300 group-hover:text-blue-600 group-hover:translate-x-0.5 transition-transform" />
                          </div>
                          <div className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                            {sf.role}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* State Input / Output Tags */}
                <div className="pt-3 flex flex-wrap items-center gap-3 text-[11px] font-mono border-t border-slate-100 mt-3">
                  <div className="text-slate-500">
                    <strong className="text-slate-700">Reads State:</strong> {node.stateRead}
                  </div>
                  <span className="text-slate-300">|</span>
                  <div className="text-emerald-700">
                    <strong className="text-slate-700">Writes State:</strong> {node.stateWrite}
                  </div>
                </div>
              </div>

              {/* Connecting Flow Arrow */}
              {idx < agentNodes.length - 1 && (
                <div className="flex justify-center my-1.5">
                  <div className="flex items-center gap-1.5 text-slate-400 font-mono text-[11px] bg-slate-100 px-3 py-0.5 rounded-full border border-slate-200">
                    <ArrowDown className="w-3.5 h-3.5 text-blue-600 animate-bounce" />
                    <span>Transfers Typed StateGraph(AgentState)</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 4 Core Pillars Detailed Cards */}
      <div className="space-y-6">
        <h3 className="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
          <Layers className="w-5 h-5 text-blue-600" />
          The 4 Engineering Pillars of FinAgent
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {ARCHITECTURE_DATA.pillars.map((pillar) => (
            <div 
              key={pillar.id}
              className="bg-white border border-slate-200 rounded-2xl p-6 card-shadow space-y-4 hover:border-slate-300 transition-all"
            >
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold text-white shadow-sm ${
                  pillar.color === 'blue' ? 'bg-blue-600' :
                  pillar.color === 'emerald' ? 'bg-emerald-600' :
                  pillar.color === 'purple' ? 'bg-purple-600' : 'bg-amber-600'
                }`}>
                  {pillar.id === 'hybrid-rag' && <Database className="w-5 h-5" />}
                  {pillar.id === 'deterministic-math' && <Calculator className="w-5 h-5" />}
                  {pillar.id === 'multi-agent-graph' && <GitBranch className="w-5 h-5" />}
                  {pillar.id === 'guardrails-pipeline' && <ShieldCheck className="w-5 h-5" />}
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900">{pillar.title}</h4>
                  <p className="text-xs text-slate-500">{pillar.tagline}</p>
                </div>
              </div>

              {/* Steps */}
              <div className="space-y-2 border-t border-slate-100 pt-3">
                {pillar.steps.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-xs">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                    <div>
                      <strong className="text-slate-800">{step.name}: </strong>
                      <span className="text-slate-600">{step.desc}</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Interview talking point box */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs space-y-1">
                <span className="font-bold text-slate-800 flex items-center gap-1">
                  <Award className="w-3.5 h-3.5 text-blue-600" />
                  Interview Answer:
                </span>
                <p className="text-slate-700 leading-relaxed">
                  {pillar.interviewAnswer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Ragas Evaluation Scorecard */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 card-shadow space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-600" />
            <h3 className="text-base sm:text-lg font-bold text-slate-900">
              Ragas LLM-as-a-Judge Evaluation Benchmark Results
            </h3>
          </div>
          <span className="px-3 py-1 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-full text-xs font-bold">
            Grade: Institutional A+ (96.4%)
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {ARCHITECTURE_DATA.benchmarks.map((b, idx) => (
            <div key={idx} className="border border-slate-200 bg-slate-50/60 rounded-xl p-4 space-y-2">
              <div className="text-xs font-semibold text-slate-500">{b.metric}</div>
              <div className="text-2xl font-extrabold text-slate-900 flex items-baseline gap-2">
                {b.score}
                <span className="text-xs font-normal text-emerald-700">{b.status}</span>
              </div>
              <p className="text-[11px] text-slate-600 leading-normal">{b.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
