import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [table[0] for table in cursor.fetchall()]

    def get_table_data(self, table_name):
        with sqlite3.connect(self.db_file) as conn:
            return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    def get_schema(self):
        schema = {}
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            for table_name in self.get_tables():
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                schema[table_name] = [
                    {"name": col[1], "type": col[2]} for col in columns
                ]
        return schema

    def execute_query(self, query):
        with sqlite3.connect(self.db_file) as conn:
            return pd.read_sql_query(query, conn)
        
    def clear_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            tables = self.get_tables()
            for table in tables:
                cursor.execute(f"DELETE FROM {table};")
                conn.commit()
                
    def drop_all_tables(self):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                tables = self.get_tables()
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {table};")
                    conn.commit()

if __name__ == "__main__":
    db_manager = DBManager("database.db")
    
    # Print information about the database
    tables = db_manager.get_tables()
    schema = db_manager.get_schema()
    
    print("Database Tables:")
    for table in tables:
        print(f"\nTable: {table}")
        print("Columns:")
        for column in schema[table]:
            print(f"  - {column['name']} ({column['type']})")
        
        # Print first few rows of each table
        print("\nSample Data:")
        print(db_manager.get_table_data(table).head())
        print("\n" + "="*50)
