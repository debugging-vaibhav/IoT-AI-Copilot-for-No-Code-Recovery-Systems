"""
Singleton loader for Qwen2.5-1.5B-Instruct via HuggingFace Transformers + LangChain.
"""
from __future__ import annotations

import logging

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline

from app.config import (
    MODEL_ID,
    MODEL_TEMPERATURE,
    MODEL_MAX_TOKENS,
)

logger = logging.getLogger("lam-server")

_llm_instance: HuggingFacePipeline | None = None


def load_llm() -> HuggingFacePipeline:
    """Download (or load cached) model from HuggingFace Hub. Returns a cached singleton."""
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    logger.info("Loading model %s from HuggingFace Hub …", MODEL_ID)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MODEL_MAX_TOKENS,
        temperature=MODEL_TEMPERATURE,
        do_sample=True,
        return_full_text=False,
    )

    _llm_instance = HuggingFacePipeline(pipeline=pipe)
    logger.info("Model %s loaded successfully.", MODEL_ID)
    return _llm_instance


def get_llm() -> HuggingFacePipeline | None:
    """Return the current LLM instance (None if not yet loaded)."""
    return _llm_instance
