import json
from pathlib import Path

from api.historical_weather import get_historical_weather


# --------------------------------------------------
# Project directories
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CITIES_FILE = BASE_DIR / "config" / "cities.json"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "historical"


# --------------------------------------------------
# Historical date range
# --------------------------------------------------

START_DATE = "2025-01-01"
END_DATE = "2025-01-07"


# --------------------------------------------------
# Load cities
# --------------------------------------------------

def load_cities():
    """
    Load city information from config/cities.json.
    """

    with open(CITIES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["cities"]


# --------------------------------------------------
# Save raw historical weather
# --------------------------------------------------

def save_raw_weather(city_name, weather_data):
    """
    Save the raw Open-Meteo historical response
    for a city as JSON.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{city_name.lower()}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(weather_data, file, indent=4)

    print(f"Saved: {output_file}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    """
    Get historical weather for all configured cities.
    """

    print("Starting historical weather collection...")
    print()

    print(f"Date range: {START_DATE} to {END_DATE}")
    print()

    cities = load_cities()

    print(f"Found {len(cities)} cities.")
    print()

    successful = 0
    failed = 0

    for city in cities:

        city_name = city["city"]
        latitude = city["latitude"]
        longitude = city["longitude"]

        print(f"Getting historical weather for {city_name}...")

        weather_data = get_historical_weather(
            latitude=latitude,
            longitude=longitude,
            start_date=START_DATE,
            end_date=END_DATE
        )

        if weather_data:

            # Add city information to the raw response
            weather_data["city"] = city_name

            save_raw_weather(
                city_name,
                weather_data
            )

            successful += 1

            print(f"✓ {city_name} completed")
            print()

        else:

            failed += 1

            print(f"✗ Failed to get historical weather for {city_name}")
            print()

    print("--------------------------------")
    print("Historical weather collection completed")
    print("--------------------------------")
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Total:      {len(cities)}")
    print()
    print("Raw data location:")
    print(OUTPUT_DIR)


# --------------------------------------------------
# Run program
# --------------------------------------------------

if __name__ == "__main__":
    main()