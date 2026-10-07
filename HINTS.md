# Hints and answers

Only replace `...` on a line marked BLANK, or a `#[FILL],` line. Text answers need
straight quotes; numbers do not. Leave the variable name, equals sign, and rest of the script alone.

## 01_ingest.py

Hint: movie information comes from the movie file; scores come from the rating file.

```python
MOVIES_FILE = "movies.csv"
RATINGS_FILE = "ratings.csv"
```

Hint for the two `#[FILL],` lines: open each CSV in `data/` and copy its header row.
Each column name goes in quotes, separated by commas, inside square brackets.
Keep the comma at the end of the line.

```python
    movies = read_csv(
        ROOT / "data" / MOVIES_FILE,
        ["movieId", "title", "genres"],
    )
    ratings = read_csv(
        ROOT / "data" / RATINGS_FILE,
        ["userId", "movieId", "rating", "timestamp"],
    )
```

## 02_clean.py

Hint: ratings range from half a star to five stars; the movie ID connects both files.

```python
MIN_RATING = 0.5
MAX_RATING = 5.0
JOIN_COLUMN = "movieId"
```

## 03_analyze.py

Hint: count measures volume; mean measures the average score.

```python
COUNT_OPERATION = "count"
AVERAGE_OPERATION = "mean"
```

Full versions are in `completed/`. You can run an answer file without
overwriting your exercise, for example `python completed/02_clean_complete.py`.

A checkpoint failure is useful feedback. Read the STOP message, fix that item,
and run the same stage again.
