"""Full answer version. Read alongside the matching exercise."""

# Find the repository even when this file is run from another folder.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _helpers import ROOT, OUTPUT, check, filled, read_csv, write_json, run

import pandas as pd


# EXERCISE 2: MovieLens ratings use half stars, from 0.5 to 5.0.
MIN_RATING = 0.5
MAX_RATING = 5.0
JOIN_COLUMN = "movieId"


def main():
    # ------------------------------------------------------------------
    # Step 1: Confirm the exercise answers are filled in and correct.
    # ------------------------------------------------------------------
    filled(MIN_RATING=MIN_RATING, MAX_RATING=MAX_RATING, JOIN_COLUMN=JOIN_COLUMN)
    check(
        MIN_RATING == 0.5 and MAX_RATING == 5.0 and JOIN_COLUMN == "movieId",
        "Use the MovieLens scale 0.5 to 5.0 and join on movieId. See HINTS.md.",
    )

    # ------------------------------------------------------------------
    # Step 2: Load the ingested data from checkpoint 1.
    # ------------------------------------------------------------------
    movies = read_csv(OUTPUT / "movies_ingested.csv", ["movieId", "title", "genres"])
    ratings = read_csv(
        OUTPUT / "ratings_ingested.csv",
        ["userId", "movieId", "rating", "timestamp"],
    )

    # The report records how many rows each cleaning step removes.
    report = {"input_movies": len(movies), "input_ratings": len(ratings)}

    # ------------------------------------------------------------------
    # Step 3: Clean the movies.
    # ------------------------------------------------------------------
    # Convert invalid numbers to missing values so we can count and remove them.
    movies["movieId"] = pd.to_numeric(movies["movieId"], errors="coerce")

    # Trim whitespace. Blank titles become "", blank genres get a placeholder.
    movies["title"] = movies["title"].fillna("").astype(str).str.strip()
    movies["genres"] = movies["genres"].fillna("(no genres listed)").astype(str).str.strip()
    movies.loc[movies["genres"].eq(""), "genres"] = "(no genres listed)"

    # A valid movie has a positive whole-number ID and a title.
    valid_movies = (
        movies["movieId"].gt(0)
        & movies["movieId"].mod(1).eq(0)
        & movies["title"].ne("")
    )
    report["invalid_movies_removed"] = int((~valid_movies).sum())
    movies = movies.loc[valid_movies].copy()

    # Identical repeated rows are safe to remove; conflicting IDs need attention.
    before = len(movies)
    movies = movies.drop_duplicates()
    report["duplicate_movies_removed"] = before - len(movies)
    check(
        not movies["movieId"].duplicated().any(),
        "One movieId has conflicting titles/genres. Inspect movies_ingested.csv before continuing.",
    )

    movies["movieId"] = movies["movieId"].astype("int64")
    check(not movies.empty, "No valid movies remain. Check the raw movies.csv file.")

    # ------------------------------------------------------------------
    # Step 4: Remove invalid ratings.
    # ------------------------------------------------------------------
    # Convert every column to numbers; anything unreadable becomes missing.
    for column in ["userId", "movieId", "rating", "timestamp"]:
        ratings[column] = pd.to_numeric(ratings[column], errors="coerce")
    dates = pd.to_datetime(ratings["timestamp"], unit="s", utc=True, errors="coerce")

    # The rating must be on the scale and land on a half star (x2 gives a whole number).
    valid_ratings = (
        ratings["rating"].between(MIN_RATING, MAX_RATING)
        & (ratings["rating"] * 2).mod(1).eq(0)
    )

    # User and movie IDs must be positive whole numbers.
    for column in ["userId", "movieId"]:
        valid_ratings &= ratings[column].gt(0) & ratings[column].mod(1).eq(0)

    # The timestamp must be a readable, non-negative whole number of seconds.
    valid_ratings &= (
        dates.notna()
        & ratings["timestamp"].ge(0)
        & ratings["timestamp"].mod(1).eq(0)
    )

    report["invalid_ratings_removed"] = int((~valid_ratings).sum())
    ratings = ratings.loc[valid_ratings].copy()

    # ------------------------------------------------------------------
    # Step 5: Remove duplicate ratings.
    # ------------------------------------------------------------------
    # Exact copies of the same row.
    before = len(ratings)
    ratings = ratings.drop_duplicates()
    report["exact_duplicate_ratings_removed"] = before - len(ratings)

    # Keep the most recent rating if a person rated the same movie again.
    before = len(ratings)
    ratings = (
        ratings.sort_values("timestamp", kind="stable")
        .drop_duplicates(["userId", JOIN_COLUMN], keep="last")
    )
    report["older_user_movie_ratings_removed"] = before - len(ratings)

    # ------------------------------------------------------------------
    # Step 6: Keep only ratings for movies in the catalog.
    # A rating needs a movie in the catalog; count unmatched rows before removing.
    # ------------------------------------------------------------------
    matched = ratings[JOIN_COLUMN].isin(movies[JOIN_COLUMN])
    report["unmatched_ratings_removed"] = int((~matched).sum())
    ratings = ratings.loc[matched].copy()
    check(
        not ratings.empty,
        "No valid ratings remain. Check rating values, timestamps, and movie IDs.",
    )

    # ------------------------------------------------------------------
    # Step 7: Tidy column types and add readable dates.
    # ------------------------------------------------------------------
    for column in ["userId", "movieId", "timestamp"]:
        ratings[column] = ratings[column].astype("int64")

    # e.g. "1996-03-29T18:36:55Z", and the month "1996-03".
    ratings["rated_at"] = (
        pd.to_datetime(ratings["timestamp"], unit="s", utc=True)
        .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    ratings["rating_month"] = ratings["rated_at"].str[:7]

    # ------------------------------------------------------------------
    # Step 8: Final checks before saving.
    # ------------------------------------------------------------------
    check(
        not ratings.duplicated(["userId", "movieId"]).any(),
        "Checkpoint failed: repeated user/movie pair.",
    )
    check(
        ratings["movieId"].isin(movies["movieId"]).all(),
        "Checkpoint failed: unknown movie ID.",
    )

    # ------------------------------------------------------------------
    # Step 9: Save the cleaned data and the report.
    # ------------------------------------------------------------------
    report.update(clean_movies=len(movies), clean_ratings=len(ratings))
    movies.to_csv(OUTPUT / "movies_clean.csv", index=False)
    ratings.to_csv(OUTPUT / "ratings_clean.csv", index=False)
    write_json(OUTPUT / "cleaning_report.json", report)

    # Delete results from earlier runs so they are not mistaken for this run's.
    for name in [
        "movie_metrics.csv",
        "genre_metrics.csv",
        "monthly_metrics.csv",
        "summary.json",
        "dashboard_data.json",
    ]:
        (OUTPUT / name).unlink(missing_ok=True)

    print(f"CHECKPOINT 2: {len(movies):,} clean movies; {len(ratings):,} clean ratings.")
    print("Read output/cleaning_report.json to see every removal count. Next: 03_analyze.py.")


if __name__ == "__main__":
    run(main)
