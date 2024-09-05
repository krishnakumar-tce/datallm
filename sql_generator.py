import os
from openai import OpenAI
from db_manager import DBManager
from similarity_search import SimilaritySearcher

class SQLGenerator:
    def __init__(self, db_file, embeddings_file):
        self.db_manager = DBManager(db_file)
        self.similarity_searcher = SimilaritySearcher(embeddings_file)
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=api_key)

    def generate_sql(self, query):
        # Find relevant tables
        relevant_tables = self.similarity_searcher.search(query)
        
        # Get schema for relevant tables
        schema = self.db_manager.get_schema()
        relevant_schema = {table: schema[table] for table, _ in relevant_tables if table in schema}
        
        # Prepare the prompt for the LLM
        prompt = self._prepare_prompt(query, relevant_schema)
        
        # Generate SQL using OpenAI's API
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a SQL expert. Generate SQL queries based on the given schema and natural language query."},
                {"role": "user", "content": prompt}
            ]
        )
        
        generated_sql = response.choices[0].message.content.strip()
        return generated_sql

    def _prepare_prompt(self, query, relevant_schema):
        schema_str = "\n".join([
            f"Table: {table}\nColumns: {', '.join([f'{col['name']} ({col['type']})' for col in columns])}"
            for table, columns in relevant_schema.items()
        ])
        
        prompt = f"""
Given the following database schema:

{schema_str}

Generate a SQL query for the following question:
"{query}"

Please provide only the SQL query without any additional explanation. Do not include any kind of string at the beginning of the query. Output nothing than the executable SQL itself.
"""
        return prompt

def main():
    generator = SQLGenerator("database.db", "embeddings.json")
    
    example_queries = [
        "What are the names of customers who have placed orders?",
        "List the products with their prices and current inventory levels.",
        "Show me the total revenue from each customer.",
        "What are the top 5 products by sales quantity?",
        "Find all orders placed in the last month with their customer details."
    ]
    
    for query in example_queries:
        print(f"\nNatural Language Query: {query}")
        sql = generator.generate_sql(query)
        print("Generated SQL:")
        print(sql)
        print("-" * 50)

if __name__ == "__main__":
    main()
