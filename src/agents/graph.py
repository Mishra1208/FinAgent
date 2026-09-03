from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.schemas.financial_state import AgentState
from src.agents.nodes import (
    supervisor_node,
    quant_analyst_node,
    risk_compliance_node,
    verifier_node
)

def create_financial_agent_graph():
    """
    Compiles the Multi-Agent Financial Intelligence StateGraph.
    Flow: START -> supervisor -> quant_analyst -> risk_compliance -> verifier -> END
    """
    workflow = StateGraph(AgentState)

    # 1. Add Agent Nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("quant_analyst", quant_analyst_node)
    workflow.add_node("risk_compliance", risk_compliance_node)
    workflow.add_node("verifier", verifier_node)

    # 2. Add Deterministic Workflow Edges
    workflow.add_edge(START, "supervisor")
    workflow.add_edge("supervisor", "quant_analyst")
    workflow.add_edge("quant_analyst", "risk_compliance")
    workflow.add_edge("risk_compliance", "verifier")
    workflow.add_edge("verifier", END)

    # 3. Compile Graph with Memory Checkpointer
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app

# Singleton compiled application
_COMPILED_APP = None

def get_agent_app():
    """Returns the singleton compiled LangGraph multi-agent application."""
    global _COMPILED_APP
    if _COMPILED_APP is None:
        _COMPILED_APP = create_financial_agent_graph()
    return _COMPILED_APP

def run_financial_analysis(
    query: str,
    ticker: Optional[str] = None,
    fiscal_year: str = "2024",
    thread_id: str = "default_session"
) -> Dict[str, Any]:
    """
    Entrypoint to invoke the complete Multi-Agent analysis workflow.
    """
    app = get_agent_app()
    initial_state = AgentState(
        query=query,
        ticker=ticker or "AAPL",
        fiscal_year=fiscal_year
    )
    
    config = {"configurable": {"thread_id": thread_id}}
    result_state = app.invoke(initial_state, config=config)
    return result_state
