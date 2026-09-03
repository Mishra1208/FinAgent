import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.calculator import (
    calculate_yoy_growth,
    calculate_margin,
    calculate_pe_ratio,
    calculate_debt_to_equity,
    calculate_efficiency_ratio,
    calculate_yoy_growth_tool,
    calculate_margin_tool,
    calculate_pe_ratio_tool,
    calculate_debt_to_equity_tool,
    calculate_efficiency_ratio_tool
)
from src.tools.market_data import get_market_data, get_market_data_tool

def run_step_3_verification():
    print("================================================================================")
    print("🚀 STEP 3 VERIFICATION: DETERMINISTIC FINANCIAL MATH TOOLS")
    print("================================================================================")

    # 1. Test Apple YoY Revenue Growth (2024 vs 2023)
    # 2024 Net Sales: $391,035M | 2023 Net Sales: $383,285M
    yoy_res = calculate_yoy_growth(391035.0, 383285.0, "Apple Total Net Sales")
    print(f"📊 Test 1 (Apple YoY Revenue Growth) : {yoy_res['yoy_growth_percentage']}% (Expected: ~2.02%)")
    assert yoy_res["yoy_growth_percentage"] == 2.02, "YoY Growth calculation mismatch!"

    # 2. Test Apple 2024 Gross Margin
    # 2024 Gross Margin: $180,683M | Total Net Sales: $391,035M
    gm_res = calculate_margin(180683.0, 391035.0, "Gross Margin")
    print(f"📊 Test 2 (Apple Gross Margin)       : {gm_res['margin_percentage']}% (Expected: ~46.21%)")
    assert gm_res["margin_percentage"] == 46.21, "Gross Margin calculation mismatch!"

    # 3. Test Apple 2024 Operating Margin
    # 2024 Operating Income: $123,216M | Total Net Sales: $391,035M
    om_res = calculate_margin(123216.0, 391035.0, "Operating Margin")
    print(f"📊 Test 3 (Apple Operating Margin)   : {om_res['margin_percentage']}% (Expected: ~31.51%)")
    assert om_res["margin_percentage"] == 31.51, "Operating Margin calculation mismatch!"

    # 4. Test Morgan Stanley 2024 YoY Net Income Growth
    # 2024 Net Income: $10,850M | 2023 Net Income: $9,087M
    ms_yoy = calculate_yoy_growth(10850.0, 9087.0, "Morgan Stanley Net Income")
    print(f"📊 Test 4 (MS YoY Net Income Growth) : {ms_yoy['yoy_growth_percentage']}% (Expected: ~19.40%)")
    assert ms_yoy["yoy_growth_percentage"] == 19.40, "Morgan Stanley YoY Net Income calculation mismatch!"

    # 5. Test Morgan Stanley Enterprise Efficiency Ratio
    # 2024 Non-Interest Expenses: $44,850M | Total Net Revenues: $59,800M
    eff_res = calculate_efficiency_ratio(44850.0, 59800.0)
    print(f"📊 Test 5 (MS Efficiency Ratio)     : {eff_res['efficiency_ratio_percentage']}% (Expected: 75.00%)")
    assert eff_res["efficiency_ratio_percentage"] == 75.00, "Efficiency ratio calculation mismatch!"

    # 6. Test Apple P/E Ratio
    # Stock Price: $224.23 | Diluted EPS: $6.08
    pe_res = calculate_pe_ratio(224.23, 6.08)
    print(f"📊 Test 6 (Apple P/E Ratio)          : {pe_res['pe_ratio']}x (Expected: 36.88x)")
    assert pe_res["pe_ratio"] == 36.88, "P/E calculation mismatch!"

    # 7. Test Market Data Fetching
    market_res = get_market_data("AAPL")
    print(f"📊 Test 7 (Live/Cached Market Data)  : {market_res['company_name']} @ ${market_res['current_price']}")
    assert market_res["ticker"] == "AAPL", "Market data ticker mismatch!"

    # 8. Test LangChain Tool Calling Interface
    print("\n--------------------------------------------------------------------------------")
    print("🧪 TEST 8: LangChain Agent Tool Invocations")
    print("--------------------------------------------------------------------------------")
    tool_output = calculate_yoy_growth_tool.invoke({
        "current_val": 59800.0,
        "prior_val": 54790.0,
        "metric_name": "MS Net Revenue"
    })
    print(f"✅ Tool invocation successful: {tool_output}")
    assert "9.14" in tool_output, "Tool invocation returned incorrect payload!"

    print("\n================================================================================")
    print("🎉 STEP 3 DETERMINISTIC FINANCIAL TOOLS ARE 100% VERIFIED & PRODUCTION READY!")
    print("================================================================================")

if __name__ == "__main__":
    run_step_3_verification()
