# 🖼️🔊 DeerFlow Image & Speech Generation Agents


## 🛠️ **Tool & Agent Functionality**

### **🖼️ Image Generation Tool**
- **Model**: Google Gemini Imagen-3 (`gemini-2.0-flash-preview-image-generation`)
- **Functionality**:
  - High-quality image generation from text descriptions
  - Supports detailed prompts and various artistic styles
  - Automatic image saving with descriptive responses
- **Output Format**: PNG files saved to `generated_images/generated_image_N.png`
- **LangChain Integration**: `@tool` decorator for seamless agent integration

### **🔊 Speech Generation Tool**
- **Model**: Google Gemini TTS (`gemini-2.5-flash-preview-tts`)  
- **Functionality**:
  - Natural speech synthesis with 30+ voice options
  - Multi-speaker dialogue generation
  - Voice name normalization and validation
  - Comprehensive error handling
- **Supported Voices**: `kore`, `puck`, `charon`, `leda`, `fenrir`, `gacrux`, and 25+ more
- **Output Format**: WAV files saved to `generated_audio/generated_speech_N.wav`
- **LangChain Integration**: Multiple `@tool` decorators for single and multi-speaker generation

---

## 🚀 **Installation & Setup**

### **Prerequisites**
- Python 3.12+
- Google API Key with access to Gemini models
- DeerFlow project environment

### **1. Install Dependencies**
```bash
# Core packages
pip install google-genai google-generativeai langchain-core

# Or install from requirements
pip install -r requirements.txt
```

### **2. Set API Key**
```bash
# Environment variable (recommended)
export GOOGLE_API_KEY="your-google-api-key-here"

# Or in .env file
echo "GOOGLE_API_KEY=your-google-api-key-here" >> .env
```

### **3. Configure DeerFlow**
Update `conf.yaml` with correct model configurations:
```yaml
BASIC_MODEL:
  base_url: "https://generativelanguage.googleapis.com/v1beta"
  model: "gemini-1.5-flash"
  api_key: "your-api-key"
  temperature: 0.7
  max_tokens: 1000
```

---

## 🔗 **Registration & Integration Details**

### **Agent Registration Location**
**File**: `src/config/agents.py`

```python
# Agent-LLM mapping
AGENT_LLM_MAP = {
    "coordinator": "basic",
    "planner": "basic", 
    "researcher": "basic",
    "coder": "basic",
    "image_generator": "basic",     # ← Added
    "speech_generator": "basic",    # ← Added
}

# Team member configurations
TEAM_MEMBER_CONFIGRATIONS = {
    "image_generator": {
        "name": "image_generator",
        "desc": "Responsible for generating images from text descriptions using Google's Imagen-3 model",
        "desc_for_llm": "Uses Google's Imagen-3 model to generate high-quality images from text descriptions. Outputs the generated image and any relevant feedback.",
        "is_optional": True,
        "llm_type": "basic",
    },
    "speech_generator": {
        "name": "speech_generator",
        "desc": "Responsible for converting text to speech using Google's Gemini TTS",
        "desc_for_llm": "Uses Google's Gemini TTS to convert text into natural-sounding speech. Outputs the generated audio and any relevant feedback.",
        "is_optional": True,
        "llm_type": "basic",
    },
}
```

### **Graph Integration Location**
**File**: `src/graph/builder.py`

```python
# Node registration
def _build_base_graph():
    builder = StateGraph(State)
    # ... existing nodes ...
    builder.add_node("image_generator", image_generator_node)    # ← Added
    builder.add_node("speech_generator", speech_generator_node)  # ← Added
    
    # Routing logic
    builder.add_conditional_edges(
        "research_team",
        continue_to_running_research_team,
        ["planner", "researcher", "coder", "image_generator", "speech_generator"],  # ← Updated
    )
```

**File**: `src/graph/nodes.py`

```python
# Node implementations
async def image_generator_node(state: State, config: RunnableConfig) -> Command[Literal["research_team"]]:
    """Image generator node that generates images from text descriptions."""
    from src.tools.imagen import generate_image
    tools = [generate_image]
    return await _setup_and_execute_agent_step(state, config, "image_generator", tools)

async def speech_generator_node(state: State, config: RunnableConfig) -> Command[Literal["research_team"]]:
    """Speech generator node that converts text to speech."""  
    from src.tools.speech import generate_speech, generate_multi_speaker_speech
    tools = [generate_speech, generate_multi_speaker_speech]
    return await _setup_and_execute_agent_step(state, config, "speech_generator", tools)
```

### **Step Type Registration**
**File**: `src/prompts/planner_model.py`

```python
class StepType(str, Enum):
    RESEARCH = "research"
    PROCESSING = "processing"
    IMAGE_GENERATION = "image_generation"     # ← Added
    SPEECH_GENERATION = "speech_generation"   # ← Added
```

### **Routing Logic Location**
**File**: `src/graph/builder.py`

```python
def continue_to_running_research_team(state: State):
    # ... existing logic ...
    if step.step_type and step.step_type == StepType.IMAGE_GENERATION:
        return "image_generator"     # ← Added
    if step.step_type and step.step_type == StepType.SPEECH_GENERATION:
        return "speech_generator"    # ← Added
    return "planner"
```

---

## 💡 **Example Commands & Expected Outputs**

### **🖼️ Image Generation Examples**

#### **Direct Tool Usage**
```python
from src.tools.imagen import generate_image

# Simple image generation
result = generate_image.invoke({"prompt": "A cute cat playing with a ball"})
print(result)
# Output: "Successfully generated 1 image(s) from prompt: 'A cute cat playing with a ball'\nSaved to:\n- generated_images/generated_image_0.png"
```

#### **Through DeerFlow Planner**
```python
import asyncio
from src.graph.builder import build_graph

async def test_image_generation():
    graph = build_graph()
    config = {"configurable": {"api_key": "your-api-key"}}
    
    result = await graph.ainvoke({
        "messages": [{"role": "user", "content": "Generate an image of a futuristic cityscape at sunset"}],
        "locale": "en-US",
        "auto_accepted_plan": True
    }, config)
    
    return result

# Run: asyncio.run(test_image_generation())
```

#### **Expected Output Structure**
```
📁 generated_images/
  └── generated_image_0.png  (High-resolution PNG image)
```

### **🔊 Speech Generation Examples**

#### **Single Speaker Generation**
```python
from src.tools.speech import generate_speech

# Basic speech generation
result = generate_speech.invoke({
    "text": "Welcome to DeerFlow! This is an AI-powered research platform.",
    "voice_name": "kore"
})
print(result)
# Output: "Successfully generated speech from text: 'Welcome to DeerFlow! This is an AI-powered research platform.'\nSaved to: generated_audio/generated_speech_0.wav"
```

#### **Multi-Speaker Dialogue**
```python
from src.tools.speech import generate_multi_speaker_speech

dialogue = """
Speaker1: Hello! Welcome to our AI demonstration.
Speaker2: Thank you! I'm excited to see what DeerFlow can do.
Speaker1: Let me show you our latest features.
"""

result = generate_multi_speaker_speech.invoke({
    "dialogue": dialogue,
    "speakers": '{"Speaker1": "kore", "Speaker2": "puck"}'
})
print(result)
# Output: "Successfully generated multi-speaker dialogue\nSaved to: generated_audio/generated_dialogue_0.wav"
```

#### **Through DeerFlow Planner**
```python
# Speech generation via natural language planning
result = await graph.ainvoke({
    "messages": [{"role": "user", "content": "Please read this text aloud: Hello world, this is a test of the speech system!"}],
    "locale": "en-US", 
    "auto_accepted_plan": True
}, config)
```

#### **Expected Output Structure**
```
📁 generated_audio/
  ├── generated_speech_0.wav     (Single speaker audio)
  ├── generated_speech_1.wav
  └── generated_dialogue_0.wav   (Multi-speaker audio)
```

### **Voice Options**
Available voices: `kore`, `puck`, `charon`, `leda`, `fenrir`, `gacrux`, `achernar`, `achird`, `algenib`, `algieba`, `alnilam`, `aoede`, `autonoe`, `callirrhoe`, `despina`, `enceladus`, `erinome`, `iapetus`, `laomedeia`, `orus`, `pulcherrima`, `rasalgethi`, `sadachbia`, `sadaltager`, `schedar`, `sulafat`, `umbriel`, `vindemiatrix`, `zephyr`, `zubenelgenubi`

---

## 🧪 **Testing & Validation**

### **Run Unit Tests**
```bash
# Test speech generation
cd tests
pytest test_speech.py -v

# Test image generation  
pytest test_imagen.py -v
```

### **Run Integration Tests**
```bash
# Test LangGraph integration
python test_langgraph_integration.py

# Test planner routing
python test_planner_routing.py
```

### **Manual Testing Commands**
```bash
# Quick image test
python -c "from src.tools.imagen import generate_image; print(generate_image.invoke({'prompt': 'A simple test image'}))"

# Quick speech test
python -c "from src.tools.speech import generate_speech; print(generate_speech.invoke({'text': 'Hello world', 'voice_name': 'kore'}))"
```

### **Expected Test Results**
- ✅ **5/5 speech tests passing** (single speaker, multi-speaker, error handling, voice normalization, different voices)
- ✅ **Image generation working** (successful image creation and file saving)
- ✅ **LangGraph integration functional** (agents respond through planner)
- ✅ **Routing working** (planner correctly identifies and routes to appropriate agents)

---

## 📁 **File Structure**

```
deer-flowWeek2/
├── src/
│   ├── tools/
│   │   ├── imagen.py              # 🖼️ Image generation tool + LangChain wrapper
│   │   └── speech.py              # 🔊 Speech generation tool + LangChain wrapper
│   ├── agents/
│   │   ├── image_agent.py         # 🖼️ LangGraph image agent
│   │   └── speech_agent.py        # 🔊 LangGraph speech agent
│   ├── graph/
│   │   ├── builder.py             # 🔗 Graph construction with new agents
│   │   └── nodes.py               # 🔗 Node definitions for image/speech generators
│   ├── config/
│   │   └── agents.py              # ⚙️ Agent registry and configuration
│   └── prompts/
│       ├── planner_model.py       # 📝 Step types (IMAGE_GENERATION, SPEECH_GENERATION)
│       └── templates/
│           ├── image_generation.txt    # 🖼️ Image agent prompt template
│           └── speech_generation.txt   # 🔊 Speech agent prompt template
├── tests/
│   ├── test_imagen.py             # 🧪 Image tool tests
│   └── test_speech.py             # 🧪 Speech tool tests
├── generated_images/              # 📁 Image output directory
├── generated_audio/               # 📁 Audio output directory
├── test_langgraph_integration.py  # 🧪 Integration test script
├── test_planner_routing.py        # 🧪 Routing test script
└── README_AGENTS.md               # 📚 This documentation file
```

---
