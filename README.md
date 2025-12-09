# Jazzsolify

**Convert a single-line jazz melody (with chord symbols) into a harmonized sax-section soli in MusicXML.**

**Convert a single-line jazz melody (with chord symbols) into a harmonized sax-section soli in MusicXML.**

### Preview: Lester Young — “Lady Be Good”
- Audio: https://mega.nz/file/noZX2QAJ#Mb56spLucwrvacseJnkZxjiTl1-H4RilTWnqMiB5m_g
- Sheet Music: https://musescore.com/user/41744844/scores/30067142

Disclaimer: ~5 minutes of manual cleanup fixed small inconsistencies. The soli writing itself took ~15 minutes (vs. ~2 hours by hand).

## Usage

jazzsolify <input_basename> <style> [--debugging] [--replace]

- **input_basename** — filename without `.musicxml`
- **style** — style name from the voicing bible
- **--debugging** — verbose logging
- **--replace** — re-harmonize existing chords instead of keeping them

Output is written to:

output/<input_basename>_modified.musicxml

## Install (local dev)

python -m pip install -e .

## Customize Voicings (the "bible")

Edit:

jazzsoli/writing/data/bible.json

Add or modify styles, chord families, and voicing rules.

Run with your custom style:

jazzsolify <input_basename> MyStyles.MyGeneric
