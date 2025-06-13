#!/usr/bin/env python3
"""
Test video generation through DeerFlow's complete architecture.
This demonstrates the proper way to use video generation within the DeerFlow system.
"""

import asyncio
from src.workflow import run_agent_workflow_async

async def test_simple_video_generation():
    """Test simple video generation without research steps."""
    
    print("🎬 Simple Video Generation Test")
    print("=" * 40)
    
    # Simple, direct video generation request
    query = "Create a short video of a cute cat playing with a ball of yarn"
    
    print(f"🚀 Processing request: {query}")
    print("-" * 40)
    
    try:
        # Run through DeerFlow with minimal steps
        await run_agent_workflow_async(
            user_input=query,
            debug=True,
            max_plan_iterations=1,
            max_step_num=1,  # Limit to 1 step to force direct generation
            enable_background_investigation=False
        )
        
        print("✅ Simple video generation test completed!")
        
    except Exception as e:
        print(f"❌ Simple video generation test failed: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_video_generation_through_deerflow():
    """Test video generation using DeerFlow's complete workflow."""
    
    print("🎬 Testing Video Generation through DeerFlow Architecture")
    print("=" * 60)
    
    # Test cases for video generation
    test_cases = [
        {
            "name": "Simple Video Request",
            "query": "Generate a video of a cute cat playing with a ball of yarn",
            "description": "Basic video generation request"
        },
        {
            "name": "Detailed Video Request", 
            "query": "Create a 5-second video showing a golden retriever puppy running through a sunny meadow with flowers, in 1080p resolution",
            "description": "Detailed video with specifications"
        },
        {
            "name": "Creative Video Request",
            "query": "I need a video for my presentation about nature. Generate a peaceful forest scene with sunlight filtering through trees",
            "description": "Context-aware video generation"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 Test Case {i}: {test_case['name']}")
        print(f"📝 Description: {test_case['description']}")
        print(f"💬 Query: {test_case['query']}")
        print("-" * 50)
        
        try:
            # Run through DeerFlow's complete workflow
            await run_agent_workflow_async(
                user_input=test_case['query'],
                debug=True,  # Enable debug for detailed logging
                max_plan_iterations=1,
                max_step_num=3,
                enable_background_investigation=False  # Skip web search for video generation
            )
            
            print(f"✅ Test Case {i} completed successfully!")
            
        except Exception as e:
            print(f"❌ Test Case {i} failed: {str(e)}")
        
        print("\n" + "="*60)
        
        # Ask if user wants to continue to next test
        if i < len(test_cases):
            try:
                continue_test = input(f"\nContinue to Test Case {i+1}? (y/n): ").lower().strip()
                if continue_test not in ['y', 'yes', '']:
                    print("Testing stopped by user.")
                    break
            except (EOFError, KeyboardInterrupt):
                print("\nTesting interrupted by user.")
                break

def test_single_video_request():
    """Test a single video generation request through DeerFlow."""
    
    print("🎬 Single Video Generation Test")
    print("=" * 40)
    
    # Get user input
    try:
        user_query = input("Enter your video generation request: ").strip()
        if not user_query:
            user_query = "Generate a video of a cute cat playing with a ball of yarn"
            print(f"Using default query: {user_query}")
    except (EOFError, KeyboardInterrupt):
        print("Input cancelled.")
        return
    
    print(f"\n🚀 Processing request: {user_query}")
    print("-" * 40)
    
    # Run through DeerFlow
    asyncio.run(
        run_agent_workflow_async(
            user_input=user_query,
            debug=True,
            max_plan_iterations=1,
            max_step_num=3,
            enable_background_investigation=False
        )
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test video generation through DeerFlow")
    parser.add_argument(
        "--mode", 
        choices=["single", "batch", "simple"], 
        default="simple",
        help="Test mode: single request, batch tests, or simple direct generation"
    )
    
    args = parser.parse_args()
    
    if args.mode == "batch":
        asyncio.run(test_video_generation_through_deerflow())
    elif args.mode == "simple":
        asyncio.run(test_simple_video_generation())
    else:
        test_single_video_request() 