import json
from pathlib import Path

from connection import engine
from sqlalchemy import text


# ---------------------------------------------------------
# Project directories
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "historical"
    / "historical_weather.json"
)


# ---------------------------------------------------------
# Load transformed historical weather data
# ---------------------------------------------------------
def delete_old_records():
    delete_query = """
        DELETE FROM historical_weather
        WHERE weather_time < DATE_SUB(CURDATE(), INTERVAL 29 DAY)
    """

    with engine.begin() as connection:
        result = connection.execute(text(delete_query))

    print(f"{result.rowcount} old historical records deleted.")

def load_weather_data():

    with open(
        PROCESSED_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------
# Insert historical weather data
# ---------------------------------------------------------

def insert_weather_data(records):

    insert_query = """
        INSERT IGNORE INTO historical_weather (
            city,
            latitude,
            longitude,
            timezone,
            weather_time,
            temperature_c,
            apparent_temperature_c,
            humidity_pct,
            precipitation_mm,
            rain_mm,
            weather_code,
            weather_description,
            cloud_cover_pct,
            pressure_msl_hpa,
            wind_speed_kmh,
            wind_direction_deg,
            wind_gusts_kmh
        )
        VALUES (
            :city,
            :latitude,
            :longitude,
            :timezone,
            :weather_time,
            :temperature_c,
            :apparent_temperature_c,
            :humidity_pct,
            :precipitation_mm,
            :rain_mm,
            :weather_code,
            :weather_description,
            :cloud_cover_pct,
            :pressure_msl_hpa,
            :wind_speed_kmh,
            :wind_direction_deg,
            :wind_gusts_kmh
        )
    """

    inserted_count = 0
    skipped_count = 0

    with engine.begin() as connection:

        for record in records:

            result = connection.execute(
                text(insert_query),
                record
            )

            if result.rowcount == 1:
                inserted_count += 1
            else:
                skipped_count += 1

    print(
        f"{inserted_count} new historical records inserted."
    )

    print(
        f"{skipped_count} duplicate records skipped."
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("Loading transformed historical weather data...")
    records = load_weather_data()

    print(f"Found {len(records)} records.")

    if not records:
        print("No historical weather records found.")
        return

    print("Deleting old historical records...")
    delete_old_records()

    print("Inserting historical records into MySQL...")
    insert_weather_data(records)

# ---------------------------------------------------------
# Run program
# ---------------------------------------------------------

if __name__ == "__main__":
    main()