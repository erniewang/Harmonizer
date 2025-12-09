# A J J J J Jazzsolify

**Convert a single-line jazz melody (with chord symbols) into a harmonized sax-section soli in MusicXML.**

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
