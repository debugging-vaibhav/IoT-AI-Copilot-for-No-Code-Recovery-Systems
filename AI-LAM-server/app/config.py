import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Model ────────────────────────────────────────────
MODEL_PATH = os.getenv(
    "MODEL_PATH",
    str(BASE_DIR / "models" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"),
)
MODEL_N_CTX = int(os.getenv("MODEL_N_CTX", "2048"))
MODEL_N_GPU = int(os.getenv("MODEL_N_GPU", "0"))  # 0 = CPU-only, -1 = full GPU offload
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
MODEL_MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "512"))

# ── Server ───────────────────────────────────────────
LAM_HOST = os.getenv("LAM_HOST", "0.0.0.0")
LAM_PORT = int(os.getenv("LAM_PORT", "8100"))

# ── Data ─────────────────────────────────────────────
TOOLS_PATH = os.getenv("TOOLS_PATH", str(BASE_DIR / "datasets" / "tools.json"))

# ── Constraints ──────────────────────────────────────
SAFE_PINS = {4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27}
ALLOWED_ACTIONS = {"on", "off", "servo_control", "sensor_stream", "schema_delete"}
SERVO_ANGLE_MIN = 0.0
SERVO_ANGLE_MAX = 180.0
DEFAULT_PIN = 17
