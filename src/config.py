from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = ROOT / "data" / "raw" / "Rotten Tomatoes Movies.csv"
OUT_PATH = ROOT / "data" / "processed" / "clean_dataset.csv"