from airflow.sdk import dag, task
from datetime import datetime 
import os
import zipfile 
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import subprocess

@dag(
    
    dag_id = "Euro_cup_2024_pipeline",
    start_date = datetime(2026,4,12),
    schedule = "@once",
    catchup = False
                    
)

def Euro_cup_2024_pipeline():
    
    @task

    def extract():
        # tell kaggle where credentials are

        os.environ['KAGGLE_CONFIG_DIR'] = '/home/airflow/.kaggle'

        subprocess.run(["/home/airflow/.local/bin/kaggle", "datasets", "download",
                "-d", "krishd123/uefa-euro-2024-records",
                "-p", "/opt/airflow/data"], check=True)
        
        with zipfile.ZipFile("/opt/airflow/data/uefa-euro-2024-records.zip","r") as zip_file:
            
            zip_file.extractall("/opt/airflow/data/Eurocup2024")
        
        os.remove("/opt/airflow/data/uefa-euro-2024-records.zip")
        print("Succesfully Extracted")
        return "/opt/airflow/data/Eurocup2024"
   
    @task 

    def transform(input_dir):
        folder = Path(input_dir)
        csv_files = list(folder.glob("*.csv"))

        print(f"Found {len(csv_files)} csv files: {[f.name for f in csv_files]}")

        result = {}
        for file in csv_files:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower().str.strip()
            df = df.drop_duplicates()
            df = df.dropna()
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
            table_name = file.stem.lower()   # assists, goals, matches
            result[table_name] = df          # {"assists": df1, "goals": df2, "matches": df3}

        print("Transformation Success")
        return result                        # ← return a dictionary of dataframes
    
    @ task

    
    def load(data):                          # ← receives the dictionary
        engine = create_engine("postgresql+psycopg2://airflow:airflow@airflow-docker-postgres-1:5432/eurocup"
        )
        with engine.connect() as conn:
            for table_name, df in data.items():   # ← loads each df as separate table
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Loaded {table_name} into PostgreSQL")
            conn.commit()
        print("Data loaded into PostgreSQL")
    folder_path = extract()         
    df = transform(folder_path)    
    load(df)
Euro_cup_2024_pipeline()