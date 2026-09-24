import json
from pathlib import Path

from connection import engine
from sqlalchemy import text


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "current"
    / "current_weather.json"
)


# --------------------------------------------------
# Load transformed weather data
# --------------------------------------------------

def load_weather_data():
    with open(PROCESSED_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Insert data into MySQL
# --------------------------------------------------

def insert_weather_data(records):

    insert_query = """
        INSERT INTO current_weather (
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
                text(insert_query),record
            )

    print(f"{len(records)} weather records inserted successfully.")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("Loading transformed weather data...")

    records = load_weather_data()

    print(f"Found {len(records)} records.")

    if not records:
        print("No weather records found.")
        return

    print("Inserting records into MySQL...")

    insert_weather_data(records)


if __name__ == "__main__":
    main()