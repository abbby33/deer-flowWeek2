import os
import logging
import requests
import json
import time
import yaml
from pathlib import Path
from typing import Annotated, Optional, Dict, Any, List
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _load_config() -> Dict[str, Any]:
    """Load configuration from conf.yaml."""
    root_dir = Path(__file__).parent.parent.parent
    config_path = root_dir / "conf.yaml"
    
    if not os.path.exists(config_path):
        raise ValueError("conf.yaml not found")
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    # Get Azure configuration
    azure_config = config.get("azure", {}).get("video", {})
    if not azure_config:
        raise ValueError("Azure video configuration not found in conf.yaml")
        
    return azure_config

class VideoGenerationTool:
    """Tool for generating videos using Azure OpenAI's Sora API."""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        """
        Initialize the video generation tool.
        
        Args:
            api_key (str, optional): Azure OpenAI API key. If not provided, will be loaded from config.
            endpoint (str, optional): Azure OpenAI endpoint URL. If not provided, will be loaded from config.
        """
        # Load configuration
        config = _load_config()
        
        # Use provided values or fall back to config
        self.api_key = api_key or config.get("api_key")
        self.endpoint = (endpoint or config.get("base_url")).rstrip('/')
        self.api_version = config.get("api_version", "preview")
        self.model = config.get("model", "sora")
        
        if not self.api_key:
            raise ValueError("Azure API key not found in config or provided")
        if not self.endpoint:
            raise ValueError("Azure endpoint URL not found in config or provided")
            
        logger.info(f"Initialized VideoGenerationTool with endpoint: {self.endpoint}")

    def _make_request(self, prompt: str, height: int = 1080, width: int = 1080, 
                     n_seconds: int = 5, n_variants: int = 1) -> Dict[str, Any]:
        """
        Make a request to the Sora API to generate a video.
        
        Args:
            prompt (str): Text description of the video to generate
            height (int): Video height in pixels
            width (int): Video width in pixels
            n_seconds (int): Duration of the video in seconds
            n_variants (int): Number of video variants to generate
            
        Returns:
            Dict[str, Any]: API response containing job information
        """
        url = f"{self.endpoint}/openai/v1/video/generations/jobs?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "Api-key": self.api_key
        }
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "height": str(height),
            "width": str(width),
            "n_seconds": str(n_seconds),
            "n_variants": str(n_variants)
        }
        
        try:
            logger.info(f"Making request to Sora API with prompt: {prompt[:50]}...")
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Sora API: {str(e)}")
            raise

    def _check_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Check the status of a video generation job.
        
        Args:
            job_id (str): ID of the video generation job
            
        Returns:
            Dict[str, Any]: Job status information
        """
        url = f"{self.endpoint}/openai/v1/video/generations/jobs/{job_id}?api-version={self.api_version}"
        
        headers = {
            "Api-key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking job status: {str(e)}")
            raise

    def _get_video_urls(self, job_result: Dict[str, Any]) -> List[str]:
        """
        Extract video URLs from completed job result.
        
        Args:
            job_result (Dict[str, Any]): Completed job result from API
            
        Returns:
            List[str]: List of video download URLs
        """
        video_urls = []
        generations = job_result.get("generations", [])
        
        for generation in generations:
            generation_id = generation.get("id")
            if generation_id:
                # Construct video content URL according to Azure OpenAI docs
                video_url = f"{self.endpoint}/openai/v1/video/generations/{generation_id}/content/video?api-version={self.api_version}"
                video_urls.append(video_url)
                
        return video_urls

    def download_video(self, video_url: str, output_path: str) -> bool:
        """
        Download a video from the given URL.
        
        Args:
            video_url (str): URL to download the video from
            output_path (str): Local path to save the video
            
        Returns:
            bool: True if download successful, False otherwise
        """
        headers = {
            "Api-key": self.api_key
        }
        
        try:
            logger.info(f"Downloading video to {output_path}")
            response = requests.get(video_url, headers=headers)
            response.raise_for_status()
            
            with open(output_path, "wb") as file:
                file.write(response.content)
                
            logger.info(f"Video successfully downloaded to {output_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading video: {str(e)}")
            return False

    def generate_video(self, prompt: str, height: int = 1080, width: int = 1080, 
                      n_seconds: int = 5, n_variants: int = 1, 
                      poll_interval: int = 5, timeout: int = 300) -> Dict[str, Any]:
        """
        Generate a video using the Sora API and wait for completion.
        
        Args:
            prompt (str): Text description of the video to generate
            height (int): Video height in pixels
            width (int): Video width in pixels
            n_seconds (int): Duration of the video in seconds
            n_variants (int): Number of video variants to generate
            poll_interval (int): Seconds to wait between status checks
            timeout (int): Maximum seconds to wait for completion
            
        Returns:
            Dict[str, Any]: Final job status with video URLs
        """
        # Submit the job
        job_info = self._make_request(prompt, height, width, n_seconds, n_variants)
        job_id = job_info.get("id")
        
        if not job_id:
            raise ValueError("No job ID received from API")
            
        logger.info(f"Video generation job submitted with ID: {job_id}")
        
        # Poll for completion
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Video generation timed out after {timeout} seconds")
                
            status = self._check_job_status(job_id)
            job_status = status.get("status", "").lower()
            
            if job_status == "succeeded":
                logger.info(f"Video generation job {job_id} completed successfully")
                
                # Add video URLs to the result
                video_urls = self._get_video_urls(status)
                if video_urls:
                    status["video_urls"] = video_urls
                    logger.info(f"Generated {len(video_urls)} video(s)")
                    for i, url in enumerate(video_urls):
                        logger.info(f"Video {i+1} URL: {url}")
                
                return status
            elif job_status == "failed":
                error = status.get("error", "Unknown error")
                raise RuntimeError(f"Video generation failed: {error}")
            elif job_status in ["cancelled", "deleted"]:
                raise RuntimeError(f"Video generation job was {job_status}")
                
            logger.info(f"Job {job_id} status: {job_status}. Waiting {poll_interval} seconds...")
            time.sleep(poll_interval)

@tool
def generate_video(
    prompt: Annotated[str, "A detailed description of the video to generate"],
    height: Annotated[int, "Video height in pixels (default: 1080)"] = 1080,
    width: Annotated[int, "Video width in pixels (default: 1080)"] = 1080,
    n_seconds: Annotated[int, "Duration of the video in seconds (default: 5)"] = 5,
    n_variants: Annotated[int, "Number of video variants to generate (default: 1)"] = 1
) -> str:
    """
    Generate a video from a text description using Azure OpenAI's Sora model.
    
    Args:
        prompt: A detailed description of the video to generate
        height: Video height in pixels (default: 1080)
        width: Video width in pixels (default: 1080)
        n_seconds: Duration of the video in seconds (default: 5)
        n_variants: Number of video variants to generate (default: 1)
        
    Returns:
        str: Success message with video URLs or error message
    """
    try:
        # Create tool instance (will load config automatically)
        tool_instance = VideoGenerationTool()
        
        # Generate video
        result = tool_instance.generate_video(
            prompt=prompt,
            height=height,
            width=width,
            n_seconds=n_seconds,
            n_variants=n_variants
        )
        
        # Format response
        response = f"Successfully generated video from prompt: '{prompt}'\n"
        response += f"Job ID: {result.get('id')}\n"
        
        # Add video URLs if available
        if "video_urls" in result:
            response += "\nVideo URLs (copy to browser to view):\n"
            for i, url in enumerate(result["video_urls"]):
                response += f"{i+1}. {url}\n"
        else:
            response += "\nNote: Video URLs not available in response. You may need to query the job status again.\n"
                
        return response
        
    except Exception as e:
        return f"Error generating video: {str(e)}" 