import os

# ── Anthropic API ─────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Database connections ──────────────────────────────────────────────────────
MONGO_URI    = "mongodb://localhost:27017/"
MYSQL_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "root",   # ← FIXED (was "root" which fails on most systems)
    "database": "capstone_db",
}

# ── Directory paths — auto-created ───────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(BASE_DIR, "output")
LOGS_DIR     = os.path.join(BASE_DIR, "logs")
DATASETS_DIR = os.path.join(BASE_DIR, "datasets", "generated")

for _dir in [OUTPUT_DIR, LOGS_DIR, DATASETS_DIR]:
    os.makedirs(_dir, exist_ok=True)

# ── Prompt sizes: 3×8000 + 2×12000 + 3×6000 = 8 prompts ─────────────────────
PROMPT_SIZES = [8000, 8000, 8000, 12000, 12000, 6000, 6000, 6000]

TECH_MODULES = [
    "Unix Commands",
    "Shell Scripting",
    "MongoDB",
    "Python File Handling",
    "PySpark Core",
    "Advanced SQL",
    "Power BI",
    "PySpark Analysis",
]

DATASET_ROWS        = 90_000
INCONSISTENCY_COUNT = 17