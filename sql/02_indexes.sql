use weather;

CREATE INDEX idx_current_weather_city
ON current_weather (city);

CREATE INDEX idx_current_weather_time
ON current_weather (weather_time);

CREATE INDEX idx_current_weather_city_time
ON current_weather (city, weather_time);

SHOW INDEX FROM current_weather;
