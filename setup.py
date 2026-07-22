from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from pathlib import Path
import shutil


class BuildPy(build_py):
    """Copy top-level bible.json into the package before building."""

    def run(self):
        dest_dir = Path("jazzsoli/data")
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy("bible.json", dest_dir / "bible.json")
        super().run()


setup(
    name="jazzsolify",
    version="1.0.0",
    description="Harmonize any Jazz solo (with chord changes) into a Jazz Soli.",
    python_requires=">=3.8",
    packages=find_packages(where="."),
    include_package_data=True,
    package_data={
        "jazzsoli": ["data/bible.json"],
    },
    cmdclass={"build_py": BuildPy},
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

