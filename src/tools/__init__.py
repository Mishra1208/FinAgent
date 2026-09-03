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
    calculate_efficiency_ratio_tool,
)
from src.tools.market_data import get_market_data, get_market_data_tool

FINANCIAL_AGENT_TOOLS = [
    calculate_yoy_growth_tool,
    calculate_margin_tool,
    calculate_pe_ratio_tool,
    calculate_debt_to_equity_tool,
    calculate_efficiency_ratio_tool,
    get_market_data_tool,
]
