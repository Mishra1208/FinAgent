from typing import List, Dict, Any, Optional, Sequence, Annotated
import operator
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

class FinancialMetricItem(BaseModel):
    """Structured deterministic financial metric item."""
    name: str = Field(description="Name of metric (e.g. Total Net Sales, Gross Margin, ROTCE)")
    value: float = Field(description="Numerical value calculated or reported")
    formatted_value: str = Field(description="Formatted display string (e.g. '$391,035M', '46.21%')")
    period: str = Field(default="2024", description="Fiscal period/year")
    formula_used: Optional[str] = Field(default=None, description="Exact arithmetic formula executed")
    citation: str = Field(default="SEC Form 10-K", description="Source document section reference")

class RiskFactorItem(BaseModel):
    """Structured compliance risk factor item."""
    category: str = Field(description="Category (e.g. Supply Chain, Regulatory/Antitrust, AI Competition)")
    title: str = Field(description="Short summary title of the risk")
    severity: str = Field(default="HIGH", description="Risk level (CRITICAL, HIGH, MEDIUM, LOW)")
    details: str = Field(description="In-depth factual summary of the risk from Item 1A")
    source_section: str = Field(default="PART I - ITEM 1A. RISK FACTORS", description="Exact SEC 10-K section citation")

class AgentState(BaseModel):
    """
    State schema for the LangGraph Multi-Agent Financial Intelligence Workflow.
    All agents communicate by reading and updating this typed state.
    """
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    query: str = Field(default="", description="Original user prompt")
    ticker: str = Field(default="AAPL", description="Target equity ticker")
    company_name: str = Field(default="", description="Full company name")
    fiscal_year: str = Field(default="2024", description="Target fiscal year")
    
    # RAG Context & Artifacts
    retrieved_docs: List[Dict[str, Any]] = Field(default_factory=list, description="Serialized retrieved SEC chunks")
    
    # Agent Output Collections
    calculated_metrics: List[FinancialMetricItem] = Field(default_factory=list, description="Metrics calculated by Quant Agent")
    risk_factors: List[RiskFactorItem] = Field(default_factory=list, description="Audited risk items from Compliance Agent")
    
    # Audit & Verification Flags
    compliance_audit_passed: bool = Field(default=False, description="Whether factual grounding verifier passed")
    hallucination_score: float = Field(default=0.0, description="Hallucination check score (0.0 is perfect grounding)")
    
    # Final Executive Dossier
    final_report: str = Field(default="", description="Synthesized Markdown research report")
    next_node: str = Field(default="", description="Pointer to next workflow execution node")
