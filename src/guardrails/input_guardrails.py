import re
from typing import Dict, Any, Tuple

# Known adversarial prompt injection triggers
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior)\s+rules?",
    r"system\s+override",
    r"you\s+are\s+now\s+(dan|an\s+unfiltered|jailbroken)",
    r"forget\s+(your\s+)?guidelines?",
    r"bypass\s+(all\s+)?security",
    r"act\s+as\s+(an\s+unrestricted|root|admin)",
    r"<script>",
    r"drop\s+database",
    r"delete\s+from"
]

# Keywords indicating relevant financial analysis intent
FINANCIAL_KEYWORDS = [
    "revenue", "sales", "margin", "profit", "net income", "ebitda", "pe ratio",
    "p/e", "eps", "diluted", "shares", "dividend", "debt", "equity", "asset",
    "balance sheet", "income statement", "cash flow", "10-k", "10k", "sec",
    "filing", "annual report", "risk", "rotce", "cet1", "efficiency ratio",
    "apple", "aapl", "morgan stanley", "ms", "wealth management", "segment",
    "growth", "ratio", "financial", "audit", "compliance", "stock", "market cap"
]

class InputGuardrail:
    """
    Enterprise Input Guardrail:
    1. Blocks Prompt Injections & Jailbreaks.
    2. Enforces Domain Scope (Rejects non-financial queries).
    3. Sanitizes user input before multi-agent execution.
    """
    @classmethod
    def validate_query(cls, query: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validates user query against security rules.
        Returns: (is_valid: bool, reason: str, metadata: dict)
        """
        if not query or len(query.strip()) < 3:
            return False, "Query is too short or empty.", {"risk_type": "EMPTY_INPUT"}

        clean_query = query.strip()
        query_lower = clean_query.lower()

        # 1. Prompt Injection Check
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, query_lower):
                return False, (
                    "Security Alert: Prompt injection or adversarial instruction detected. "
                    "Query blocked by enterprise AI guardrails."
                ), {"risk_type": "PROMPT_INJECTION", "matched_pattern": pattern}

        # 2. Financial Scope Enforcement Check
        has_financial_intent = any(kw in query_lower for kw in FINANCIAL_KEYWORDS)
        if not has_financial_intent and len(query_lower.split()) > 4:
            return False, (
                "Out-of-Scope Query: FinAgent is restricted to financial statement analysis, "
                "SEC Form 10-K auditing, and quantitative equity research."
            ), {"risk_type": "OUT_OF_SCOPE"}

        # 3. Passed all security checks
        return True, "Input validation passed.", {"risk_type": "CLEAN", "sanitized_query": clean_query}
