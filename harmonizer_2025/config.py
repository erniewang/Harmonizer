"""Central configuration for Harmonizer 2025."""
from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent

# core behavior toggles
REPLACE_EXISTING_CHORDS = True

# styling defaults
SELECTED_STYLE = "Stan Kenton"

# logging and diagnostics
SHOW_DEBUG_MESSAGES = False

# filesystem locations
INPUT_FOLDER = PROJECT_ROOT / "testFiles"
OUTPUT_FOLDER = PROJECT_ROOT / "testResults"

BIBLE_FOLDER = PACKAGE_ROOT / "writing" / "data"
BIBLE_PATH = BIBLE_FOLDER / "gptBible.json"


__all__ = [
    "BIBLE_FOLDER",
    "BIBLE_PATH",
    "INPUT_FOLDER",
    "OUTPUT_FOLDER",
    "PACKAGE_ROOT",
    "PROJECT_ROOT",
    "REPLACE_EXISTING_CHORDS",
    "SELECTED_STYLE",
    "SHOW_DEBUG_MESSAGES",
]