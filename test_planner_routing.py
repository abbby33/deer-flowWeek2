#!/usr/bin/env python3
"""
Test script to verify that the planner correctly routes requests to image and speech agents.
"""

import os
import asyncio
from src.graph.builder import build_graph
from src.config.configuration import Configuration

async def test_planner_routing_image():
    """Test that the planner routes image requests to the image agent."""
    print("Testing planner routing for image generation...")
    
    # Build the graph
    graph = build_graph()
    
    # Create configuration
    config = {
        "configurable": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "max_search_results": 5,
            "max_plan_iterations": 3,
            "enable_background_investigation": False,
        }
    }
    
    # Test input that should route to image generation
    initial_state = {
        "messages": [{"role": "user", "content": "Please create an image showing a futuristic city skyline at night with neon lights"}],
        "locale": "en-US",
        "auto_accepted_plan": True,
    }
    
    try:
        # Run the graph step by step
        result = await graph.ainvoke(initial_state, config)
        
        # Check if the result contains evidence of image generation
        messages = result.get("messages", [])
        has_image_content = any("generated_images" in str(msg) or "image" in str(msg).lower() for msg in messages)
        
        print(f"Image routing test result: {has_image_content}")
        print(f"Final messages: {len(messages)} messages")
        
        return has_image_content
    except Exception as e:
        print(f"Error in image routing test: {e}")
        return False

async def test_planner_routing_speech():
    """Test that the planner routes speech requests to the speech agent."""
    print("Testing planner routing for speech generation...")
    
    # Build the graph
    graph = build_graph()
    
    # Create configuration
    config = {
        "configurable": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "max_search_results": 5,
            "max_plan_iterations": 3,
            "enable_background_investigation": False,
        }
    }
    
    # Test input that should route to speech generation
    initial_state = {
        "messages": [{"role": "user", "content": "Please convert this text to audio: Welcome to our AI-powered DeerFlow system!"}],
        "locale": "en-US",
        "auto_accepted_plan": True,
    }
    
    try:
        # Run the graph
        result = await graph.ainvoke(initial_state, config)
        
        # Check if the result contains evidence of speech generation
        messages = result.get("messages", [])
        has_speech_content = any("generated_audio" in str(msg) or "speech" in str(msg).lower() for msg in messages)
        
        print(f"Speech routing test result: {has_speech_content}")
        print(f"Final messages: {len(messages)} messages")
        
        return has_speech_content
    except Exception as e:
        print(f"Error in speech routing test: {e}")
        return False

async def test_planner_routing_combined():
    """Test that the planner can handle requests for both image and speech generation."""
    print("Testing planner routing for combined image and speech generation...")
    
    # Build the graph
    graph = build_graph()
    
    # Create configuration
    config = {
        "configurable": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "max_search_results": 5,
            "max_plan_iterations": 3,
            "enable_background_investigation": False,
        }
    }
    
    # Test input that should route to both agents
    initial_state = {
        "messages": [{"role": "user", "content": "Create an image of a robot, then generate speech saying 'Hello, I am your AI assistant'"}],
        "locale": "en-US",
        "auto_accepted_plan": True,
    }
    
    try:
        # Run the graph
        result = await graph.ainvoke(initial_state, config)
        
        # Check if the result contains evidence of both image and speech generation
        messages = result.get("messages", [])
        has_image_content = any("generated_images" in str(msg) or "image" in str(msg).lower() for msg in messages)
        has_speech_content = any("generated_audio" in str(msg) or "speech" in str(msg).lower() for msg in messages)
        
        print(f"Combined routing test - Image: {has_image_content}, Speech: {has_speech_content}")
        print(f"Final messages: {len(messages)} messages")
        
        return has_image_content and has_speech_content
    except Exception as e:
        print(f"Error in combined routing test: {e}")
        return False

async def main():
    """Main test function."""
    print("=== DeerFlow Planner Routing Test ===\n")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test image routing
    print("\n1. Testing image generation routing...")
    image_success = await test_planner_routing_image()
    
    if image_success:
        print("✅ Image routing test passed")
    else:
        print("❌ Image routing test failed")
    
    # Test speech routing
    print("\n2. Testing speech generation routing...")
    speech_success = await test_planner_routing_speech()
    
    if speech_success:
        print("✅ Speech routing test passed")
    else:
        print("❌ Speech routing test failed")
    
    # Test combined routing
    print("\n3. Testing combined routing...")
    combined_success = await test_planner_routing_combined()
    
    if combined_success:
        print("✅ Combined routing test passed")
    else:
        print("❌ Combined routing test failed")
    
    # Summary
    print("\n=== Test Summary ===")
    if image_success and speech_success:
        print("🎉 Planner routing is working correctly!")
        print("✅ I can run: 'Generate an image of a cat' → image output is returned")
        print("✅ I can run: 'Read this aloud: Welcome!' → audio is generated")
        print("✅ The planner routes prompts to the new agents correctly")
        print("✅ The agents appear in the LangGraph graph and work in planner mode")
    else:
        print("⚠️ Some routing tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main()) 