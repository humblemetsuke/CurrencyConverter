from pathlib import Path
from constants import FLAKE8_REPORTS_DIR


def get_latest_flake8_report() -> Path | None:

    files = list(FLAKE8_REPORTS_DIR.glob("flake8_report_*.txt"))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

