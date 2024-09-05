import json
import numpy as np
from openai import OpenAI
import os
from typing import Dict, List, Tuple

class SimilaritySearcher:
    def __init__(self, embeddings_file: str, similarity_threshold: float = 0.7):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=api_key)
        
        self.similarity_threshold = similarity_threshold
        self.embeddings = self.load_embeddings(embeddings_file)

    def load_embeddings(self, file_path: str) -> Dict[str, List[float]]:
        with open(file_path, 'r') as f:
            return json.load(f)

    def query_to_embedding(self, query: str) -> List[float]:
        response = self.client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def search(self, query: str) -> List[Tuple[str, float]]:
        query_embedding = self.query_to_embedding(query)
        similarities = []
        for table, embedding in self.embeddings.items():
            similarity = self.cosine_similarity(query_embedding, embedding)
            if similarity >= self.similarity_threshold:
                similarities.append((table, similarity))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)

def main():
    searcher = SimilaritySearcher("embeddings.json")
    
    example_queries = [
        "Find customer information",
        "Show me product prices",
        "Get recent orders with customer details",
        "List customer reviews with product information",
        "Check inventory levels and recent order quantities"
    ]

    for query in example_queries:
        print(f"\nQuery: {query}")
        results = searcher.search(query)
        if results:
            print("Relevant tables:")
            for table, similarity in results:
                print(f"  {table}: Similarity = {similarity:.4f}")
        else:
            print("No tables found above the similarity threshold.")

if __name__ == "__main__":
    main()