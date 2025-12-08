from __future__ import annotations
import warnings

#warnings can come from imports as well so have them before importing everything else
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 .* doesn't match a supported version.*",
    category=Warning,
    module=r"requests.*",
)

import json
from functools import partial
from config import BIBLE_PATH, INPUT_FOLDER, SELECTED_STYLE, SHEET_MUSIC_NAME
from parsing.score_reader import (
    load_musicxml,
    noteIterator,
    write_score_to_results,
)
from writing.chord_writer import chordWriter


DEFAULT_SOURCE_FILE = INPUT_FOLDER / SHEET_MUSIC_NAME


def harmonize(file_path: str, algorithm: dict) -> None:
    pass

#json.load 
def main() -> None:
    source_file = DEFAULT_SOURCE_FILE
    with open(BIBLE_PATH, "r") as bible_file:
        bible_data = json.load(bible_file)
    style_bible = bible_data.get(SELECTED_STYLE)

    test_score = load_musicxml(source_file)
    modified = noteIterator(test_score, modifier=partial(chordWriter, bible=style_bible))
    output_path = write_score_to_results(modified, source_file)
    print(f"Modified MusicXML written to {output_path}")


if __name__ == "__main__":
    main()