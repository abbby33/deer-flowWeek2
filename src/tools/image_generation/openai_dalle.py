import requests
from typing import Dict, Any
from src.tools.image_generation.base import ImageGenerationTool


OPENAI_API_KEY = "your_openai_api_key_here"

class OpenAIDalleTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("chatgpt-image-1")
        self.api_url = "https://api.openai.com/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
       
        body = {
            "model": "dall-e-3",  
            "prompt": payload["prompt"],
            "n": payload.get("n", 1),
            "size": payload.get("size", "1024x1024"),
            "quality": payload.get("quality", "standard"),
            "response_format": "url"
        }

        response = requests.post(self.api_url, json=body, headers=self.headers)
        if not response.ok:
            error_detail = response.json().get("error", {}).get("message", response.text)
            raise RuntimeError(f"OpenAI API request failed: {response.status_code} - {error_detail}")

        data = response.json()
        image_url = data["data"][0]["url"]
        
        return {
            "image_url": image_url,
            "metadata": {
                "size": payload.get("size", "1024x1024"),
                "quality": payload.get("quality", "standard"),
                "revised_prompt": data["data"][0].get("revised_prompt")  
            }
        }
