from __future__ import annotations
import json
from functools import partial
from pathlib import Path
from typing import Union
from music21 import converter, stream
from parsing.score_reader import (
    load_musicxml,
    noteIterator,
    write_score_to_results,
)
from writing.chord_writer import chordWriter

PathLike = Union[str, Path]

BIBLE_PATH = Path(__file__).resolve().parent / "writing" / "data" / "gemBible.json"
PRIMARY_STYLE = "GenericChromatic"
FALLBACK_STYLE = "Generic"


def harmonize(file_path: str, algorithm: dict) -> None:
    pass

#json.load 
def main() -> None:
    source_file = Path("../testFiles/chuWithChords.musicxml")
    with open(BIBLE_PATH, "r") as bible_file:
        bible_data = json.load(bible_file)
    style_bible = bible_data.get(PRIMARY_STYLE)

    test_score = load_musicxml(source_file)
    modified = noteIterator(test_score, modifier=partial(chordWriter, bible=style_bible))
    output_path = write_score_to_results(modified, source_file)
    print(f"Modified MusicXML written to {output_path}")


if __name__ == "__main__":
    main()