import requests
import tempfile
import webbrowser
import os
from src.tools.video import _load_config

def view_video_from_url(video_url: str):
    """
    Download video from URL and open in default video player.
    
    Args:
        video_url (str): The video URL from Sora API
    """
    try:
        # Load config to get API key
        config = _load_config()
        api_key = config.get("api_key")
        
        if not api_key:
            print("❌ API key not found in configuration")
            return
            
        print(f"🔄 Downloading video from URL...")
        print(f"URL: {video_url}")
        
        # Make authenticated request
        headers = {
            "Api-key": api_key
        }
        
        response = requests.get(video_url, headers=headers)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
            
        print(f"✅ Video downloaded successfully!")
        print(f"📁 Temporary file: {temp_path}")
        
        # Open in default video player
        print(f"🎬 Opening video in default player...")
        
        # Try different methods to open the video
        try:
            # Windows
            os.startfile(temp_path)
        except AttributeError:
            try:
                # macOS
                os.system(f'open "{temp_path}"')
            except:
                try:
                    # Linux
                    os.system(f'xdg-open "{temp_path}"')
                except:
                    print(f"⚠️ Could not auto-open video. Please manually open: {temp_path}")
                    
        print(f"🎉 Done! Video should be playing now.")
        print(f"📝 Note: Temporary file will be cleaned up when you close the video.")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading video: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    # Use the URL from your recent generation
    video_url = "https://ai-sherlockscofield1621ai532464794360.openai.azure.com/openai/v1/video/generations/gen_01jxn58m5terd93xycxnhheg2n/content/video?api-version=preview"
    
    print("🎬 Sora Video Viewer")
    print("=" * 50)
    
    view_video_from_url(video_url) 