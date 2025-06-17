import requests
import time
from typing import Dict, Any
from src.tools.image_generation.base import ImageGenerationTool

# 替换为你真实的 Replicate API Token
REPLICATE_TOKEN = "your_token_here"  # 从环境变量或配置文件获取
REPLICATE_MODEL_VERSION = "2c56db660f453e54fb816eaa7135a279d22a4f23937b854d77903ee21094d32b"  # flux-pulid的版本ID

class FluxPulidTool(ImageGenerationTool):
    def __init__(self):
        super().__init__("flux-pulid")
        self.api_url = "https://api.replicate.com/v1/predictions"
        self.headers = {
            "Authorization": f"Token {REPLICATE_TOKEN}",
            "Content-Type": "application/json"
        }

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """调用Replicate API生成图像"""
        body = {
            "version": REPLICATE_MODEL_VERSION,
            "input": payload
        }

        # 创建预测请求
        response = requests.post(self.api_url, json=body, headers=self.headers)
        if not response.ok:
            raise RuntimeError(f"API request failed: {response.status_code} {response.text}")

        data = response.json()
        prediction_id = data["id"]

        # 轮询等待结果
        max_attempts = 60  # 最多等待5分钟
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
                time.sleep(5)  # 等待5秒后重试
                continue
            else:
                raise RuntimeError(f"Unexpected status: {status}")
        
        raise RuntimeError("Request timed out after maximum attempts")
