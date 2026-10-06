"""Guided exercise. Only edit lines marked BLANK."""

# Find the repository even when this file is run from another folder.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from _helpers import ROOT, OUTPUT, check, filled, read_csv, write_json, run

import json
from fastapi import FastAPI, HTTPException, Query

# EXERCISE 4: these are URL paths, so each begins with /.
SUMMARY_PATH = ...  # BLANK: replace ... using the word bank in WORKSHOP.md
MOVIES_PATH = ...  # BLANK: replace ... using the word bank in WORKSHOP.md
filled(SUMMARY_PATH=SUMMARY_PATH, MOVIES_PATH=MOVIES_PATH)
check(SUMMARY_PATH == "/summary" and MOVIES_PATH == "/movies", "Use /summary and /movies so the dashboard contract matches.")
app = FastAPI(title="MovieLens Workshop API", description="Read-only movie rating analytics. Try each route at /docs.")

def data():
    # Read the finished export each time; restarting is unnecessary after rerunning analytics.
    try:
        return json.loads((OUTPUT / "dashboard_data.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise HTTPException(status_code=503, detail="Analytics are missing or unreadable. Run: python run_workshop.py pipeline --completed") from None

@app.get("/")
def welcome():
    return {"message": "MovieLens workshop API", "try": "/docs"}

@app.get("/health")
def health():
    data()
    return {"status": "ready"}

@app.get(SUMMARY_PATH)
def summary():
    return data()["summary"]

@app.get(MOVIES_PATH)
def movies(limit: int = Query(10, ge=1, le=100), min_ratings: int = Query(20, ge=1),
           sort: str = Query("rating_count", pattern="^(rating_count|average_rating)$")):
    # Filter before ranking: one five-star review should not dominate a leaderboard.
    rows = [row for row in data()["movies"] if row["rating_count"] >= min_ratings]
    rows.sort(key=lambda row: (-row[sort], -row["rating_count"], row["movieId"]))
    return rows[:limit]

@app.get("/genres")
def genres():
    return data()["genres"]

@app.get("/monthly")
def monthly():
    return data()["monthly"]

@app.get("/dashboard")
def dashboard():
    return data()

if __name__ == "__main__":
    # This is a local teaching server; Ctrl+C stops it.
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
