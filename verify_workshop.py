"""Instructor verification with the real local dataset. No generated sample data.
Run after installing requirements and preparing data. Regenerates output/.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def command(path, expected=0):
    # Capture output so failures show the useful message instead of a long test log.
    result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    check(result.returncode == expected, f"{path.name}: {result.stdout} {result.stderr}")
    return result.stdout + result.stderr

def main():
    import pandas as pd
    from fastapi.testclient import TestClient
    raw_paths = [ROOT / "data" / name for name in ["movies.csv", "ratings.csv"]]
    for path in raw_paths:
        check(path.is_file() and path.stat().st_size, "No real input available. Run prepare-data; no synthetic data will be substituted.")
    hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in raw_paths]
    # Syntax validation includes unfilled exercises: ... is a valid Python placeholder.
    for path in list((ROOT / "scripts").glob("*.py")) + list((ROOT / "completed").glob("*.py")) + [ROOT / "run_workshop.py"]:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    for stage in ["01_ingest", "02_clean", "03_analyze"]:
        print(command(ROOT / "completed" / f"{stage}_complete.py").strip())
    out = ROOT / "output"
    summary = json.loads((out / "summary.json").read_text())
    report = json.loads((out / "cleaning_report.json").read_text())
    ratings = pd.read_csv(out / "ratings_clean.csv")
    movies = pd.read_csv(out / "movie_metrics.csv")
    monthly = pd.read_csv(out / "monthly_metrics.csv")
    check(summary["ratings"] == len(ratings) == int(movies.rating_count.sum()) == int(monthly.rating_count.sum()), "Totals differ between outputs.")
    check(summary["users"] == ratings.userId.nunique(), "Unique-user count differs.")
    check(summary["average_rating"] == round(float(ratings.rating.mean()), 4), "Average score differs.")
    removed = sum(report[k] for k in ["invalid_ratings_removed", "exact_duplicate_ratings_removed", "older_user_movie_ratings_removed", "unmatched_ratings_removed"])
    check(report["input_ratings"] == report["clean_ratings"] + removed, "Removal report does not reconcile.")
    check(not ratings.duplicated(["userId", "movieId"]).any(), "Clean ratings have repeated user/movie pairs.")
    # Check one genre directly from the clean ratings, independently of its output.
    catalog = pd.read_csv(out / "movies_clean.csv")
    genre_rows = pd.read_csv(out / "genre_metrics.csv")
    first = genre_rows.iloc[0]
    ids = catalog.loc[catalog.genres.str.split("|").apply(lambda names: first.genre in names), "movieId"]
    scores = ratings.loc[ratings.movieId.isin(ids), "rating"]
    check(int(first.rating_count) == len(scores) and float(first.average_rating) == round(float(scores.mean()), 4), "Genre metrics differ from real ratings.")
    check(hashes == [hashlib.sha256(path.read_bytes()).hexdigest() for path in raw_paths], "A raw file changed.")
    print("PASS: totals, weighted genre average, removal accounting, unique pairs, and raw-file preservation.")

    spec = importlib.util.spec_from_file_location("workshop_api", ROOT / "completed" / "04_api_complete.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with TestClient(module.app) as client:
        for route in ["/", "/health", "/summary", "/movies", "/genres", "/monthly", "/dashboard", "/docs", "/openapi.json"]:
            check(client.get(route).status_code == 200, f"API route failed: {route}")
        check(client.get("/summary").json() == summary, "API summary differs from file.")
        for sort in ["average_rating", "rating_count"]:
            rows = client.get(f"/movies?limit=3&min_ratings=20&sort={sort}").json()
            check(len(rows) <= 3 and all(row["rating_count"] >= 20 for row in rows), "Movie filter/limit failed.")
            check([r[sort] for r in rows] == sorted([r[sort] for r in rows], reverse=True), "Movie ordering failed.")
        check(client.get("/movies?min_ratings=1000000000").json() == [], "Empty movie filter should return [].")
        for query in ["limit=0", "limit=101", "min_ratings=0", "sort=unknown"]:
            check(client.get("/movies?" + query).status_code == 422, "Invalid API parameter was accepted.")
        with tempfile.TemporaryDirectory() as temporary:
            previous = module.OUTPUT
            module.OUTPUT = Path(temporary)
            check(client.get("/health").status_code == 503, "Missing analytics should report 503.")
            check(client.get("/summary").status_code == 503, "Missing summary should report 503.")
            module.OUTPUT = previous
    print("PASS: API routes, documentation, filtering, ordering, parameter errors, and missing-output errors.")

    # Run filled student files in an isolated copy with these actual MovieLens inputs.
    replacements = {"MOVIES_FILE": '"movies.csv"', "RATINGS_FILE": '"ratings.csv"',
                    "MIN_RATING": "0.5", "MAX_RATING": "5.0", "JOIN_COLUMN": '"movieId"',
                    "COUNT_OPERATION": '"count"', "AVERAGE_OPERATION": '"mean"',
                    "SUMMARY_PATH": '"/summary"', "MOVIES_PATH": '"/movies"'}
    import shutil
    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary)
        shutil.copytree(ROOT / "scripts", copy / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(ROOT / "data", copy / "data")
        message = command(copy / "scripts" / "01_ingest.py", expected=1)
        check("Complete these blanks first" in message, "Unfilled exercise should explain what to edit.")
        for path in (copy / "scripts").glob("*.py"):
            text = path.read_text()
            for key, answer in replacements.items():
                text = text.replace(f"{key} = ...", f"{key} = {answer}")
            path.write_text(text)
        for stage in ["01_ingest", "02_clean", "03_analyze"]:
            command(copy / "scripts" / f"{stage}.py")
        check(json.loads((copy / "output" / "dashboard_data.json").read_text()) == json.loads((out / "dashboard_data.json").read_text()), "Student and completed exports differ.")
        api_spec = importlib.util.spec_from_file_location("student_api", copy / "scripts" / "04_api.py")
        student_api = importlib.util.module_from_spec(api_spec)
        api_spec.loader.exec_module(student_api)
        student_api.OUTPUT = copy / "output"
        with TestClient(student_api.app) as student_client:
            check(student_client.get("/summary").json() == summary, "Filled student API differs from completed API.")
        (copy / "data" / "ratings.csv").unlink()
        message = command(copy / "scripts" / "01_ingest.py", expected=1)
        check("Missing or empty file" in message and "README.md" in message, "Missing input should explain setup.")
        (copy / "data" / "ratings.csv").write_text("")
        message = command(copy / "scripts" / "01_ingest.py", expected=1)
        check("Missing or empty file" in message, "Empty input should explain setup.")
    print("PASS: filled exercises match answers; blanks, missing files, and empty files fail clearly.")
    print("All checks passed using real local MovieLens data. No fake rows were created.")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ImportError, OSError, ValueError) as exc:
        raise SystemExit(f"VERIFY STOP: {exc}\nSee README.md for setup and troubleshooting.") from None
