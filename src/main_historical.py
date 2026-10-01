import json
from pathlib import Path
from datetime import date, timedelta

from api.historical_weather import get_historical_weather


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
CITIES_FILE = BASE_DIR / "config" / "cities.json"
OUTPUT_DIR = BASE_DIR / "data" / "raw" / "historical"


# Automatically calculate latest 30 days
END_DATE = date.today()
START_DATE = END_DATE - timedelta(days=29)


def load_cities():
    with open(CITIES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["cities"]


def save_raw_weather(city_name, weather_data):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = OUTPUT_DIR / f"{city_name}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(weather_data, file, indent=4)

    print(f"Raw historical data saved for {city_name}")


def main():

    print("Starting historical weather data collection...")
    print(f"Start date: {START_DATE}")
    print(f"End date: {END_DATE}")

    cities = load_cities()

    successful_cities = []
    failed_cities = []

    for city in cities:

        city_name = city["city"]
        latitude = city["latitude"]
        longitude = city["longitude"]

        print(f"\nFetching historical weather for {city_name}...")

        try:

            weather_data = get_historical_weather(
                latitude,
                longitude,
                START_DATE.isoformat(),
                END_DATE.isoformat()
            )

            weather_data["city"] = city_name

            save_raw_weather(city_name, weather_data)

            successful_cities.append(city_name)

        except Exception as error:

            print(f"Failed to fetch data for {city_name}: {error}")

            failed_cities.append(city_name)

    print("\nHistorical weather collection completed.")

    print(f"Successful cities: {len(successful_cities)}")
    print(f"Failed cities: {len(failed_cities)}")

    if successful_cities:
        print("\nSuccessful:")
        for city in successful_cities:
            print(f" - {city}")

    if failed_cities:
        print("\nFailed:")
        for city in failed_cities:
            print(f" - {city}")


if __name__ == "__main__":
    main()