"""
PDF parser module for extracting text with layout information from PDF files.
Uses PyMuPDF (fitz) to extract text blocks with their coordinates.
"""
from pathlib import Path
from typing import Dict, List, Any

import fitz  # PyMuPDF


def extract_text_with_layout(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract text from a PDF file with layout information.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        List of dictionaries containing text blocks with coordinates
    """
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    # Open the PDF file
    doc = fitz.open(file_path)
    
    # List to store all text blocks from all pages
    all_blocks = []
    
    # Process each page
    for page_num, page in enumerate(doc):
        # Extract text with dict format to get blocks with coordinates
        blocks = page.get_text("dict")["blocks"]
        
        # Process each block
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    if "spans" in line:
                        for span in line["spans"]:
                            # Extract text and position data
                            text_block = {
                                "text": span["text"],
                                "page": page_num + 1,
                                "x0": span["bbox"][0],
                                "y0": span["bbox"][1],
                                "x1": span["bbox"][2],
                                "y1": span["bbox"][3],
                                "font": span.get("font", ""),
                                "size": span.get("size", 0),
                                "color": span.get("color", 0)
                            }
                            all_blocks.append(text_block)
    
    # Close the document
    doc.close()
    
    return all_blocks


def is_pdf_file(file_path: Path) -> bool:
    """
    Check if a file is a PDF based on its extension and content.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a PDF, False otherwise
    """
    # Check file extension
    if file_path.suffix.lower() != ".pdf":
        return False
    
    # Check file content (PDF signature)
    try:
        with open(file_path, "rb") as f:
            header = f.read(4)
            return header == b"%PDF"
    except Exception:
        return False
