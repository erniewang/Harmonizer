from __future__ import annotations
import warnings
import logging

#warnings can come from imports as well so have them before importing everything else
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 .* doesn't match a supported version.*",
    category=Warning,
    module=r"requests.*",
)

import json
from pathlib import Path
from functools import partial
from .parsing.score_reader import (
    load_musicxml,
    noteIterator,
    write_score_to_results,
)
from .writing.chord_writer import chordWriter

#json.load 
#       pip install pipreqs
#CLI stuff
import typer
app = typer.Typer()


@app.command()
def harmonize(
    input: str,
    style: str,
    debugging: bool = False,
    replace: bool = typer.Option(False, "--replace", is_flag=True),
):
    """Harmonize a MusicXML solo into a sax soli."""
    # Configure logging based on debugging flag
    logging.basicConfig(
        level=logging.DEBUG if debugging else logging.INFO,
        format="%(levelname)s:%(name)s:%(message)s",
    )
    input = input + ".musicxml"
    # Load bible.json relative to this file so it works as a package
    bible_path = Path(__file__).resolve().parent / "writing" / "data" / "bible.json"
    with bible_path.open("r") as bible_file:
        bible_data = json.load(bible_file)

    style_bible = bible_data.get(style)
    if not style_bible:
        raise Exception("style does not exist. find a style in the bible or create your own style.")

    test_score = load_musicxml(input)
    modified = noteIterator(
        test_score,
        modifier=partial(chordWriter, bible=style_bible),
        replace_existing_chords=replace,
    )
    output_path = write_score_to_results(modified, input)
    logging.info(f"Done: modified MusicXML written to {output_path}")


def main():
    """Entry point for the console script."""
    app()


if __name__ == "__main__":
    main()