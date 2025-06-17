import requests
import time
from typing import Dict, Any
from src.tools.image_generation.base import ImageGenerationTool

REPLICATE_TOKEN = "your_token_here"
KONTEXT_FLUX_MODEL_VERSION = "fc4dfcbd-8a25-4efc-ad15-4e74c77ae567"  # Kontext Flux的版本ID

class KontextFluxTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("kontext-flux")
        self.api_url = "https://api.replicate.com/v1/predictions"
        self.headers = {
            "Authorization": f"Token {REPLICATE_TOKEN}",
            "Content-Type": "application/json"
        }

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        
        body = {
            "version": KONTEXT_FLUX_MODEL_VERSION,
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
                        "mode": payload.get("mode", "text-to-image"),
                        "has_input_image": "image" in payload,
                        "has_mask": "mask" in payload,
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
