from music21 import note, chord


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
