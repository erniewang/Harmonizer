from music21 import note, chord, harmony

def split(chord_f):
    start = None
    for i in range(len(chord_f) - 1, -1, -1):
        if chord_f[i] in "ABCDEFG#-":
            start = i + 1
            break
    return [chord_f[:start]] + [chord_f[start:]]

def upgrade_chord(chord):
    """
    Upgrades the given chord to a more complex chord type.
    Example: dim -> dim7, m7 -> m9
    """
    #print("original: ", chord.figure)
    chord_figure = split(chord.figure)

    # Map to upgrade chord types
    chord_upgrade_map = {
        "dim": "dim7",
        "aug": "aug7",
        #"": "maj7", #this fucks up everythin
        "m": "m7",  # Minor chords to minor 7th
        'ø7': "dim7",
        "6" : "maj7 add 6"
    }

    # Upgrade the chord based on the map
    for key, upgrade in chord_upgrade_map.items():
        if key == chord_figure[1]:
            answer = harmony.ChordSymbol(chord_figure[0] + chord_figure[1].replace(key, upgrade))
            print("Upgraded: ", answer )
            return answer

    # If no specific type found, assume it's a major chord
    return (
        harmony.ChordSymbol(chord_figure[0] + "maj7")
        if "7" not in chord_figure[1]
        else harmony.ChordSymbol(chord.figure)
    )



def verify(NOTE, CHORD):
    for i in range(len(CHORD.pitches)):
        chord_note = CHORD.pitches[i]
        if chord_note.name == NOTE.name:
            return i
    return -1

# such a bullshit thing to happen. 0 being treated as false

def chord_tone(NOTE, CHORD, number_notes=4):

    # print(f"fitting {NOTE.name} into {CHORD.figure}")

    note_index = verify(NOTE, CHORD)

    if note_index == -1:
        return None
    answer_chord = CHORD.pitches[note_index + 1 :] + CHORD.pitches[: note_index + 1]
    return answer_chord[-4:]

def skip_note(note):
    return note

def diminished_chord(note, number_notes):
    answer_chord = [note]
    for i in range(number_notes - 1):
        note = note.transpose("-m3")
        answer_chord.append(note)
    return answer_chord
