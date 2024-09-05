# datallm
A DataLLM allows a user to interact with a database using prompts and getting user-friendly answers.
It works as follows -
1. Convert metadata from a DB into embeddings using an Embeddings API (metadata_embedder.py)
2. Store the embeddings in a document retriever (metadata_embedder.py)
3. When the user enters a prompt, convert the prompt into an embedding (similarity_search.py)
4. Compare the uses prompt embedding with the DB metadata embeddings using a cosine similarity search and return the most relevant tables for answering the prompt (similarity_search.py)
5. Send the user prompt and the table metadata to an LLM and ask to generate a SQL query (sql_generator.py)
6. Execute the SQL query in the DB and fetch the results (query_executor.py)
7. Send the user prompt and the SQL query results to an LLM and ask to generate a user-friendly response (generate_response.py)
8. Return the user-friendly response to the user (generate_response.py)
