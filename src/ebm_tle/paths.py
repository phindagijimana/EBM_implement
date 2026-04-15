from pathlib import Path

# src/ebm_tle/paths.py -> repo root is parents[2]
ROOT = Path(__file__).resolve().parents[2]
VENV_PY = ROOT / ".venv" / "bin" / "python"
RUN_DIR = ROOT / ".ebm" / "run"
LOG_DIR = ROOT / ".ebm" / "logs"
PID_FILE = RUN_DIR / "pid"
LOG_FILE = LOG_DIR / "fit.log"
