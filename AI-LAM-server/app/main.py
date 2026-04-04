"""
AI-LAM-Server — FastAPI microservice that converts natural-language
hardware descriptions into validated JSON commands using
Qwen2.5-3B Q4 + LangChain + LangGraph.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import LAM_PORT
from app.models.schemas import (
    ProcessRequest,
    ProcessResponse,
    HardwareCommand,
    HealthResponse,
)
from app.services.llm import load_llm, get_llm
from app.services.rag import load_tools
from app.agent.graph import agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("lam-server")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────
    logger.info("AI-LAM-Server starting up …")
    load_tools()
    try:
        load_llm()
    except FileNotFoundError as exc:
        logger.error(str(exc))
        logger.error("Server will start but /process will fail until the model is available.")
    yield
    # ── Shutdown ─────────────────────────────────────
    logger.info("AI-LAM-Server shutting down.")


app = FastAPI(
    title="AI-LAM-Server",
    description="LLM-powered hardware action model for IoT Copilot",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Endpoints ───────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", model_loaded=get_llm() is not None)


@app.post("/process", response_model=ProcessResponse)
async def process(req: ProcessRequest):
    """
    Main endpoint: takes a natural-language description,
    runs the LangGraph agent, returns validated hardware commands.
    """
    llm = get_llm()
    if llm is None:
        return ProcessResponse(
            is_safe=False,
            message="LLM model is not loaded. Place the GGUF file in models/ and restart.",
            commands=[],
            reasoning="",
        )

    # Run the LangGraph agent
    initial_state = {
        "user_input": req.description,
        "device_context": req.device_context or {},
        "retries": 0,
    }

    result = agent.invoke(initial_state)

    # Build response
    error = result.get("error", "")
    commands_raw = result.get("commands", [])
    is_safe = result.get("is_safe", False)
    validation_msg = result.get("validation_message", "")
    reasoning = result.get("reasoning", "")

    if error and not commands_raw:
        return ProcessResponse(
            is_safe=False,
            message=f"Agent error: {error}",
            commands=[],
            reasoning=reasoning,
        )

    commands = [
        HardwareCommand(
            pin=cmd["pin"],
            action=cmd["action"],
            angle=cmd.get("angle"),
        )
        for cmd in commands_raw
    ]

    return ProcessResponse(
        is_safe=is_safe,
        message=validation_msg or ("Safe to execute" if is_safe else "Validation failed"),
        commands=commands,
        reasoning=reasoning,
    )


# ─── Run directly ───────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=LAM_PORT, reload=False)
