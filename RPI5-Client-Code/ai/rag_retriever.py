"""
RAG Retriever — retrieves relevant tool definitions for a given query.
Uses simple keyword matching for the demo; would use embeddings in production.
"""
import json
import os
from logger import logger

TOOLS_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "tools.json")


def load_tools():
    try:
        with open(TOOLS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Could not load tools.json: {e}")
        return []


def retrieve_tool(query: str) -> dict:
    """Find the most relevant tool for a natural language query."""
    tools = load_tools()
    query_lower = query.lower()

    best_match = None
    best_score = 0

    for tool in tools:
        content = tool.get("content", "").lower()
        tool_name = tool.get("tool", "").lower()

        # Simple keyword overlap score
        score = 0
        for word in query_lower.split():
            if word in content or word in tool_name:
                score += 1

        if score > best_score:
            best_score = score
            best_match = tool

    if best_match:
        logger.info(f"RAG match for '{query[:40]}': {best_match['tool']} (score={best_score})")
    else:
        logger.info(f"No RAG match for '{query[:40]}'")

    return best_match or {}
