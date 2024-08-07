import os
import requests
from flask import Flask, request, jsonify

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.gemini.com"

    def search(self, query):
        if self.is_inappropriate(query):
            return {"error": "Inappropriate content detected"}
        
        url = f"{self.base_url}/search?query={query}&key={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return self.process_response(response.json())
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "message": str(http_err)}
        except Exception as err:
            return {"error": "Other error occurred", "message": str(err)}

    def is_inappropriate(self, query):
        inappropriate_keywords = ["racism", "hacking", "sexual"]
        return any(keyword in query.lower() for keyword in inappropriate_keywords)

    def process_response(self, response):
        return response

# Retrieve the API key from environment variables
api_key = os.getenv("YOUR_API_KEY")
if not api_key:
    raise ValueError("No API key found. Please set the YOUR_API_KEY environment variable.")

api = GeminiAPI(api_key)

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def handler():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    result = api.search(query)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
