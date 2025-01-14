import os
import sys
from music21 import converter, note, chord, harmony, pitch

def fileSecurity(file_path):
    score = converter.parse(file_path)
    if len(score.parts) > 1:
        return False
    return True

if __name__ == "__main__":
    folder_name = "h_test"
    song_name = "Ko_Ko"
    test_file_path = "../unpreparedMusic.musicxml"
    file_path = f"./{folder_name}/{song_name}.musicxml"
    print(fileSecurity(test_file_path))