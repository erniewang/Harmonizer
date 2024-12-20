from music21 import note, chord


def correct_octave(note, voicing):
    note_octave = note.octave

    for i in range(len(voicing)):
        voicing[i].octave = note_octave

    for j in range(len(voicing)):
        if voicing[j].frequency > note.pitch.frequency:
            voicing[j].octave -= 1

    answer = [(str(note.name) + str(note.octave)) for note in voicing]
    # have to construct the chord by itself. changing the octave will not do anything
    return chord.Chord(answer)
