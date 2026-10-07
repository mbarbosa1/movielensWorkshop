# Guided lab: from raw files to useful questions

You are an engineer on a fictional streaming team. Your task is to turn movie
ratings into a small analytics product. Work through one section at a time.
The instructor explains the idea, you fill two or three blanks, then you run the
script and inspect a real output. You do not need to invent any Python code.

Before starting, complete README.md steps 1–3. Keep `HINTS.md` nearby.

**The journey (ETL):** raw CSV → ingest (Extract) → clean + analyze (Transform) → JSON file (Load) → dashboard.

A CSV is a file with rows and named columns. A DataFrame is Python's way to work
with that file like a spreadsheet. JSON is named data that apps can read.

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

Open `scripts/01_ingest.py`. Replace the two `...` values.
Word bank: `"movies.csv"`, `"ratings.csv"`.

- `MOVIES_FILE` is the file with movie names and genres.
- `RATINGS_FILE` is the file with user scores.

Then replace the two `#[FILL],` lines with each file's column names, in square
brackets, like `["movieId", "title", "genres"],`. Copy them from the header row of
the matching file in `data/`. This list tells the script which columns must exist,
so a wrong file stops right away instead of breaking a later stage.

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
support, so the dashboard leaderboard defaults to at least 20 ratings.

## 5. Build the dashboard with ChatGPT (20 minutes)

Find `output/dashboard_data.json`. It holds the real results in one file:
summary numbers plus movie, genre, and monthly lists. Open ChatGPT, ask it to
build a Site, attach this JSON file, and paste the prompt below. If ChatGPT
cannot read the file, fix the upload rather than letting it invent examples.

> Build a beginner-friendly movie rating analytics dashboard using Sites and the
> attached dashboard_data.json. Use only the attached real data. If you cannot
> read it, tell me and stop; do not invent numbers or movies.
>
> Show four summary cards: catalog movies, rated movies, ratings, and users.
> Add a movie list with title, genres, number of ratings, and average rating.
> Let me switch between most rated and highest average, and choose a minimum
> rating count, defaulting to 20. Filter before sorting. Break tied averages by
> rating count descending and then movieId ascending. Display average ratings
> to two decimal places.
>
> Add genre rating counts and genre average ratings, plus a monthly rating
> activity chart sorted chronologically using the field rating_month.
> Explain that genre totals overlap and these are ratings, not watches or revenue.
>
> Use plain labels, readable text, and a layout that works on a phone. Include
> GroupLens MovieLens attribution and a link to the dataset.
> Do not add a recommendation model, login, or fabricated data.

**Checkpoint:**

1. The four cards match `output/summary.json`.
2. With the minimum count at 20, every visible movie has at least 20 ratings.
3. Sorting by highest average shows scores descending; most rated ranks by count.
4. One genre matches its row in `output/genre_metrics.csv`.

If something is wrong, tell ChatGPT the exact discrepancy and the expected value
from the output file. If you rerun the pipeline, upload the new JSON again.
Save one cautious observation, such as "Among movies with at least 20 ratings in this sample, …".

## Finish

You have built an ETL pipeline: raw files → dependable rows → metrics → a dashboard.
The completed files are available for reviewing the full flow later. For a recovery
run at any time, use `python run_workshop.py --completed`.
