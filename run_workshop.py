"""Run stages in order with the same Python environment as this command."""
import argparse
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description="MovieLens workshop helper")
    parser.add_argument("action", choices=["pipeline", "api", "prepare-data"])
    parser.add_argument("--completed", action="store_true", help="Run answer versions instead of student exercises")
    args = parser.parse_args()
    if args.action == "prepare-data":
        import shutil
        # Validate both bundled files before copying; preserve nonempty student data.
        names = ["movies.csv", "ratings.csv"]
        for name in names:
            source = ROOT / "ml-latest-small" / name
            if not source.is_file() or not source.stat().st_size:
                raise SystemExit("STOP: bundled MovieLens files are absent. Follow README.md > Data setup.")
        (ROOT / "data").mkdir(exist_ok=True)
        for name in names:
            target = ROOT / "data" / name
            if target.exists() and target.stat().st_size:
                print(f"Kept existing data/{name}.")
            else:
                shutil.copy2(ROOT / "ml-latest-small" / name, target)
                print(f"Copied original MovieLens file to data/{name}.")
        return
    folder = "completed" if args.completed else "scripts"
    suffix = "_complete" if args.completed else ""
    stages = ["04_api"] if args.action == "api" else ["01_ingest", "02_clean", "03_analyze"]
    for stage in stages:
        print(f"\nRunning {stage} ({folder})...", flush=True)
        result = subprocess.run([sys.executable, str(ROOT / folder / f"{stage}{suffix}.py")], cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)
    if args.action == "pipeline":
        print("\nAll pipeline checkpoints passed. Start the API or open DASHBOARD.md.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped. Your files are saved.")
