from langgraph.prebuilt import create_react_agent
from src.tools.imagen import generate_image
from src.prompts import apply_prompt_template
from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP

def create_image_agent(agent_name: str = "image_generator"):
    """Create an agent for image generation."""
    tools = [generate_image]
    
    return create_react_agent(
        name=agent_name,
        model=get_llm_by_type(AGENT_LLM_MAP.get(agent_name, "basic")),
        tools=tools,
        prompt=lambda state: apply_prompt_template(
            "image_generation",
            state
        )
    ) 