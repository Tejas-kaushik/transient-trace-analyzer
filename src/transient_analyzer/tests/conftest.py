import sys
from pathlib import Path

# Add /src to sys.path so tests can import transient_analyzer without PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
