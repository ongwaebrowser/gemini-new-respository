import os
import requests
from flask import Flask, request, jsonify

# Define a class for interacting with the Gemini API
class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.gemini.com"

    def search(self, query):
        # Check for inappropriate content in the query
        if self.is_inappropriate(query):
            return {"error": "Inappropriate content detected"}
        
        # Construct the URL for the API request
        url = f"{self.base_url}/search?query={query}&key={self.api_key}"
        try:
            # Send a GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            # Process the JSON response
            return self.process_response(response.json())
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            return {"error": "HTTP error occurred", "message": str(http_err)}
        except Exception as err:
            # Handle any other errors
            return {"error": "Other error occurred", "message": str(err)}

    def is_inappropriate(self, query):
        # List of inappropriate keywords to check for
        inappropriate_keywords = ["racism", "hacking", "sexual"]
        return any(keyword in query.lower() for keyword in inappropriate_keywords)

    def process_response(self, response):
        # Placeholder for processing the response data
        return response

# Retrieve the API key from environment variables
api_key = os.getenv("YOUR_API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set the YOUR_API_KEY environment variable.")

# Instantiate the GeminiAPI with the API key
api = GeminiAPI(api_key)

# Create a Flask application
app = Flask(__name__)

# Define a route for handling search requests
@app.route('/search', methods=['GET'])
def handler():
    # Get the query parameter from the request
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    # Use the GeminiAPI to perform the search
    result = api.search(query)
    return jsonify(result)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
