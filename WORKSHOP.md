# Guided lab: from raw files to useful questions

You are an engineer on a fictional streaming team. Your task is to turn movie
ratings into a small analytics product. Work through one section at a time.
The instructor explains the idea, you fill two or three blanks, then you run the
script and inspect a real output. You do not need to invent any Python code.

Before starting, complete README.md steps 1–3. Keep `HINTS.md` nearby.

**The journey:** raw CSV → ingestion → cleaning → analytics → API → dashboard.

A CSV is a file with rows and named columns. A DataFrame is Python's way to work
with that file like a spreadsheet. JSON is named data that apps can read.
An API is a way for another app to request data from a URL.

## 1. Meet the raw data (5 minutes)

Open `data/movies.csv`. Each row describes a movie:
`movieId` is its identifier, `title` is its name, and `genres` lists categories separated by `|`.
Open `data/ratings.csv`. Each row describes a rating:
`userId` identifies a person, `movieId` identifies the movie, `rating` is a half-star
score from 0.5 to 5.0, and `timestamp` is seconds since January 1, 1970 in UTC.

The same `movieId` connects the two files. Names are not reliable identifiers.
Do not edit the CSV files. Tags and external links are outside this lab.

**Checkpoint:** point to the column shared by both files: `movieId`.

## 2. Ingest: read the files (10 minutes)

Open `scripts/01_ingest.py`. Replace just the two `...` values.
Word bank: `"movies.csv"`, `"ratings.csv"`.

- `MOVIES_FILE` is the file with movie names and genres.
- `RATINGS_FILE` is the file with user scores.

Run:

```sh
python scripts/01_ingest.py
```

**Expected:** CHECKPOINT 1 and two files in `output/`: `movies_ingested.csv` and
`ratings_ingested.csv`. For this supplied snapshot, expect 9,742 and 100,836 rows.
Open the movie output: it should have the same three columns as the original.
Ingestion organizes the input; cleaning comes next.
If a file is missing or empty, follow README.md > Data setup.

## 3. Clean: make rows dependable (15 minutes)

Open `scripts/02_clean.py`. Word bank: `0.5`, `5.0`, `"movieId"`.

- `MIN_RATING` is the smallest allowed score.
- `MAX_RATING` is the largest allowed score.
- `JOIN_COLUMN` connects a rating to its movie.

Run:

```sh
python scripts/02_clean.py
```

The prepared code converts numeric columns, trims titles, removes invalid rows
and exact duplicates, keeps the latest score for repeated user/movie pairs, and
removes ratings for unknown movies. Ties in repeated timestamps keep the last
input row. Conflicting catalog IDs stop the run for human inspection.
Missing genres become `(no genres listed)`; we do not invent categories or titles.

**Expected:** CHECKPOINT 2, `movies_clean.csv`, `ratings_clean.csv`, and
`cleaning_report.json`. Open the report to see input counts, removed counts, and
remaining counts. The original provided snapshot should lose zero rows.
Open the clean ratings: `rated_at` is a readable UTC date, and `rating_month`
is year-month, such as `1996-03`.

Cleaning does not have to delete rows to be useful: it verifies that the input
is already usable. If a checkpoint stops, fix the named input issue and rerun.

## 4. Analyze: answer product questions (15 minutes)

Open `scripts/03_analyze.py`. Word bank: `"count"`, `"mean"`.

- `COUNT_OPERATION` answers “How many ratings?”
- `AVERAGE_OPERATION` answers “What is the average score?”

Run:

```sh
python scripts/03_analyze.py
```

**Expected:** CHECKPOINT 3, three metric CSV files, `summary.json`, and
`dashboard_data.json`. Open `summary.json` first; it is the smallest output.
Then open `movie_metrics.csv` and compare `rating_count` with `average_rating`.

- Movie popularity = count of ratings, not count of watches.
- Average score = sum of scores divided by number of ratings. It is not a prediction.
- Genre averages use individual ratings, not averages of movie averages.
- Multi-genre movies contribute to each genre; genre totals overlap.
- Monthly activity = rating count and unique raters in observed months.
  Months without ratings are omitted; a dashboard may display them as zero counts.
- Unrated catalog movies count toward `catalog_movies` but have no movie metric row.

**Checkpoint:** movie counts and monthly counts each add up to cleaned ratings.
The script checks both automatically. A movie with one five-star score has little
support, so the API leaderboard defaults to at least 20 ratings.

## 5. API: request the results (10 minutes)

Open `scripts/04_api.py`. Word bank: `"/summary"`, `"/movies"`.
Use each path for its matching variable. A route is a URL path like `/summary`.

Run:

```sh
python run_workshop.py api
```

Leave the terminal running. Open http://127.0.0.1:8000/docs.
Choose **GET /summary → Try it out → Execute**.
The response is the same summary you saw in the file.
Choose **GET /movies** and execute with `limit=10`, `min_ratings=20`, and
`sort=average_rating`. You should receive up to ten movies with sufficient ratings,
ordered by average score. Try `sort=rating_count` to see popularity instead.

Other routes: `/genres`, `/monthly`, `/dashboard` (all data), `/health` (ready check).
A 200 response means success. A 422 response means a parameter was invalid.
A 503 response means analytics output is missing; rerun the pipeline.
The minimum count is a teaching choice, not a statistical guarantee.

**Checkpoint:** change `limit` to 3; at most three rows should be returned.
Press Ctrl+C in the terminal to stop the API.

## 6. Build the dashboard (20 minutes)

Follow `DASHBOARD.md`. Import the real `output/dashboard_data.json`, then use the
provided prompt to build a dashboard with ChatGPT's Sites functionality.
This file approach works without exposing your computer's local API to the internet.

**Checkpoint:** dashboard totals match `summary.json`, and changing the minimum
rating filter changes the visible movie list. Save one cautious business observation,
such as “Among movies with at least 20 ratings in this sample, …”.

## Finish

You have connected raw files, dependable rows, metrics, an API, and a dashboard.
The completed files are available for reviewing the full flow later. For a recovery
run at any time, use `python run_workshop.py pipeline --completed`.
