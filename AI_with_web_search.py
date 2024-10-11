import os
import requests
from google.generativeai import genai

# Initialize API keys and endpoints
gemini_api_key = 'replace_with_your_api_key'
bing_api_key = 'replace_with_your_api_key'
bing_api_url = 'https://api.bing.microsoft.com/v7.0/search'

def perform_search(query):
    """Conducts a Bing search and returns the results."""
    market = 'en-US'
    parameters = {'q': query, 'mkt': market}
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}

    try:
        response = requests.get(bing_api_url, headers=headers, params=parameters)
        response.raise_for_status()
        json_response = response.json()
        return json_response.get("webPages", {}).get("value", [])
    except Exception as error:
        raise error

# Prompt the user for input
user_query = input("What would you like to know? ")

# Execute the search function to fetch results
search_results = perform_search(user_query)

if search_results:
    # Format search results for the prompt
    formatted_results = [
        f"Source:\nTitle: {result['name']}\nURL: {result['url']}\nSnippet: {result['snippet']}"
        for result in search_results
    ]

    prompt_text = "Using the following sources, provide an answer to the question:\n\n" + \
                  "\n\n".join(formatted_results) + "\n\nQuestion: " + user_query + "\n\n"

    # Set the Gemini API key
    genai.api_key = gemini_api_key

    # Query the Gemini model with the prepared prompt
    try:
        response = genai.GenerativeModel.generate(
            model='gemini-1.0',  # Replace with your specific Gemini model
            prompt=prompt_text,
            max_tokens=4000,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Display the response from Gemini
        response_text = response.text
        print(f"Response: {response_text}")

    except Exception as e:
        print(f"An error occurred while querying the Gemini API: {e}")
else:
    print("Error: No search results found for your query.")
