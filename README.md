# Harmonizer 2025

Tiny playground package that works with MusicXML files using `music21`.

## Install (editable for local dev)

```bash
pip install -e .
```

## Usage

Programmatic:

```python
from harmonizer_2025 import load_musicxml

score = load_musicxml("path/to/file.musicxml")
print(score)
```

CLI:

```bash
harmonizer-2025 path/to/file.musicxml
```
