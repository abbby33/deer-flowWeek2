# src/tools/speech.py
import os
import logging
import base64
from typing import Annotated

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Warning: google-genai package not found. Please install it with: pip install google-genai")
    genai = None
    types = None

from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported voices based on Google API
SUPPORTED_VOICES = [
    "achernar", "achird", "algenib", "algieba", "alnilam", "aoede", "autonoe", 
    "callirrhoe", "charon", "despina", "enceladus", "erinome", "fenrir", 
    "gacrux", "iapetus", "kore", "laomedeia", "leda", "orus", "puck", 
    "pulcherrima", "rasalgethi", "sadachbia", "sadaltager", "schedar", 
    "sulafat", "umbriel", "vindemiatrix", "zephyr", "zubenelgenubi"
]

class SpeechGenerationTool:
    def __init__(self, api_key):
        if genai is None:
            raise ImportError("google-genai package is required. Install with: pip install google-genai")
        
        self.client = genai.Client(api_key=api_key)
        self.output_dir = "generated_audio"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        logger.info("Initialized SpeechGenerationTool with Google Gemini TTS API")

    def generate_speech(self, text, voice_name="kore", output_filename=None):
        """
        Generate speech from text using Google Gemini TTS API.
        
        Args:
            text (str): The text to convert to speech
            voice_name (str): The voice to use (default: "kore")
            output_filename (str): Optional output filename
            
        Returns:
            str: Path to the generated audio file, or None if failed
        """
        # Input validation
        if not text or not text.strip():
            logger.error("Empty or whitespace-only text provided")
            return None
        
        # Normalize voice name to lowercase
        voice_name = voice_name.lower()
        
        # Validate voice name
        if voice_name not in SUPPORTED_VOICES:
            logger.error(f"Voice '{voice_name}' not supported. Supported voices: {', '.join(SUPPORTED_VOICES)}")
            return None
        
        try:
            logger.info(f"Generating speech with voice '{voice_name}' for text: {text[:50]}...")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=f"Say: {text}",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name,
                            )
                        )
                    ),
                )
            )

            # Validate response
            if not response or not response.candidates:
                logger.error("No response or candidates received from API")
                return None
                
            if not response.candidates[0].content or not response.candidates[0].content.parts:
                logger.error("No content or parts in response")
                return None

            # Extract audio data
            audio_part = response.candidates[0].content.parts[0]
            if not hasattr(audio_part, 'inline_data') or not audio_part.inline_data:
                logger.error("No inline_data in response part")
                return None
                
            audio_data = audio_part.inline_data.data
            
            if not audio_data:
                logger.error("No audio data in response")
                return None
            
            if output_filename is None:
                output_filename = f"generated_speech_{len(os.listdir(self.output_dir))}.wav"
            
            if not output_filename.endswith('.wav'):
                output_filename += '.wav'
                
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Decode base64 audio data and save as WAV file
            audio_bytes = base64.b64decode(audio_data)
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            
            logger.info(f"Saved audio file to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            return None

    def generate_multi_speaker_speech(self, dialogue, speakers=None):
        """
        Generate multi-speaker dialogue using Google Gemini TTS API.
        
        Args:
            dialogue (str): The dialogue text with speaker labels
            speakers (dict): Optional mapping of speaker names to voice names
            
        Returns:
            str: Path to the generated audio file, or None if failed
        """
        # Input validation
        if not dialogue or not dialogue.strip():
            logger.error("Empty or whitespace-only dialogue provided")
            return None
        
        if speakers is None:
            speakers = {
                "Speaker1": "kore",
                "Speaker2": "puck"
            }

        # Validate all voice names
        for speaker, voice in speakers.items():
            voice_lower = voice.lower()
            if voice_lower not in SUPPORTED_VOICES:
                logger.error(f"Voice '{voice}' for {speaker} not supported. Using 'kore' instead.")
                speakers[speaker] = "kore"
            else:
                speakers[speaker] = voice_lower

        try:
            logger.info(f"Generating multi-speaker speech for dialogue: {dialogue[:50]}...")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=f"TTS the following conversation: {dialogue}",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                            speaker_voice_configs=[
                                types.SpeakerVoiceConfig(
                                    speaker=speaker,
                                    voice_config=types.VoiceConfig(
                                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                            voice_name=voice
                                        )
                                    )
                                )
                                for speaker, voice in speakers.items()
                            ]
                        )
                    )
                )
            )

            # Validate response
            if not response or not response.candidates:
                logger.error("No response or candidates received from API")
                return None
                
            if not response.candidates[0].content or not response.candidates[0].content.parts:
                logger.error("No content or parts in response")
                return None

            # Extract audio data
            audio_part = response.candidates[0].content.parts[0]
            if not hasattr(audio_part, 'inline_data') or not audio_part.inline_data:
                logger.error("No inline_data in response part")
                return None
                
            audio_data = audio_part.inline_data.data
            
            if not audio_data:
                logger.error("No audio data in response")
                return None
            
            output_filename = f"generated_dialogue_{len(os.listdir(self.output_dir))}.wav"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Decode base64 audio data and save as WAV file
            audio_bytes = base64.b64decode(audio_data)
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            
            logger.info(f"Saved audio file to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating multi-speaker speech: {str(e)}")
            return None


@tool
def generate_speech(
    text: Annotated[str, "The text to convert to speech"],
    voice_name: Annotated[str, "The voice to use (e.g., kore, puck, charon, leda)"] = "kore"
) -> str:
    """Convert text to speech using Google's Gemini TTS API."""
    try:
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY environment variable not set"
        
        # Create tool instance
        tool_instance = SpeechGenerationTool(api_key)
        
        # Generate speech
        output_path = tool_instance.generate_speech(text, voice_name)
        
        if not output_path:
            return "Failed to generate speech"
        
        return f"Successfully generated speech from text: '{text}'\nSaved to: {output_path}"
        
    except Exception as e:
        return f"Error generating speech: {str(e)}"


@tool
def generate_multi_speaker_speech(
    dialogue: Annotated[str, "The dialogue text with speaker labels"],
    speakers: Annotated[str, "JSON string mapping speaker names to voice names"] = None
) -> str:
    """Generate multi-speaker dialogue using Google's Gemini TTS API."""
    try:
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY environment variable not set"
        
        # Create tool instance
        tool_instance = SpeechGenerationTool(api_key)
        
        # Parse speakers if provided
        speakers_dict = None
        if speakers:
            import json
            try:
                speakers_dict = json.loads(speakers)
            except json.JSONDecodeError:
                return "Error: Invalid JSON format for speakers parameter"
        
        # Generate multi-speaker speech
        output_path = tool_instance.generate_multi_speaker_speech(dialogue, speakers_dict)
        
        if not output_path:
            return "Failed to generate multi-speaker speech"
        
        return f"Successfully generated multi-speaker dialogue\nSaved to: {output_path}"
        
    except Exception as e:
        return f"Error generating multi-speaker speech: {str(e)}"
