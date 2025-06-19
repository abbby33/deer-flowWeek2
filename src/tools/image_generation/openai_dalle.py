import base64
from typing import Dict, Any
from openai import OpenAI
from src.tools.image_generation.base import ImageGenerationTool
from src.config.api_config import get_api_config

class GPTImageTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("gpt-image-1")
        self.config = get_api_config()
        
        
        openai_key = self.config.get_openai_key()
        if not openai_key:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable or configure api_keys.yaml")
        
        self.client = OpenAI(api_key=openai_key)

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        
        
        if "image" in payload and payload["image"]:
            return self._call_edit_api(payload)
        else:
            return self._call_generate_api(payload)
    
    def _call_generate_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            generate_params = {
                "model": "gpt-image-1",
                "prompt": payload["prompt"],
                "size": payload.get("size", "1024x1024")
            }
            
            if "quality" in payload:
                generate_params["quality"] = payload["quality"]
            
            response = self.client.images.generate(**generate_params)
            
            image_b64 = response.data[0].b64_json
            
            
            image_url = f"data:image/png;base64,{image_b64}"
            
            return {
                "image_url": image_url,
                "metadata": {
                    "mode": "text-to-image",
                    "size": payload.get("size", "1024x1024"),
                    "quality": payload.get("quality", "standard"),
                    "model": "gpt-image-1"
                }
            }
            
        except Exception as e:
            raise RuntimeError(f"GPT-Image-1 generation failed: {str(e)}")
    
    def _call_edit_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            image_input = payload["image"]
            
            edit_params = {
                "model": "gpt-image-1",
                "prompt": payload["prompt"],
                "image": [image_input],  
                "size": payload.get("size", "1024x1024"),
                "quality": payload.get("quality", "standard")
            }
            
            
            if "mask" in payload and payload["mask"]:
                edit_params["mask"] = payload["mask"]
            
            response = self.client.images.edit(**edit_params)
            
            
            image_b64 = response.data[0].b64_json
            image_url = f"data:image/png;base64,{image_b64}"
            
            return {
                "image_url": image_url,
                "metadata": {
                    "mode": "image-to-image",
                    "size": payload.get("size", "1024x1024"),
                    "quality": payload.get("quality", "standard"),
                    "has_mask": "mask" in payload,
                    "model": "gpt-image-1"
                }
            }
            
        except Exception as e:
            raise RuntimeError(f"GPT-Image-1 editing failed: {str(e)}")
