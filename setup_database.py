import sqlite3
import pandas as pd
from data_loader import DataLoader

def create_table(cursor, table_name, df):
    # Create a string of column names and types
    columns = ', '.join([f"{col} {get_sqlite_type(df[col].dtype)}" for col in df.columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

def get_sqlite_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TEXT"
    else:
        return "TEXT"

def insert_data(cursor, table_name, df):
    # Convert datetime columns to string
    for col in df.select_dtypes(include=['datetime64']).columns:
        df[col] = df[col].astype(str)

    # Convert DataFrame to list of tuples
    data = [tuple(x) for x in df.to_numpy()]
    # Create the INSERT statement
    placeholders = ', '.join(['?' for _ in df.columns])
    cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", data)

def setup_database(excel_file, db_file):
    # Load data from Excel
    loader = DataLoader(excel_file)
    loader.load_data()
    data_dict = loader.get_data()

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables and insert data
    for table_name, df in data_dict.items():
        create_table(cursor, table_name, df)
        insert_data(cursor, table_name, df)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Database created and data loaded into {db_file}")

if __name__ == "__main__":
    setup_database("data.xlsx", "database.db")