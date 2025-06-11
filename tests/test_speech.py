# tests/test_speech.py
import os
import unittest
from src.tools.speech import SpeechGenerationTool

class TestSpeechGenerationTool(unittest.TestCase):
    def setUp(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.speech_tool = SpeechGenerationTool(api_key=self.api_key)

    def test_single_speaker_speech_generation(self):
        text = "Hello, this is a test of the speech generation tool."
        output_path = self.speech_tool.generate_speech(text)
        
        self.assertIsNotNone(output_path)
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith(".wav"))
        
        # Clean up
        os.remove(output_path)

    def test_multi_speaker_speech_generation(self):
        dialogue = """
        Speaker1: Hi there! How are you today?
        Speaker2: I'm doing great, thanks for asking!
        """
        
        speakers = {
            "Speaker1": "kore",
            "Speaker2": "puck"
        }
        
        output_path = self.speech_tool.generate_multi_speaker_speech(dialogue, speakers)
        
        self.assertIsNotNone(output_path)
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith(".wav"))
        
        # Clean up
        os.remove(output_path)

    def test_different_voices(self):
        text = "Hello world"  # Use simple text
        # Test with known working voices
        working_voices = ["kore", "puck", "charon", "leda"]
        
        for voice in working_voices:
            with self.subTest(voice=voice):
                output_path = self.speech_tool.generate_speech(text, voice_name=voice)
                
                self.assertIsNotNone(output_path, f"Voice '{voice}' should work")
                if output_path and os.path.exists(output_path):
                    self.assertTrue(output_path.endswith(".wav"))
                    os.remove(output_path)

    def test_error_handling(self):
        # Test with invalid voice name
        output_path = self.speech_tool.generate_speech("Test text", voice_name="InvalidVoice")
        self.assertIsNone(output_path, "Invalid voice should return None")

        # Test with empty text
        output_path = self.speech_tool.generate_speech("")
        self.assertIsNone(output_path, "Empty text should return None")
        
        # Test with whitespace-only text
        output_path = self.speech_tool.generate_speech("   ")
        self.assertIsNone(output_path, "Whitespace-only text should return None")

    def test_voice_normalization(self):
        """Test that voice names are properly normalized to lowercase."""
        text = "Hello world"
        
        # Test uppercase voice name
        output_path = self.speech_tool.generate_speech(text, voice_name="KORE")
        self.assertIsNotNone(output_path, "Uppercase voice name should be normalized")
        
        if output_path and os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    unittest.main()
