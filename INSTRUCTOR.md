# Instructor preparation and pacing

## Before the event

1. Install requirements in a Python 3.10+ virtual environment and prepare real inputs.
2. Run `python verify_workshop.py`. This runs the completed pipeline and checks the API.
3. Rehearse `python run_workshop.py api --completed` and the `/docs` page. Stop it afterward.
4. Build or rehearse a Sites dashboard with `output/dashboard_data.json` in the account
   you will use. Confirm file import and Sites availability before students arrive.
5. Distribute this entire folder, including the GroupLens README/license. Keep `.venv/`
   and `__pycache__/` out of the download; students create their own environment.
6. Keep completed files available as a recovery option. Student scripts deliberately
   retain nine blanks even after you run the completed pipeline.

Plan about 75–90 minutes after setup. Demonstrate the concept and one expected
output, allow silent work, show the checkpoint, and move on. No live coding or
continuous question prompts are required. Setup should happen before the session.

## Teaching emphasis

- Raw data: identify a row, column, and shared movie ID.
- Ingestion: reading and checking a file is a distinct step.
- Cleaning: dependable data can already be clean; zero removals is a valid result.
- Analytics: count and average answer different questions.
- API: a URL returns the same prepared metrics; it does not perform machine learning.
- Dashboard: a view helps people inspect those metrics, but cannot create evidence.

Use the full scripts as read-along material; beginners edit only marked blanks.
Do not require students to explain every pandas expression. Comments identify
what each section does, and HINTS.md contains exact replacements.

## Decisions you may want to change later

- Repeated user/movie pairs keep the latest timestamp; tied timestamps keep the last row.
- Invalid IDs, blank titles, invalid scores/dates, and unmatched ratings are removed and counted.
- Conflicting movie IDs stop the run rather than choosing a catalog record silently.
- Genre averages are rating-weighted; multi-genre rating counts overlap.
- Monthly outputs contain observed months only. Activity is rating activity, not watch activity.
- Movie average scores are rounded to four decimals for export; the dashboard may display two.
- API movie requests default to 20 ratings and return at most 100 rows.

To change pipeline rules, update both the student and completed versions, the hints
if needed, and the expected checks. The shared helper manages I/O errors, not business logic.
The API has no authentication or hosting setup; it is for local teaching.

## Recovery

If several students fall behind, have them run
`python run_workshop.py pipeline --completed`, then rejoin at the API/dashboard stage.
If Sites is unavailable, inspect `/docs` and the output files; clearly identify the
Site activity as pending rather than claiming the dashboard is complete.
