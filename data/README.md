# Raw inputs

Use real GroupLens MovieLens Latest Small `movies.csv` and `ratings.csv` here.
If these files are missing or empty, run `python run_workshop.py prepare-data`
from the repository folder. It copies supplied `ml-latest-small/` originals and
preserves nonempty existing inputs. See the root README for manual download instructions.

movies.csv header: movieId,title,genres
ratings.csv header: userId,movieId,rating,timestamp

Do not manually edit these files during the workshop. The pipeline makes working
copies in output/. Keep `ml-latest-small/README.txt` for source attribution and license.
