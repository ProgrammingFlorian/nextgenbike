import psycopg2
import sys
import os
import pandas as pd

# TODO: Database connection

def connect():
    try:
        print('Connecting to the database')
        conn = psycopg2.connect(
            host=os.environ['DB_PATH'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        sys.exit(1)
    print("Connection Successful")
    return conn


def extract_training_dataset(col_names):
    query = ""
    return run_query_to_dataset(query, col_names)


def run_query_to_dataset(query, col_names):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.exectute(query)
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        sys.exit(1)
    cursor.close()
    data = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(data, col_names)
