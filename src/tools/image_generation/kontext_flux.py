import requests
import time
from typing import Dict, Any
from src.tools.image_generation.base import ImageGenerationTool
from src.config.api_config import get_api_config

class FluxKontextProTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("flux-kontext-pro")
        self.config = get_api_config()
        self.api_url = "https://api.replicate.com/v1/predictions"
        
        
        replicate_key = self.config.get_replicate_key()
        if not replicate_key:
            raise ValueError("Replicate API key not configured. Please set REPLICATE_API_TOKEN environment variable or configure api_keys.yaml")
        
        self.headers = {
            "Authorization": f"Token {replicate_key}",
            "Content-Type": "application/json"
        }
        
        self.model_name = "black-forest-labs/flux-kontext-pro"

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        
        api_url = f"https://api.replicate.com/v1/models/{self.model_name}/predictions"
        
        body = {
            "input": payload
        }

        response = requests.post(api_url, json=body, headers=self.headers)
        if not response.ok:
            raise RuntimeError(f"API request failed: {response.status_code} {response.text}")

        data = response.json()
        prediction_id = data["id"]
        
        
        return self._wait_for_result(prediction_id)

    def _wait_for_result(self, prediction_id: str) -> Dict[str, Any]:
        
        max_attempts = 30  
        attempt = 0
        
        while attempt < max_attempts:
            check_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
            response = requests.get(check_url, headers=self.headers)
            
            if response.ok:
                data = response.json()
                status = data.get("status")
                
                if status == "succeeded":
                    # Flux Kontext Pro 返回图像URL
                    if data.get("output"):
                        image_url = data["output"]
                        return {
                            "image_url": image_url,
                            "metadata": {
                                "model": "flux-kontext-pro",
                                "provider": "replicate",
                                "status": status,
                                "has_input_image": True,
                                "mode": "image-to-image"
                            }
                        }
                
                elif status == "failed":
                    error = data.get("error", "Unknown error")
                    raise RuntimeError(f"Prediction failed: {error}")
                
                elif status in ["starting", "processing"]:
                    # 继续等待
                    time.sleep(10)
                    attempt += 1
                else:
                    raise RuntimeError(f"Unknown status: {status}")
            else:
                raise RuntimeError(f"Failed to check prediction status: {response.status_code}")
        
        raise RuntimeError("Timeout waiting for prediction to complete")
