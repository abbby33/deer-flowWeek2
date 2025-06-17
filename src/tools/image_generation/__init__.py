from typing import Dict, Any
from .flux_pulid import FluxPulidTool
from .openai_dalle import OpenAIDalleTool
from .juggernaut import JuggernautTool
from .kontext_flux import KontextFluxTool

# 工具注册表
TOOL_REGISTRY = {
    "flux-pulid": FluxPulidTool,
    "chatgpt-image-1": OpenAIDalleTool,
    "juggernaut-xl-v7": JuggernautTool,
    "kontext-flux": KontextFluxTool,
}

class ImageGenerationFactory:
    
    @staticmethod
    def create_tool(model_name: str):
        if model_name not in TOOL_REGISTRY:
            available_models = list(TOOL_REGISTRY.keys())
            raise ValueError(f"Unsupported model: {model_name}. Available models: {available_models}")
        
        tool_class = TOOL_REGISTRY[model_name]
        return tool_class()
    
    @staticmethod
    def generate_image(model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        tool = ImageGenerationFactory.create_tool(model_name)
        return tool.generate(input_data)
    
    @staticmethod
    def get_available_models() -> list:
        return list(TOOL_REGISTRY.keys())

# 统一接口
def generate_image(model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    
    return ImageGenerationFactory.generate_image(model_name, input_data) 