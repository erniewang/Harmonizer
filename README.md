# Jazzsolify

**Convert a single-line jazz melody (with chord symbols) into a harmonized sax-section soli in MusicXML.**

### Preview: Lester Young — “Lady Be Good”
- Audio: https://mega.nz/file/noZX2QAJ#Mb56spLucwrvacseJnkZxjiTl1-H4RilTWnqMiB5m_g
- Sheet Music: https://musescore.com/user/41744844/scores/30067142

## Install

Download the Zip file and unzip on your computer


```bash
pip install .
```

## Usage

```bash
jazzsolify <input> [style] [--debugging] [--replace]
```

- `input` — path to a `.xml`/`.musicxml` file, or a bare name found in `test_input/`
- `style` — voicing style (defaults to `Generic`)

Output is written to `output/<input>_modified.musicxml`.

## The Bible

Voicings live in `bible.json` — edit it to customize or add your own styles.
