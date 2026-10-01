CREATE INDEX idx_historical_weather_city
ON historical_weather (city);

CREATE INDEX idx_historical_weather_time
ON historical_weather (weather_time);

CREATE UNIQUE INDEX idx_historical_weather_city_time
ON historical_weather (city, weather_time);

SHOW INDEX FROM historical_weather;

select count(*) from historical_weather;