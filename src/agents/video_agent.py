from typing import List, Dict, Any
from langchain_core.tools import BaseTool
from src.tools.video import generate_video

class VideoGenerationAgent:
    """Agent for generating videos using Azure OpenAI's Sora model."""
    
    def __init__(self):
        """Initialize the video generation agent with its tools."""
        self.tools: List[BaseTool] = [generate_video]
        
    def get_tools(self) -> List[BaseTool]:
        """Get the list of tools available to this agent."""
        return self.tools
        
    def get_description(self) -> str:
        """Get a description of this agent's capabilities."""
        return """I am a video generation agent that can create videos from text descriptions 
        using Azure OpenAI's Sora model. I can generate high-quality videos with specified 
        dimensions, duration, and number of variants."""
        
    def get_instructions(self) -> str:
        """Get instructions for using this agent."""
        return """To generate a video, provide a detailed text description of what you want to see.
        You can optionally specify:
        - Video dimensions (height and width in pixels)
        - Duration in seconds
        - Number of video variants to generate
        
        The agent will handle the video generation process and return URLs to the generated videos.""" 