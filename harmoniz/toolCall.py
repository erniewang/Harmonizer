import os
import sys
from music21 import converter, note, chord, harmony, pitch
from chordTones import chord_tone
from diminished import diminished_chord, skip_note
from octave_correction import correct_octave
from rules_tones import dictionary_lookup

# print(harmony.CHORD_TYPES)


def upgrade_chord(chord):
    """
    Upgrades the given chord to a more complex chord type.
    Example: dim -> dim7, m7 -> m9
    """
    chord_figure = chord.figure

    # Map to upgrade chord types
    chord_upgrade_map = {
        "dim": "dim7",  # Diminished chords to diminished 7th
        "aug": "aug7",  # Augmented chords to augmented 7th
        #"": "maj7", this fucks up everythin
        "m": "m7",  # Minor chords to minor 7th
    }

    # Upgrade the chord based on the map
    for key, upgrade in chord_upgrade_map.items():
        if key in chord_figure:
            return harmony.ChordSymbol(chord_figure.replace(key, upgrade))

    # If no specific type found, assume it's a major chord
    return (
        harmony.ChordSymbol(chord_figure + "maj7")
        if "7" not in chord_figure
        else harmony.ChordSymbol(chord_figure)
    )


def iterate(target_note, chord, number_notes=4):
    
    """
    Most importiant function that would need the most changing
    1. (optional) try direct chord tone harmonzation first 
    2. run through the rules json file
    3. return empty or have (optional) one size fits all strategy (in this case diminished)
    """

    note_enharms = pitch.Pitch(target_note.name).getAllCommonEnharmonics() + [pitch.Pitch(target_note.name)]
    note_enharms = [(note.Note(E.name)) for E in note_enharms]

    CHORD = None
    for NOTE in note_enharms:
        CHORD = chord_tone(NOTE, chord)
        if CHORD != None:
            return correct_octave(target_note, CHORD)
    if CHORD == None:
        new_CHORD = dictionary_lookup(target_note, chord, "ernie")
        for NOTE in note_enharms:
            NEWCHORD = chord_tone(NOTE, new_CHORD)
            if NEWCHORD != None:
                return correct_octave(target_note, NEWCHORD)
    return diminished_chord(target_note, 4)


def replace_write(measure, note_element, voicings):
    """
    Replace a note in the measure with a chord based on the provided voicings.
    """
    new_chord = chord.Chord(voicings)
    new_chord.duration = note_element.duration
    measure.replace(note_element, new_chord)


def parse(file_path, name):
    """
    Parses a musicXML file, upgrades chords, and replaces notes with chord voicings.
    """
    NOTE = None
    CHORD = None
    score = converter.parse(file_path)

    for part in score.parts:
        defer_chord = None
        tie_status = ""  # Default status has no tie
        for measure in part.getElementsByClass("Measure"):
            last_tied_note = None

            for element in measure.notes:
                voicings = None

                if isinstance(element, note.Note):
                    NOTE = element

                    # Handle tied notes
                    last_tied_note = None
                    if element.tie:
                        if element.tie.type == "start":
                            tie_status = "Tie start"
                            last_tied_note = element
                        elif element.tie.type == "stop":
                            tie_status = "Tie stop"
                        elif element.tie.type == "continue":
                            tie_status = "Tie continue"
                            last_tied_note = element

                    if defer_chord:
                        voicings = iterate(NOTE, CHORD)
                        CHORD = defer_chord
                        defer_chord = None
                    else:
                        voicings = iterate(NOTE, CHORD)

                    tie_status = tie_status if tie_status != "Tie stop" else ""
                    replace_write(measure, element, voicings)

                elif isinstance(element, chord.Chord):
                    # Handle chords
                    if tie_status in ["Tie start", "Tie continue"]:
                        defer_chord = element if not defer_chord else element
                    else:
                        CHORD = element
                        CHORD = upgrade_chord(CHORD)
                        measure.replace(element, CHORD)

    # Write the modified score to a new file
    try:
        os.remove("results.musicxml")
    except FileNotFoundError:
        pass

    score.write("musicxml", f"results/{name}_Modified.musicxml")


if __name__ == "__main__":

    # Run the parser for testing purposes
    try:
        os.remove("output.txt")
    except FileNotFoundError:
        pass

    folder_name = "h_test"
    song_name = "Ko_Ko"
    file_path = f"./{folder_name}/{song_name}.musicxml"
    parse(file_path, song_name)
