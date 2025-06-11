import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.imagen import ImageGenerationTool, ImageGenerationConfig
from src.tools.speech import SpeechGenerationTool, SpeechConfig

def test_image_generation(api_key):
    print("\nTesting Image Generation Tool...")
    image_tool = ImageGenerationTool(api_key)
    
    prompt = "A cute deer in a magical forest, digital art style"
    print(f"Generating image for prompt: {prompt}")
    
    config = ImageGenerationConfig(
        number_of_images=1,
        aspect_ratio="16:9",
        safety_filter_level="block_medium_and_above",
        person_generation="allow_adult"
    )
    
    try:
        images = image_tool.generate_images(prompt, config)
        print(f"Successfully generated {len(images)} image(s)")
        
        # Save the images
        paths = image_tool.save_images(images)
        print(f"Images saved to: {paths}")
        return True
    except Exception as e:
        print(f"❌ Image generation failed: {str(e)}")
        return False

def test_speech_generation(api_key):
    print("\nTesting Speech Generation Tool...")
    speech_tool = SpeechGenerationTool(api_key)
    
    text = "Hello! This is a test of the speech generation system."
    print(f"Generating speech for text: {text}")
    
    config = SpeechConfig(
        language_code="en-US",
        voice_name="en-US-Neural2-C",
        speaking_rate=1.0
    )
    
    try:
        audio_data = speech_tool.generate_speech(text, config)
        print("Successfully generated speech")
        
        # Save the audio
        path = speech_tool.save_audio(audio_data)
        print(f"Audio saved to: {path}")
        return True
    except Exception as e:
        print(f"❌ Speech generation failed: {str(e)}")
        return False

def main():
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")
    
    # Run tests
    image_success = test_image_generation(api_key)
    speech_success = test_speech_generation(api_key)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Image Generation: {'✅ Success' if image_success else '❌ Failed'}")
    print(f"Speech Generation: {'✅ Success' if speech_success else '❌ Failed'}")

if __name__ == "__main__":
    main() 