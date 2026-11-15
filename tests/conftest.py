import sys
from pathlib import Path

# Allow running `pytest tests` from the repo root without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "supervisor"))


def pytest_configure(config):
    config.addinivalue_line("markers", "ver(id): links a test to a VER protocol")
