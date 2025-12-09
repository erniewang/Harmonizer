from __future__ import annotations
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Union
from tqdm import tqdm
from music21 import converter, note, stream, harmony, chord
import logging
#somehow this was not added 
PathLike = Union[str, Path]


def load_musicxml(path: PathLike) -> stream.Score:
    logging.debug(f"trying to resolve {path}")
    xml_path = Path(path).expanduser().resolve()
    if not xml_path.is_file():
        # Backward-compatible fallback: try the testFiles directory
        xml_path = Path("input") / path
        xml_path = xml_path.expanduser().resolve()
    if not xml_path.is_file():
        raise FileNotFoundError(f"MusicXML file not found: {xml_path}")
    score = converter.parse(str(xml_path))
    return score


# type is not that simple
#
# checking types to isinstance or equality
def noteIterator(
    score: stream.Score,
    modifier: Callable[[note.Note], chord.Chord] | None = None,
    *,
    replace_existing_chords: bool = True
) -> stream.Score:
    """Iterate through the first part and optionally harmonize notes.

    Parameters
    ----------
    score:
        The parsed `music21.stream.Score`.
    modifier:
        Function that takes a note and current chord symbol and returns a
        replacement chord (or None to leave it unchanged).
    replace_existing_chords:
        When False, existing `chord.Chord` objects are left untouched.
    debug:
        When True, prints simple progress/debug information.
    """

    currentChord = None
    skippedNotes = 0

    for i, measureStream in (enumerate(score.parts[0].iter())):
        logging.debug(f"Measure {i}")
        try:
            if "stream" in str(type(measureStream)):
                # Harmonize if it's a note, otherwise record a new chord
                for mysteryObject in measureStream:
                    if isinstance(mysteryObject, harmony.ChordSymbol):
                        currentChord = mysteryObject
                    else:
                        replacement_object = None
                        if isinstance(mysteryObject, chord.Chord):
                            if not replace_existing_chords:
                                logging.info(
                                    "Object was actually a chord, so it was skipped. "
                                    "Use '--replace' to modify and reharmonize this chord."
                                )
                                continue
                            anchor_note = mysteryObject[-1]
                            replacement_object = (
                                modifier(anchor_note, currentChord) if modifier else None
                            )
                        elif isinstance(mysteryObject, note.Note):
                            replacement_object = (
                                modifier(mysteryObject, currentChord) if modifier else None
                            )
                        if replacement_object is not None:
                            measureStream.replace(mysteryObject, replacement_object)
        except Exception as e:  # pragma: no cover - defensive
            raise RuntimeError(
                "Unresolvable Error Occured, Stopping program. Error shown below \n"
            ) from e
    return score


def write_score_to_results(
    score: stream.Score,
    source_path: PathLike,
    output_folder: Path | None = None,
) -> Path:
    """Write the modified score to a MusicXML file in the results directory."""
    if output_folder is None:
        results_dir = Path(__file__).resolve().parents[2] / "output"
    else:
        results_dir = Path(output_folder)
    results_dir.mkdir(parents=True, exist_ok=True)

    destination = results_dir / f"{Path(source_path).stem}_modified.musicxml"
    #print("DEBUG: destination", destination)
    score.write("musicxml", fp=str(destination))
    return destination
