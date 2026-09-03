import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.graph import run_financial_analysis
from src.evaluation.benchmark import RAGEvaluationBenchmark

def run_step_6_verification():
    print("================================================================================")
    print("🚀 STEP 6 VERIFICATION: RAGAS LLM-AS-A-JUDGE EVALUATION BENCHMARK")
    print("================================================================================")

    evaluator = RAGEvaluationBenchmark()

    # --- CASE 1: Apple Financial Statement Audit ---
    print("\nEvaluating Case 1: Apple Inc. Net Sales & Gross Margins...")
    aapl_run = run_financial_analysis(
        query="What was Apple's total net sales in 2024 and its gross margin percentage?",
        ticker="AAPL",
        fiscal_year="2024",
        thread_id="eval_aapl_1"
    )
    retrieved_texts_1 = [d["content"] for d in aapl_run["retrieved_docs"]]
    evaluator.run_benchmark_case(
        case_name="Apple 2024 Sales & Gross Margin",
        query="What was Apple's total net sales in 2024 and its gross margin percentage?",
        response_text=aapl_run["final_report"],
        retrieved_contexts=retrieved_texts_1,
        ground_truth_keywords=["391,035", "180,683", "46.2%", "Gross Margin"]
    )

    # --- CASE 2: Apple Supply Chain & Semiconductor Risk Audit ---
    print("Evaluating Case 2: Apple Supply Chain & TSMC Concentration Risks...")
    aapl_risk_run = run_financial_analysis(
        query="Analyze Apple supply chain vulnerabilities, TSMC chip reliance, and Foxconn assembly",
        ticker="AAPL",
        fiscal_year="2024",
        thread_id="eval_aapl_2"
    )
    retrieved_texts_2 = [d["content"] for d in aapl_risk_run["retrieved_docs"]]
    evaluator.run_benchmark_case(
        case_name="Apple Supply Chain & TSMC Risk",
        query="Analyze Apple supply chain vulnerabilities, TSMC chip reliance, and Foxconn assembly",
        response_text=aapl_risk_run["final_report"],
        retrieved_contexts=retrieved_texts_2,
        ground_truth_keywords=["TSMC", "Foxconn", "Taiwan", "China", "Supply Chain"]
    )

    # --- CASE 3: Morgan Stanley 2024 Net Income & Efficiency Ratio ---
    print("Evaluating Case 3: Morgan Stanley Net Income Growth & Efficiency Ratio...")
    ms_run = run_financial_analysis(
        query="Audit Morgan Stanley 2024 Net Income growth and enterprise efficiency ratio",
        ticker="MS",
        fiscal_year="2024",
        thread_id="eval_ms_1"
    )
    retrieved_texts_3 = [d["content"] for d in ms_run["retrieved_docs"]]
    evaluator.run_benchmark_case(
        case_name="Morgan Stanley Income & Efficiency Ratio",
        query="Audit Morgan Stanley 2024 Net Income growth and enterprise efficiency ratio",
        response_text=ms_run["final_report"],
        retrieved_contexts=retrieved_texts_3,
        ground_truth_keywords=["10,850", "44,850", "59,800", "75.0%", "Efficiency Ratio"]
    )

    # --- CASE 4: Morgan Stanley Capital Adequacy & CET1 Ratio ---
    print("Evaluating Case 4: Morgan Stanley Regulatory CET1 Capital & Basel III...")
    ms_cap_run = run_financial_analysis(
        query="Audit Morgan Stanley Common Equity Tier 1 CET1 capital ratio and Basel III compliance",
        ticker="MS",
        fiscal_year="2024",
        thread_id="eval_ms_2"
    )
    retrieved_texts_4 = [d["content"] for d in ms_cap_run["retrieved_docs"]]
    evaluator.run_benchmark_case(
        case_name="Morgan Stanley CET1 Capital Adequacy",
        query="Audit Morgan Stanley Common Equity Tier 1 CET1 capital ratio and Basel III compliance",
        response_text=ms_cap_run["final_report"],
        retrieved_contexts=retrieved_texts_4,
        ground_truth_keywords=["15.2%", "CET1", "Basel III", "Standardized", "Capital"]
    )

    # --- PRINT QUANTITATIVE SCORECARD ---
    print("\n" + "=" * 80)
    print("📊 RAGAS EVALUATION BENCHMARK SCORECARD")
    print("=" * 80)
    print(f"{'Evaluation Scenario':<38} | {'Faithful':<8} | {'Relevance':<9} | {'Precision':<9} | {'Recall':<8} | {'Grade'}")
    print("-" * 80)

    total_faith = 0.0
    total_rel = 0.0
    total_prec = 0.0
    total_rec = 0.0

    for r in evaluator.benchmark_results:
        print(f"{r['case_name']:<38} | {r['faithfulness']:<8.2f} | {r['answer_relevance']:<9.2f} | {r['context_precision']:<9.2f} | {r['context_recall']:<8.2f} | {r['grade']}")
        total_faith += r["faithfulness"]
        total_rel += r["answer_relevance"]
        total_prec += r["context_precision"]
        total_rec += r["context_recall"]

    n = len(evaluator.benchmark_results)
    avg_faith = total_faith / n
    avg_rel = total_rel / n
    avg_prec = total_prec / n
    avg_rec = total_rec / n
    avg_overall = (avg_faith + avg_rel + avg_prec + avg_rec) / 4.0

    print("-" * 80)
    print(f"{'AVERAGE SYSTEM BENCHMARK':<38} | {avg_faith:<8.2f} | {avg_rel:<9.2f} | {avg_prec:<9.2f} | {avg_rec:<8.2f} | {'A+ (100%)' if avg_overall >= 0.95 else 'A'}")
    print("=" * 80)

    # Assert rigorous production benchmarks
    assert avg_faith >= 0.95, f"Faithfulness benchmark failed ({avg_faith:.2f} < 0.95)!"
    assert avg_rel >= 0.90, f"Answer relevance benchmark failed ({avg_rel:.2f} < 0.90)!"
    assert avg_prec >= 0.90, f"Context precision benchmark failed ({avg_prec:.2f} < 0.90)!"
    assert avg_rec >= 0.90, f"Context recall benchmark failed ({avg_rec:.2f} < 0.90)!"

    print("\n🎉 ALL 4 RAGAS BENCHMARK METRICS MET OR EXCEEDED PRODUCTION TARGETS (95%+ FAITHFULNESS)!")
    print("================================================================================")

if __name__ == "__main__":
    run_step_6_verification()
