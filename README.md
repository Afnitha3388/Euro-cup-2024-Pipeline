# UEFA Euro 2024 Data Pipeline
An end-to-end data engineering pipeline that extracts UEFA Euro 2024 match data from Kaggle, transforms it using Python and Pandas, loads it into PostgreSQL, and visualizes it in Power BI — all orchestrated with Apache Airflow running in Docker.

# Pipeline Architecture

Kaggle Dataset → Extract → Transform → Load → PostgreSQL → Power BI Dashboard
                                ↑
                         Apache Airflow DAG
                         (Docker Container)


# Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline logic |
| Apache Airflow 3.x | Pipeline orchestration |
| Docker | Containerized Airflow environment |
| Pandas | Data transformation |
| PostgreSQL | Data storage |
| SQLAlchemy | Database connection |
| Power BI | Data visualization |
| Kaggle API | Data source |

# Project Structure

├── dags/
│   └── euro_cup.py       ← Airflow DAG (extract, transform, load)
├── docker-compose.yaml   ← Airflow + PostgreSQL setup
└── README.md

# Pipeline Steps

# 1. Extract

Downloads the UEFA Euro 2024 dataset from Kaggle using the Kaggle CLI
Extracts the ZIP file into /opt/airflow/data/Eurocup2024
Returns the folder path to the next task

# 2. Transform

Dynamically discovers all CSV files in the extracted folder using pathlib.glob
For each CSV:
Lowercases and strips column names
Removes duplicates
Drops null values
Converts date columns where present
Returns a dictionary of DataFrames keyed by table name

# 3. Load

Connects to PostgreSQL using SQLAlchemy
Loads each DataFrame as a separate table:

assists — player assist records
goals — player goal records
matches — match results and statistics

# Dataset

Source: UEFA Euro 2024 Records on Kaggle
Tables:

matches — match number, teams, date, stadium, goals, shots
goals — player, team, goals scored
assists — player, team, assists made

# Setup Instructions
Prerequisites

Docker Desktop installed and running
Kaggle account with API token
Power BI Desktop (for visualization

1. Start Airflow with Docker

docker compose up -d

2. Add Kaggle credentials into the worker container

docker exec airflow-docker-airflow-worker-1 mkdir -p /home/airflow/.kaggle
docker cp C:\Users\<your-username>\.kaggle\kaggle.json airflow-docker-airflow-worker-1:/home/airflow/.kaggle/kaggle.json
docker exec -u root airflow-docker-airflow-worker-1 chmod 600 /home/airflow/.kaggle/kaggle.json

 3. Create the target database in PostgreSQL

docker exec -it airflow-docker-postgres-1 psql -U airflow -c "CREATE DATABASE eurocup

4. Trigger the DAG

Open Airflow UI at http://localhost:8080
Find Euro_cup_2024_pipeline
Click the play button to trigger manually

# Power BI Dashboard

Connected Power BI Desktop to PostgreSQL at localhost:5433 with the following visuals:

Total Matches, Total Goals, Total Audience KPI cards
Top goal scorers bar chart
Top assist providers bar chart
Team performance table
Date slicer for filtering match data
















