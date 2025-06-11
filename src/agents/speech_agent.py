from langgraph.prebuilt import create_react_agent
from src.tools.speech import generate_speech, generate_multi_speaker_speech
from src.prompts import apply_prompt_template
from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP

def create_speech_agent(agent_name: str = "speech_generator"):
    """Create an agent for speech generation."""
    tools = [generate_speech, generate_multi_speaker_speech]
    
    return create_react_agent(
        name=agent_name,
        model=get_llm_by_type(AGENT_LLM_MAP.get(agent_name, "basic")),
        tools=tools,
        prompt=lambda state: apply_prompt_template(
            "speech_generation",
            state
        )
    ) 