import json
from pathlib import Path
from datetime import datetime


# ============================================================
# Project directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RAW_DIR = BASE_DIR / "data" / "raw" / "historical"
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "historical"


# ============================================================
# Weather code mapping
# Open-Meteo WMO weather interpretation codes
# ============================================================

WEATHER_CODE_MAP = {
    0: "Clear sky",

    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",

    45: "Fog",
    48: "Depositing rime fog",

    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",

    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",

    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",

    66: "Light freezing rain",
    67: "Heavy freezing rain",

    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",

    77: "Snow grains",

    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",

    85: "Slight snow showers",
    86: "Heavy snow showers",

    95: "Thunderstorm",

    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


# ============================================================
# Load one raw JSON file
# ============================================================

def load_raw_weather(file_path):
    """
    Load a raw historical weather JSON file.

    Parameters
    ----------
    file_path : Path
        Path to the raw JSON file.

    Returns
    -------
    dict
        Raw historical weather data.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# Transform one city's historical weather data
# ============================================================

def transform_weather(raw_data):
    """
    Transform raw Open-Meteo historical weather JSON
    into flat database-ready dictionaries.

    Historical weather contains hourly arrays,
    so one city produces multiple records.
    """

    hourly = raw_data.get("hourly", {})

    times = hourly.get("time", [])

    transformed_records = []

    for index in range(len(times)):

        weather_code = hourly.get(
            "weather_code", []
        )[index]

        transformed_data = {
            # ----------------------------------------------------
            # Location information
            # ----------------------------------------------------

            "city": raw_data.get("city"),

            "latitude": raw_data.get("latitude"),

            "longitude": raw_data.get("longitude"),

            "timezone": raw_data.get("timezone"),

            # ----------------------------------------------------
            # Weather timestamp
            # ----------------------------------------------------

            "weather_time": times[index],

            # ----------------------------------------------------
            # Temperature
            # ----------------------------------------------------

            "temperature_c": hourly.get(
                "temperature_2m", []
            )[index],

            "apparent_temperature_c": hourly.get(
                "apparent_temperature", []
            )[index],

            # ----------------------------------------------------
            # Humidity
            # ----------------------------------------------------

            "humidity_pct": hourly.get(
                "relative_humidity_2m", []
            )[index],

            # ----------------------------------------------------
            # Precipitation
            # ----------------------------------------------------

            "precipitation_mm": hourly.get(
                "precipitation", []
            )[index],

            "rain_mm": hourly.get(
                "rain", []
            )[index],

            # ----------------------------------------------------
            # Weather condition
            # ----------------------------------------------------

            "weather_code": weather_code,

            "weather_description": WEATHER_CODE_MAP.get(
                weather_code,
                "Unknown"
            ),

            # ----------------------------------------------------
            # Cloud / pressure
            # ----------------------------------------------------

            "cloud_cover_pct": hourly.get(
                "cloud_cover", []
            )[index],

            "pressure_msl_hpa": hourly.get(
                "pressure_msl", []
            )[index],

            # ----------------------------------------------------
            # Wind
            # ----------------------------------------------------

            "wind_speed_kmh": hourly.get(
                "wind_speed_10m", []
            )[index],

            "wind_direction_deg": hourly.get(
                "wind_direction_10m", []
            )[index],

            "wind_gusts_kmh": hourly.get(
                "wind_gusts_10m", []
            )[index],
        }

        transformed_records.append(
            transformed_data
        )

    return transformed_records


# ============================================================
# Transform all historical weather files
# ============================================================

def transform_all_historical_weather():
    """
    Read all raw historical-weather JSON files and
    transform them into flat records.
    """

    if not RAW_DIR.exists():

        print(
            f"Raw data directory does not exist: {RAW_DIR}"
        )

        return []

    json_files = list(
        RAW_DIR.glob("*.json")
    )

    if not json_files:

        print(
            f"No JSON files found in: {RAW_DIR}"
        )

        return []

    transformed_records = []

    print(
        "Starting historical weather transformation..."
    )

    print()

    for file_path in json_files:

        print(
            f"Processing: {file_path.name}"
        )

        try:

            raw_data = load_raw_weather(
                file_path
            )

            records = transform_weather(
                raw_data
            )

            transformed_records.extend(
                records
            )

            print(
                f"✓ {raw_data.get('city')} transformed "
                f"({len(records)} hourly records)"
            )

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            IndexError
        ) as error:

            print(
                f"✗ Failed to transform "
                f"{file_path.name}: {error}"
            )

    print()

    print("--------------------------------")

    print(
        "Historical transformation completed"
    )

    print("--------------------------------")

    print(
        f"Successful files: {len(json_files)}"
    )

    print(
        f"Total hourly records: "
        f"{len(transformed_records)}"
    )

    return transformed_records


# ============================================================
# Save transformed data
# ============================================================

def save_transformed_data(records):
    """
    Save transformed historical records as a JSON file.

    This is useful for checking the transformation
    before inserting data into SQL.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        PROCESSED_DIR /
        "historical_weather.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4
        )

    print()

    print(
        f"Transformed data saved to: {output_file}"
    )


# ============================================================
# Main
# ============================================================

def main():

    records = (
        transform_all_historical_weather()
    )

    if records:

        save_transformed_data(
            records
        )

        print()

        print(
            "Historical transformation successful."
        )

    else:

        print()

        print(
            "No historical records were transformed."
        )


# ============================================================
# Run directly
# ============================================================

if __name__ == "__main__":
    main()