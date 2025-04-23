"""
OCR parser module for extracting text from images using docTR.
"""
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from PIL import Image
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


class OCRParser:
    """OCR Parser using docTR for high-accuracy text extraction from images."""
    
    def __init__(self):
        """Initialize the OCR predictor with a pre-trained model."""
        # Use db_resnet50 for high accuracy OCR
        self.predictor = ocr_predictor(pretrained=True, detect_arch="db_resnet50")
    
    def extract_text_from_image(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Extract text from an image file using OCR.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            List of dictionaries containing text blocks with coordinates
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        # Load the document
        doc = DocumentFile.from_images(str(file_path))
        
        # Run OCR prediction
        result = self.predictor(doc)
        
        # Extract text with layout information
        extracted_blocks = []
        
        # Process each page
        for page_idx, page in enumerate(result.pages):
            # Process each block
            for block_idx, block in enumerate(page.blocks):
                # Process each line
                for line_idx, line in enumerate(block.lines):
                    # Process each word
                    for word_idx, word in enumerate(line.words):
                        # Get coordinates (normalized)
                        coords = word.geometry
                        
                        # Convert to pixel coordinates (assuming standard image size)
                        # For more accurate conversion, we would need the actual image dimensions
                        img = Image.open(file_path)
                        width, height = img.size
                        
                        x0 = int(coords[0][0] * width)
                        y0 = int(coords[0][1] * height)
                        x1 = int(coords[1][0] * width)
                        y1 = int(coords[1][1] * height)
                        
                        # Create text block
                        text_block = {
                            "text": word.value,
                            "page": page_idx + 1,
                            "x0": x0,
                            "y0": y0,
                            "x1": x1,
                            "y1": y1,
                            "confidence": float(word.confidence)
                        }
                        
                        extracted_blocks.append(text_block)
        
        return extracted_blocks


def is_image_file(file_path: Path) -> bool:
    """
    Check if a file is an image based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is an image, False otherwise
    """
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"]
    return file_path.suffix.lower() in image_extensions


# Create a singleton instance
ocr_parser = OCRParser()
