# Setup Instructions for AI-Powered PPT Generator

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `python-pptx` - PowerPoint manipulation
- `PyPDF2` - PDF text extraction
- `python-docx` - Word document extraction
- `google-generativeai` - Google AI SDK (Gemini)
- `python-dotenv` - Environment variable management

### 2. Get Google AI Studio API Key (FREE)

The application uses Google's Gemini 2.0 Flash model, which is 100% FREE through Google AI Studio.

**Steps to get API key:**

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### 3. Configure Environment Variables

**Option A: Create .env file (Recommended)**

Create a file named `.env` in the project root:

```bash
GOOGLE_AI_STUDIO_KEY=your_api_key_here
```

**Option B: Set environment variable**

Windows:
```cmd
set GOOGLE_AI_STUDIO_KEY=your_api_key_here
```

Linux/Mac:
```bash
export GOOGLE_AI_STUDIO_KEY=your_api_key_here
```

### 4. Verify Installation

Run the test suite:

```bash
# Test Module 1: Template Management
python tests/test_module1_template.py

# Test Module 2: Content Ingestion (requires API key)
python tests/test_module2_ingestion.py
```

## Testing Without API Key

For testing Module 1 (Template Management), no API key is required:

```bash
python tests/test_module1_template.py
python tests/test_generated_template_usage.py
```

## Project Structure

```
PrezO/
├── agents/                  # AI Agents (Modules 2-7)
│   ├── content_ingestion.py  # Module 2 ✓
│   ├── strategy.py           # Module 3 (in progress)
│   ├── content_generation.py # Module 4 (pending)
│   ├── image_prompt.py       # Module 5 (pending)
│   ├── template_selector.py  # Module 6 (pending)
│   └── formatting.py         # Module 7 (pending)
├── tools/                   # Custom Tools
│   ├── template_analyzer.py  # Module 1 ✓
│   └── document_extractor.py # Module 1 ✓
├── templates/               # Generated template functions
├── output/                  # Generated presentations
├── tests/                   # Test files
└── main.py                  # CLI interface (pending)
```

## Current Status

### ✅ Completed Modules

**Module 1: Template Management System**
- Template analyzer
- Function generator
- Document extractor
- Fully tested with presentation-template.pptx

**Module 2: Content Ingestion Agent**
- Document analysis with Gemini AI
- Text extraction from PDF/DOCX/TXT
- Content structure analysis
- Named entity recognition

### 🚧 In Progress

- Module 3: Presentation Strategy Agent
- Module 4: Content Generation Agent

## Troubleshooting

### "ModuleNotFoundError: No module named 'pptx'"
```bash
pip install python-pptx
```

### "GOOGLE_AI_STUDIO_KEY not found"
Make sure you've set the environment variable or created a .env file with your API key.

### "Template file not found"
Ensure you're running commands from the project root directory where `presentation-template.pptx` is located.

## Next Steps

1. Complete Module 3 (Presentation Strategy Agent)
2. Complete Module 4 (Content Generation Agent)
3. Test Modules 2-4 together
4. Continue with Modules 5-8
5. Build orchestration layer
6. Create CLI interface

## Support

For issues or questions, refer to:
- README.md
- User Story: userstory.md
- Module summaries: MODULE1_SUMMARY.md, etc.
