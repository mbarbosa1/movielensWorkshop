"""Small safety helpers; students do not need to edit this file."""
import json
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"

class WorkshopError(Exception):
    """An expected setup or checkpoint problem with a readable solution."""

def check(condition, message):
    # Unlike Python's assert keyword, this checkpoint also works with python -O.
    if not condition:
        raise WorkshopError(message)

def read_csv(path, columns):
    check(path.is_file() and path.stat().st_size > 0,
          f"Missing or empty file: {path}. Read README.md > Data setup; run the earlier stage if this is an output file.")
    try:
        frame = pd.read_csv(path)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeError) as exc:
        raise WorkshopError(f"Cannot read {path.name} as UTF-8 CSV. Use the original MovieLens file. {exc}") from exc
    check(set(columns).issubset(frame.columns), f"{path.name} needs columns: {', '.join(columns)}. Check that you selected MovieLens Latest Small.")
    check(not frame.empty, f"{path.name} has headers but no rows. Use the full MovieLens file.")
    return frame[list(columns)].copy()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")

def run(main):
    try:
        main()
    except (WorkshopError, OSError, ValueError) as exc:
        raise SystemExit(f"\nSTOP: {exc}\nNo need to start over. Fix the item above and rerun this stage.") from None
