from __future__ import annotations
import warnings

#warnings can come from imports as well so have them before importing everything else
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 .* doesn't match a supported version.*",
    category=Warning,
    module=r"requests.*",
)

import builtins
_original_print = builtins.print

def make_debug_print(debug_enabled: bool):
    """Return a print function that only prints when debugging is enabled."""
    def _print(*args, **kwargs):
        if not debug_enabled:
            # debugging flag is False -> silence all prints
            return
        _original_print(*args, **kwargs)
    return _print

import json
from functools import partial
from parsing.score_reader import (
    load_musicxml,
    noteIterator,
    write_score_to_results,
)
from writing.chord_writer import chordWriter

#json.load 

#CLI stuff
import typer
app = typer.Typer()


#python main.py chuWithChords Generic
@app.command()
def harmonize(input: str, style: str, debugging: bool = False):
    # Override global print based on debugging flag
    builtins.print = make_debug_print(debugging)
    input = input + ".musicxml"
    #make in the future it works regardless
    with open("writing/data/bible.json", "r") as bible_file:
        bible_data = json.load(bible_file)

    style_bible = bible_data.get(style)
    if not style_bible:
        raise Exception("style does not exist. find a style in the bible or create your own style")
    test_score = load_musicxml(input)
    modified = noteIterator(test_score, modifier=partial(chordWriter, bible=style_bible))
    output_path = write_score_to_results(modified, input)
    builtins.print = make_debug_print(True)
    print(f"Done: modified MusicXML written to {output_path}")
    
if __name__ == "__main__":
    app()
    #python main.py chuWithChords Generic --debugging