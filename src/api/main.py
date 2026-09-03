import os
import sys
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agents.graph import run_financial_analysis
from src.guardrails.input_guardrails import InputGuardrail
from src.guardrails.output_guardrails import OutputGuardrail, FinancialDossierResponse

app = FastAPI(
    title="FinAgent Enterprise API",
    description="Multi-Agent SEC 10-K Financial Intelligence & Quantitative Audit System",
    version="1.0.0"
)

# Enable CORS for local development and UI integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    query: str = Field(..., description="User question or financial analysis prompt")
    ticker: Optional[str] = Field(default="AAPL", description="Stock ticker symbol (e.g. AAPL, MS)")
    fiscal_year: Optional[str] = Field(default="2024", description="Fiscal year (e.g. 2024)")
    session_id: Optional[str] = Field(default="default_session", description="Session ID for state checkpointing")

@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "FinAgent Enterprise API",
        "status": "online",
        "version": "1.0.0",
        "supported_tickers": ["AAPL", "MS"],
        "docs_url": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "engine": "LangGraph Stateful Multi-Agent System",
        "retriever": "Hybrid ChromaDB + BM25Okapi",
        "guardrails": "Active"
    }

@app.post("/api/analyze", response_model=FinancialDossierResponse, tags=["Analysis"])
async def analyze_financials(request: AnalysisRequest):
    """
    Executes the complete multi-agent SEC financial analysis workflow:
    1. Input Guardrail: Blocks prompt injection and out-of-scope queries.
    2. LangGraph Execution: Supervisor -> Quant Analyst -> Risk Auditor -> Verifier.
    3. Output Guardrail: PII scrubbing and strict Pydantic validation.
    """
    # 1. Input Guardrails Check
    is_valid, reason, meta = InputGuardrail.validate_query(request.query)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Input Guardrail Rejection",
                "reason": reason,
                "risk_type": meta.get("risk_type")
            }
        )

    # 2. Execute Multi-Agent Graph
    try:
        final_state = run_financial_analysis(
            query=request.query,
            ticker=request.ticker,
            fiscal_year=request.fiscal_year,
            thread_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent workflow execution error: {str(e)}"
        )

    # 3. Output Guardrails Validation
    response_payload = OutputGuardrail.validate_and_format_response(final_state)
    return response_payload
