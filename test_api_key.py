import requests
import json

def test_api_key(api_key: str):
    """Test if the Google AI API key works."""
    try:
        # API endpoint for Imagen
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
        
        # Request headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Request body
        data = {
            "instances": [
                {
                    "prompt": "A simple test image of a blue sky"
                }
            ],
            "parameters": {
                "sampleCount": 1
            }
        }
        
        # Make the request
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("API key works! Successfully connected to Imagen API.")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing API key: {str(e)}")
        return False

if __name__ == "__main__":
    # The API key provided
    API_KEY = "AIzaSyDOvSL6kgq6a8O2sGYj-fGVnsxr8ULD1o0"
    
    test_api_key(API_KEY) 