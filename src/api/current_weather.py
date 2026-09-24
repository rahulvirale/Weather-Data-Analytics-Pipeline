
import requests


# Open-Meteo Forecast API
BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(latitude, longitude):
    """
    Get current weather data from Open-Meteo
    for a specific latitude and longitude.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,

        # Current weather variables
        "current": (
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
        print(f"Weather API request failed: {error}")
        return None


if __name__ == "__main__":

    # Test with Pune
    latitude = 18.5204
    longitude = 73.8567

    weather_data = get_current_weather(
        latitude,
        longitude
    )

    if weather_data:
        print("Current Weather Data:")
        print(weather_data["current"])

