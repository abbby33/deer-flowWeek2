import os
from dotenv import load_dotenv
from src.tools.imagen import ImageGenerationTool
from src.tools.speech import SpeechGenerationTool

# API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable must be set")

def test_image_generation():
    """Test image generation."""
    print("Testing image generation...")
    tool = ImageGenerationTool(API_KEY)
    images = tool.generate_images("A beautiful sunset over mountains", num_images=1)
    
    # Save the generated image
    images[0].save("generated_sunset.png")
    print("Image saved as generated_sunset.png")

def test_speech_generation():
    """Test speech generation."""
    print("Testing speech generation...")
    tool = SpeechGenerationTool(API_KEY)
    audio = tool.generate_speech("Hello, this is a test of the speech generation tool.")
    
    # Save the generated audio
    with open("generated_speech.mp3", "wb") as f:
        f.write(audio)
    print("Audio saved as generated_speech.mp3")

if __name__ == "__main__":
    # Test image generation
    test_image_generation()
    
    # Test speech generation
    test_speech_generation() 