# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "coordinator": "basic",
    "planner": "basic",
    "researcher": "basic",
    "coder": "basic",
    "reporter": "basic",
    "podcast_script_writer": "basic",
    "ppt_composer": "basic",
    "prose_writer": "basic",
    "prompt_enhancer": "basic",
    "image_generator": "basic",
    "speech_generator": "basic",
    "video_generator": "basic",
}

# Team configuration
TEAM_MEMBER_CONFIGRATIONS = {
    "researcher": {
        "name": "researcher",
        "desc": (
            "Responsible for searching and collecting relevant information, understanding user needs and conducting research analysis"
        ),
        "desc_for_llm": (
            "Uses search engines and web crawlers to gather information from the internet. "
            "Outputs a Markdown report summarizing findings. Researcher can not do math or programming."
        ),
        "is_optional": False,
    },
    "coder": {
        "name": "coder",
        "desc": (
            "Responsible for code implementation, debugging and optimization, handling technical programming tasks"
        ),
        "desc_for_llm": (
            "Executes Python or Bash commands, performs mathematical calculations, and outputs a Markdown report. "
            "Must be used for all mathematical computations."
        ),
        "is_optional": True,
    },
    "image_generator": {
        "name": "image_generator",
        "desc": (
            "Responsible for generating images from text descriptions using Google's Imagen-3 model"
        ),
        "desc_for_llm": (
            "Uses Google's Imagen-3 model to generate high-quality images from text descriptions. "
            "Outputs the generated image and any relevant feedback."
        ),
        "is_optional": True,
        "llm_type": "basic",
    },
    "speech_generator": {
        "name": "speech_generator",
        "desc": (
            "Responsible for converting text to speech using Google's Gemini TTS"
        ),
        "desc_for_llm": (
            "Uses Google's Gemini TTS to convert text into natural-sounding speech. "
            "Outputs the generated audio and any relevant feedback."
        ),
        "is_optional": True,
        "llm_type": "basic",
    },
    "video_generator": {
        "name": "video_generator",
        "desc": (
            "Responsible for generating videos from text descriptions using Azure OpenAI's Sora model"
        ),
        "desc_for_llm": (
            "Uses Azure OpenAI's Sora model to generate high-quality videos from text descriptions. "
            "Can create videos with specified dimensions, duration, and number of variants. "
            "Outputs the generated video URLs and any relevant feedback."
        ),
        "is_optional": True,
        "llm_type": "basic",
    },
}
