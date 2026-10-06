# ChatGPT-assisted dashboard with Sites

## Prepare

Complete analytics first. Find `output/dashboard_data.json`. This is the real
workshop data packaged into one file: summary numbers plus movie, genre, and monthly lists.
Use ChatGPT with the Sites functionality available in your account. The exact UI
can vary; ask it to build a Site and attach this JSON file or provide it through the
available file picker. If the file cannot be read, stop and fix the upload rather
than letting the dashboard invent examples.

You do not need the local Python server for this activity. A published website
cannot fetch your laptop's `127.0.0.1` address; that address refers to whichever
computer is making the request. Importing the JSON avoids API hosting and browser
cross-origin setup during this beginner lab.

## Copy this prompt after attaching the JSON

> Build a beginner-friendly movie rating analytics dashboard using Sites and the
> attached dashboard_data.json. Use only the attached real data. If you cannot
> read it, tell me and stop; do not invent numbers or movies.
>
> Show four summary cards: catalog movies, rated movies, ratings, and users.
> Add a movie list with title, genres, number of ratings, and average rating.
> Let me switch between most rated and highest average, and choose a minimum
> rating count, defaulting to 20. Filter before sorting. Break tied averages by
> rating count descending and then movieId ascending. Display average ratings
> to two decimal places without changing the underlying values.
>
> Add genre rating counts and genre average ratings, plus a monthly rating
> activity chart sorted chronologically. Use the monthly field rating_month.
> Explain that genre totals overlap and these are ratings, not watches or revenue.
> If you insert absent months into the chart, use zero rating count and zero
> active raters. Do not invent average scores for missing periods.
>
> Use plain labels, readable text, clear empty states, and an accessible layout
> that works on a phone. Include GroupLens MovieLens attribution, a link to the
> dataset, and its usage conditions from the supplied source README. Preserve
> those conditions when distributing the data or derived outputs.
> Do not add a recommendation model, sentiment analysis, login, or fabricated data.

## Check the result

1. Compare all four cards with `output/summary.json`.
2. Set the minimum count to 20. Every visible movie must have at least 20 ratings.
3. Sort by highest average. Scores should descend; changing to most rated should
   rank by rating counts instead.
4. Compare one genre with `genre_metrics.csv`. Do not add genre counts together.
5. Check the chart's first and last month against `summary.json`.
6. If your filter matches no movies, expect a helpful empty state, not placeholder rows.

If anything is wrong, tell ChatGPT the exact discrepancy and the expected value
from the output file. After rerunning Python with new data, reimport the new JSON;
the Site uses a snapshot and does not automatically follow changes on your laptop.

## Optional API connection for a later workshop

The API contract is `/summary`, `/movies?limit=10&min_ratings=20&sort=average_rating`,
`/genres`, `/monthly`, and `/dashboard`. A real integration would need a reachable
HTTPS backend and configured allowed origins. This repository starts a local,
read-only server and does not deploy that backend. Use the file import for this lab.
