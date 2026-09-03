import math
from typing import Dict, Any, Union
from langchain_core.tools import tool

def calculate_yoy_growth(current_val: float, prior_val: float, metric_name: str = "Metric") -> Dict[str, Any]:
    """
    Deterministically calculates Year-over-Year (YoY) percentage growth.
    Formula: ((Current - Prior) / abs(Prior)) * 100
    """
    if prior_val == 0:
        return {
            "metric": metric_name,
            "error": "Prior value is zero; cannot divide by zero to compute growth."
        }
    
    growth_pct = ((current_val - prior_val) / abs(prior_val)) * 100.0
    return {
        "metric": metric_name,
        "current_period_value": current_val,
        "prior_period_value": prior_val,
        "absolute_change": round(current_val - prior_val, 2),
        "yoy_growth_percentage": round(growth_pct, 2),
        "formula": f"(({current_val} - {prior_val}) / abs({prior_val})) * 100"
    }

def calculate_margin(numerator: float, total_revenue: float, margin_type: str = "Operating Margin") -> Dict[str, Any]:
    """
    Deterministically calculates financial margins (Gross Margin, Operating Margin, Net Margin).
    Formula: (Numerator / Total Revenue) * 100
    """
    if total_revenue == 0:
        return {
            "margin_type": margin_type,
            "error": "Total revenue is zero; cannot compute margin."
        }
    
    margin_pct = (numerator / total_revenue) * 100.0
    return {
        "margin_type": margin_type,
        "numerator_value": numerator,
        "total_revenue": total_revenue,
        "margin_percentage": round(margin_pct, 2),
        "formula": f"({numerator} / {total_revenue}) * 100"
    }

def calculate_pe_ratio(stock_price: float, diluted_eps: float) -> Dict[str, Any]:
    """
    Deterministically calculates Price-to-Earnings (P/E) Ratio.
    Formula: Stock Price / Diluted Earnings Per Share
    """
    if diluted_eps <= 0:
        return {
            "error": "EPS is zero or negative; P/E ratio is not meaningful."
        }
    
    pe = stock_price / diluted_eps
    return {
        "stock_price": stock_price,
        "diluted_eps": diluted_eps,
        "pe_ratio": round(pe, 2),
        "formula": f"{stock_price} / {diluted_eps}"
    }

def calculate_debt_to_equity(total_debt: float, total_equity: float) -> Dict[str, Any]:
    """
    Deterministically calculates the Debt-to-Equity (D/E) Leverage Ratio.
    Formula: Total Debt / Total Shareholders' Equity
    """
    if total_equity <= 0:
        return {
            "error": "Shareholders' equity is zero or negative; leverage ratio cannot be computed."
        }
    
    de_ratio = total_debt / total_equity
    return {
        "total_debt": total_debt,
        "total_equity": total_equity,
        "debt_to_equity_ratio": round(de_ratio, 2),
        "formula": f"{total_debt} / {total_equity}"
    }

def calculate_efficiency_ratio(non_interest_expenses: float, total_net_revenue: float) -> Dict[str, Any]:
    """
    Deterministically calculates Enterprise Efficiency Ratio (Standard Bank Metric used by Morgan Stanley).
    Formula: (Non-Interest Expenses / Total Net Revenue) * 100
    A lower ratio indicates a more efficient bank.
    """
    if total_net_revenue <= 0:
        return {
            "error": "Net revenue is zero or negative; efficiency ratio cannot be computed."
        }
    
    eff_ratio = (non_interest_expenses / total_net_revenue) * 100.0
    return {
        "metric": "Bank Efficiency Ratio",
        "non_interest_expenses": non_interest_expenses,
        "total_net_revenue": total_net_revenue,
        "efficiency_ratio_percentage": round(eff_ratio, 2),
        "formula": f"({non_interest_expenses} / {total_net_revenue}) * 100"
    }

# ----------------------------------------------------------------------
# LangChain Tool Wrappers (for Agent Tool Calling)
# ----------------------------------------------------------------------

@tool
def calculate_yoy_growth_tool(current_val: float, prior_val: float, metric_name: str = "Metric") -> str:
    """Calculates exact Year-over-Year (YoY) percentage growth given current and prior period numerical values."""
    res = calculate_yoy_growth(current_val, prior_val, metric_name)
    return str(res)

@tool
def calculate_margin_tool(numerator: float, total_revenue: float, margin_type: str = "Operating Margin") -> str:
    """Calculates exact percentage margins (e.g. Gross Margin, Operating Margin, Net Margin) given numerator and revenue."""
    res = calculate_margin(numerator, total_revenue, margin_type)
    return str(res)

@tool
def calculate_pe_ratio_tool(stock_price: float, diluted_eps: float) -> str:
    """Calculates Price-to-Earnings (P/E) ratio given current stock price and diluted earnings per share."""
    res = calculate_pe_ratio(stock_price, diluted_eps)
    return str(res)

@tool
def calculate_debt_to_equity_tool(total_debt: float, total_equity: float) -> str:
    """Calculates Debt-to-Equity leverage ratio given total debt and shareholders equity."""
    res = calculate_debt_to_equity(total_debt, total_equity)
    return str(res)

@tool
def calculate_efficiency_ratio_tool(non_interest_expenses: float, total_net_revenue: float) -> str:
    """Calculates Banking Efficiency Ratio given total non-interest expenses and total net revenues."""
    res = calculate_efficiency_ratio(non_interest_expenses, total_net_revenue)
    return str(res)
