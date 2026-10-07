"""Run all three pipeline stages in order with the same Python environment."""
import argparse
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description="MovieLens workshop helper")
    parser.add_argument("--completed", action="store_true", help="Run answer versions instead of student exercises")
    args = parser.parse_args()
    folder = "completed" if args.completed else "scripts"
    suffix = "_complete" if args.completed else ""
    for stage in ["01_ingest", "02_clean", "03_analyze"]:
        print(f"\nRunning {stage} ({folder})...", flush=True)
        result = subprocess.run([sys.executable, str(ROOT / folder / f"{stage}{suffix}.py")], cwd=ROOT)
        if result.returncode:
            raise SystemExit(result.returncode)
    print("\nAll pipeline checkpoints passed. Give output/dashboard_data.json to ChatGPT.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped. Your files are saved.")
