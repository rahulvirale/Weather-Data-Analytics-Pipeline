import json
from pathlib import Path
from datetime import datetime


# ============================================================
# Project directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RAW_DIR = BASE_DIR / "data" / "raw" / "current"
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "current"


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
    Load a raw weather JSON file.

    Parameters
    ----------
    file_path : Path
        Path to the raw JSON file.

    Returns
    -------
    dict
        Raw weather data.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# Transform one city's weather data
# ============================================================

def transform_weather(raw_data):
    """
    Transform raw Open-Meteo current weather JSON
    into a flat database-ready dictionary.
    """

    current = raw_data.get("current", {})

    weather_code = current.get("weather_code")

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
        "weather_time": current.get("time"),

        # ----------------------------------------------------
        # Temperature
        # ----------------------------------------------------
        "temperature_c": current.get("temperature_2m"),

        "apparent_temperature_c": current.get(
            "apparent_temperature"
        ),

        # ----------------------------------------------------
        # Humidity
        # ----------------------------------------------------
        "humidity_pct": current.get(
            "relative_humidity_2m"
        ),

        # ----------------------------------------------------
        # Precipitation
        # ----------------------------------------------------
        "precipitation_mm": current.get(
            "precipitation"
        ),

        "rain_mm": current.get(
            "rain"
        ),

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
        "cloud_cover_pct": current.get(
            "cloud_cover"
        ),

        "pressure_msl_hpa": current.get(
            "pressure_msl"
        ),

        # ----------------------------------------------------
        # Wind
        # ----------------------------------------------------
        "wind_speed_kmh": current.get(
            "wind_speed_10m"
        ),

        "wind_direction_deg": current.get(
            "wind_direction_10m"
        ),

        "wind_gusts_kmh": current.get(
            "wind_gusts_10m"
        ),
    }

    return transformed_data


# ============================================================
# Transform all current weather files
# ============================================================

def transform_all_current_weather():
    """
    Read all raw current-weather JSON files and transform
    them into flat records.
    """

    if not RAW_DIR.exists():
        print(f"Raw data directory does not exist: {RAW_DIR}")
        return []

    json_files = list(RAW_DIR.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in: {RAW_DIR}")
        return []

    transformed_records = []

    print("Starting current weather transformation...")
    print()

    for file_path in json_files:

        print(f"Processing: {file_path.name}")

        try:
            raw_data = load_raw_weather(file_path)

            transformed_data = transform_weather(
                raw_data
            )

            transformed_records.append(
                transformed_data
            )

            print(
                f"✓ {transformed_data['city']} transformed"
            )

        except (json.JSONDecodeError, KeyError, TypeError) as error:

            print(
                f"✗ Failed to transform "
                f"{file_path.name}: {error}"
            )

    print()
    print("--------------------------------")
    print("Transformation completed")
    print("--------------------------------")
    print(
        f"Successful: {len(transformed_records)}"
    )
    print(
        f"Total files: {len(json_files)}"
    )

    return transformed_records


# ============================================================
# Save transformed data
# ============================================================

def save_transformed_data(records):
    """
    Save transformed records as a JSON file.

    This is useful for checking the transformation
    before inserting data into SQL.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        PROCESSED_DIR /
        "current_weather.json"
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

    records = transform_all_current_weather()

    if records:
        save_transformed_data(records)

        print()
        print("Transformation successful.")

    else:
        print()
        print("No records were transformed.")


# ============================================================
# Run directly
# ============================================================

if __name__ == "__main__":
    main()