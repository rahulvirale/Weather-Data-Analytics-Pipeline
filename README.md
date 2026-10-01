# 🌦️ Weather Data Analytics Pipeline

An end-to-end **data engineering and analytics pipeline** that automatically collects current and historical weather data from the **Open-Meteo API**, processes and transforms the data using **Python**, stores structured data in **MySQL**, automates execution using **Windows Task Scheduler**, and visualizes the results through **Power BI**.

---

## 📌 Project Overview

This project demonstrates a complete data pipeline:

```text
Open-Meteo API
      ↓
Python Data Ingestion
      ↓
Raw JSON Storage
      ↓
Data Transformation
      ↓
Processed JSON
      ↓
MySQL Database
      ↓
Power BI Dashboard
```

The entire pipeline is automated using **Windows Task Scheduler**, allowing the weather data to be updated without manually running the Python scripts.

The project works with two types of weather data:

### Current Weather

Provides the latest weather conditions for five cities:

* Mumbai
* Kolhapur
* Pune
* Sangli
* Jalgaon

The current-weather table maintains **one latest record per city**, resulting in five current records.

### Historical Weather

Collects **30 days of hourly weather data** for the same five cities.

```text
5 Cities × 30 Days × 24 Hours
= 3,600 hourly records
```

The historical dataset is maintained as a rolling 30-day window.

---

# 🏗️ Architecture

```text
                     ┌─────────────────────────┐
                     │ Windows Task Scheduler  │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ Python Pipeline         │
                     │ Orchestration           │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ Open-Meteo API          │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ Raw JSON Data           │
                     │ data/raw/               │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ Python Transformation   │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ Processed JSON          │
                     │ data/processed/         │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ MySQL Database          │
                     │                         │
                     │ current_weather         │
                     │ historical_weather      │
                     └────────────┬────────────┘
                                  ↓
                     ┌─────────────────────────┐
                     │ Power BI Dashboard      │
                     └─────────────────────────┘
```

---

# 🛠️ Technology Stack

| Technology                 | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| **Python 3.13**            | Pipeline development, ingestion and transformation |
| **Open-Meteo API**         | Weather data source                                |
| **Requests**               | HTTP API communication                             |
| **JSON**                   | Configuration and raw API data storage             |
| **MySQL**                  | Structured data storage                            |
| **SQLAlchemy**             | Python–MySQL database connection                   |
| **Windows Task Scheduler** | Pipeline automation                                |
| **Power BI**               | Data visualization and analytics                   |
| **SQL**                    | Database schema, indexes and views                 |

---

# 📂 Project Structure

```text
Weather-Data-Analytics-Pipeline/
│
├── config/
│   └── cities.json
│
├── data/
│   ├── raw/
│   │   ├── current/
│   │   └── historical/
│   │
│   └── processed/
│       ├── current/
│       └── historical/
│
├── src/
│   ├── api/
│   │   ├── current_weather.py
│   │   └── historical_weather.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── insert_weather.py
│   │   └── insert_historical.py
│   │
│   ├── transformation/
│   │   ├── transformation_current.py
│   │   └── transformation_historical.py
│   │
│   ├── main_current.py
│   └── main_historical.py
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_indexes.sql
│   ├── 03_views.sql
│   ├── 04_create_historical_table.sql
│   └── 05_historical_indexes.sql
│
├── scheduler/
│   ├── run_pipeline.py
│   └── run_current_pipeline.py
│
├── requirements.txt
└── README.md
```

---

# 🔄 Data Pipeline

## 1. City Configuration

The pipeline uses:

```text
config/cities.json
```

to store the configured cities and their latitude/longitude coordinates.

This allows the pipeline to dynamically process the configured cities instead of hard-coding city information throughout the Python code.

---

## 2. Data Ingestion

Python reads the city configuration and calls the Open-Meteo API for each city.

For current weather, the pipeline uses:

```text
Open-Meteo Forecast API
```

For historical weather, it uses:

```text
Open-Meteo Archive API
```

The API provides weather variables such as:

* Temperature
* Apparent temperature
* Relative humidity
* Precipitation
* Rain
* Weather code
* Cloud cover
* Atmospheric pressure
* Wind speed
* Wind direction
* Wind gusts

---

## 3. Raw Data Storage

The original API responses are preserved as JSON files.

```text
data/
└── raw/
    ├── current/
    └── historical/
```

Keeping the raw API response provides a source layer that can be used for debugging, validation, and reprocessing if required.

---

## 4. Data Transformation

The raw API responses are transformed into structured records using Python.

Example fields include:

```text
city
latitude
longitude
timezone
weather_time
temperature_c
apparent_temperature_c
humidity_pct
precipitation_mm
rain_mm
weather_code
weather_description
cloud_cover_pct
pressure_msl_hpa
wind_speed_kmh
wind_direction_deg
wind_gusts_kmh
```

The transformation layer also converts numerical WMO weather codes into human-readable weather descriptions.

For example:

```text
weather_code
      ↓
weather_description
      ↓
Rain / Clear Sky / Cloudy / Thunderstorm / ...
```

---

# 🗄️ MySQL Database

After transformation, the structured records are loaded into MySQL.

The project separates the data into two main tables:

```text
current_weather
historical_weather
```

## Current Weather Table

The current-weather pipeline represents the latest available weather snapshot.

The process is:

```text
Delete previous current records
            ↓
Insert latest records
            ↓
Commit transaction
```

The result is:

```text
5 cities
↓
5 latest weather records
```

The table contains fields such as:

```text
weather_id
city
latitude
longitude
timezone
weather_time
temperature_c
apparent_temperature_c
humidity_pct
precipitation_mm
rain_mm
weather_code
weather_description
cloud_cover_pct
pressure_msl_hpa
wind_speed_kmh
wind_direction_deg
wind_gusts_kmh
created_at
```

The distinction between timestamps is important:

* `weather_time` → time of the weather observation
* `created_at` → time when the record was stored in MySQL

---

# 📊 Historical Weather Data

The historical pipeline retrieves hourly weather data for the latest 30-day period.

```text
5 cities
×
30 days
×
24 hours
=
3,600 records
```

The historical dataset therefore provides a time-series foundation for analysis.

The historical table also uses a unique constraint/index based on:

```text
(city, weather_time)
```

This prevents duplicate records for the same city and timestamp.

---

# 🔁 Rolling 30-Day Window

The historical dataset is designed as a rolling 30-day window.

Conceptually:

```text
Current Day
    ↓
Latest 30 Days
    ↓
Older data removed
    ↓
Latest data inserted
```

As time progresses, the historical dataset moves forward:

```text
Day 1  → Day 30
Day 2  → Day 31
Day 3  → Day 32
...
```

This keeps the historical dataset focused on recent weather behavior.

---

# ⚙️ Automation

The complete pipeline is automated using **Windows Task Scheduler**.

Instead of manually executing Python scripts, Windows starts the pipeline according to the configured schedule.

```text
Windows Task Scheduler
          ↓
Python Orchestrator
          ↓
Weather Pipeline
```

The scheduler starts the appropriate orchestration script, which then executes the required pipeline stages.

### Current Pipeline

```text
Task Scheduler
      ↓
run_current_pipeline.py
      ↓
main_current.py
      ↓
Open-Meteo API
      ↓
Raw JSON
      ↓
Transformation
      ↓
Processed JSON
      ↓
MySQL
```

The scheduled task is considered successful when the Python process completes successfully.

---

# 📈 Power BI Analytics

Power BI acts as the visualization and analytics layer.

It connects to the structured MySQL database rather than directly consuming the raw API responses.

```text
MySQL
  ↓
Power BI
  ↓
Dashboard
```

The dashboard can use both:

```text
current_weather
```

and:

```text
historical_weather
```

to provide current conditions and historical context.

### Example Analytics

The dataset supports visualizations such as:

* Current temperature by city
* Humidity comparison
* Wind speed
* Rainfall
* Temperature trends
* Humidity trends
* Weather conditions
* Pressure trends
* Cloud cover
* City-level filtering
* Historical time-series analysis

---

# 📊 Current vs Historical Data

The project intentionally separates current and historical data.

| Dataset            | Purpose               | Approximate Size |
| ------------------ | --------------------- | ---------------: |
| Current Weather    | Latest conditions     |        5 records |
| Historical Weather | Recent hourly history |    3,600 records |

### Current Data

Answers:

> **What is the weather right now?**

### Historical Data

Answers:

> **How has the weather behaved over the recent past?**

Together they provide both current state and historical context.

---

# 🧠 Data Engineering Concepts Demonstrated

This project demonstrates several practical data engineering concepts:

* REST API integration
* HTTP requests
* JSON data handling
* Configuration-driven pipelines
* Raw data preservation
* Data transformation
* Data normalization
* Database design
* MySQL
* SQL
* Database indexes
* Unique constraints
* Duplicate prevention
* Transaction handling
* Time-series data
* Rolling data windows
* Pipeline orchestration
* Automated scheduling
* Logging
* Business intelligence
* Data visualization

---

# 🔐 Data Flow Design

The project follows a layered data architecture:

```text
SOURCE
  ↓
Open-Meteo API
  ↓
INGESTION
  ↓
Python + Requests
  ↓
RAW LAYER
  ↓
JSON
  ↓
TRANSFORMATION
  ↓
Python
  ↓
PROCESSED LAYER
  ↓
JSON
  ↓
STORAGE
  ↓
MySQL
  ↓
ANALYTICS
  ↓
Power BI
```

Each technology has a specific responsibility:

| Layer          | Responsibility                              |
| -------------- | ------------------------------------------- |
| Open-Meteo     | Provides weather data                       |
| Python         | Ingestion, transformation and orchestration |
| JSON           | Configuration and raw/intermediate storage  |
| MySQL          | Structured persistent storage               |
| SQL            | Schema, indexes and database logic          |
| Task Scheduler | Automated execution                         |
| Power BI       | Analytics and visualization                 |

---

# 🚀 How to Run the Project

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Weather-Data-Analytics-Pipeline
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Cities

Update:

```text
config/cities.json
```

with the required city names and coordinates.

## 5. Configure MySQL

Create the required database and execute the SQL scripts in the `sql/` directory.

The database connection configuration should be provided through the project's database connection setup.

> **Security:** Do not commit database passwords, credentials, API keys, or other secrets to GitHub.

## 6. Run the Current Pipeline

```bash
python src/main_current.py
```

## 7. Run the Historical Pipeline

```bash
python src/main_historical.py
```

## 8. Run Through the Scheduler

The scheduler scripts are located in:

```text
scheduler/
```

Windows Task Scheduler can be configured to execute the orchestration scripts automatically.

---

# 🗃️ SQL Layer

The `sql/` directory contains scripts for setting up the database.

```text
sql/
├── 01_create_tables.sql
├── 02_indexes.sql
├── 03_views.sql
├── 04_create_historical_table.sql
└── 05_historical_indexes.sql
```

These scripts handle:

* Table creation
* Index creation
* Database views
* Historical table setup
* Historical indexes
* Query optimization
* Duplicate protection

---

# 🔍 Example SQL Queries

Get the latest weather data:

```sql
SELECT *
FROM current_weather;
```

Get temperature by city:

```sql
SELECT
    city,
    temperature_c
FROM current_weather;
```

Calculate average historical temperature:

```sql
SELECT
    city,
    AVG(temperature_c) AS avg_temperature
FROM historical_weather
GROUP BY city;
```

Analyze historical weather for a specific city:

```sql
SELECT
    weather_time,
    temperature_c,
    humidity_pct,
    rain_mm
FROM historical_weather
WHERE city = 'Pune'
ORDER BY weather_time;
```

---

# 🎯 Project Objectives

The main objectives of this project are to:

1. Collect weather data automatically.
2. Preserve raw API responses.
3. Transform API data into analytics-ready records.
4. Store structured data in MySQL.
5. Maintain separate current and historical datasets.
6. Prevent duplicate historical records.
7. Maintain a rolling 30-day historical dataset.
8. Automate pipeline execution.
9. Build an analytics layer using Power BI.
10. Demonstrate an end-to-end data engineering workflow.

---

# 💡 Key Project Highlights

### Configuration-driven

Cities are maintained in a JSON configuration file rather than being hard-coded throughout the pipeline.

### Raw + Processed Architecture

The original API responses are preserved before transformation.

### Current Snapshot

The current table maintains the latest weather conditions for the configured cities.

### Historical Time Series

Hourly weather data is maintained for a rolling 30-day period.

### Duplicate Protection

Historical records are protected using a city + timestamp uniqueness rule.

### Automated Execution

Windows Task Scheduler automatically triggers the pipeline.

### Analytics Ready

The processed data is stored in MySQL and consumed by Power BI for visualization and analysis.

---

# 🧩 End-to-End Workflow

The complete workflow can be summarized as:

```text
┌──────────────────────────┐
│ Windows Task Scheduler   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Python Orchestration     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Open-Meteo API           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Raw JSON Storage         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Python Transformation    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Processed JSON           │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ MySQL Database           │
│                          │
│ Current + Historical     │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Power BI                 │
│ Dashboard & Analytics    │
└──────────────────────────┘
```

---

# 📌 Project Outcome

This project goes beyond simply creating a weather dashboard.

It implements a complete automated data pipeline covering:

```text
Data Source
     ↓
Data Ingestion
     ↓
Raw Data Storage
     ↓
Data Transformation
     ↓
Database Storage
     ↓
Automation
     ↓
Business Intelligence
```

The result is an end-to-end **Weather Data Analytics Pipeline** capable of continuously collecting, processing, storing, and analyzing weather data.

---

# 👨‍💻 Skills Demonstrated

**Programming**

* Python
* Object-oriented and modular scripting
* API integration
* JSON processing

**Data Engineering**

* ETL/ELT concepts
* Data ingestion
* Data transformation
* Pipeline orchestration
* Data validation
* Time-series data processing

**Database**

* MySQL
* SQL
* Database schema design
* Indexing
* Unique constraints
* Transactions

**Automation**

* Windows Task Scheduler
* Scheduled Python execution
* Pipeline logging

**Analytics**

* Power BI
* Dashboard development
* Time-series analysis
* Data visualization

---

# 📄 License

This project is intended for educational and portfolio purposes.

---

# ⭐ Summary

**Weather Data Analytics Pipeline** is an automated end-to-end data engineering project that:

```text
Collects weather data
        ↓
Stores raw API responses
        ↓
Transforms the data
        ↓
Loads it into MySQL
        ↓
Runs automatically on schedule
        ↓
Feeds Power BI
        ↓
Produces weather analytics
```

It demonstrates how multiple technologies can be integrated to build a practical, automated data pipeline from **API ingestion to business intelligence**.
