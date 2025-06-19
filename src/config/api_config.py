import os
import yaml
from typing import Dict, Any
from pathlib import Path

class APIConfig:
    """API配置管理器，支持YAML文件和环境变量"""
    
    def __init__(self):
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        
        # 1. 尝试加载YAML配置文件
        config_paths = [
            Path("src/config/api_keys.yaml"),
            Path("api_keys.yaml"),
            Path("config/api_keys.yaml")
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        self.config = yaml.safe_load(f) or {}
                    print(f"✅ Loaded config from {config_path}")
                    break
                except Exception as e:
                    print(f"⚠️ Error loading {config_path}: {e}")
        
        
        self._load_from_env()
    
    def _load_from_env(self):
        
        if openai_key := os.getenv("OPENAI_API_KEY"):
            if "openai" not in self.config:
                self.config["openai"] = {}
            self.config["openai"]["api_key"] = openai_key
            
          
        if replicate_key := os.getenv("REPLICATE_API_TOKEN"):
            if "replicate" not in self.config:
                self.config["replicate"] = {}
            self.config["replicate"]["api_key"] = replicate_key
    
    def get_openai_key(self) -> str:
        
        return self.config.get("openai", {}).get("api_key", "")
    
    def get_replicate_key(self) -> str:
        
        return self.config.get("replicate", {}).get("api_key", "")
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        
        return self.config.get("models", {}).get(model_name, {})
    
    def get_model_version(self, model_name: str) -> str:
        
        return self.get_model_config(model_name).get("model_version", "")


_config_instance = None

def get_api_config() -> APIConfig:
    
    global _config_instance
    if _config_instance is None:
        _config_instance = APIConfig()
    return _config_instance 