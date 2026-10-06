# Hints and answers

Only replace `...` on a line marked BLANK. Text answers need straight quotes;
numbers do not. Leave the variable name, equals sign, and rest of the script alone.

## 01_ingest.py

Hint: movie information comes from the movie file; scores come from the rating file.

```python
MOVIES_FILE = "movies.csv"
RATINGS_FILE = "ratings.csv"
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

## 04_api.py

Hint: match the URL path to the kind of data it returns.

```python
SUMMARY_PATH = "/summary"
MOVIES_PATH = "/movies"
```

Full versions are in `completed/`. You may run the corresponding answer file
without overwriting your exercise, for example:
`python completed/02_clean_complete.py` after ingestion succeeds.

A checkpoint failure is useful feedback. Read the STOP message, fix that item,
and run the same stage again. You do not need to reinstall Python or restart the lab.
