"""Guided exercise. Only edit lines marked BLANK."""

# Find the repository even when this file is run from another folder.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _helpers import ROOT, OUTPUT, check, read_csv, write_json, run

# EXERCISE 3: count ratings; use their mean (average).
COUNT_OPERATION = ...  # BLANK: replace ... using the word bank in WORKSHOP.md
AVERAGE_OPERATION = ...  # BLANK: replace ... using the word bank in WORKSHOP.md

def main():
    # ------------------------------------------------------------------
    # Step 1: Load the cleaned data from checkpoint 2.
    # ------------------------------------------------------------------
    movies = read_csv(OUTPUT / "movies_clean.csv", ["movieId", "title", "genres"])
    ratings = read_csv(
        OUTPUT / "ratings_clean.csv",
        ["userId", "movieId", "rating", "rating_month"],
    )

    # ------------------------------------------------------------------
    # Step 2: Per-movie metrics.
    # One row per rated movie. Movies with no ratings are still counted in the catalog.
    # ------------------------------------------------------------------
    # How many ratings each movie got, and its average rating.
    metrics = ratings.groupby("movieId", as_index=False).agg(
        rating_count=("rating", COUNT_OPERATION),
        average_rating=("rating", AVERAGE_OPERATION),
    )

    # Add each movie's title and genres.
    metrics = metrics.merge(movies, on="movieId", validate="one_to_one")

    # Put the columns in a readable order, most-rated movies first.
    metrics = metrics[["movieId", "title", "genres", "rating_count", "average_rating"]]
    metrics = metrics.sort_values(["rating_count", "movieId"], ascending=[False, True])

    # ------------------------------------------------------------------
    # Step 3: Per-genre metrics.
    # Multi-genre movies contribute once to each listed genre. Do not add genre totals.
    # ------------------------------------------------------------------
    # Attach genres to every rating, then split "Action|Comedy" into a list.
    joined = ratings.merge(movies, on="movieId", validate="many_to_one")
    joined["genre"] = joined["genres"].str.split("|")

    # explode() gives each genre in the list its own row, so we can group by genre.
    genres = joined.explode("genre").groupby("genre", as_index=False).agg(
        rating_count=("rating", "count"),
        average_rating=("rating", "mean"),
        movie_count=("movieId", "nunique"),
    )
    genres = genres.sort_values(["rating_count", "genre"], ascending=[False, True])

    # ------------------------------------------------------------------
    # Step 4: Per-month activity.
    # ------------------------------------------------------------------
    monthly = ratings.groupby("rating_month", as_index=False).agg(
        rating_count=("rating", "count"),
        active_raters=("userId", "nunique"),
    )

    # ------------------------------------------------------------------
    # Step 5: Headline numbers for the whole dataset.
    # ------------------------------------------------------------------
    summary = {
        "catalog_movies": len(movies),
        "rated_movies": int(ratings["movieId"].nunique()),
        "ratings": len(ratings),
        "users": int(ratings["userId"].nunique()),
        "average_rating": round(float(ratings["rating"].mean()), 4),
        "first_rating_month": str(monthly["rating_month"].min()),
        "last_rating_month": str(monthly["rating_month"].max()),
    }

    # ------------------------------------------------------------------
    # Step 6: Sanity checks. Totals must add up and averages must be on the 0.5-5 scale.
    # ------------------------------------------------------------------
    check(
        int(metrics["rating_count"].sum()) == len(ratings),
        "Movie totals must equal the cleaned rating count.",
    )
    check(
        int(monthly["rating_count"].sum()) == len(ratings),
        "Monthly totals must equal the cleaned rating count.",
    )
    check(
        metrics["average_rating"].between(0.5, 5).all(),
        "Averages must stay within the MovieLens scale.",
    )

    # ------------------------------------------------------------------
    # Step 7: Save the results.
    # ------------------------------------------------------------------
    # Round averages only after the checks, so the checks use exact values.
    metrics["average_rating"] = metrics["average_rating"].round(4)
    genres["average_rating"] = genres["average_rating"].round(4)

    metrics.to_csv(OUTPUT / "movie_metrics.csv", index=False)
    genres.to_csv(OUTPUT / "genre_metrics.csv", index=False)
    monthly.to_csv(OUTPUT / "monthly_metrics.csv", index=False)
    write_json(OUTPUT / "summary.json", summary)

    # This single file is what you give ChatGPT to build the dashboard.
    write_json(OUTPUT / "dashboard_data.json", {
        "schema_version": 1,
        "source": "GroupLens MovieLens Latest Small",
        "notes": [
            "Ratings are not watches, revenue, or all streaming customers.",
            "Genre counts overlap. Monthly counts describe rating activity in this sample.",
        ],
        "summary": summary,
        "movies": metrics.to_dict(orient="records"),
        "genres": genres.to_dict(orient="records"),
        "monthly": monthly.to_dict(orient="records"),
    })

    print(f"CHECKPOINT 3: {summary['ratings']:,} ratings summarized; dashboard_data.json is ready.")
    print("Next: give output/dashboard_data.json to ChatGPT (WORKSHOP.md step 5).")


if __name__ == "__main__":
    run(main)
