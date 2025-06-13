import os
import asyncio
import yaml
from pathlib import Path
from src.graph.builder import build_graph

def _load_config() -> dict:
    """Load configuration from conf.yaml."""
    root_dir = Path(__file__).parent.parent
    config_path = root_dir / "conf.yaml"
    
    if not os.path.exists(config_path):
        print("Error: conf.yaml not found")
        return None
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    # Get Azure configuration
    azure_config = config.get("azure", {}).get("video", {})
    if not azure_config or not azure_config.get("api_key"):
        print("Error: Azure video configuration not found in conf.yaml")
        return None
        
    return azure_config

async def generate_video_example():
    """Example of generating a video using the DeerFlow agent system."""
    # Load configuration
    config = _load_config()
    if not config:
        return
    
    # Build graph
    graph = build_graph()
    graph_config = {"configurable": {"api_key": config["api_key"]}}
    
    # Generate video through planner
    prompt = "Generate a video of a cute cat playing with a ball of yarn in a sunny room"
    print(f"Generating video for prompt: {prompt}")
    
    result = await graph.ainvoke({
        "messages": [{"role": "user", "content": prompt}],
        "locale": "en-US",
        "auto_accepted_plan": True
    }, graph_config)
    
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    asyncio.run(generate_video_example()) 