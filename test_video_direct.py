from src.tools.video import VideoGenerationTool, _load_config
import json

def test_video_direct():
    """Test video generation directly using the tool."""
    # Create tool instance
    tool = VideoGenerationTool()
    
    # 获取API参数
    config = _load_config()
    api_key = config.get("api_key")
    endpoint = config.get("base_url").rstrip('/')
    api_version = config.get("api_version", "preview")
    model = config.get("model", "sora")
    
    prompt = "A cute puppy playing with a ball of yarn"
    height = 1080
    width = 1080
    n_seconds = 5
    n_variants = 1
    
    # 打印等价cURL命令
    curl_cmd = f'''
curl -X POST "{endpoint}/openai/v1/video/generations/jobs?api-version={api_version}" \\
  -H "Content-Type: application/json" \\
  -H "Api-key: {api_key}" \\
  -d '{{
     "model": "{model}",
     "prompt" : "{prompt}",
     "height" : "{height}",
     "width" : "{width}",
     "n_seconds" : "{n_seconds}",
     "n_variants" : "{n_variants}"
    }}'
'''
    print("\nSample Request (cURL):")
    print(curl_cmd)
    
    print(f"Generating video for prompt: {prompt}")
    
    try:
        # Generate video
        result = tool.generate_video(
            prompt=prompt,
            height=height,
            width=width,
            n_seconds=n_seconds,
            n_variants=n_variants,
            timeout=300  # 5 minutes timeout
        )
        
        # Print results
        print("\nVideo generation completed!")
        print(f"Job ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        
        # Print full response for debugging
        print("\nFull API Response:")
        print(json.dumps(result, indent=2))
        
        # Print video URLs if available
        if "video_urls" in result:
            print("\n🎬 Video URLs (copy to browser to view):")
            for i, url in enumerate(result["video_urls"]):
                print(f"{i+1}. {url}")
                
            # Ask if user wants to download videos
            print("\n📥 Download videos? (y/n): ", end="")
            try:
                choice = input().lower().strip()
                if choice in ['y', 'yes']:
                    for i, url in enumerate(result["video_urls"]):
                        output_filename = f"generated_video_{i+1}.mp4"
                        print(f"Downloading video {i+1} to {output_filename}...")
                        success = tool.download_video(url, output_filename)
                        if success:
                            print(f"✅ Video {i+1} downloaded successfully!")
                        else:
                            print(f"❌ Failed to download video {i+1}")
            except (EOFError, KeyboardInterrupt):
                print("\nSkipping download.")
        else:
            print("\n⚠️ No video URLs found in response.")
            print("This might be because the API response format has changed.")
            print("You can try manually constructing the URL using the generation IDs above.")
                
    except Exception as e:
        print(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    test_video_direct() 