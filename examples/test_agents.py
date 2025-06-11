import asyncio
import os
from src.workflow import run_agent_workflow_async

# API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable must be set")

async def test_image_generation():
    """Test image generation through the agent system."""
    print("\nTesting image generation...")
    result = await run_agent_workflow_async(
        "Generate an image of a cute cat playing with a ball of yarn",
        debug=True,
        max_plan_iterations=2,
        max_step_num=3,
    )
    print("Image generation test completed")
    return result

async def test_speech_generation():
    """Test speech generation through the agent system."""
    print("\nTesting speech generation...")
    result = await run_agent_workflow_async(
        "Convert this text to speech: Welcome to DeerFlow, the next generation AI system!",
        debug=True,
        max_plan_iterations=2,
        max_step_num=3,
    )
    print("Speech generation test completed")
    return result

async def main():
    """Run all tests."""
    # Test image generation
    await test_image_generation()
    
    # Test speech generation
    await test_speech_generation()

if __name__ == "__main__":
    asyncio.run(main()) 