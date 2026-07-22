from __future__ import annotations
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Union
from tqdm import tqdm
from music21 import converter, note, stream, harmony, chord
import logging
#somehow this was not added 
PathLike = Union[str, Path]


from ..paths import resolve_output_dir

VALID_EXTENSIONS = (".musicxml", ".xml")

# Dev fallback when running from the Harmonizer project tree.
_DEV_TEST_INPUT_DIR = Path(__file__).resolve().parents[2] / "test_input"


def _candidate_paths(path: PathLike) -> Iterator[Path]:
    """Yield possible file locations for a user-supplied input.

    Supports:
    - absolute or relative paths to a .xml/.musicxml file anywhere
    - a path/name without an extension (we try .musicxml then .xml)
    - a bare filename that lives in the project's test_input/ folder
    """
    raw = Path(path).expanduser()
    has_ext = raw.suffix.lower() in VALID_EXTENSIONS

    # 1) As given, relative to the current working directory.
    if has_ext:
        yield raw
    else:
        for ext in VALID_EXTENSIONS:
            yield raw.with_suffix(ext)

    # 2) Fallback: look in cwd/test_input/, then the dev project's test_input/.
    name = raw.name
    test_input_dirs = [Path.cwd() / "test_input", _DEV_TEST_INPUT_DIR]
    for test_input_dir in test_input_dirs:
        if has_ext:
            yield test_input_dir / name
        else:
            for ext in VALID_EXTENSIONS:
                yield (test_input_dir / name).with_suffix(ext)


def load_musicxml(path: PathLike) -> stream.Score:
    logging.debug(f"trying to resolve {path}")
    for candidate in _candidate_paths(path):
        resolved = candidate.expanduser().resolve()
        logging.debug(f"checking candidate {resolved}")
        if resolved.is_file():
            score = converter.parse(str(resolved))
            return score
    raise FileNotFoundError(
        f"MusicXML file not found for '{path}'. Provide a path to a "
        f".xml/.musicxml file, or place it in ./test_input/."
    )


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
        results_dir = resolve_output_dir()
    else:
        results_dir = Path(output_folder)
    results_dir.mkdir(parents=True, exist_ok=True)

    destination = results_dir / f"{Path(source_path).stem}_modified.musicxml"
    #print("DEBUG: destination", destination)
    score.write("musicxml", fp=str(destination))
    return destination
