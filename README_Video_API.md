# Video Generation API - Azure OpenAI Sora Integration

This document explains how to use the video generation functionality integrated into the DeerFlow system using Azure OpenAI's Sora model.

## Overview

The video generation feature allows you to create high-quality videos from text descriptions. The system is built with a modular architecture that includes:

- **Video Generation Tool** (`src/tools/video.py`) - Core API integration
- **Video Generation Agent** (`src/agents/video_agent.py`) - Agent wrapper
- **DeerFlow Integration** - Complete workflow integration

## Quick Start

### 1. Configuration

First, ensure your `conf.yaml` file contains the Azure OpenAI configuration:

```yaml
azure:
  video:
    api_key: "your-azure-openai-api-key"
    base_url: "https://your-endpoint.openai.azure.com"
    api_version: "preview"
    model: "sora"
```

### 2. Direct Tool Usage

```python
from src.tools.video import VideoGenerationTool

# Initialize the tool
video_tool = VideoGenerationTool()

# Generate a video
result = video_tool.generate_video(
    prompt="A cute cat playing with a ball of yarn",
    height=1080,
    width=1080,
    n_seconds=15,
    n_variants=1
)

# Access video URLs
video_urls = result.get("video_urls", [])
print(f"Generated videos: {video_urls}")

# Download video (optional)
if video_urls:
    video_tool.download_video(video_urls[0], "output_video.mp4")
```

### 3. LangChain Tool Usage

```python
from src.tools.video import generate_video

# Use as a LangChain tool
result = generate_video(
    prompt="A golden retriever running through a sunny meadow",
    height=1080,
    width=1920,
    n_seconds=10
)
```

### 4. DeerFlow Integration

Simply ask DeerFlow to generate a video:

```python
from src.workflow import run_agent_workflow_async

# Run through complete DeerFlow workflow
await run_agent_workflow_async(
    user_input="Generate a video of a sunset over the ocean",
    debug=True,
    max_step_num=3,
    enable_background_investigation=False
)
```

Or use the test script:

```bash
python test_deerflow_video.py --mode simple
```

## API Parameters

### Video Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Text description of the video to generate |
| `height` | int | 1080 | Video height in pixels |
| `width` | int | 1080 | Video width in pixels |
| `n_seconds` | int | 5 | Duration of the video in seconds |
| `n_variants` | int | 1 | Number of video variants to generate |

### Configuration Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | Azure OpenAI API key |
| `base_url` | string | Azure OpenAI endpoint URL |
| `api_version` | string | API version (default: "preview") |
| `model` | string | Model name (default: "sora") |

## Response Format

The API returns a dictionary with the following structure:

```json
{
  "id": "job-12345",
  "status": "succeeded",
  "generations": [
    {
      "id": "gen-67890",
      "status": "succeeded"
    }
  ],
  "video_urls": [
    "https://your-endpoint.openai.azure.com/openai/v1/video/generations/gen-67890/content/video?api-version=preview"
  ]
}
```

## Error Handling

The system includes comprehensive error handling:

```python
try:
    result = video_tool.generate_video("A cat playing with yarn")
    print("Video generated successfully!")
except TimeoutError:
    print("Video generation timed out")
except RuntimeError as e:
    print(f"Generation failed: {e}")
except ValueError as e:
    print(f"Invalid parameters: {e}")
```

## Best Practices

### Prompt Writing

- **Be specific**: Include details about actions, settings, and visual elements
- **Use descriptive language**: Mention lighting, colors, and mood
- **Keep it clear**: Avoid conflicting or impossible scenarios

**Good examples:**
- "A fluffy orange cat playfully batting at a red ball of yarn in a cozy living room with warm lighting"
- "A golden retriever running through a sunny meadow with wildflowers, shot from a low angle"

**Avoid:**
- "A cat" (too vague)
- "A flying cat in space eating pizza" (unrealistic)

### Technical Considerations

- **Duration**: 5-30 seconds works best for quality
- **Resolution**: Use standard resolutions (1080x1080, 1920x1080)
- **Timeout**: Allow sufficient time for generation (default: 5 minutes)

## Testing

### Direct API Test

```bash
python test_video_direct.py
```

### Complete Workflow Test

```bash
python test_deerflow_video.py --mode simple
```

### Batch Testing

```bash
python test_deerflow_video.py --mode batch
```

## Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   Error: Azure API key not found in config or provided
   ```
   Solution: Check your `conf.yaml` configuration

2. **Template Not Found**
   ```
   Error: 'video_generator.md' not found
   ```
   Solution: Ensure `src/prompts/video_generator.md` exists

3. **Generation Timeout**
   ```
   Error: Video generation timed out after 300 seconds
   ```
   Solution: Increase timeout parameter or try a simpler prompt

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Architecture

```
User Request
    ↓
Coordinator (identifies video request)
    ↓
Planner (creates video_generation step)
    ↓
Video Generator Agent
    ↓
Video Generation Tool
    ↓
Azure OpenAI Sora API
    ↓
Generated Video URLs
```

## Files Structure

```
src/
├── tools/
│   └── video.py              # Core video generation tool
├── agents/
│   └── video_agent.py        # Video generation agent
├── prompts/
│   └── video_generator.md    # Agent prompt template
├── graph/
│   ├── builder.py            # Graph structure with video node
│   └── nodes.py              # Video generator node implementation
└── config/
    └── agents.py             # Agent configuration

test_video_direct.py          # Direct API testing
test_deerflow_video.py        # Complete workflow testing
conf.yaml                     # Configuration file
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the test scripts for examples
3. Enable debug mode for detailed logs
4. Verify your Azure OpenAI configuration

## License

This integration is part of the DeerFlow system. Please refer to the main project license. 