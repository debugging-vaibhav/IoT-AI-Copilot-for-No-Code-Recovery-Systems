"""
RAG retriever — loads tools.json and finds the most relevant tool descriptions
for a given user query.  MVP uses keyword-overlap scoring.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from app.config import TOOLS_PATH

logger = logging.getLogger("lam-server")

_tools: list[dict] = []


def load_tools() -> list[dict]:
    """Load tool definitions from datasets/tools.json (cached)."""
    global _tools
    if _tools:
        return _tools

    path = Path(TOOLS_PATH)
    if not path.exists():
        logger.warning("tools.json not found at %s — RAG disabled", TOOLS_PATH)
        return []

    with open(path, encoding="utf-8") as f:
        _tools = json.load(f)

    logger.info("Loaded %d tool definitions from %s", len(_tools), TOOLS_PATH)
    return _tools


def _score(query_tokens: set[str], text: str) -> int:
    """Count how many query tokens appear in the text."""
    text_lower = text.lower()
    return sum(1 for t in query_tokens if t in text_lower)


def retrieve_tools(query: str, top_k: int = 4) -> str:
    """
    Return a formatted string of the most relevant tool descriptions.
    With only 4 tools we just return all of them ranked by relevance.
    """
    tools = load_tools()
    if not tools:
        return "(no tool definitions available)"

    tokens = set(query.lower().split())
    scored = sorted(tools, key=lambda t: _score(tokens, t["content"]), reverse=True)
    ranked = scored[:top_k]

    lines: list[str] = []
    for t in ranked:
        lines.append(f"- {t['tool']}: {t['content']}")
    return "\n".join(lines)
