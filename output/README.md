# Generated results

Run the scripts in order. They overwrite these results; they never overwrite raw inputs.

1. Ingestion: `movies_ingested.csv`, `ratings_ingested.csv`.
2. Cleaning: `movies_clean.csv`, `ratings_clean.csv`, `cleaning_report.json`.
3. Analytics: `movie_metrics.csv`, `genre_metrics.csv`, `monthly_metrics.csv`,
   `summary.json`, `dashboard_data.json`.

Start by reading `summary.json`. For the dashboard activity, use `dashboard_data.json`.
CSV files can be opened in an editor or spreadsheet. Do not manually edit generated
files; change a pipeline rule or input, then rerun the pipeline. Earlier stages
remove older downstream outputs, so run all stages again after changing inputs.

Metric columns:
- Movies: movieId, title, genres, rating_count, average_rating.
- Genres: genre, rating_count, average_rating, movie_count (rated movies in that genre).
- Months: rating_month (UTC year-month), rating_count, active_raters (unique user IDs).

Genre counts overlap. Movie and monthly rating counts each add up to cleaned ratings.
The dashboard export is a snapshot; reimport it after rerunning analytics.
Keep the original GroupLens license with these transformed data when redistributing.
