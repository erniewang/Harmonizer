"""CLI entrypoint for Harmonizer 2025.
For now this is a tiny wrapper that just tries to load the given
MusicXML file with music21 and prints a short summary.
"""
from __future__ import annotations
import argparse #writing CLI commands
from pathlib import Path
from main import load_musicxml #import relative module (from a diff file in the same folder)
import os 
print("current directory",os.getcwd())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser( prog="harmonizer", 
    description="algorithmically writes musicl voicings given a melody and a harmony",)
    parser.add_argument("musicxml", type=str, help="Path to a MusicXML file",)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    xml_path = Path(args.musicxml).expanduser()

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
