"""
Custom Tools for PPT Generator
"""

from .template_analyzer import analyze_ppt_template, generate_template_functions
from .document_extractor import extract_document_content

__all__ = [
    'analyze_ppt_template',
    'generate_template_functions',
    'extract_document_content'
]
