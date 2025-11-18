"""
Document Content Extraction Tool
Extracts text from PDF, DOCX, and TXT files
"""

import os
from typing import Dict, Any


def extract_document_content(file_path: str) -> Dict[str, Any]:
    """
    Extract text from PDF/DOCX/TXT

    Args:
        file_path: Path to document file

    Returns:
        Dictionary with file_type, full_text, and word_count
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document not found: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == '.pdf':
        return _extract_from_pdf(file_path)
    elif file_ext == '.docx':
        return _extract_from_docx(file_path)
    elif file_ext == '.txt':
        return _extract_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Supported: .pdf, .docx, .txt")


def _extract_from_pdf(file_path: str) -> Dict[str, Any]:
    """Extract text from PDF"""
    try:
        import PyPDF2
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF extraction. Install with: pip install PyPDF2")

    text = ""
    page_count = 0

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page_count = len(pdf_reader.pages)

        # Limit to 50 pages as per spec
        max_pages = min(page_count, 50)

        for page_num in range(max_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n\n"

    return {
        "file_type": "pdf",
        "file_name": os.path.basename(file_path),
        "full_text": text,
        "word_count": len(text.split()),
        "page_count": page_count,
        "pages_processed": min(page_count, 50)
    }


def _extract_from_docx(file_path: str) -> Dict[str, Any]:
    """Extract text from DOCX"""
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx is required for DOCX extraction. Install with: pip install python-docx")

    doc = Document(file_path)
    paragraphs = []

    # Extract paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text)

    text = "\n".join(paragraphs)

    return {
        "file_type": "docx",
        "file_name": os.path.basename(file_path),
        "full_text": text,
        "word_count": len(text.split()),
        "paragraph_count": len(paragraphs)
    }


def _extract_from_txt(file_path: str) -> Dict[str, Any]:
    """Extract text from TXT"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()

    return {
        "file_type": "txt",
        "file_name": os.path.basename(file_path),
        "full_text": text,
        "word_count": len(text.split()),
        "line_count": len(text.split('\n'))
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        doc_path = sys.argv[1]
    else:
        print("Usage: python document_extractor.py <path_to_document>")
        sys.exit(1)

    print(f"Extracting content from: {doc_path}")
    result = extract_document_content(doc_path)

    print(f"\nFile Type: {result['file_type']}")
    print(f"Word Count: {result['word_count']}")
    print(f"\nFirst 500 characters:")
    print(result['full_text'][:500])
