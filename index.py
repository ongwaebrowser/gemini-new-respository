import requests
import re

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.gemini.com"  # Updated base URL

    def search(self, query):
        if self.is_inappropriate(query):
            return {"error": "Inappropriate content detected"}
        
        url = f"{self.base_url}/search?query={query}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return self.process_response(response.json())
        else:
            return {"error": response.status_code, "message": response.text}

    def is_inappropriate(self, query):
        inappropriate_keywords = ["racism", "hacking", "sexual"]
        return any(keyword in query.lower() for keyword in inappropriate_keywords)

    def process_response(self, response):
        # Process the response to give long answers and perform math if needed
        # This is a placeholder for actual processing logic
        return response

if __name__ == "__main__":
    api = GeminiAPI("YOUR_API_KEY")
    result = api.search("example query")
    print(result)
