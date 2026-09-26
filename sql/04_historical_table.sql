use weather;
CREATE TABLE IF NOT EXISTS historical_weather (
    weather_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    timezone VARCHAR(50),
    weather_time DATETIME NOT NULL,
    temperature_c DECIMAL(5,2),
    apparent_temperature_c DECIMAL(5,2),
    humidity_pct DECIMAL(5,2),
    precipitation_mm DECIMAL(8,2),
    rain_mm DECIMAL(8,2),
    weather_code INT,
    weather_description VARCHAR(100),
    cloud_cover_pct DECIMAL(5,2),
    pressure_msl_hpa DECIMAL(8,2),
    wind_speed_kmh DECIMAL(8,2),
    wind_direction_deg DECIMAL(6,2),
    wind_gusts_kmh DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
