from __future__ import annotations
from music21 import chord, harmony, note
from typing import Any, Mapping

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
def chordWriter(
    root_note: note.Note,
    currChord: harmony.ChordSymbol,
    bible: Mapping[str, Any],
) -> chord.Chord:
    #sanity checks 

    chord_data = None
    note_octave = root_note.octave

    #get the interval in of the note in relation to the chord. also root is a pitch class for some reason
    difference = abs(root_note.pitch.midi - currChord.root().midi) % 12
    chord_figure = extractFigure(currChord.figure)

    try:
        chord_dict = bible.get(chordRouter[chord_figure])
        chord_data = chord_dict.get(str(difference))
    except KeyError:
        pass
    except AttributeError:
        print(f"No Data for {root_note} for {currChord.figure}") 
        return
        # do fallback style here

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