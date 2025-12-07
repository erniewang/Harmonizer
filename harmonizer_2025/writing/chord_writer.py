from __future__ import annotations
import builtins
from music21 import chord, harmony, note
from typing import Any, Mapping
from config import SHOW_DEBUG_MESSAGES

_PRINT_LIMIT = 50
_print_count = 0
_SUPPRESSION_NOTICE = (
    "[chord_writer] Additional log output suppressed to keep the console readable."
)


def _limited_print(*args: Any, **kwargs: Any) -> None:
    """Prevent runaway console spam from this module."""
    global _print_count
    if _print_count < _PRINT_LIMIT:
        builtins.print(*args, **kwargs)
        _print_count += 1
        if _print_count == _PRINT_LIMIT:
            builtins.print(_SUPPRESSION_NOTICE)


print = _limited_print


chordRouter = {
  "": "maj7",
  "+": "maj7",
  "6": "maj7",
  "add2": "maj7",
  "pedal": "dom7",
  "power": "maj7",
  "/E": "maj7",
  "M7": "maj7",
  "M9": "maj7",
  "Maj7": "maj7",
  "maj7": "maj7",
  "maj9": "maj7",
  "Maj9": "maj7",
  "m": "min7",
  "m7": "min7",
  "m7b5": "min7",
  "mM7": "min7",
  "m6": "min6",
  "m9": "min7",
  "m11": "min7",
  "m13": "min7",
  "m7/E-": "min7",
  "minor6": "min6",
  "ø7" : "dim7",
  "dim": "dim7",
  "dim7": "dim7",
  "N6": "maj7",
  "7 add b9" : "alt7",
  "It+6": "alt7",
  "Fr+6": "alt7",
  "Gr+6": "alt7",
  "tristan": "",
  "italian": "",
  "french": "",
  "german": "",
  "7": "dom7",
  "9": "dom7",
  "11": "dom7",
  "13": "dom7",
  "Maj11": "dom7",
  "Maj13": "dom7",
  "7+": "alt7",
  "7omit3": "dom7"
}

#attrs = [attr for attr in dir(note) if not attr.startswith('_')]
# if i have chordRouter loaded in here. will be it open the whole duration of the program?
def _debug(message: str) -> None:
    if SHOW_DEBUG_MESSAGES:
        print(message)


def chordWriter(
    root_note: note.Note,
    currChord: harmony.ChordSymbol,
    bible: Mapping[str, Any],
) -> chord.Chord:
    _debug(
        f"Harmonizing note {root_note!s} "
        f"with chord {currChord.figure if currChord else 'None'}"
    )
    if not currChord:
        _debug("No existing chord found")
        return

    chord_data = None
    note_octave = root_note.octave

    difference = abs(root_note.pitch.midi - currChord.root().midi) % 12
    chord_figure = extractFigure(currChord.figure)

    try:
        chord_dict = bible.get(chordRouter[chord_figure])
    except KeyError:
        print(f"chord {currChord.figure} does not exist in the router")
        return
    except AttributeError:
        try:
            print(f"{chordRouter[chord_figure]} does not exist in this version of the bible")
        except KeyError:
            print(f"{chord_figure} does not exist in the router nor the bible")
        return
    except Exception as e:
        # Code to handle the exception
        print(f"An unknown error occurred while trying to get the voiciing list {e}")
        return

    try:
        chord_data = chord_dict.get(str(difference))
    except KeyError:
        print(f"voicing non-existent for {root_note} and {currChord.figure}")
        return
    except AttributeError:
        print(f"voicing non-existent for {root_note} and {currChord.figure}")
        return
    except Exception as e:
        # Code to handle the exception
        print(f"An unknown error occurred while trying to get the exact voicing")
        return
    if chord_data == []:
        print(f"voicing for {root_note} and {currChord.figure} is unfinished")
        return

    #create a note with the same properties as the root
    rootAsNote = note.Note(str(currChord.root()))
    rootAsNote.duration.quarterLength = root_note.duration.quarterLength
    rootAsNote.octave = note_octave

    chord_data = [rootAsNote.transpose(distance) for distance in chord_data]
    chord_data[0] = root_note

    
    lead_note = chord_data[0]
    for i in range(1, len(chord_data)):
        chord_note = chord_data[i]
        while chord_note.pitch.midi >= lead_note.pitch.midi:
            chord_note = chord_note.transpose(-12)
        chord_data[i] = chord_note
    return chord.Chord(chord_data)


def extractFigure(figure: str):
    if "#" in figure or "-" in figure:
        return figure[2:]
    else:
        return figure[1:]

def correctOctaves():
    return