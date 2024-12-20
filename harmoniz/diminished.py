from music21 import note, chord


def skip_note(note):
    return note


def diminished_chord(note, number_notes):
    answer_chord = [note]
    for i in range(number_notes - 1):
        note = note.transpose("-m3")
        answer_chord.append(note)
    return answer_chord
