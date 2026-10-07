# From raw movie data to a product dashboard

A guided beginner lab for a fictional streaming team. You build a small ETL
pipeline (Extract, Transform, Load) on real MovieLens data, then give the result
to ChatGPT to build a dashboard. No machine learning or live coding is needed.

**Start here:** set up Python, then open `WORKSHOP.md`.
Only replace the lines marked **BLANK** or `#[FILL]` in `scripts/`. There are nine in total.
If you get stuck, use `HINTS.md` or read the matching full file in `completed/`.

## 1. Open this folder

Open this folder in your editor and open its terminal. You should see
`requirements.txt`, `scripts/`, and `run_workshop.py`. All commands run from here.
Type each command and press Enter. Do not type the surrounding ``` marks.

## 2. Set up Python once

Use Python 3.10 or newer. Check with `python3 --version` on macOS/Linux or
`py --version` on Windows. If Python is missing, install it from https://www.python.org/downloads/.
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

Activate the environment again whenever you open a new terminal. If PowerShell
blocks activation, use `.venv\Scripts\python.exe` in place of `python`.

## 3. Data setup

`data/movies.csv` and `data/ratings.csv` are the raw inputs. Do not edit them.
If they are missing or empty, download **MovieLens Latest Small** from
https://grouplens.org/datasets/movielens/latest/, unzip it, and copy its
`movies.csv` and `ratings.csv` into `data/`.

The included snapshot has **9,742 movies, 100,836 ratings, and 610 users**.

## What is in this folder?

- `data/`: raw movies and ratings, plus the GroupLens license (`README.txt`).
- `scripts/01_ingest.py`: **Extract** — read the raw CSV files.
- `scripts/02_clean.py`: **Transform** — validate rows, remove duplicates, add readable dates.
- `scripts/03_analyze.py`: **Transform + Load** — calculate metrics and save `dashboard_data.json`.
- `scripts/_helpers.py`: shared file checks and readable error messages; leave it alone.
- `completed/`: full answer versions of all three scripts.
- `output/`: generated files; safe to delete and regenerate.
- `run_workshop.py`: runs all three stages in order.
- `verify_workshop.py`: instructor check that everything works.

## Troubleshooting

- **A BLANK message:** replace `...` with a word-bank answer. Keep quotes around text.
- **Missing/empty raw file:** follow Data setup above.
- **Missing output file:** run stages 1, 2, and 3 in order.
- **No module named pandas:** activate `.venv`, then rerun the install command.
- **SyntaxError:** check quotes and accidental edits. Compare with `completed/`.
- **Fell behind:** run `python run_workshop.py --completed` to generate every output.

## Data meaning and attribution

A rating is one user's opinion, not a stream, sale, or subscription.
Popularity here means number of ratings. Users are anonymous IDs.

Source: GroupLens MovieLens Latest Small. See `data/README.txt` for the usage
conditions, including commercial-use restrictions. Citation: F. Maxwell Harper and
Joseph A. Konstan (2015), *The MovieLens Datasets: History and Context*,
https://doi.org/10.1145/2827872.
