import json
from pathlib import Path

from connection import engine
from sqlalchemy import text


# ============================================================
# Project directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "historical"
    / "historical_weather.json"
)


# ============================================================
# Load transformed historical weather data
# ============================================================

def load_weather_data():

    with open(
        PROCESSED_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# Insert historical weather data
# ============================================================

def insert_weather_data(records):

    insert_query = """
        INSERT INTO historical_weather (
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

    with engine.begin() as connection:

        for record in records:

            connection.execute(
                text(insert_query),
                record
            )

    print(
        f"{len(records)} historical weather records "
        f"inserted successfully."
    )


# ============================================================
# Main
# ============================================================

def main():

    print(
        "Loading transformed historical weather data..."
    )

    records = load_weather_data()

    print(
        f"Found {len(records)} records."
    )

    if not records:

        print(
            "No historical weather records found."
        )

        return

    print(
        "Inserting historical records into MySQL..."
    )

    insert_weather_data(records)


# ============================================================
# Run directly
# ============================================================

if __name__ == "__main__":
    main()