# AI-LAM-Server Implementation Plan

## Overview

The AI-LAM-server is a standalone FastAPI microservice that replaces the current keyword-based `ai_copilot.py` in the backend with a real LLM-powered agent. It uses **Qwen2.5-3B Q4 GGUF** running locally via `llama-cpp-python`, orchestrated through **LangChain + LangGraph** to interpret natural language hardware descriptions and produce structured JSON commands.

---

## Architecture & Data Flow

```
User (React Frontend)
  |
  |  POST /api/describe-robot  { "description": "..." }
  v
Backend (FastAPI :8000)
  |
  |  POST /process  { "description": "...", "context": {...} }
  v
AI-LAM-Server (FastAPI :8100)              <--- THIS SERVICE
  |
  |  1. RAG retrieval (tools.json)
  |  2. LangGraph agent (Qwen2.5-3B Q4)
  |  3. Constraint validation
  |  4. Return structured command(s)
  |
  v
Backend receives validated command(s)
  |
  |  POST /execute  { "pin": 17, "action": "on" }
  v
RPI5 Flask Server (:5000)
  |  execution_engine.py -> schema_validator -> GPIO/PWM/Sensor
  v
Hardware
```

---

## What Currently Exists (to be replaced/augmented)

| Component | Location | Current State |
|---|---|---|
| AI Copilot service | `backend/app/services/ai_copilot.py` | Keyword-based parser, no LLM |
| LAM Engine | `RPI5-Client-Code/ai/lam_engine.py` | GGUF loader stub + keyword fallback |
| RAG Retriever | `RPI5-Client-Code/ai/rag_retriever.py` | Keyword overlap, no embeddings |
| Tools dataset | `RPI5-Client-Code/datasets/tools.json` | 4 tool definitions |
| Backend route | `backend/app/api/routes.py` `/describe-robot` | Calls ai_copilot.parse_description() |

The AI-LAM-server centralizes all AI logic into one service. The backend's `/describe-robot` route will be modified to call this server instead of the local keyword parser.

---

## Tool Definitions & Constraints

From `tools.json` and `schema_validator.py`, the agent can emit these actions:

| Tool / Action | Parameters | Constraints |
|---|---|---|
| `on` (pin_write HIGH) | `pin` (int) | Pin must be in SAFE_PINS: {4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27} |
| `off` (pin_write LOW) | `pin` (int) | Same safe pin constraint |
| `servo_control` | `pin` (int), `angle` (float) | Angle: 0-180. PWM duty: 2 + (angle/18). PWM signal range: ~800-2200us at 50Hz |
| `sensor_stream` | `pin` (int) | Pin must be in SAFE_PINS |
| `schema_delete` | `pin` (int) | Pin must be in SAFE_PINS |

**Safe GPIO BCM Pins:** 4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

---

## Folder Structure

```
AI-LAM-server/
|-- app/
|   |-- __init__.py
|   |-- main.py                 # FastAPI app entry point (:8100)
|   |-- config.py               # Settings (model path, ports, etc.)
|   |-- models/
|   |   |-- __init__.py
|   |   |-- schemas.py          # Pydantic request/response models
|   |-- agent/
|   |   |-- __init__.py
|   |   |-- graph.py            # LangGraph agent definition
|   |   |-- nodes.py            # Graph node functions (retrieve, reason, validate)
|   |   |-- tools.py            # LangChain tool definitions wrapping hardware actions
|   |   |-- state.py            # TypedDict for graph state
|   |-- services/
|   |   |-- __init__.py
|   |   |-- llm.py              # Qwen2.5-3B GGUF loader via llama-cpp-python + LangChain
|   |   |-- rag.py              # RAG retriever for tools.json
|   |   |-- validator.py        # Constraint validation (pins, angles, actions)
|-- datasets/
|   |-- tools.json              # Copy/symlink of tool definitions
|-- models/                     # Directory to place GGUF model file
|   |-- .gitkeep
|-- requirements.txt
|-- plan.md                     # This file
```

---

## Implementation Steps

### Step 1: Project Scaffolding & Dependencies

Create all folders, `__init__.py` files, and `requirements.txt`.

**Key dependencies:**
```
fastapi
uvicorn[standard]
langchain>=0.3
langchain-community
langgraph
llama-cpp-python
pydantic>=2.0
```

### Step 2: Configuration (`app/config.py`)

```python
# Settings
MODEL_PATH      = env("MODEL_PATH", "models/qwen2.5-3b-instruct-q4_k_m.gguf")
MODEL_N_CTX     = 2048        # context window
MODEL_N_GPU     = -1          # offload all layers to GPU (-1), 0 = CPU only
TEMPERATURE     = 0.1         # low temp for deterministic tool selection
LAM_PORT        = 8100
TOOLS_PATH      = "datasets/tools.json"
```

### Step 3: Pydantic Schemas (`app/models/schemas.py`)

```python
class ProcessRequest(BaseModel):
    description: str                         # natural language from user
    device_context: dict | None = None       # optional: current pin states, sensor readings

class HardwareCommand(BaseModel):
    pin: int
    action: str                              # on | off | servo_control | sensor_stream | schema_delete
    angle: float | None = None               # required when action == servo_control

class ProcessResponse(BaseModel):
    is_safe: bool
    message: str
    commands: list[HardwareCommand]          # one or more commands
    reasoning: str                           # agent's chain-of-thought summary
```

### Step 4: LLM Loader (`app/services/llm.py`)

- Load Qwen2.5-3B Q4 GGUF using `langchain_community.llms.LlamaCpp`
- Singleton pattern so model loads once at startup
- Configure: n_ctx=2048, temperature=0.1, max_tokens=512, verbose=False

### Step 5: RAG Retriever (`app/services/rag.py`)

- Load `datasets/tools.json` at startup
- For MVP: keyword-overlap scoring (same approach as existing `rag_retriever.py`)
- Returns top-k relevant tool descriptions to inject into the LLM prompt
- Future: swap to sentence-transformer embeddings for better matching

### Step 6: Constraint Validator (`app/services/validator.py`)

Validates the LLM's output before returning to backend:
- Pin is in SAFE_PINS set
- Action is one of the allowed actions
- If servo_control: angle is present and in [0, 180]
- Returns `(is_valid: bool, reason: str)`

### Step 7: LangGraph Agent

This is the core. A **stateful graph** with 4 nodes:

#### State (`app/agent/state.py`)

```python
class AgentState(TypedDict):
    user_input: str                # original description
    device_context: dict           # optional current state
    retrieved_tools: str           # RAG results as formatted text
    llm_output: str                # raw LLM response
    commands: list[dict]           # parsed commands
    validation_result: dict        # {is_safe, message}
    error: str | None              # error if any step fails
```

#### Tools (`app/agent/tools.py`)

Define LangChain `@tool` decorated functions that the LLM can "call":

```python
@tool
def servo_control(pin: int, angle: float) -> str:
    """Move a servo motor to a specific angle. Pin must be a safe GPIO pin. Angle: 0-180."""

@tool
def pin_write(pin: int, value: int) -> str:
    """Set a GPIO pin to HIGH (1) or LOW (0)."""

@tool
def sensor_stream(pin: int) -> str:
    """Start continuous sensor reading on a GPIO pin."""

@tool
def schema_delete(pin: int) -> str:
    """Stop control on a pin and free the resource."""
```

These tools don't execute hardware -- they return structured JSON that the backend forwards to RPi5.

#### Nodes (`app/agent/nodes.py`)

```
retrieve_context(state)   -> adds retrieved_tools to state
reason(state)             -> calls LLM with tools + prompt, adds llm_output
parse_output(state)       -> extracts JSON commands from llm_output
validate(state)           -> validates each command against constraints
```

#### Graph (`app/agent/graph.py`)

```
START -> retrieve_context -> reason -> parse_output -> validate -> END
                                          |
                                     (parse error) -> retry_reason -> parse_output
```

- Max 2 retries if LLM output isn't valid JSON
- On final failure: return `is_safe=False` with error message

### Step 8: FastAPI App (`app/main.py`)

```python
@app.on_event("startup")
async def startup():
    # Load GGUF model (takes a few seconds)
    # Load tools.json

@app.post("/process", response_model=ProcessResponse)
async def process(req: ProcessRequest):
    # Run LangGraph agent
    # Return structured response

@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": bool(llm)}
```

### Step 9: Backend Integration

Modify `backend/app/services/ai_copilot.py` to call the AI-LAM-server:

```python
# OLD: keyword parsing
# NEW: HTTP call to AI-LAM-server
async def parse_description(description: str) -> dict:
    resp = httpx.post("http://localhost:8100/process", json={"description": description})
    return resp.json()
```

Modify `backend/app/api/routes.py` `/describe-robot` to:
1. Call AI-LAM-server `/process`
2. Map response to existing `ValidationResult` schema
3. Return to frontend (no frontend changes needed)

---

## LLM Prompt Strategy

The system prompt injected into Qwen2.5-3B:

```
You are a hardware control agent for a Raspberry Pi 5 robotics system.
Your job is to convert user descriptions into structured JSON commands.

Available actions:
- pin_write: Set a GPIO pin HIGH (action: "on") or LOW (action: "off"). Params: pin, action.
- servo_control: Move a servo motor. Params: pin, action: "servo_control", angle (0-180).
- sensor_stream: Start reading a sensor. Params: pin, action: "sensor_stream".
- schema_delete: Stop and free a pin. Params: pin, action: "schema_delete".

Safe GPIO pins (BCM): 4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

Constraints:
- Servo angle must be 0-180 degrees
- PWM signal range: 800-2200 microseconds (handled automatically from angle)
- Only use pins from the safe list
- Default to pin 17 if user doesn't specify

Respond with ONLY a JSON object:
{
  "commands": [{"pin": <int>, "action": "<str>", "angle": <float|null>}],
  "reasoning": "<brief explanation>"
}
```

The RAG-retrieved tool descriptions are appended to give the model additional context about which tool fits the user's intent.

---

## MVP Scope (What We Build Now)

1. Single-endpoint FastAPI server (`/process` + `/health`)
2. Qwen2.5-3B Q4 GGUF via llama-cpp-python
3. LangGraph agent with 4 nodes (retrieve -> reason -> parse -> validate)
4. Tool definitions matching the 4 tools in tools.json
5. Constraint validation (safe pins, angle range, allowed actions)
6. Backend integration (modify `ai_copilot.py` + `routes.py`)
7. No frontend changes needed (response maps to existing `ValidationResult`)

## What We Skip for MVP

- Embedding-based RAG (use keyword matching)
- Multi-step command sequences (single command per request)
- Conversation memory / chat history
- Authentication between services
- GPU acceleration setup (CPU-only is fine for 3B Q4)
- Unit tests (manual testing via API)

---

## How to Run (After Implementation)

```bash
# 1. Download model
# Place qwen2.5-3b-instruct-q4_k_m.gguf in AI-LAM-server/models/

# 2. Install dependencies
cd AI-LAM-server
pip install -r requirements.txt

# 3. Start AI-LAM-server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8100

# 4. Start backend (separate terminal)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 5. Start frontend (separate terminal)
npm start
```

---

## Execution Order for Implementation

| Step | Task | Files |
|---|---|---|
| 1 | Scaffolding + requirements.txt | All `__init__.py`, `requirements.txt` |
| 2 | Config | `app/config.py` |
| 3 | Schemas | `app/models/schemas.py` |
| 4 | LLM loader | `app/services/llm.py` |
| 5 | RAG retriever | `app/services/rag.py` |
| 6 | Validator | `app/services/validator.py` |
| 7 | Agent state | `app/agent/state.py` |
| 8 | Agent tools | `app/agent/tools.py` |
| 9 | Agent nodes | `app/agent/nodes.py` |
| 10 | Agent graph | `app/agent/graph.py` |
| 11 | FastAPI main | `app/main.py` |
| 12 | Tools dataset | `datasets/tools.json` |
| 13 | Backend integration | `backend/app/services/ai_copilot.py`, `backend/app/api/routes.py` |
