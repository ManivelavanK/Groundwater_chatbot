import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import re

def clean_column_names(df):
    """
    Cleans column names by replacing characters not allowed in MongoDB field names.
    """
    new_columns = {}
    for col in df.columns:
        # Replace any character that is not a letter, number, or underscore with an underscore
        cleaned_col = re.sub(r'[^A-Za-z0-9_]', '_', col)
        new_columns[col] = cleaned_col
    df.rename(columns=new_columns, inplace=True)
    return df

def ingest_csv_to_mongodb(csv_file_path, db_name, collection_name):
    """
    Reads data from a standard CSV file and ingests it into a MongoDB collection.
    """
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        print("Error: MONGO_URI not found in environment variables.")
        return

    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Simple, direct read from the clean CSV file
        df = pd.read_csv(csv_file_path, encoding='utf-8')

        df = clean_column_names(df)

        records = df.to_dict(orient='records')

        collection.delete_many({})
        print(f"Cleared existing documents in collection '{collection_name}'.")

        if records:
            collection.insert_many(records)
            print(f"---!!! SUCCESS!!!---")
            print(f"Successfully ingested {len(records)} records from the clean CSV file.")
        else:
            print("No records to ingest.")

    except FileNotFoundError:
        print(f"Error: The file at {csv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()
            print("MongoDB connection closed.")

if __name__ == '__main__':
    # --- Configuration ---
    CSV_PATH = 'data/ingres_data.csv' # This name MUST be correct
    DATABASE_NAME = 'ingres_db'
    COLLECTION_NAME = 'information'

    ingest_csv_to_mongodb(CSV_PATH, DATABASE_NAME, COLLECTION_NAME)