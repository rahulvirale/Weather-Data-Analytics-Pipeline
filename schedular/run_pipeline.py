import subprocess
import sys
import os
import logging
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Log directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file
LOG_FILE = LOG_DIR / "pipeline.log"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def run_script(script_path):

    logging.info("=" * 60)
    logging.info(f"Running: {script_path}")
    logging.info("=" * 60)

    # Check whether the script exists
    if not script_path.exists():
        logging.error(f"Script not found: {script_path}")
        sys.exit(1)

    try:

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            env=env
        )

        # Read output line by line
        for line in process.stdout:
            line = line.rstrip()

            if line:
                logging.info(line)

        process.wait()

        if process.returncode != 0:
            logging.error(
                f"Pipeline failed while running: {script_path}"
            )
            sys.exit(process.returncode)

        logging.info(
            f"Completed successfully: {script_path}"
        )

    except Exception as error:

        logging.exception(
            f"Unexpected error while running {script_path}: {error}"
        )

        sys.exit(1)


def main():

    logging.info("")
    logging.info("Starting weather data pipeline...")

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

    logging.info("=" * 60)
    logging.info("Weather data pipeline completed successfully.")
    logging.info("=" * 60)


if __name__ == "__main__":
    main()