from typing import Dict, Any
from .flux_pulid import FluxPulidTool as FluxPuLIDTool
from .openai_dalle import GPTImageTool as GPTImage1Tool
from .juggernaut import JuggernautTool
from .kontext_flux import FluxKontextProTool

# 工具注册表
TOOL_REGISTRY = {
    "flux-pulid": FluxPuLIDTool,
    "gpt-image-1": GPTImage1Tool,
    "juggernaut-xl-v7": JuggernautTool,
    "flux-kontext-pro": FluxKontextProTool,
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

# 导出函数
def get_available_models() -> list:
    """获取所有可用的模型列表"""
    return ImageGenerationFactory.get_available_models()

def create_image_generation_tool(model_name: str):
    """创建图像生成工具实例"""
    return ImageGenerationFactory.create_tool(model_name)

# 统一接口
def generate_image(model_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """生成图像的统一接口"""
    return ImageGenerationFactory.generate_image(model_name, input_data)

# 导出所有类
__all__ = [
    'get_available_models',
    'create_image_generation_tool', 
    'generate_image',
    'ImageGenerationFactory',
    'FluxPuLIDTool',
    'GPTImage1Tool', 
    'JuggernautTool',
    'FluxKontextProTool'
] 