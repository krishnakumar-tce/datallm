from db_manager import DBManager
from sql_generator import SQLGenerator
import pandas as pd

class QueryExecutor:
    def __init__(self, db_file, embeddings_file):
        self.db_manager = DBManager(db_file)
        self.sql_generator = SQLGenerator(db_file, embeddings_file)

    def execute_query(self, natural_language_query):
        try:
            # Generate SQL query
            sql_query = self.sql_generator.generate_sql(natural_language_query)
            print("Generated SQL Query:")
            print(sql_query)
            print("\nExecuting query...")

            # Execute SQL query
            result = self.db_manager.execute_query(sql_query)

            # Format and return results
            return self.format_results(result)
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def format_results(self, result):
        if isinstance(result, pd.DataFrame):
            if result.empty:
                return "The query returned no results."
            else:
                return result.to_string(index=False)
        else:
            return str(result)

def main():
    executor = QueryExecutor("database.db", "embeddings.json")
    
    while True:
        query = input("\nEnter your query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        result = executor.execute_query(query)
        print("\nResult:")
        print(result)

if __name__ == "__main__":
    main()
