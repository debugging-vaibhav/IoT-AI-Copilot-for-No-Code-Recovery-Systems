"""
Singleton loader for the Qwen2.5-3B Q4 GGUF model via llama-cpp-python + LangChain.
"""
from __future__ import annotations

import logging
from pathlib import Path

from langchain_community.llms import LlamaCpp
from app.config import (
    MODEL_PATH,
    MODEL_N_CTX,
    MODEL_N_GPU,
    MODEL_TEMPERATURE,
    MODEL_MAX_TOKENS,
)

logger = logging.getLogger("lam-server")

_llm_instance: LlamaCpp | None = None


def load_llm() -> LlamaCpp:
    """Load the GGUF model. Returns a cached singleton on subsequent calls."""
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    model_file = Path(MODEL_PATH)
    if not model_file.exists():
        raise FileNotFoundError(
            f"GGUF model not found at {MODEL_PATH}. "
            "Download qwen2.5-3b-instruct-q4_k_m.gguf and place it in AI-LAM-server/models/"
        )

    logger.info("Loading GGUF model from %s …", MODEL_PATH)
    _llm_instance = LlamaCpp(
        model_path=str(model_file),
        n_ctx=MODEL_N_CTX,
        n_gpu_layers=MODEL_N_GPU,
        temperature=MODEL_TEMPERATURE,
        max_tokens=MODEL_MAX_TOKENS,
        verbose=False,
    )
    logger.info("Model loaded successfully.")
    return _llm_instance


def get_llm() -> LlamaCpp | None:
    """Return the current LLM instance (None if not yet loaded)."""
    return _llm_instance
