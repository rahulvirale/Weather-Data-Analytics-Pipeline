import subprocess
import sys
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


def run_script(script_path):

    print("\n" + "=" * 60)
    print(f"Running: {script_path}")
    print("=" * 60)

    # Check whether the file exists
    if not script_path.exists():
        print(f"\nERROR: Script not found:")
        print(script_path)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR
    )

    if result.returncode != 0:
        print(f"\nPipeline failed while running:")
        print(script_path)
        sys.exit(result.returncode)

    print(f"\nCompleted successfully: {script_path}")


def main():

    print("\nStarting weather data pipeline...")

    # Step 1: Fetch latest 30 days
    run_script(
        BASE_DIR / "src" / "main_historical.py"
    )

    # Step 2: Transform historical data
    run_script(
        BASE_DIR / "src" / "transformation" / "transformation_historical.py"
    )

    # Step 3: Insert data into MySQL
    run_script(
        BASE_DIR / "src" / "database" / "insert_historical.py"
    )

    print("\n" + "=" * 60)
    print("Weather data pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()