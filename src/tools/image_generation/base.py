from typing import Any, Dict
from schema.model_schemas import MODEL_SCHEMAS  

class ImageGenerationTool:
    def __init__(self, model_name: str):
        self.model_name = model_name
        if model_name not in MODEL_SCHEMAS:
            raise ValueError(f"Unsupported model: {model_name}")
        self.schema = MODEL_SCHEMAS[model_name]

    def parse_agent_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        parsed = {}
        for key, info in self.schema["input_fields"].items():
            alias = info.get("alias", key)
            required = info.get("required", False)
            default = info.get("default", None)
            value = input_data.get(key, default)

            if required and value is None:
                raise ValueError(f"Missing required field: {key} for model {self.model_name}")

            if value is not None:
                parsed[alias] = value
        return parsed

    def call_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement call_api")

    def format_response(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "image",
            "image_url": raw.get("image_url"),
            "generation_metadata": {
                "provider": self.schema["provider"],
                "model": self.model_name,
                **{
                    k: v for k, v in raw.get("metadata", {}).items()
                }
            }
        }

    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        api_payload = self.parse_agent_input(input_data)
        raw_response = self.call_api(api_payload)
        return self.format_response(raw_response)
