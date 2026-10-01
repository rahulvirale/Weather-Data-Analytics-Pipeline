import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def run_script(script_path):
    print("\n" + "=" * 60)
    print(f"Running: {script_path}")
    print("=" * 60)

    if not script_path.exists():
        print(f"\nERROR: Script not found:")
        print(script_path)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR
    )

    if result.returncode != 0:
        print(f"\nPipeline failed while running: {script_path}")
        sys.exit(result.returncode)

    print(f"\nCompleted successfully: {script_path}")


def main():
    print("\nStarting current weather pipeline...")

    run_script(
        BASE_DIR / "src" / "main_current.py"
    )

    run_script(
        BASE_DIR / "src" / "transformation" / "transformation_current.py"
    )

    run_script(
        BASE_DIR / "src" / "database" / "insert_weather.py"
    )

    print("\n" + "=" * 60)
    print("Current weather pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()