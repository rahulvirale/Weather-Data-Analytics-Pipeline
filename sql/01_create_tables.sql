create database weather;
use weather;
-- ============================================================
-- Weather Analytics Pipeline
-- Current Weather Table
-- MySQL
-- ============================================================

CREATE TABLE IF NOT EXISTS current_weather (

    -- Primary key
    weather_id INT AUTO_INCREMENT PRIMARY KEY,

    -- City information
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    timezone VARCHAR(50),

    -- Weather observation time
    weather_time DATETIME NOT NULL,

    -- Temperature
    temperature_c DECIMAL(5,2),
    apparent_temperature_c DECIMAL(5,2),

    -- Humidity
    humidity_pct DECIMAL(5,2),

    -- Precipitation
    precipitation_mm DECIMAL(8,2),
    rain_mm DECIMAL(8,2),

    -- Weather condition
    weather_code INT,
    weather_description VARCHAR(100),

    -- Cloud and pressure
    cloud_cover_pct DECIMAL(5,2),
    pressure_msl_hpa DECIMAL(8,2),

    -- Wind
    wind_speed_kmh DECIMAL(8,2),
    wind_direction_deg DECIMAL(6,2),
    wind_gusts_kmh DECIMAL(8,2),

    -- Database insertion timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
