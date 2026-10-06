# Verification record

Verified on October 5, 2026 using the actual supplied MovieLens Latest Small files.
Environment: pandas 2.3.1, FastAPI 0.115.13, Uvicorn 0.34.3, and httpx 0.27.2.

- Completed ingestion, cleaning, and analytics passed, individually and through the helper runner.
- All Python exercise and answer files passed syntax checks.
- Filled student pipeline exports exactly matched completed pipeline exports.
- The filled student API returned the same summary as the completed API.
- Raw input file hashes remained unchanged during pipeline verification.
- Movie/month totals, user count, average score, one independently calculated genre,
  removal accounting, and unique user/movie pairs passed checks.
- All API routes, API documentation, and the schema endpoint returned successful responses
  using FastAPI's in-process test client.
- Movie filters, both ranking choices, request limits, and an empty result passed checks.
- Invalid parameters returned 422; missing analytics returned 503.
- Unfilled exercises, missing raw files, and empty raw files stopped with clear instructions.
- No fabricated data was used in verification.

Results: 9,742 catalog movies, 9,724 rated movies, 100,836 ratings, 610 users,
3.5016 average rating, and observed rating months from 1996-03 through 2018-09.
The supplied snapshot required zero row removals.

Student files still contain nine intentional blanks. The completed files run immediately
when dependencies are installed. Generated results are already available in output/.

The Sites activity is documented with a real JSON export and a validation checklist;
a Site was not created or published as part of this repository implementation.
A deployed backend and a browser-to-hosted-API connection were not tested.

Rerun: python verify_workshop.py
