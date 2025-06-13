import os
import pytest
import yaml
from pathlib import Path
from src.tools.video import VideoGenerationTool, generate_video

def _load_config() -> dict:
    """Load configuration from conf.yaml."""
    root_dir = Path(__file__).parent.parent
    config_path = root_dir / "conf.yaml"
    
    if not os.path.exists(config_path):
        pytest.skip("conf.yaml not found")
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    # Get Azure configuration
    azure_config = config.get("azure", {}).get("video", {})
    if not azure_config or not azure_config.get("api_key"):
        pytest.skip("Azure video configuration not found in conf.yaml")
        
    return azure_config

def test_video_generation():
    """Test video generation using the Sora API."""
    # Load configuration
    config = _load_config()
    
    # Create tool instance
    tool = VideoGenerationTool()
    
    # Test video generation
    prompt = "A cute cat playing with a ball of yarn"
    try:
        # Test direct tool usage
        result = tool.generate_video(
            prompt=prompt,
            height=1080,
            width=1080,
            n_seconds=5,
            n_variants=1,
            timeout=60  # Short timeout for testing
        )
        
        # Verify response structure
        assert "id" in result, "No job ID in response"
        assert "status" in result, "No status in response"
        assert result["status"].lower() == "succeeded", f"Job failed with status: {result['status']}"
        
        # Verify video URLs
        if "output" in result and "videos" in result["output"]:
            assert len(result["output"]["videos"]) > 0, "No videos in output"
            for video in result["output"]["videos"]:
                assert "url" in video, "No URL in video output"
                assert video["url"].startswith("http"), "Invalid video URL"
        
        # Test LangChain tool wrapper
        tool_result = generate_video.invoke({
            "prompt": prompt,
            "height": 1080,
            "width": 1080,
            "n_seconds": 5,
            "n_variants": 1
        })
        
        assert "Successfully generated video" in tool_result, "Tool wrapper failed"
        assert "Job ID:" in tool_result, "No job ID in tool response"
        
        print(f"✅ Video generation test passed!")
        print(f"Job ID: {result.get('id')}")
        if "output" in result and "videos" in result["output"]:
            print("Video URLs:")
            for i, video in enumerate(result["output"]["videos"]):
                print(f"{i+1}. {video.get('url')}")
                
    except Exception as e:
        pytest.fail(f"Video generation test failed: {str(e)}")

if __name__ == "__main__":
    test_video_generation() 