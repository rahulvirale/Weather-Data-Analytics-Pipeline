
import requests


# Open-Meteo Historical Weather API
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def get_historical_weather(latitude, longitude, start_date, end_date):
    """
    Get historical hourly weather data from Open-Meteo
    for a specific latitude and longitude.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,

        # Date range
        "start_date": start_date,
        "end_date": end_date,

        # Historical hourly weather variables
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "rain,"
            "weather_code,"
            "cloud_cover,"
            "pressure_msl,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "wind_gusts_10m"
        ),

        # India timezone
        "timezone": "Asia/Kolkata",

        # Units
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )

        # Raise error if API request failed
        response.raise_for_status()

        # Convert JSON response into Python dictionary
        data = response.json()

        return data

    except requests.exceptions.RequestException as error:

        print(f"Historical weather API request failed: {error}")

        return None


if __name__ == "__main__":

    # Test with Pune
    latitude = 18.5204
    longitude = 73.8567

    # Example historical date range
    start_date = "2025-01-01"
    end_date = "2025-01-07"

    weather_data = get_historical_weather(
        latitude,
        longitude,
        start_date,
        end_date
    )

    if weather_data:

        print("Historical Weather Data:")

        print(
            f"Location: "
            f"{weather_data['latitude']}, "
            f"{weather_data['longitude']}"
        )

        print(
            f"Timezone: "
            f"{weather_data['timezone']}"
        )

        print(
            f"Number of hourly records: "
            f"{len(weather_data['hourly']['time'])}"
        )

        print(
            "First timestamp:",
            weather_data["hourly"]["time"][0]
        )

        print(
            "First temperature:",
            weather_data["hourly"]["temperature_2m"][0]
        )

