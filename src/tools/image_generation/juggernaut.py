import requests
import time
from typing import Dict, Any
from src.tools.image_generation.base import ImageGenerationTool


REPLICATE_TOKEN = "your_token_here"
JUGGERNAUT_MODEL_VERSION = "bdd0319b-c4a5-4acb-9774-7cf3c4c4f97f"  # Juggernaut XL v7的版本ID

class JuggernautTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("juggernaut-xl-v7")
        self.api_url = "https://api.replicate.com/v1/predictions"
        self.headers = {
            "Authorization": f"Token {REPLICATE_TOKEN}",
            "Content-Type": "application/json"
        }

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = {
            "version": JUGGERNAUT_MODEL_VERSION,
            "input": payload
        }

        response = requests.post(self.api_url, json=body, headers=self.headers)
        if not response.ok:
            raise RuntimeError(f"API request failed: {response.status_code} {response.text}")

        data = response.json()
        prediction_id = data["id"]

        max_attempts = 60  
        for attempt in range(max_attempts):
            poll_response = requests.get(f"{self.api_url}/{prediction_id}", headers=self.headers)
            poll_data = poll_response.json()
            status = poll_data["status"]
            
            if status == "succeeded":
                output_urls = poll_data["output"]
                image_url = output_urls[0] if isinstance(output_urls, list) else output_urls
                return {
                    "image_url": image_url,
                    "metadata": {
                        "width": payload.get("width", 512),
                        "height": payload.get("height", 768),
                        "guidance_scale": payload.get("guidance_scale", 7),
                        "prediction_id": prediction_id
                    }
                }
            elif status == "failed":
                error_detail = poll_data.get("error", "Unknown error")
                raise RuntimeError(f"Prediction failed: {error_detail}")
            elif status in ["starting", "processing"]:
                time.sleep(5)  
                continue
            else:
                raise RuntimeError(f"Unexpected status: {status}")
        
        raise RuntimeError("Request timed out after maximum attempts")
