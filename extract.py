import os
import glob
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .pg_env
load_dotenv(".pg_env")

# PostgreSQL connection parameters from environment variables
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),  # Default to localhost
    "port": os.getenv("POSTGRES_PORT", "5432"),  # Default PostgreSQL port
}

CSV_FOLDER = "./data"  # Directory containing CSV files

# Mapping of table names to expected columns
TABLES = {
    "contracts": [
        "id", "type", "energy", "usage", "usagenet", "createdat", "startdate",
        "enddate", "fillingdatecancellation", "cancellationreason", "city",
        "status", "productid", "modificationdate"
    ],
    "products": [
        "id", "productcode", "productname", "energy",
        "consumptiontype", "deleted", "modificationdate"
    ],
    "prices": [
        "id", "productid", "pricecomponentid", "productcomponent",
        "price", "unit", "valid_from", "valid_until", "modificationdate"
    ]
}

# Function to determine table based on filename
def get_table_name(file_name):
    """Extract table name from file name."""
    for table in TABLES.keys():
        if table in file_name:
            return table
    return None  # Return None if file type is unknown

def load_csv_to_postgres(file_path, table_name):
    """Loads a CSV file into PostgreSQL with historization"""
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    # Get column names for the table
    columns = TABLES[table_name] + ["file_name", "ingestion_time"]

    sql = f"""
        COPY raw.{table_name} ({', '.join(columns)})
        FROM '{file_path}'
        DELIMITER ';'
        CSV HEADER
        NULL AS '';  -- Converts empty fields to NULL
    """

    try:
        cur.execute(sql)
        conn.commit()
        print(f"✅ Successfully loaded {file_path} into raw.{table_name}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error loading {file_path}: {e}")
    finally:
        cur.close()
        conn.close()

def process_csv_files():
    """Detects all CSV files and loads them"""
    for file in glob.glob(os.path.join(CSV_FOLDER, "*.csv")):
        file_name = os.path.basename(file)
        table_name = get_table_name(file_name)

        if table_name:
            print(f"📥 Processing {file_name} into {table_name}...")
            load_csv_to_postgres(os.path.abspath(file), table_name)
        else:
            print(f"⚠️ Skipping {file_name} (unknown format)")

if __name__ == "__main__":
    process_csv_files()
