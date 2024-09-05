from openai import OpenAI
import pandas as pd
import os
import json
from typing import Dict, List
from data_loader import DataLoader

class MetadataEmbedder:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=api_key)

    def extract_metadata(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, str]:
        metadata = {}
        for table_name, df in data_dict.items():
            table_info = f"Table: {table_name}\nColumns:\n"
            for column in df.columns:
                table_info += f"- {column} (Type: {df[column].dtype})\n"
            metadata[table_name] = table_info
        return metadata

    def generate_embeddings(self, metadata: Dict[str, str]) -> Dict[str, List[float]]:
        embeddings = {}
        for table_name, table_info in metadata.items():
            response = self.client.embeddings.create(
                input=table_info,
                model="text-embedding-ada-002"
            )
            # Print the full API response
            print(f"\nAPI Response for {table_name}:")
            print(json.dumps(response.model_dump(), indent=2))
            
            embeddings[table_name] = response.data[0].embedding
        return embeddings

    def store_embeddings(self, embeddings: Dict[str, List[float]], file_path: str):
        with open(file_path, 'w') as f:
            json.dump(embeddings, f)
        print(f"Embeddings stored in {file_path}")

def main():
    # Step 1: Load data
    loader = DataLoader("data.xlsx")
    loader.load_data()
    data = loader.get_data()

    # Step 2: Extract metadata and generate embeddings
    embedder = MetadataEmbedder()
    metadata = embedder.extract_metadata(data)
    embeddings = embedder.generate_embeddings(metadata)

    # Store embeddings
    embedder.store_embeddings(embeddings, "embeddings.json")

    # Print some information
    print("\nExtracted Metadata:")
    for table, info in metadata.items():
        print(f"\n{info}")

    print("\nGenerated Embeddings:")
    for table, embedding in embeddings.items():
        print(f"{table}: Length {len(embedding)}")

if __name__ == "__main__":
    main()