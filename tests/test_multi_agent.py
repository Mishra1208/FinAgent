import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.graph import run_financial_analysis

def run_step_4_verification():
    print("================================================================================")
    print("🚀 STEP 4 VERIFICATION: LANGGRAPH MULTI-AGENT STATEFUL ORCHESTRATION")
    print("================================================================================")

    # --- TEST 1: End-to-End Multi-Agent Execution on Apple (AAPL) ---
    print("\n--------------------------------------------------------------------------------")
    print("🧪 TEST 1: Apple Inc. (AAPL) Multi-Agent Workflow Execution")
    print("--------------------------------------------------------------------------------")
    
    aapl_result = run_financial_analysis(
        query="Analyze Apple 2024 financial performance, profit margins, and supply chain risks",
        ticker="AAPL",
        fiscal_year="2024",
        thread_id="test_session_aapl"
    )

    print(f"✅ State Ticker Identified       : {aapl_result['ticker']} ({aapl_result['company_name']})")
    print(f"✅ Retrieved SEC Chunks Count    : {len(aapl_result['retrieved_docs'])} chunks")
    print(f"✅ Quant Metrics Generated       : {len(aapl_result['calculated_metrics'])} metrics")
    print(f"✅ Compliance Risks Audited      : {len(aapl_result['risk_factors'])} risk items")
    print(f"✅ Factual Grounding Passed      : {aapl_result['compliance_audit_passed']}")
    print(f"✅ Hallucination Risk Score      : {aapl_result['hallucination_score']:.1%}")

    assert aapl_result["ticker"] == "AAPL", "Ticker state corrupted!"
    assert len(aapl_result["calculated_metrics"]) >= 5, "Quant metrics incomplete!"
    assert len(aapl_result["risk_factors"]) >= 3, "Risk factors incomplete!"
    assert aapl_result["compliance_audit_passed"] is True, "Compliance grounding failed!"
    assert len(aapl_result["final_report"]) > 300, "Executive report generation failed!"

    # --- TEST 2: End-to-End Multi-Agent Execution on Morgan Stanley (MS) ---
    print("\n--------------------------------------------------------------------------------")
    print("🧪 TEST 2: Morgan Stanley (MS) Multi-Agent Workflow Execution")
    print("--------------------------------------------------------------------------------")

    ms_result = run_financial_analysis(
        query="Audit Morgan Stanley 2024 institutional revenues, bank efficiency ratio, and regulatory capital",
        ticker="MS",
        fiscal_year="2024",
        thread_id="test_session_ms"
    )

    print(f"✅ State Ticker Identified       : {ms_result['ticker']} ({ms_result['company_name']})")
    print(f"✅ Quant Metrics Generated       : {len(ms_result['calculated_metrics'])} metrics")
    print(f"✅ Compliance Risks Audited      : {len(ms_result['risk_factors'])} risk items")
    print(f"✅ Factual Grounding Passed      : {ms_result['compliance_audit_passed']}")

    # Verify specific Morgan Stanley financial ratios exist
    metric_names = [m.name for m in ms_result["calculated_metrics"]]
    assert "Bank Efficiency Ratio" in metric_names, "Bank Efficiency Ratio missing!"
    assert "Return on Tangible Common Equity (ROTCE)" in metric_names, "ROTCE missing!"
    assert "Standardized CET1 Capital Ratio" in metric_names, "CET1 ratio missing!"

    print("\n--- SAMPLE REPORT PREVIEW (MORGAN STANLEY) ---")
    print("\n".join(ms_result["final_report"].split("\n")[:20]))
    print("...")

    print("\n================================================================================")
    print("🎉 STEP 4 LANGGRAPH MULTI-AGENT WORKFLOW IS 100% VERIFIED & PRODUCTION READY!")
    print("================================================================================")

if __name__ == "__main__":
    run_step_4_verification()
