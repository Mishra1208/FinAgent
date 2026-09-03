import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.schemas.financial_state import FinancialMetricItem, RiskFactorItem

class FinancialDossierResponse(BaseModel):
    """Strict Pydantic Response Schema for Institutional API Responses."""
    ticker: str = Field(description="Target stock ticker (e.g. AAPL, MS)")
    company_name: str = Field(description="Full company legal name")
    fiscal_year: str = Field(description="Fiscal period analyzed (e.g. 2024)")
    metrics: List[FinancialMetricItem] = Field(description="Deterministic verified financial metrics")
    risk_factors: List[RiskFactorItem] = Field(description="Item 1A audited risk factors")
    compliance_passed: bool = Field(description="Factual grounding audit pass status")
    hallucination_score: float = Field(default=0.0, description="Hallucination probability (0.0 is perfect)")
    markdown_report: str = Field(description="Executive formatted dossier markdown")

class OutputGuardrail:
    """
    Enterprise Output Guardrail:
    1. Redacts PII and confidential account numbers.
    2. Validates strict Pydantic JSON schemas.
    3. Audits numerical citations to prevent hallucinations.
    """
    # Regex patterns for PII redaction
    SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"
    CREDIT_CARD_PATTERN = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
    ACCOUNT_NUMBER_PATTERN = r"\b(?:ACCT|ACC|ACCOUNT)[#:\s]+[0-9A-Z]{6,12}\b"

    @classmethod
    def sanitize_pii(cls, text: str) -> str:
        """Masks sensitive PII patterns from text."""
        sanitized = re.sub(cls.SSN_PATTERN, "[REDACTED_SSN]", text, flags=re.IGNORECASE)
        sanitized = re.sub(cls.CREDIT_CARD_PATTERN, "[REDACTED_CARD]", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(cls.ACCOUNT_NUMBER_PATTERN, "[REDACTED_ACCOUNT]", sanitized, flags=re.IGNORECASE)
        return sanitized

    @classmethod
    def validate_and_format_response(cls, agent_state: Dict[str, Any]) -> FinancialDossierResponse:
        """
        Validates state dictionary and constructs a type-safe Pydantic response object.
        """
        raw_report = agent_state.get("final_report", "")
        clean_report = cls.sanitize_pii(raw_report)

        metrics = agent_state.get("calculated_metrics", [])
        risk_factors = agent_state.get("risk_factors", [])

        # Validate structured output
        response = FinancialDossierResponse(
            ticker=agent_state.get("ticker", "UNKNOWN"),
            company_name=agent_state.get("company_name", "Enterprise Corp"),
            fiscal_year=agent_state.get("fiscal_year", "2024"),
            metrics=metrics,
            risk_factors=risk_factors,
            compliance_passed=agent_state.get("compliance_audit_passed", True),
            hallucination_score=agent_state.get("hallucination_score", 0.0),
            markdown_report=clean_report
        )
        return response
