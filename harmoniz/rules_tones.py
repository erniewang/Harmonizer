from music21 import converter, note, chord, harmony
import json
import os

#otherwise fastapi python shit will never know this is where the file is actually is. so fucking dumb
dir_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(dir_path, 'style_completion.json')

f = open(json_path)
data = json.load(f)
f.close()


def split(chord_f):
    start = None
    for i in range(len(chord_f) - 1, -1, -1):
        if chord_f[i] in "ABCDEFG#-":
            start = i + 1
            break
    return chord_f[start:]


def dictionary_lookup(note, chord, style):

    # figure out the difference between the note and the root of the chord
    note_number = note.pitch.midi

    # grab the corrosponding part
    chord_root_number = chord.bass().midi

    # get the amount of change needed
    difference = (note_number % 12) - (chord_root_number % 12)
    if difference < 0:
        difference += 12

    # chordtone that shit
    new_chord = data[style][split(chord.figure)][difference]
    new_root = chord.bass().transpose(new_chord[0])
    new_chord = new_root.name + str(new_chord[1])
    return harmony.ChordSymbol(new_chord)
