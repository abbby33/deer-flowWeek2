from src.tools.imagen import ImageGenerationTool
import os

def test_image_generation():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")
    tool = ImageGenerationTool(api_key=api_key)
    
    # Generate images
    prompt = "Please generate a cartoon image of a cat."
    try:
        images = tool.generate_images(prompt)
        print(f"Generated {len(images)} images")
        assert len(images) > 0, "No images were generated"
        
        # Test saving images
        paths = tool.save_images(images)
        assert len(paths) == len(images), "Not all images were saved"
        
        # Verify files were created
        for path in paths:
            assert os.path.exists(path), f"Image file not found at {path}"
            # 暂时注释掉删除图片的代码
            # Clean up test files
            # os.remove(path)
        
        # 暂时注释掉删除目录的代码
        # Clean up test directory if empty
        # try:
        #     os.rmdir("generated_images")
        # except OSError:
        #     pass  # Directory not empty or already deleted
            
    except Exception as e:
        print(f"Error during image generation: {str(e)}")
        raise
