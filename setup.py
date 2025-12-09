from setuptools import setup, find_packages

setup(
    name="jazzsolify",
    version="1.0.0",
    description="Harmonize any Jazz solo (with chord changes) into a Jazz Soli.",
    python_requires=">=3.8",
    packages=find_packages(where="."),
    install_requires=[
        "music21==9.9.1",
        "tqdm==4.67.1",
        "typer==0.20.0",
    ],
    entry_points={
        "console_scripts": [
            "jazzsolify=jazzsoli.main:main",
        ],
    },
)

