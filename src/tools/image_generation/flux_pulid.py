import requests
import time
from typing import Dict, Any
from src.tools.image_generation.base import ImageGenerationTool
from src.config.api_config import get_api_config

class FluxPulidTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("flux-pulid")
        self.config = get_api_config()
        self.api_url = "https://api.replicate.com/v1/predictions"
        
        # 获取API
        replicate_key = self.config.get_replicate_key()
        if not replicate_key:
            raise ValueError("Replicate API key not configured. Please set REPLICATE_API_TOKEN environment variable or configure api_keys.yaml")
        
        self.headers = {
            "Authorization": f"Token {replicate_key}",
            "Content-Type": "application/json"
        }
        
        
        self.model_version = self.config.get_model_version("flux-pulid") or "2c56db660f453e54fb816eaa7135a279d22a4f23937b854d77903ee21094d32b"

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = {
            "version": self.model_version,
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
                        "style": payload.get("style", "default"),
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
