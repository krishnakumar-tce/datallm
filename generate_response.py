from openai import OpenAI
import os
from query_executor import QueryExecutor

# Initialize OpenAI API client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
client = OpenAI(api_key=api_key)

def generate_user_friendly_response(query_result, user_input):
    prompt = f"""
    User query: "{user_input}"
    The result of the database query is as follows:
    {query_result}

    Please provide a user-friendly response based on the query result.
    """

    try:
        # Send request to OpenAI's Chat API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant with expertise in summarizing database query results."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )

        # Print the entire response object for debugging
        #print("API Response:")
        #print(response)

        # Access and print the content from the response for debugging
        if hasattr(response, 'choices') and len(response.choices) > 0:
            print("Response Choices:")
            print(response.choices)
            message_content = response.choices[0].message.content  # Adjusted to access the content
            return message_content.strip()
        else:
            return "The response does not contain valid content."
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"

def main():
    # Create an instance of QueryExecutor
    executor = QueryExecutor("database.db", "embeddings.json")
    
    while True:
        query = input("\nEnter your query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        # Execute the query and get the result
        query_result = executor.execute_query(query)
        print("\nQuery Result:")
        print(query_result)

        # Generate a user-friendly response using OpenAI API
        friendly_response = generate_user_friendly_response(query_result, query)
        print("\nUser-Friendly Response:")
        print(friendly_response)

if __name__ == "__main__":
    main()