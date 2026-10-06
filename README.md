# From raw movie data to a product dashboard

A guided beginner lab for a fictional streaming team. The team wants to explore
which movies receive many ratings, which receive high ratings, and how rating
activity changes over time. We use real MovieLens data for an educational simulation.
No machine learning, sentiment analysis, or live coding is needed.

**Start here:** set up Python, prepare the data, then open `WORKSHOP.md`.
Only replace the lines marked **BLANK** in `scripts/`. There are nine blanks total.
If you get stuck, use `HINTS.md` or read the matching full file in `completed/`.

## 1. Open this folder

Open the inner `movielens-workshop` folder in your editor. Open its terminal.
You should see `requirements.txt`, `scripts/`, and `run_workshop.py` in the same folder.
Commands below run from this folder. A terminal is the text window where you type commands.
Type the command and press Enter. Do not type the surrounding ``` marks.

## 2. Set up Python once

Use Python 3.10 or newer. Check with `python3 --version` on macOS/Linux or
`py --version` on Windows. If Python is absent, install it from https://www.python.org/downloads/.
On Windows, enable the installer option to add Python to PATH.

macOS / Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

A virtual environment keeps this workshop's packages together. Activate it again
when you open a new terminal. If PowerShell blocks activation, use
`.venv\Scripts\python.exe` in place of `python` in every command; no policy change is needed.
On macOS/Linux, `.venv/bin/python` also works without activation.
Package installation requires internet access. Complete it before the event.

## 3. Data setup

`data/movies.csv` and `data/ratings.csv` are the raw inputs. Never edit these as part
of an exercise. The original supplied placeholders were empty; the repository also
included a real `ml-latest-small/` download. To copy those originals into empty or missing inputs:

```sh
python run_workshop.py prepare-data
```

This command preserves any existing nonempty input file. It does not download
anything or make up sample rows. If the originals are missing, download **MovieLens
Latest Small** from https://grouplens.org/datasets/movielens/latest/, unzip it, and copy
its `movies.csv` and `ratings.csv` into `data/`. Keep the supplied GroupLens README
and license with redistributed data, including transformed outputs.

The included September 2018 snapshot has **9,742 movies, 100,836 ratings, and 610 users**.
Other snapshots can have different counts; the scripts do not require those exact totals.
The full-size datasets are unnecessary for this beginner workshop.

## 4. Choose how to run

For the guided lab, follow `WORKSHOP.md` and complete one stage at a time.
After filling the pipeline blanks, you may also run all three stages together:

```sh
python run_workshop.py pipeline
python run_workshop.py api
```

For the instructor's ready-to-run demonstration or a recovery path:

```sh
python run_workshop.py pipeline --completed
python run_workshop.py api --completed
```

With the API running, open http://127.0.0.1:8000/docs in your browser.
Leave that terminal open. Press Ctrl+C when finished.
Open `DASHBOARD.md` for the ChatGPT-assisted Sites activity.

## What is in this folder?

- `data/`: original movies and ratings; no edits during the lab.
- `ml-latest-small/`: preserved original download, tags, links, and GroupLens license.
- `scripts/01_ingest.py`: read raw CSV files and check their columns.
- `scripts/02_clean.py`: validate rows, remove duplicates, and create readable dates.
- `scripts/03_analyze.py`: calculate movie, genre, and monthly metrics.
- `scripts/04_api.py`: serve those results through URLs.
- `scripts/_helpers.py`: shared file checks and readable error messages; leave it alone.
- `completed/`: full answer versions of all four scripts.
- `output/`: generated working files and dashboard export; safe to regenerate.
- `run_workshop.py`: optional helper to prepare inputs, run the pipeline, or start the API.
- `verify_workshop.py`: instructor checks using the actual local files, without fake data.
- `WORKSHOP.md`, `HINTS.md`, `DASHBOARD.md`, `INSTRUCTOR.md`: guided lab and teaching notes.

## Troubleshooting

- **A BLANK message:** replace `...` with a word-bank answer. Keep quotes around text.
- **Missing/empty raw file:** run `prepare-data` or follow Data setup above.
- **Missing output file / API returns 503:** run stages 1, 2, and 3 in order.
- **No module named pandas/fastapi/uvicorn/httpx:** activate `.venv`, then rerun the install command.
- **Cannot find a script:** open the terminal in the inner `movielens-workshop` folder.
- **SyntaxError:** check quotes and accidental edits. Compare with `completed/`.
- **Port 8000 already in use:** stop an earlier workshop server with Ctrl+C and retry.
- **Conflicting movie IDs:** inspect the input; the script deliberately stops instead of guessing a title.
- **Unexpected removal counts:** open `output/cleaning_report.json` and compare the raw input.
- **Old dashboard:** rerun analytics and reimport `output/dashboard_data.json` into the dashboard.

Rerunning ingestion removes downstream outputs; rerunning cleaning removes analytics outputs.
This prevents older metrics from appearing to come from the new input. An API request during
that interval returns 503 until analytics finishes. Run stages sequentially with the API stopped
for the simplest workflow. Generated files are overwritten; original raw files are preserved.

## Data meaning and attribution

A rating is one user's opinion, not evidence of a stream, sale, or subscription.
Popularity here means number of ratings. Users are anonymous IDs in a selected MovieLens sample.
The timestamps are historical rating dates, not movie release dates. No commercial conclusions
or claims about all streaming customers should be drawn from this teaching exercise.

Source: GroupLens MovieLens Latest Small. See `ml-latest-small/README.txt` for the
full usage conditions, including commercial-use restrictions. For publications, acknowledge:
F. Maxwell Harper and Joseph A. Konstan (2015), *The MovieLens Datasets: History and Context*,
https://doi.org/10.1145/2827872.

Helpful references: https://grouplens.org/datasets/movielens/latest/ and
https://fastapi.tiangolo.com/tutorial/first-steps/.
