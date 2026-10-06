"""Full answer version. Read alongside the matching exercise."""

# Find the repository even when this file is run from another folder.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _helpers import ROOT, OUTPUT, check, filled, read_csv, write_json, run


# EXERCISE 1: choose the raw file names (keep quotation marks).
MOVIES_FILE = "movies.csv"
RATINGS_FILE = "ratings.csv"


def main():
    # ------------------------------------------------------------------
    # Step 1: Confirm the exercise answers are filled in.
    # ------------------------------------------------------------------
    filled(MOVIES_FILE=MOVIES_FILE, RATINGS_FILE=RATINGS_FILE)

    # ------------------------------------------------------------------
    # Step 2: Read the raw files.
    # Ingestion means reading raw files and saving a consistent working copy.
    # We do not change or overwrite the original data/ files.
    # ------------------------------------------------------------------
    movies = read_csv(ROOT / "data" / MOVIES_FILE, ["movieId", "title", "genres"])
    ratings = read_csv(
        ROOT / "data" / RATINGS_FILE,
        ["userId", "movieId", "rating", "timestamp"],
    )

    # ------------------------------------------------------------------
    # Step 3: Save working copies to output/.
    # ------------------------------------------------------------------
    OUTPUT.mkdir(exist_ok=True)
    movies.to_csv(OUTPUT / "movies_ingested.csv", index=False)
    ratings.to_csv(OUTPUT / "ratings_ingested.csv", index=False)

    # ------------------------------------------------------------------
    # Step 4: Delete results from earlier runs.
    # Older downstream results must not look like results from this new run.
    # ------------------------------------------------------------------
    for name in [
        "movies_clean.csv",
        "ratings_clean.csv",
        "cleaning_report.json",
        "movie_metrics.csv",
        "genre_metrics.csv",
        "monthly_metrics.csv",
        "summary.json",
        "dashboard_data.json",
    ]:
        (OUTPUT / name).unlink(missing_ok=True)

    print(f"CHECKPOINT 1: read {len(movies):,} movies and {len(ratings):,} ratings.")
    print("Open output/movies_ingested.csv. Next: 02_clean.py.")


if __name__ == "__main__":
    run(main)
