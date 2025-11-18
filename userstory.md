# 🎯 AI-Powered PPT Generator - MVP User Story & Development Specification
## **FREE TIER OPTIMIZED - Image Prompt Generation Version**

---

## Project Overview

**Project Name:** AI-Powered Enterprise PPT Generator (Free Tier MVP)  
**Timeline:** 2.5 weeks (17.5 days)  
**Platform:** Google AI Studio + GCP Free Tier  
**Cost:** $0 (100% Free Tier)  
**Target:** Course submission demonstrating multi-agent systems, tools, sessions, and observability

---

## Executive Summary

Build an intelligent presentation generation system that:
1. Accepts uploaded PPTX templates and auto-extracts their structure
2. Generates callable Python functions for each template layout
3. Accepts user content as reference material (PDF/text/document upload)
4. AI agents analyze reference content and generate appropriate slide content
5. **Generates detailed image prompts instead of actual images (MVP simplification)**
6. Selects optimal templates and layouts using AI reasoning
7. Assembles branded presentations with image placeholders showing prompts
8. Demonstrates multi-agent orchestration, custom tools, sessions, and observability
9. **Runs entirely on GCP Free Tier**

---

## Key MVP Simplification

### ❌ REMOVED from MVP:
```
- Vertex AI Imagen 3 image generation ($0.04 per image)
- External image APIs
- Image processing libraries
- Large file storage for images
```

### ✅ ADDED to MVP:
```
- AI-generated detailed image prompts
- Image placeholder slides with prompts displayed
- Prompt quality scoring
- Prompt refinement capabilities
- Export prompts for future use with image generators
```

### 💡 Value Proposition:
```
This MVP proves the entire content-to-presentation pipeline
while staying 100% free tier. The image prompts generated
can later be used with:
- Imagen 3 (when budget available)
- DALL-E, Midjourney, Stable Diffusion
- Stock photo searches
- Design team assignments
```

---

## User Stories

### Epic 1: Template Management System

#### Story 1.1: Upload and Analyze PPT Template
**As a** system administrator  
**I want to** upload a PowerPoint template and have it automatically analyzed  
**So that** the system can extract layouts, placeholders, and styling information

**Acceptance Criteria:**
- [ ] User can upload .pptx file through interface
- [ ] System extracts all slide layouts from template
- [ ] System identifies placeholders: title, content, images, charts, headers, footers
- [ ] System captures positioning (x, y, width, height) for each placeholder
- [ ] System extracts color scheme, fonts, and styling
- [ ] System generates comprehensive metadata JSON file
- [ ] Processing completes within 30 seconds for typical templates

**Technical Requirements:**
```python
@tool
def analyze_ppt_template(template_file_path: str) -> dict:
    """
    Extract complete structure from PPTX template
    
    Args:
        template_file_path: Path to uploaded PPTX
    
    Returns:
        Template metadata with layouts, slots, positioning
    """
    from pptx import Presentation
    import json
    
    prs = Presentation(template_file_path)
    
    metadata = {
        "template_id": generate_template_id(template_file_path),
        "template_name": os.path.basename(template_file_path),
        "layouts": []
    }
    
    # Extract each layout
    for idx, layout in enumerate(prs.slide_layouts):
        layout_info = {
            "layout_id": f"layout_{idx}",
            "layout_name": layout.name,
            "slots": {}
        }
        
        # Extract placeholders
        for shape in layout.placeholders:
            slot_info = {
                "type": shape.placeholder_format.type,
                "position": {
                    "x": shape.left.inches,
                    "y": shape.top.inches,
                    "width": shape.width.inches,
                    "height": shape.height.inches
                }
            }
            layout_info["slots"][shape.name] = slot_info
        
        metadata["layouts"].append(layout_info)
    
    return metadata
```

---

#### Story 1.2: Generate Template Functions
**As a** system  
**I want to** auto-generate Python functions from template metadata  
**So that** agents can programmatically create slides using the template

**Acceptance Criteria:**
- [ ] System reads template metadata JSON
- [ ] System generates Python class with methods for each layout
- [ ] Each method includes proper type hints and docstrings
- [ ] Methods handle text insertion, bullet points, and **image placeholder boxes**
- [ ] Generated code includes error handling for invalid inputs
- [ ] Functions enforce template constraints (max chars, required fields)
- [ ] Code is saved as `{template_id}_functions.py`

**Technical Requirements:**
```python
@tool
def generate_template_functions(template_metadata: dict) -> str:
    """
    Auto-generate Python functions from template metadata
    
    Args:
        template_metadata: Parsed template structure
    
    Returns:
        Path to generated functions.py file
    """
    
    class_code = f'''
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

class {template_metadata["template_id"].title()}Template:
    """
    Auto-generated template functions
    Template: {template_metadata["template_name"]}
    """
    
    def __init__(self, prs: Presentation):
        self.prs = prs
        self.template_metadata = {template_metadata}
    
    def add_title_slide(self, title: str, subtitle: str = None) -> None:
        """Add title slide"""
        layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(layout)
        
        slide.shapes.title.text = title
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle
    
    def add_content_slide(self, title: str, bullets: list) -> None:
        """Add bullet point slide"""
        layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(layout)
        
        slide.shapes.title.text = title
        
        content = slide.placeholders[1]
        text_frame = content.text_frame
        text_frame.clear()
        
        for bullet in bullets:
            p = text_frame.add_paragraph()
            p.text = bullet
            p.level = 0
    
    def add_image_placeholder_slide(self, title: str, image_prompt: str, 
                                     context: str = None) -> None:
        """
        Add slide with image placeholder showing prompt
        
        Args:
            title: Slide title
            image_prompt: AI-generated image prompt to display
            context: Optional context about why this image
        """
        layout = self.prs.slide_layouts[5]  # Blank layout
        slide = self.prs.slides.add_slide(layout)
        
        # Add title
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.5), 
            Inches(9), Inches(0.8)
        )
        title_frame = title_box.text_frame
        title_frame.text = title
        title_frame.paragraphs[0].font.size = Pt(32)
        title_frame.paragraphs[0].font.bold = True
        
        # Add image placeholder box
        placeholder_box = slide.shapes.add_shape(
            1,  # Rectangle
            Inches(1.5), Inches(2),
            Inches(7), Inches(4)
        )
        placeholder_box.fill.solid()
        placeholder_box.fill.fore_color.rgb = RGBColor(232, 244, 248)
        placeholder_box.line.color.rgb = RGBColor(30, 58, 138)
        placeholder_box.line.width = Pt(2)
        
        # Add prompt text inside placeholder
        text_frame = placeholder_box.text_frame
        text_frame.word_wrap = True
        
        p1 = text_frame.paragraphs[0]
        p1.text = "📷 IMAGE PROMPT:"
        p1.font.size = Pt(14)
        p1.font.bold = True
        
        p2 = text_frame.add_paragraph()
        p2.text = image_prompt
        p2.font.size = Pt(12)
        p2.space_before = Pt(12)
        
        if context:
            p3 = text_frame.add_paragraph()
            p3.text = f"\\n💡 Context: {{context}}"
            p3.font.size = Pt(10)
            p3.font.italic = True
            p3.space_before = Pt(12)
    '''
    
    # Save to file
    output_path = f"templates/{template_metadata['template_id']}_functions.py"
    with open(output_path, 'w') as f:
        f.write(class_code)
    
    return output_path
```

---

### Epic 2: Content Analysis & Generation

#### Story 2.1: Content Ingestion Agent
**As a** user  
**I want to** upload reference materials or paste content  
**So that** the AI can understand my subject matter and create relevant slides

**Acceptance Criteria:**
- [ ] Accepts PDF document upload
- [ ] Accepts Word document (.docx) upload
- [ ] Accepts plain text paste
- [ ] Extracts text from PDFs (up to 50 pages)
- [ ] Extracts text from Word documents preserving structure
- [ ] Identifies document structure: headings, sections, lists
- [ ] Extracts key entities: names, dates, numbers, concepts
- [ ] Outputs structured content analysis

**Agent Configuration:**
```python
# Agent 1: Content Ingestion Agent
# Type: Tool-based + LLM-powered
# Model: Gemini 2.0 Flash (Google AI Studio - FREE)
# Tools: extract_document_content

import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO_KEY"])

class ContentIngestionAgent:
    """
    Analyzes uploaded reference documents
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def analyze_document(self, file_path: str) -> dict:
        """
        Extract and analyze document content
        """
        # Extract text
        extracted = self.extract_document_content(file_path)
        
        # Analyze with Gemini
        prompt = f"""
        Analyze this document and extract structured information.
        
        DOCUMENT TEXT:
        {extracted['full_text'][:50000]}  # Limit to 50K chars
        
        EXTRACT:
        1. Document type (product_brief, business_report, proposal, etc.)
        2. Main topic
        3. Key themes (top 5)
        4. Document structure (sections with summaries)
        5. Named entities (companies, products, people, dates)
        6. Complexity level
        
        OUTPUT FORMAT (JSON):
        {{
          "content_type": "string",
          "main_topic": "string",
          "key_themes": ["array"],
          "document_structure": [
            {{
              "section_title": "string",
              "content_summary": "string",
              "key_points": ["array"]
            }}
          ],
          "named_entities": {{
            "companies": ["array"],
            "products": ["array"],
            "people": ["array"]
          }},
          "complexity_level": "basic|intermediate|advanced"
        }}
        """
        
        response = self.model.generate_content(prompt)
        analysis = json.loads(response.text)
        
        # Add full text for later agents
        analysis["full_text"] = extracted["full_text"]
        analysis["total_words"] = extracted["word_count"]
        
        return analysis
    
    def extract_document_content(self, file_path: str) -> dict:
        """Extract text from PDF/DOCX/TXT"""
        import PyPDF2
        from docx import Document
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
            
            return {
                "file_type": "pdf",
                "full_text": text,
                "word_count": len(text.split())
            }
        
        elif file_ext == '.docx':
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            
            return {
                "file_type": "docx",
                "full_text": text,
                "word_count": len(text.split())
            }
        
        else:  # .txt
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            return {
                "file_type": "txt",
                "full_text": text,
                "word_count": len(text.split())
            }
```

---

#### Story 2.2: Presentation Strategy Agent
**As a** system  
**I want to** understand presentation requirements and create strategy  
**So that** I can build an effective narrative structure

**Acceptance Criteria:**
- [ ] Accepts user guidance: purpose, audience, tone, slide count
- [ ] Analyzes reference content to understand key messages
- [ ] Determines presentation type (pitch, report, training)
- [ ] Creates high-level slide structure/outline
- [ ] Identifies which slides need visual support
- [ ] Balances information density across slides
- [ ] Outputs detailed slide outline

**Agent Configuration:**
```python
# Agent 2: Presentation Strategy Agent
# Type: LLM-powered
# Model: Gemini 2.0 Flash (FREE)

class PresentationStrategyAgent:
    """
    Creates presentation strategy and outline
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def create_strategy(self, content_analysis: dict, user_guidance: dict) -> dict:
        """
        Create presentation strategy from content and guidance
        """
        
        prompt = f"""
        You are a presentation strategist. Create an effective slide outline.
        
        REFERENCE CONTENT:
        - Type: {content_analysis['content_type']}
        - Main Topic: {content_analysis['main_topic']}
        - Key Themes: {', '.join(content_analysis['key_themes'])}
        
        USER GUIDANCE:
        - Purpose: {user_guidance['purpose']}
        - Audience: {user_guidance['audience']}
        - Tone: {user_guidance['tone']}
        - Desired Slides: {user_guidance.get('slide_count_preference', '8-10')}
        
        TASK:
        Create a compelling presentation outline that tells a story.
        
        PRESENTATION PATTERNS:
        - Pitch: Hook → Problem → Solution → Benefits → Proof → CTA
        - Report: Summary → Background → Findings → Analysis → Recommendations
        - Training: Objectives → Concepts → Examples → Practice → Summary
        
        OUTPUT FORMAT (JSON):
        {{
          "presentation_type": "pitch|report|training|general",
          "narrative_arc": "string describing story flow",
          "total_slides": int,
          "slide_outline": [
            {{
              "slide_number": int,
              "slide_purpose": "opening|problem|solution|data|story|closing",
              "slide_title": "string",
              "content_source": "which section from reference",
              "key_message": "one sentence - what this slide says",
              "content_type": "title_only|bullets|text|comparison|data",
              "visual_needed": bool,
              "visual_type": "illustration|icon|diagram|photo|chart|none",
              "visual_purpose": "string - why visual needed",
              "estimated_text_amount": "minimal|moderate|substantial"
            }}
          ]
        }}
        
        IMPORTANT:
        - Be specific about visual needs
        - Balance text vs visual slides
        - Ensure logical flow
        """
        
        response = self.model.generate_content(prompt)
        strategy = json.loads(response.text)
        
        return strategy
```

**Example Output:**
```json
{
  "presentation_type": "pitch",
  "narrative_arc": "Start with customer pain, introduce solution, prove value with data, close with clear next steps",
  "total_slides": 8,
  "slide_outline": [
    {
      "slide_number": 1,
      "slide_purpose": "opening",
      "slide_title": "The Enterprise AI Challenge",
      "content_source": "Executive Summary",
      "key_message": "Enterprise AI adoption is failing",
      "content_type": "title_only",
      "visual_needed": false,
      "estimated_text_amount": "minimal"
    },
    {
      "slide_number": 2,
      "slide_purpose": "problem",
      "slide_title": "Why Traditional AI Fails",
      "content_source": "Market Problem section",
      "key_message": "Current solutions are complex and slow",
      "content_type": "bullets",
      "visual_needed": true,
      "visual_type": "illustration",
      "visual_purpose": "Show complexity and confusion of current state",
      "estimated_text_amount": "moderate"
    }
  ]
}
```

---

#### Story 2.3: Content Generation Agent
**As a** system  
**I want to** generate actual slide content from reference materials  
**So that** each slide has relevant, well-written content

**Acceptance Criteria:**
- [ ] Reads reference content and slide outline
- [ ] Generates appropriate content for each slide
- [ ] Extracts relevant information from reference material
- [ ] Writes compelling slide titles
- [ ] Creates concise bullet points
- [ ] Includes relevant data points and statistics
- [ ] Maintains consistent tone throughout
- [ ] Respects character limits

**Agent Configuration:**
```python
# Agent 3: Content Generation Agent
# Type: LLM-powered
# Model: Gemini 2.0 Flash (FREE)

class ContentGenerationAgent:
    """
    Generates slide content from reference materials
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_slides(self, reference_content: str, 
                       slide_outline: list, tone: str) -> dict:
        """
        Generate content for all slides
        """
        
        generated_slides = []
        
        for slide_spec in slide_outline:
            prompt = f"""
            Generate professional presentation content.
            
            SLIDE SPECIFICATION:
            - Number: {slide_spec['slide_number']}
            - Title: {slide_spec['slide_title']}
            - Purpose: {slide_spec['slide_purpose']}
            - Key Message: {slide_spec['key_message']}
            - Content Type: {slide_spec['content_type']}
            - Content Source: {slide_spec['content_source']}
            
            REFERENCE CONTENT (excerpt):
            {self._get_relevant_excerpt(reference_content, slide_spec['content_source'])}
            
            TONE: {tone}
            
            CONTENT WRITING RULES:
            1. Titles: Clear, benefit-oriented, under 80 chars
            2. Bullets: Concise, parallel structure, under 100 chars each
            3. Use specific numbers and data
            4. Lead with benefits, not features
            5. Active voice and strong verbs
            
            OUTPUT FORMAT (JSON):
            {{
              "title": "string (max 80 chars)",
              "subtitle": "string or null (max 100 chars)",
              "content": {{
                "type": "bullets|paragraph|comparison",
                "bullets": ["array of strings"] or null,
                "paragraph": "string" or null,
                "left_column": "string or array" or null,
                "right_column": "string or array" or null
              }},
              "source_excerpts": ["relevant quotes"],
              "rationale": "why this content"
            }}
            """
            
            response = self.model.generate_content(prompt)
            slide_content = json.loads(response.text)
            slide_content["slide_number"] = slide_spec["slide_number"]
            
            generated_slides.append(slide_content)
        
        return {"slides": generated_slides}
    
    def _get_relevant_excerpt(self, full_text: str, section_name: str) -> str:
        """Extract relevant portion of reference content"""
        # Simple keyword search - can be enhanced
        words = section_name.split()
        
        # Find paragraphs containing keywords
        paragraphs = full_text.split('\n\n')
        relevant = []
        
        for para in paragraphs:
            if any(word.lower() in para.lower() for word in words):
                relevant.append(para)
            
            if len(' '.join(relevant).split()) > 500:
                break
        
        return '\n\n'.join(relevant[:3])  # Max 3 paragraphs
```

---

#### Story 2.4: Image Prompt Generation Agent (🆕 KEY MVP FEATURE)
**As a** system  
**I want to** generate detailed, professional image prompts  
**So that** slides can later have high-quality images without generating them now

**Acceptance Criteria:**
- [ ] Generates detailed image prompts for slides needing visuals
- [ ] Prompts are specific enough to guide image generation tools
- [ ] Includes style, composition, colors, mood specifications
- [ ] Matches template color scheme
- [ ] Considers slide context and message
- [ ] Prompts are 100-300 words with clear descriptions
- [ ] Outputs can be used with Imagen, DALL-E, Midjourney, etc.
- [ ] Includes quality scoring for prompts

**Agent Configuration:**
```python
# Agent 4: Image Prompt Generation Agent (NEW FOR MVP)
# Type: LLM-powered
# Model: Gemini 2.0 Flash (FREE)

class ImagePromptGenerationAgent:
    """
    Generates detailed image prompts instead of actual images
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_image_prompts(self, slide_outline: list, 
                               generated_content: dict,
                               template_colors: dict) -> dict:
        """
        Generate detailed image prompts for slides needing visuals
        """
        
        image_prompts = []
        
        for slide_spec in slide_outline:
            if not slide_spec.get('visual_needed'):
                continue
            
            # Find generated content for this slide
            slide_content = next(
                s for s in generated_content['slides'] 
                if s['slide_number'] == slide_spec['slide_number']
            )
            
            prompt = f"""
            Generate a detailed, professional image generation prompt.
            
            SLIDE CONTEXT:
            - Title: {slide_content['title']}
            - Purpose: {slide_spec['slide_purpose']}
            - Key Message: {slide_spec['key_message']}
            - Visual Type Needed: {slide_spec['visual_type']}
            - Visual Purpose: {slide_spec.get('visual_purpose', 'Support slide message')}
            
            SLIDE CONTENT:
            {json.dumps(slide_content['content'], indent=2)}
            
            TEMPLATE COLORS:
            - Primary: {template_colors['primary']}
            - Secondary: {template_colors['secondary']}
            - Accent: {template_colors.get('accent', 'complementary color')}
            
            TASK:
            Create a detailed image generation prompt that would produce a 
            professional, presentation-quality image for this slide.
            
            PROMPT STRUCTURE:
            1. Subject: What is shown (be specific)
            2. Style: Professional, modern, minimalist, corporate
            3. Composition: Layout, arrangement, perspective
            4. Colors: Use template colors, professional palette
            5. Details: Important visual elements
            6. Mood: Professional, trustworthy, innovative, etc.
            7. Technical: Aspect ratio 16:9, high quality, suitable for business presentation
            
            GOOD PROMPT EXAMPLE:
            "Professional business illustration showing three interconnected gears 
            labeled 'Integration', 'Automation', and 'Security'. Modern flat design 
            style with clean lines. Corporate blue color scheme (#1E3A8A primary, 
            #3B82F6 secondary). Gears arranged in triangular composition on white 
            background. Subtle gradient effects. Convey sense of efficiency and 
            seamless operation. Vector-style, minimalist aesthetic. 16:9 aspect 
            ratio. High quality for presentation display."
            
            OUTPUT FORMAT (JSON):
            {{
              "slide_number": int,
              "visual_type": "string",
              "prompt": "detailed 150-300 word image generation prompt",
              "prompt_keywords": ["key", "concepts", "in", "prompt"],
              "style_tags": ["professional", "minimalist", "corporate"],
              "color_palette": ["#hex", "#hex"],
              "technical_specs": {{
                "aspect_ratio": "16:9",
                "style": "illustration|photo|icon|diagram",
                "quality": "high"
              }},
              "alternative_prompt": "shorter backup prompt if needed",
              "search_query": "if using stock photos, what to search",
              "rationale": "why this visual supports the slide"
            }}
            """
            
            response = self.model.generate_content(prompt)
            prompt_data = json.loads(response.text)
            
            # Score prompt quality
            prompt_data["quality_score"] = self._score_prompt(prompt_data)
            
            image_prompts.append(prompt_data)
        
        return {"image_prompts": image_prompts}
    
    def _score_prompt(self, prompt_data: dict) -> float:
        """
        Score prompt quality (0-1)
        Based on: specificity, length, style tags, color info
        """
        score = 0.0
        
        # Length check (150-300 words optimal)
        word_count = len(prompt_data['prompt'].split())
        if 150 <= word_count <= 300:
            score += 0.3
        elif word_count > 100:
            score += 0.15
        
        # Has style tags
        if len(prompt_data.get('style_tags', [])) >= 3:
            score += 0.2
        
        # Has color specifications
        if len(prompt_data.get('color_palette', [])) >= 2:
            score += 0.2
        
        # Has technical specs
        if 'technical_specs' in prompt_data:
            score += 0.15
        
        # Has alternative options
        if prompt_data.get('alternative_prompt') or prompt_data.get('search_query'):
            score += 0.15
        
        return min(score, 1.0)
```

**Example Output:**
```json
{
  "slide_number": 2,
  "visual_type": "illustration",
  "prompt": "Professional business illustration depicting the complexity of traditional AI implementation. Central image shows a tangled web of system icons (databases, applications, servers, cloud services) connected by chaotic, overlapping lines representing difficult integrations. Each system icon is distinct: database cylinders, application windows, server racks, cloud symbols. Lines between them are twisted and knotted, conveying confusion. Color scheme: corporate blue (#1E3A8A) for main systems, gray (#6B7280) for connection lines, subtle red (#EF4444) hints showing pain points. Modern flat design style with subtle shadows for depth. White or light gray background. Composition: systems arranged in circular pattern with tangled connections in center. Visual metaphor for complexity and integration challenges. Style: clean, professional, minimalist but clearly communicating difficulty. 16:9 aspect ratio. Vector-style illustration suitable for business presentation. Convey sense of overwhelming complexity that executives will recognize.",
  "prompt_keywords": [
    "tangled web",
    "system integration",
    "complexity",
    "enterprise systems",
    "difficult connections"
  ],
  "style_tags": [
    "professional",
    "flat design",
    "minimalist",
    "corporate",
    "vector-style"
  ],
  "color_palette": [
    "#1E3A8A",
    "#6B7280",
    "#EF4444"
  ],
  "technical_specs": {
    "aspect_ratio": "16:9",
    "style": "illustration",
    "quality": "high"
  },
  "alternative_prompt": "Simplified version: Multiple system icons connected by messy, tangled lines on white background. Blue and gray corporate colors.",
  "search_query": "complex enterprise system integration illustration",
  "rationale": "Visual metaphor of tangled systems directly supports the 'complexity' message of the slide about why traditional AI fails",
  "quality_score": 0.95
}
```

---

#### Story 2.5: Template Selector Agent
**As a** system  
**I want to** select optimal template and layouts  
**So that** content is presented effectively

**Acceptance Criteria:**
- [ ] Reviews available templates
- [ ] Matches presentation type to template style
- [ ] Selects specific layout for each slide
- [ ] Ensures layouts support required elements
- [ ] Provides reasoning for selections

**Agent Configuration:**
```python
# Agent 5: Template Selector Agent
# Type: LLM-powered with template catalog
# Model: Gemini 2.0 Flash (FREE)

class TemplateSelectorAgent:
    """
    Selects optimal templates and layouts
    """
    
    def __init__(self, template_catalog: dict):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.template_catalog = template_catalog
    
    def select_template(self, presentation_type: str, 
                       audience: str, 
                       slide_outline: list) -> dict:
        """
        Select best template and layouts
        """
        
        prompt = f"""
        Select the optimal template and layouts for this presentation.
        
        AVAILABLE TEMPLATES:
        {json.dumps(self.template_catalog, indent=2)}
        
        PRESENTATION INFO:
        - Type: {presentation_type}
        - Audience: {audience}
        - Total Slides: {len(slide_outline)}
        
        SLIDE OUTLINE:
        {json.dumps(slide_outline, indent=2)}
        
        TASK:
        1. Select best overall template
        2. For each slide, select optimal layout
        3. Ensure layouts support required content types
        
        SELECTION CRITERIA:
        - Template style matches presentation type
        - Layouts match content needs (bullets, images, etc.)
        - Professional and appropriate for audience
        
        OUTPUT FORMAT (JSON):
        {{
          "selected_template": "template_id",
          "template_name": "string",
          "selection_reasoning": "why this template",
          "slide_layout_mappings": [
            {{
              "slide_number": int,
              "layout_id": "string",
              "layout_name": "string",
              "reasoning": "why this layout"
            }}
          ]
        }}
        """
        
        response = self.model.generate_content(prompt)
        selection = json.loads(response.text)
        
        return selection
```

---

#### Story 2.6: Content Formatting Agent
**As a** system  
**I want to** format content to fit template slots perfectly  
**So that** slides look professional

**Acceptance Criteria:**
- [ ] Maps generated content to template slots
- [ ] Enforces character limits
- [ ] Formats bullet points correctly
- [ ] Creates image prompt placeholders
- [ ] Prepares function call parameters
- [ ] Validates all required slots are filled

**Agent Configuration:**
```python
# Agent 6: Content Formatting Agent
# Type: LLM-powered
# Model: Gemini 2.0 Flash (FREE)

class ContentFormattingAgent:
    """
    Formats content for template slots
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def format_content(self, generated_content: dict,
                      template_selection: dict,
                      image_prompts: dict) -> dict:
        """
        Format content to fit template slots
        """
        
        formatted_slides = []
        
        for slide_content in generated_content['slides']:
            slide_num = slide_content['slide_number']
            
            # Find layout mapping
            layout_mapping = next(
                m for m in template_selection['slide_layout_mappings']
                if m['slide_number'] == slide_num
            )
            
            # Find image prompt if needed
            image_prompt = next(
                (p for p in image_prompts.get('image_prompts', [])
                 if p['slide_number'] == slide_num),
                None
            )
            
            formatted = {
                "slide_number": slide_num,
                "template_function": self._get_function_name(layout_mapping['layout_id']),
                "function_parameters": {
                    "title": slide_content['title'][:80],
                    "subtitle": slide_content.get('subtitle', '')[:100] if slide_content.get('subtitle') else None
                },
                "image_prompt_data": None
            }
            
            # Add content based on type
            content_data = slide_content['content']
            
            if content_data['type'] == 'bullets' and content_data.get('bullets'):
                formatted['function_parameters']['bullets'] = [
                    b[:100] for b in content_data['bullets'][:6]
                ]
            
            elif content_data['type'] == 'paragraph' and content_data.get('paragraph'):
                formatted['function_parameters']['content'] = content_data['paragraph'][:500]
            
            # Add image prompt if slide has visual
            if image_prompt:
                formatted['image_prompt_data'] = {
                    "prompt": image_prompt['prompt'],
                    "visual_type": image_prompt['visual_type'],
                    "style_tags": image_prompt['style_tags'],
                    "quality_score": image_prompt['quality_score'],
                    "context": f"Supports: {slide_content.get('rationale', '')}"
                }
            
            formatted_slides.append(formatted)
        
        return {"slides": formatted_slides}
    
    def _get_function_name(self, layout_id: str) -> str:
        """Map layout ID to template function name"""
        mapping = {
            "layout_0": "add_title_slide",
            "layout_1": "add_content_slide",
            "layout_2": "add_image_placeholder_slide",
            "layout_5": "add_image_placeholder_slide"
        }
        return mapping.get(layout_id, "add_content_slide")
```

---

#### Story 2.7: PPT Assembler Agent
**As a** system  
**I want to** assemble the final presentation with image prompts displayed  
**So that** users get a complete, professional presentation

**Acceptance Criteria:**
- [ ] Loads selected template
- [ ] Imports generated template functions
- [ ] Creates slides programmatically
- [ ] Inserts content into proper slots
- [ ] **Creates image placeholder boxes with prompts displayed**
- [ ] Validates PPTX structure
- [ ] Saves final presentation
- [ ] **Exports image prompts to separate JSON file**

**Agent Configuration:**
```python
# Agent 7: PPT Assembler Agent
# Type: Tool-based
# Tools: assemble_presentation

@tool
def assemble_presentation(template_id: str,
                         formatted_slides: dict,
                         output_name: str = None) -> dict:
    """
    Assemble final PPTX with image prompt placeholders
    
    Args:
        template_id: Selected template ID
        formatted_slides: Formatted content and image prompts
        output_name: Optional custom output filename
    
    Returns:
        Dict with pptx_path and prompts_json_path
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    import importlib.util
    
    # Load template
    template_path = f"templates/{template_id}/template.pptx"
    prs = Presentation(template_path)
    
    # Import template functions
    func_path = f"templates/{template_id}_functions.py"
    spec = importlib.util.spec_from_file_location("template", func_path)
    template_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(template_module)
    
    # Initialize template class
    template = template_module.TemplateClass(prs)
    
    # Track all image prompts for export
    all_prompts = []
    
    # Create slides
    for slide_data in formatted_slides['slides']:
        func_name = slide_data['template_function']
        params = slide_data['function_parameters']
        
        # Get template function
        func = getattr(template, func_name)
        
        # If slide has image prompt, use special function
        if slide_data.get('image_prompt_data'):
            prompt_data = slide_data['image_prompt_data']
            
            template.add_image_placeholder_slide(
                title=params['title'],
                image_prompt=prompt_data['prompt'],
                context=prompt_data.get('context')
            )
            
            # Save prompt for export
            all_prompts.append({
                "slide_number": slide_data['slide_number'],
                "slide_title": params['title'],
                **prompt_data
            })
        
        else:
            # Regular content slide
            func(**params)
    
    # Save PPTX
    output_filename = output_name or f"generated_{int(time.time())}.pptx"
    pptx_path = f"output/{output_filename}"
    prs.save(pptx_path)
    
    # Export image prompts to JSON
    prompts_filename = output_filename.replace('.pptx', '_image_prompts.json')
    prompts_path = f"output/{prompts_filename}"
    
    with open(prompts_path, 'w') as f:
        json.dump({
            "presentation": output_filename,
            "total_image_prompts": len(all_prompts),
            "prompts": all_prompts,
            "usage_instructions": "These prompts can be used with Imagen 3, DALL-E, Midjourney, Stable Diffusion, or given to a designer"
        }, f, indent=2)
    
    return {
        "pptx_path": pptx_path,
        "prompts_json_path": prompts_path,
        "slides_created": len(formatted_slides['slides']),
        "prompts_generated": len(all_prompts)
    }
```

---

### Epic 3: Orchestration & Workflow

#### Story 3.1: Sequential Agent Orchestration
**As a** system  
**I want to** execute agents in proper sequence  
**So that** reference materials become polished presentations

**Acceptance Criteria:**
- [ ] Agents execute in order: Ingestion → Strategy → Content → Prompts → Template → Formatting → Assembly
- [ ] Each agent receives correct inputs
- [ ] Failed agent stops workflow with error
- [ ] Progress visible to user
- [ ] Execution time tracked

**Implementation:**
```python
class ContentDrivenOrchestrator:
    """
    Orchestrates 7-agent workflow (100% free tier)
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.session = PPTGeneratorSession(session_id)
        
        # Initialize agents (all using free Gemini)
        self.agent1_ingestion = ContentIngestionAgent()
        self.agent2_strategy = PresentationStrategyAgent()
        self.agent3_content = ContentGenerationAgent()
        self.agent4_prompts = ImagePromptGenerationAgent()  # NEW
        self.agent5_template = TemplateSelectorAgent(self.load_template_catalog())
        self.agent6_formatting = ContentFormattingAgent()
        self.agent7_assembler = PPTAssemblerAgent()
    
    def execute_workflow(self, reference_file_path: str, 
                        user_guidance: dict) -> dict:
        """
        Execute full workflow (FREE TIER)
        
        Returns:
            Dict with pptx_path and prompts_json_path
        """
        
        start_time = time.time()
        
        try:
            # Stage 1: Content Ingestion (3s)
            logger.info("Stage 1/7: Analyzing reference content")
            self.session.advance_stage("ingesting_content")
            
            content_analysis = self.agent1_ingestion.analyze_document(reference_file_path)
            self.session.update_state("content_analysis", content_analysis)
            
            # Stage 2: Presentation Strategy (4s)
            logger.info("Stage 2/7: Creating presentation strategy")
            self.session.advance_stage("planning_strategy")
            
            strategy = self.agent2_strategy.create_strategy(
                content_analysis=content_analysis,
                user_guidance=user_guidance
            )
            self.session.update_state("strategy", strategy)
            
            # Stage 3: Content Generation (10s)
            logger.info("Stage 3/7: Generating slide content")
            self.session.advance_stage("generating_content")
            
            generated_content = self.agent3_content.generate_slides(
                reference_content=content_analysis["full_text"],
                slide_outline=strategy["slide_outline"],
                tone=user_guidance["tone"]
            )
            self.session.update_state("generated_content", generated_content)
            
            # Stage 4: Image Prompt Generation (8s) - NEW
            logger.info("Stage 4/7: Generating image prompts")
            self.session.advance_stage("generating_prompts")
            
            template_colors = self._get_template_colors()
            image_prompts = self.agent4_prompts.generate_image_prompts(
                slide_outline=strategy["slide_outline"],
                generated_content=generated_content,
                template_colors=template_colors
            )
            self.session.update_state("image_prompts", image_prompts)
            logger.info(f"Generated {len(image_prompts.get('image_prompts', []))} image prompts")
            
            # Stage 5: Template Selection (2s)
            logger.info("Stage 5/7: Selecting template and layouts")
            self.session.advance_stage("selecting_template")
            
            template_selection = self.agent5_template.select_template(
                presentation_type=strategy["presentation_type"],
                audience=user_guidance["audience"],
                slide_outline=strategy["slide_outline"]
            )
            self.session.update_state("template_selection", template_selection)
            
            # Stage 6: Content Formatting (3s)
            logger.info("Stage 6/7: Formatting content for template")
            self.session.advance_stage("formatting_content")
            
            formatted_slides = self.agent6_formatting.format_content(
                generated_content=generated_content,
                template_selection=template_selection,
                image_prompts=image_prompts
            )
            self.session.update_state("formatted_slides", formatted_slides)
            
            # Stage 7: Presentation Assembly (3s)
            logger.info("Stage 7/7: Assembling final presentation")
            self.session.advance_stage("assembling")
            
            result = assemble_presentation(
                template_id=template_selection["selected_template"],
                formatted_slides=formatted_slides,
                output_name=f"presentation_{self.session_id}.pptx"
            )
            
            self.session.complete(result["pptx_path"])
            
            total_time = time.time() - start_time
            logger.info(f"Workflow complete in {total_time:.1f}s")
            
            result["total_time"] = total_time
            result["session_id"] = self.session_id
            
            return result
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            self.session.fail(str(e))
            raise
    
    def load_template_catalog(self) -> dict:
        """Load available templates"""
        # Implementation
        pass
    
    def _get_template_colors(self) -> dict:
        """Get default template colors"""
        return {
            "primary": "#1E3A8A",
            "secondary": "#3B82F6",
            "accent": "#60A5FA"
        }
```

---

### Epic 4: Session Management & Memory

#### Story 4.1: Session State Management (FREE TIER)
**As a** system  
**I want to** maintain session state using Firestore free tier  
**So that** I can track progress and enable resume

**Acceptance Criteria:**
- [ ] Uses Firestore free tier (50K reads, 20K writes per day)
- [ ] Stores session state across workflow stages
- [ ] Enables workflow resume
- [ ] Tracks metrics and costs
- [ ] Auto-cleanup old sessions

**Implementation:**
```python
from google.cloud import firestore

class PPTGeneratorSession:
    """
    Session management (Firestore free tier)
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.db = firestore.Client()
        self.doc_ref = self.db.collection('sessions').document(session_id)
        
        # Load or initialize
        doc = self.doc_ref.get()
        
        if doc.exists:
            self.state = doc.to_dict()
        else:
            self.state = {
                "session_id": session_id,
                "created_at": firestore.SERVER_TIMESTAMP,
                "stage": "initialized",
                "metrics": {
                    "start_time": time.time(),
                    "gemini_requests": 0,
                    "prompts_generated": 0
                }
            }
            self.doc_ref.set(self.state)
    
    def update_state(self, key: str, value: any):
        """Update session state"""
        self.state[key] = value
        self.doc_ref.update({key: value})
    
    def advance_stage(self, new_stage: str):
        """Move to next stage"""
        self.update_state("stage", new_stage)
        logger.info(f"Session {self.session_id}: {new_stage}")
    
    def complete(self, pptx_path: str):
        """Mark session complete"""
        self.state["metrics"]["end_time"] = time.time()
        self.state["metrics"]["total_duration"] = (
            self.state["metrics"]["end_time"] - 
            self.state["metrics"]["start_time"]
        )
        self.update_state("stage", "complete")
        self.update_state("pptx_path", pptx_path)
        self.update_state("metrics", self.state["metrics"])
```

---

### Epic 5: Observability & Monitoring (FREE TIER)

#### Story 5.1: Cloud Logging (FREE)
**As a** developer  
**I want to** see structured logs  
**So that** I can debug issues

**Acceptance Criteria:**
- [ ] Uses Cloud Logging free tier (50 GB/month)
- [ ] Structured logs with session context
- [ ] Agent performance tracking
- [ ] Error logging with stack traces

**Implementation:**
```python
import logging
from google.cloud import logging as cloud_logging

# Setup
logging_client = cloud_logging.Client()
logging_client.setup_logging()
logger = logging.getLogger(__name__)

class ObservableAgent:
    """Base class with logging"""
    
    def __init__(self, agent_name: str, session_id: str):
        self.agent_name = agent_name
        self.session_id = session_id
    
    def log_execution(self, operation: str, duration: float, **kwargs):
        """Log agent execution"""
        logger.info(f"{self.agent_name}: {operation}", extra={
            "session_id": self.session_id,
            "agent": self.agent_name,
            "duration_seconds": duration,
            **kwargs
        })
```

---

#### Story 5.2: Metrics Tracking (FREE)
**As a** system administrator  
**I want to** track usage metrics  
**So that** I can monitor free tier limits

**Implementation:**
```python
class FreeTheirMetricsTracker:
    """
    Track usage against free tier limits
    """
    
    FREE_TIER_LIMITS = {
        "gemini_requests_per_day": 1500,
        "firestore_reads_per_day": 50000,
        "firestore_writes_per_day": 20000,
        "storage_gb": 5
    }
    
    def __init__(self):
        self.db = firestore.Client()
        self.metrics_ref = self.db.collection('metrics').document('daily')
    
    def increment_metric(self, metric_name: str, amount: int = 1):
        """Increment usage metric"""
        self.metrics_ref.update({
            metric_name: firestore.Increment(amount)
        })
    
    def check_limits(self) -> dict:
        """Check if approaching limits"""
        doc = self.metrics_ref.get()
        if not doc.exists:
            return {"status": "ok"}
        
        metrics = doc.to_dict()
        warnings = []
        
        for limit_name, limit_value in self.FREE_TIER_LIMITS.items():
            current = metrics.get(limit_name, 0)
            usage_percent = (current / limit_value) * 100
            
            if usage_percent > 90:
                warnings.append(f"{limit_name}: {usage_percent:.1f}% used")
        
        return {
            "status": "warning" if warnings else "ok",
            "warnings": warnings,
            "metrics": metrics
        }
```

---

## Data Models

### Session State Schema
```json
{
  "session_id": "string",
  "user_id": "string",
  "created_at": "timestamp",
  "stage": "initialized|ingesting_content|planning_strategy|generating_content|generating_prompts|selecting_template|formatting_content|assembling|complete|failed",
  "reference_material": {
    "file_path": "string",
    "file_type": "pdf|docx|txt"
  },
  "user_guidance": {
    "purpose": "string",
    "audience": "string",
    "tone": "string"
  },
  "content_analysis": {...},
  "strategy": {...},
  "generated_content": {...},
  "image_prompts": {...},
  "template_selection": {...},
  "formatted_slides": {...},
  "pptx_path": "string",
  "prompts_json_path": "string",
  "metrics": {
    "start_time": float,
    "end_time": float,
    "total_duration": float,
    "gemini_requests": int,
    "prompts_generated": int,
    "estimated_cost": 0.0
  }
}
```

### Image Prompt Schema
```json
{
  "slide_number": 2,
  "visual_type": "illustration",
  "prompt": "Detailed 150-300 word image generation prompt...",
  "prompt_keywords": ["array"],
  "style_tags": ["professional", "minimalist"],
  "color_palette": ["#1E3A8A", "#3B82F6"],
  "technical_specs": {
    "aspect_ratio": "16:9",
    "style": "illustration",
    "quality": "high"
  },
  "alternative_prompt": "Simpler version...",
  "search_query": "What to search in stock photos",
  "rationale": "Why this visual",
  "quality_score": 0.95
}
```

---

## Development Phases

### Phase 1: Foundation (Days 1-5)
- [ ] Setup GCP free tier project
- [ ] Configure Google AI Studio
- [ ] Implement template extraction
- [ ] Implement function generation
- [ ] Create 2 sample templates

### Phase 2: Content Agents (Days 6-10)
- [ ] Agent 1: Content Ingestion
- [ ] Agent 2: Presentation Strategy
- [ ] Agent 3: Content Generation
- [ ] **Agent 4: Image Prompt Generation (NEW)**
- [ ] Test content pipeline

### Phase 3: Assembly (Days 11-14)
- [ ] Agent 5: Template Selector
- [ ] Agent 6: Content Formatting
- [ ] Agent 7: PPT Assembler
- [ ] Image placeholder rendering
- [ ] Prompt JSON export
- [ ] End-to-end testing

### Phase 4: Polish (Days 15-17)
- [ ] Session management
- [ ] Observability
- [ ] CLI interface
- [ ] Documentation
- [ ] Demo preparation
- [ ] Course submission package

---

## Testing Strategy

### Test Scenarios
1. **Product Brief → Pitch** (8 slides, 3 image prompts)
2. **Report → Summary** (6 slides, 2 image prompts)
3. **Meeting Notes → Action Items** (5 slides, 1 image prompt)

### Success Criteria
- ✅ PPTX opens without errors
- ✅ Content is relevant and well-written
- ✅ Image prompts are detailed (150-300 words)
- ✅ Prompt quality scores > 0.8
- ✅ Total time < 40 seconds
- ✅ Cost: $0 (100% free tier)

---

## Cost Analysis

### MVP Development (2.5 weeks)
```
Development & Testing (50 presentations):
- Gemini API: FREE (AI Studio)
- Firestore: FREE (within daily limits)
- Cloud Storage: FREE (< 1 GB)
- Cloud Run: FREE (< 1M requests)
- Logging: FREE (< 50 GB)

Total Cost: $0.00
```

### Per Presentation
```
- LLM requests: 7 agents × ~5K tokens = 35K tokens
- Cost: $0 (AI Studio free tier)
- Storage: ~2 MB
- Processing time: ~35 seconds

Per presentation cost: $0
```

---

## Course Feature Mapping

### ✅ 1. Multi-Agent System
- **Sequential agents:** 7-agent pipeline
- **Agent specialization:** Each agent has clear role
- **Agent coordination:** Output of one → input of next

### ✅ 2. Tools
- **Custom tools:**
  1. `analyze_ppt_template` - Template extraction
  2. `generate_template_functions` - Code generation
  3. `extract_document_content` - PDF/DOCX parsing
  4. `assemble_presentation` - PPTX assembly
- **Built-in tools:** Code Execution (for template functions)

### ✅ 3. Sessions & Memory
- **Session management:** Firestore state across 7 stages
- **Progress tracking:** Stage-by-stage status
- **Resume capability:** Can continue from any stage

### ✅ 4. Observability
- **Logging:** Cloud Logging with structured logs
- **Metrics:** Usage tracking against free tier limits
- **Performance:** Duration tracking per agent

### ✅ 5. Long-Running Operations (Optional)
- **Checkpoint system:** Save state after each stage
- **Resume:** Can restart from last checkpoint

---

## Deliverables

### Code
- Complete source code
- Requirements.txt
- Setup instructions
- Environment configuration

### Documentation
- Architecture diagram
- Agent descriptions
- Tool specifications
- API documentation

### Demo
- 3 example presentations
- Image prompts JSON files
- Demo video (5 minutes)
- Before/after comparisons

### Submission
- Feature showcase document
- Technical write-up
- Challenges & solutions
- Future enhancements

---

## Future Enhancements

**Phase 2 (With Budget):**
- Integrate Imagen 3 to generate actual images
- Batch process multiple prompts
- A/B test different prompts
- Fine-tune prompts based on feedback

**Phase 3:**
- Web UI
- Google Drive integration
- Collaborative editing
- Template marketplace

---

## Summary

### ✅ What This MVP Does:
- Reads uploaded reference documents (PDF/DOCX/TXT)
- Analyzes content intelligently
- Creates presentation strategy
- Generates slide content
- **Generates detailed, professional image prompts**
- Selects appropriate templates
- Assembles branded presentations
- **Displays prompts in placeholder boxes**
- **Exports prompts to JSON for later use**

### ✅ What Makes It Special:
- **100% Free Tier** - Zero cost to build and run
- **Complete Pipeline** - Proves entire concept
- **Reusable Prompts** - Can be used with any image generator
- **Production-Quality** - Professional presentations
- **Course Requirements** - Demonstrates all required features

### 🎯 Perfect for MVP/POC:
- Validates the concept
- Shows value to stakeholders
- Can be demoed extensively
- Easy to add image generation later
- Stays within free tier limits

---

**Ready for development! This specification provides everything needed to build a complete, free-tier PPT generator that meets all course requirements while providing real business value.** 🚀