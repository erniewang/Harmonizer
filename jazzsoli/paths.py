from __future__ import annotations

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent


def resolve_bible_path() -> Path:
    """Find bible.json: cwd override, dev project root, then bundled default."""
    candidates = [
        Path.cwd() / "bible.json",
        _PACKAGE_DIR.parent / "bible.json",
        _PACKAGE_DIR / "data" / "bible.json",
    ]
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(
        "bible.json not found. Place one in the current directory, "
        f"at the project root, or use the bundled copy in {_PACKAGE_DIR / 'data'}."
    )


def resolve_output_dir() -> Path:
    """Write harmonized scores to output/ in the current working directory."""
    return Path.cwd() / "output"
