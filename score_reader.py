from __future__ import annotations
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Union
from music21 import converter, note, stream, harmony, chord

PathLike = Union[str, Path]


def load_musicxml(path: PathLike) -> stream.Score:
    xml_path = Path(path).expanduser().resolve()
    if not xml_path.is_file():
        raise FileNotFoundError(f"MusicXML file not found: {xml_path}")
    score = converter.parse(str(xml_path))
    return score

#type is not that simple

#checking types to isinstance or equality
def noteIterator(score: stream.Score, note_filter: Callable[[note.Note], bool] | None = None,
) -> stream.Score:
    museStream = score.parts[0].iter()
    currentChord = None
    for measureStream in score.parts[0].iter():
        if "stream" in str(type(measureStream)):
            for mysteryObject in measureStream:
                if isinstance(mysteryObject, note.Note):
                    measureStream.replace(mysteryObject,chord.Chord([mysteryObject, mysteryObject.transpose(5)]))
                elif isinstance(mysteryObject, harmony.ChordSymbol):
                    currentChord = mysteryObject
    return score


def write_score_to_results(score: stream.Score, source_path: PathLike) -> Path:
    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    source_path = Path(source_path)
    destination = results_dir / f"{source_path.stem}_modified.musicxml"
    score.write("musicxml", fp=str(destination))
    return destination


if __name__ == "__main__":
    source_file = Path("../../testFiles/chuWithChords.musicxml")
    test_score = load_musicxml(source_file)
    modified = noteIterator(test_score)
    output_path = write_score_to_results(modified, source_file)
    print(f"Modified MusicXML written to {output_path}")