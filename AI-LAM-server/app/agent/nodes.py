"""
LangGraph node functions — each takes the current AgentState,
does one piece of work, and returns a partial state update.
"""
from __future__ import annotations

import json
import logging
import re

from app.config import SAFE_PINS, DEFAULT_PIN
from app.services.rag import retrieve_tools
from app.services.llm import get_llm
from app.services.validator import validate_commands
from app.agent.state import AgentState

logger = logging.getLogger("lam-server")

# ── System prompt injected before every LLM call ────────────────────────
SYSTEM_PROMPT = """\
You are a hardware control agent for a Raspberry Pi 5 robotics system.
Your job is to convert the user's natural-language instruction into one or more structured JSON commands.

Available actions:
- "on"             : Set a GPIO pin HIGH (turn on a device).
- "off"            : Set a GPIO pin LOW (turn off a device).
- "servo_control"  : Move a servo motor. Requires extra field "angle" (0-180).
- "sensor_stream"  : Start continuous sensor reading on a pin.
- "schema_delete"  : Stop control on a pin and free the resource.

Safe GPIO BCM pins: 4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
Default pin (if the user does not specify): 17

Constraints:
- Servo angle must be between 0 and 180 degrees.
- Only use pins from the safe list above.

You MUST respond with ONLY a JSON object — no extra text, no markdown fences.
Use this exact format:
{"commands": [{"pin": <int>, "action": "<string>", "angle": <number or null>}], "reasoning": "<brief explanation>"}
"""


def retrieve_context(state: AgentState) -> dict:
    """Node 1 — RAG: fetch relevant tool descriptions."""
    user_input = state["user_input"]
    tools_text = retrieve_tools(user_input)
    logger.debug("RAG retrieved:\n%s", tools_text)
    return {"retrieved_tools": tools_text}


def reason(state: AgentState) -> dict:
    """Node 2 — call the LLM to produce a JSON command."""
    llm = get_llm()
    if llm is None:
        return {"error": "LLM not loaded"}

    tools_text = state.get("retrieved_tools", "")
    user_input = state["user_input"]
    retries = state.get("retries", 0)

    # On retry, add a stronger nudge
    retry_hint = ""
    if retries > 0:
        prev_error = state.get("error", "")
        retry_hint = (
            f"\n\nYour previous response could not be parsed: {prev_error}\n"
            "Respond with ONLY a single valid JSON object, nothing else."
        )

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Available tool reference:\n{tools_text}\n\n"
        f"User instruction: {user_input}{retry_hint}\n\n"
        f"JSON response:"
    )

    raw = llm.invoke(prompt)
    logger.info("LLM raw output: %s", raw)
    return {"llm_output": raw}


def _try_parse(text: str) -> dict | None:
    """Attempt json.loads; return dict on success, None on failure."""
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except (json.JSONDecodeError, ValueError):
        return None


def _extract_json(text: str) -> dict | None:
    """
    Robust JSON extraction that handles the common LLM quirk of
    placing "reasoning" outside the first JSON brace, e.g.:
        {"commands": [...]}, "reasoning": "..."}
    Strategy:
      1. Try parsing the whole text as JSON.
      2. Fix the split-brace pattern by re-wrapping.
      3. Fall back to bracket-matching for the first valid object.
    """
    # ── Strategy 1: full text is valid JSON ──
    obj = _try_parse(text)
    if obj is not None:
        return obj

    # ── Strategy 2: fix  {"commands":[...]}, "reasoning":"..."} ──
    # The model closes the object after commands, then appends reasoning
    # outside.  We re-wrap: find the first ]} then capture everything
    # up to the final }.
    fix_match = re.search(
        r'(\{"commands"\s*:\s*\[.*?\])\s*\}\s*,\s*("reasoning"\s*:\s*".*?")\s*\}',
        text, re.DOTALL,
    )
    if fix_match:
        fixed = f"{fix_match.group(1)}, {fix_match.group(2)}}}"
        obj = _try_parse(fixed)
        if obj is not None:
            return obj

    # ── Strategy 3: bracket-match the first complete {...} ──
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == "\\":
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                obj = _try_parse(text[start : i + 1])
                if obj is not None:
                    return obj
                break  # matched braces but invalid JSON — give up
    return None


def _extract_angle_from_text(text: str) -> float | None:
    """
    Fallback: pull a numeric angle from the user's original instruction.
    Looks for patterns like '90 degrees', 'angle 45', 'to 0'.
    """
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:degree|deg|°)', text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    m = re.search(r'angle\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    m = re.search(r'to\s+(\d+(?:\.\d+)?)\b', text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    return None


def parse_output(state: AgentState) -> dict:
    """Node 3 — extract JSON commands from the LLM's text output."""
    raw = state.get("llm_output", "")
    retries = state.get("retries", 0)
    user_input = state.get("user_input", "")

    # Strip markdown fences if present
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()

    data = _extract_json(cleaned)
    if data is None:
        logger.warning("Could not extract JSON from: %s", cleaned[:300])
        return {
            "error": f"No valid JSON object found in LLM output: {raw[:200]}",
            "commands": [],
            "reasoning": "",
            "retries": retries + 1,
        }

    # Extract commands list
    commands = data.get("commands", [])
    if isinstance(data, dict) and "pin" in data and "action" in data and "commands" not in data:
        # LLM returned a single command without wrapping in "commands"
        commands = [data]

    if not commands:
        return {
            "error": "LLM returned empty commands list",
            "commands": [],
            "reasoning": data.get("reasoning", ""),
            "retries": retries + 1,
        }

    # Normalise each command
    for cmd in commands:
        cmd.setdefault("angle", None)
        cmd["action"] = cmd["action"].lower().strip()
        if "pin" not in cmd:
            cmd["pin"] = DEFAULT_PIN

        # Fix: if servo_control but angle is missing/null, try to extract from user text
        if cmd["action"] == "servo_control" and cmd.get("angle") is None:
            extracted = _extract_angle_from_text(user_input)
            if extracted is not None:
                cmd["angle"] = extracted
                logger.info("Recovered angle %.1f from user input text", extracted)

    reasoning = data.get("reasoning", "")
    return {"commands": commands, "reasoning": reasoning, "error": ""}


def validate(state: AgentState) -> dict:
    """Node 4 — validate every command against hardware constraints."""
    commands = state.get("commands", [])
    is_safe, message = validate_commands(commands)
    return {"is_safe": is_safe, "validation_message": message}
