import base64
import os
from io import BytesIO
from PIL import Image
from typing import List, Annotated
import google.generativeai as genai
import logging
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerationTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-preview-image-generation')
        logger.info(f"Initialized ImageGenerationTool with model: {self.model.model_name}")

    def generate_images(self, prompt: str) -> List[Image.Image]:
        try:
            logger.info(f"Generating image with prompt: {prompt}")
            
            response = self.model.generate_content(
                contents=prompt,
                generation_config={
                    "temperature": 0.9,
                    "top_p": 1,
                    "top_k": 32,
                    "max_output_tokens": 2048,
                    "response_modalities": ["TEXT", "IMAGE"]
                }
            )
            
            logger.info("Response received from model")
            
            images = []
            for part in response.candidates[0].content.parts:
                if part.text:
                    logger.info(f"Text response: {part.text}")
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_bytes = part.inline_data.data
                    image = Image.open(BytesIO(image_bytes))
                    images.append(image)
            
            logger.info(f"Successfully generated {len(images)} images")
            return images
            
        except Exception as e:
            logger.error(f"Error generating images: {str(e)}")
            raise

    def save_images(self, images: List[Image.Image], output_dir: str = "generated_images") -> List[str]:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        saved_paths = []
        for i, image in enumerate(images):
            path = os.path.join(output_dir, f"generated_image_{i}.png")
            image.save(path)
            saved_paths.append(path)
            
        return saved_paths


@tool
def generate_image(prompt: Annotated[str, "A detailed description of the image to generate"]) -> str:
    """Generate an image from a text description using Google's Imagen-3 model."""
    try:
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY environment variable not set"
        
        # Create tool instance
        tool_instance = ImageGenerationTool(api_key)
        
        # Generate images
        images = tool_instance.generate_images(prompt)
        
        if not images:
            return "No images were generated"
        
        # Save images
        saved_paths = tool_instance.save_images(images)
        
        result = f"Successfully generated {len(images)} image(s) from prompt: '{prompt}'\n"
        result += "Saved to:\n"
        for path in saved_paths:
            result += f"- {path}\n"
        
        return result
        
    except Exception as e:
        return f"Error generating image: {str(e)}"
