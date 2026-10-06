"""Guided exercise. Only edit lines marked BLANK."""

# Find the repository even when this file is run from another folder.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _helpers import ROOT, OUTPUT, check, filled, read_csv, write_json, run

# EXERCISE 3: count ratings; use their mean (average).
COUNT_OPERATION = ...  # BLANK: replace ... using the word bank in WORKSHOP.md
AVERAGE_OPERATION = ...  # BLANK: replace ... using the word bank in WORKSHOP.md

def main():
    filled(COUNT_OPERATION=COUNT_OPERATION, AVERAGE_OPERATION=AVERAGE_OPERATION)
    check(COUNT_OPERATION == "count" and AVERAGE_OPERATION == "mean", "Use count and mean. See HINTS.md.")
    movies = read_csv(OUTPUT / "movies_clean.csv", ["movieId", "title", "genres"])
    ratings = read_csv(OUTPUT / "ratings_clean.csv", ["userId", "movieId", "rating", "rating_month"])
    # One row per rated movie. Movies with no ratings are still counted in the catalog.
    metrics = ratings.groupby("movieId", as_index=False).agg(
        rating_count=("rating", COUNT_OPERATION), average_rating=("rating", AVERAGE_OPERATION))
    metrics = metrics.merge(movies, on="movieId", validate="one_to_one")
    metrics = metrics[["movieId", "title", "genres", "rating_count", "average_rating"]]
    metrics = metrics.sort_values(["rating_count", "movieId"], ascending=[False, True])
    # Multi-genre movies contribute once to each listed genre. Do not add genre totals.
    joined = ratings.merge(movies, on="movieId", validate="many_to_one")
    joined["genre"] = joined["genres"].str.split("|")
    genres = joined.explode("genre").groupby("genre", as_index=False).agg(
        rating_count=("rating", "count"), average_rating=("rating", "mean"), movie_count=("movieId", "nunique"))
    genres = genres.sort_values(["rating_count", "genre"], ascending=[False, True])
    monthly = ratings.groupby("rating_month", as_index=False).agg(
        rating_count=("rating", "count"), active_raters=("userId", "nunique"))
    summary = {"catalog_movies": len(movies), "rated_movies": int(ratings["movieId"].nunique()),
               "ratings": len(ratings), "users": int(ratings["userId"].nunique()),
               "average_rating": round(float(ratings["rating"].mean()), 4),
               "first_rating_month": str(monthly["rating_month"].min()),
               "last_rating_month": str(monthly["rating_month"].max())}
    check(int(metrics["rating_count"].sum()) == len(ratings), "Movie totals must equal the cleaned rating count.")
    check(int(monthly["rating_count"].sum()) == len(ratings), "Monthly totals must equal the cleaned rating count.")
    check(metrics["average_rating"].between(0.5, 5).all(), "Averages must stay within the MovieLens scale.")
    metrics["average_rating"] = metrics["average_rating"].round(4)
    genres["average_rating"] = genres["average_rating"].round(4)
    metrics.to_csv(OUTPUT / "movie_metrics.csv", index=False)
    genres.to_csv(OUTPUT / "genre_metrics.csv", index=False)
    monthly.to_csv(OUTPUT / "monthly_metrics.csv", index=False)
    write_json(OUTPUT / "summary.json", summary)
    # This single file can power a Sites dashboard without a hosted Python API.
    write_json(OUTPUT / "dashboard_data.json", {
        "schema_version": 1, "source": "GroupLens MovieLens Latest Small",
        "notes": ["Ratings are not watches, revenue, or all streaming customers.",
                  "Genre counts overlap. Monthly counts describe rating activity in this sample."],
        "summary": summary, "movies": metrics.to_dict(orient="records"),
        "genres": genres.to_dict(orient="records"), "monthly": monthly.to_dict(orient="records")})
    print(f"CHECKPOINT 3: {summary['ratings']:,} ratings summarized; dashboard_data.json is ready.")
    print("Next: start the API with run_workshop.py api, or follow DASHBOARD.md.")

if __name__ == "__main__":
    run(main)
