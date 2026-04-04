"""
LangGraph agent — wires the nodes into a stateful graph.

Flow:
  START -> retrieve_context -> reason -> parse_output -+-> validate -> END
                                                       |
                                              (parse error, retries < 2)
                                                       +-> reason  (retry)
"""
from __future__ import annotations

import logging

from langgraph.graph import StateGraph, END

from app.agent.state import AgentState
from app.agent.nodes import retrieve_context, reason, parse_output, validate

logger = logging.getLogger("lam-server")

MAX_RETRIES = 2


def _should_retry(state: AgentState) -> str:
    """Conditional edge after parse_output — retry reasoning or move to validate."""
    error = state.get("error", "")
    retries = state.get("retries", 0)
    commands = state.get("commands", [])

    if commands and not error:
        return "validate"

    if retries < MAX_RETRIES:
        logger.warning("Parse failed (attempt %d/%d): %s — retrying", retries, MAX_RETRIES, error)
        return "reason"

    # Give up — pass through to validate which will report the failure
    logger.error("Parse failed after %d retries: %s", MAX_RETRIES, error)
    return "validate"


def build_graph() -> StateGraph:
    """Construct and compile the LangGraph agent."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("reason", reason)
    graph.add_node("parse_output", parse_output)
    graph.add_node("validate", validate)

    # Edges
    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "reason")
    graph.add_edge("reason", "parse_output")
    graph.add_conditional_edges("parse_output", _should_retry, {
        "validate": "validate",
        "reason": "reason",
    })
    graph.add_edge("validate", END)

    return graph.compile()


# Compiled graph singleton — import and invoke this
agent = build_graph()
