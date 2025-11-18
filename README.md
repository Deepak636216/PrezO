# AI-Powered PPT Generator (Free Tier MVP)

Transform reference documents into professional PowerPoint presentations using multi-agent AI system.

## Features

- 🎯 **7 Specialized AI Agents** - Sequential pipeline for content-to-presentation
- 📄 **Smart Content Analysis** - Processes PDF, DOCX, and text files
- 🎨 **Template-Driven** - Auto-extracts and uses your PowerPoint templates
- 🖼️ **Image Prompt Generation** - Creates detailed prompts for image generators
- 💰 **100% Free Tier** - Uses Google AI Studio and GCP free tier
- 📊 **Session Management** - Track progress and resume workflows
- 🔍 **Full Observability** - Logging and metrics tracking

## Architecture

### 7-Agent Pipeline

1. **Content Ingestion Agent** - Analyzes reference documents
2. **Presentation Strategy Agent** - Creates slide outline and narrative
3. **Content Generation Agent** - Generates slide content
4. **Image Prompt Generation Agent** - Creates detailed image prompts
5. **Template Selector Agent** - Chooses optimal layouts
6. **Content Formatting Agent** - Formats content for templates
7. **PPT Assembler Agent** - Builds final presentation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your Google AI Studio API key
```

Get your free API key from: https://makersuite.google.com/app/apikey

### 3. Run Example

```bash
python main.py
```

## Project Structure

```
PrezO/
├── agents/                 # All 7 AI agents
│   ├── __init__.py
│   ├── content_ingestion.py
│   ├── strategy.py
│   ├── content_generation.py
│   ├── image_prompt.py
│   ├── template_selector.py
│   ├── formatting.py
│   └── assembler.py
├── tools/                  # Custom tools
│   ├── __init__.py
│   ├── template_analyzer.py
│   └── document_extractor.py
├── orchestration/          # Workflow management
│   ├── __init__.py
│   ├── orchestrator.py
│   └── session.py
├── observability/          # Logging & metrics
│   ├── __init__.py
│   ├── logger.py
│   └── metrics.py
├── templates/              # PPT templates
├── output/                 # Generated presentations
├── tests/                  # Test files
├── main.py                 # CLI interface
├── requirements.txt
└── README.md
```

## Usage

### Basic Usage

```python
from orchestration.orchestrator import ContentDrivenOrchestrator

# Initialize
orchestrator = ContentDrivenOrchestrator(session_id="unique_session_id")

# Run workflow
result = orchestrator.execute_workflow(
    reference_file_path="path/to/document.pdf",
    user_guidance={
        "purpose": "pitch",
        "audience": "executives",
        "tone": "professional",
        "slide_count_preference": "8-10"
    }
)

print(f"Presentation created: {result['pptx_path']}")
print(f"Image prompts: {result['prompts_json_path']}")
```

## Testing

Run tests for each module:

```bash
# Test template analysis
python -m pytest tests/test_template_analyzer.py

# Test content pipeline
python -m pytest tests/test_content_pipeline.py

# Test full workflow
python -m pytest tests/test_orchestrator.py
```

## Cost Analysis

**Development & Testing (50 presentations):**
- Gemini API: FREE (AI Studio)
- Firestore: FREE (within daily limits)
- Total Cost: $0.00

**Per Presentation:**
- Processing time: ~35 seconds
- Cost: $0

## Future Enhancements

- [ ] Integrate Imagen 3 for actual image generation
- [ ] Web UI interface
- [ ] Google Drive integration
- [ ] Template marketplace

## License

MIT License
