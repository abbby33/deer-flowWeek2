#!/usr/bin/env python3
"""
Test script to verify LangGraph integration for image and speech agents.
"""

import os
import asyncio
from src.graph.builder import build_graph
from src.config.configuration import Configuration

async def test_image_generation():
    """Test image generation through LangGraph."""
    print("Testing image generation...")
    
    # Build the graph
    graph = build_graph()
    
    # Create configuration
    config = {
        "configurable": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "max_search_results": 5,
            "max_plan_iterations": 3,
        }
    }
    
    # Test input for image generation
    initial_state = {
        "messages": [{"role": "user", "content": "Generate an image of a cute cat playing with a ball"}],
        "locale": "en-US",
        "auto_accepted_plan": True,
    }
    
    try:
        # Run the graph
        result = await graph.ainvoke(initial_state, config)
        print(f"Image generation result: {result}")
        return True
    except Exception as e:
        print(f"Error testing image generation: {e}")
        return False

async def test_speech_generation():
    """Test speech generation through LangGraph."""
    print("Testing speech generation...")
    
    # Build the graph
    graph = build_graph()
    
    # Create configuration
    config = {
        "configurable": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "max_search_results": 5,
            "max_plan_iterations": 3,
        }
    }
    
    # Test input for speech generation
    initial_state = {
        "messages": [{"role": "user", "content": "Convert this text to speech: Hello, welcome to DeerFlow!"}],
        "locale": "en-US",
        "auto_accepted_plan": True,
    }
    
    try:
        # Run the graph
        result = await graph.ainvoke(initial_state, config)
        print(f"Speech generation result: {result}")
        return True
    except Exception as e:
        print(f"Error testing speech generation: {e}")
        return False

async def test_tools_directly():
    """Test the tools directly."""
    print("Testing tools directly...")
    
    try:
        from src.tools.imagen import generate_image
        from src.tools.speech import generate_speech
        
        # Test image generation tool
        image_result = generate_image.invoke({"prompt": "A beautiful sunset over mountains"})
        print(f"Direct image tool result: {image_result}")
        
        # Test speech generation tool
        speech_result = generate_speech.invoke({"text": "Hello, this is a test", "voice_name": "Kore"})
        print(f"Direct speech tool result: {speech_result}")
        
        return True
    except Exception as e:
        print(f"Error testing tools directly: {e}")
        return False

async def main():
    """Main test function."""
    print("=== DeerFlow LangGraph Integration Test ===\n")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test tools directly first
    print("\n1. Testing tools directly...")
    direct_success = await test_tools_directly()
    
    if direct_success:
        print("✅ Direct tool tests passed")
    else:
        print("❌ Direct tool tests failed")
        return
    
    # Test image generation through LangGraph
    print("\n2. Testing image generation through LangGraph...")
    image_success = await test_image_generation()
    
    if image_success:
        print("✅ Image generation test passed")
    else:
        print("❌ Image generation test failed")
    
    # Test speech generation through LangGraph
    print("\n3. Testing speech generation through LangGraph...")
    speech_success = await test_speech_generation()
    
    if speech_success:
        print("✅ Speech generation test passed")
    else:
        print("❌ Speech generation test failed")
    
    # Summary
    print("\n=== Test Summary ===")
    if direct_success and image_success and speech_success:
        print("🎉 All tests passed! LangGraph integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main()) 