"""LangGraph agent state definition."""
from __future__ import annotations
from typing import TypedDict


class AgentState(TypedDict, total=False):
    user_input: str               # original natural-language description
    device_context: dict          # optional current device state
    retrieved_tools: str          # RAG results formatted as text
    llm_output: str               # raw text returned by the LLM
    commands: list[dict]          # parsed command dicts
    is_safe: bool                 # validation result
    validation_message: str       # validation reason string
    reasoning: str                # LLM's reasoning / explanation
    error: str                    # error message if a step fails
    retries: int                  # number of parse retries attempted
