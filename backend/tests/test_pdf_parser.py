"""
Tests for the pdf_parser module.
"""
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path to import modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_parser import extract_text_with_layout, is_pdf_file


class TestPDFParser(unittest.TestCase):
    """Test cases for the pdf_parser module."""
    
    @patch('pdf_parser.fitz.open')
    def test_extract_text_with_layout(self, mock_fitz_open):
        """Test that extract_text_with_layout extracts text blocks with coordinates."""
        # Mock the PDF document and page
        mock_doc = MagicMock()
        mock_page = MagicMock()
        
        # Set up the mock to return our test data
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz_open.return_value = mock_doc
        
        # Mock the get_text method to return test blocks
        mock_page.get_text.return_value = {
            "blocks": [
                {
                    "lines": [
                        {
                            "spans": [
                                {
                                    "text": "Test Text",
                                    "bbox": [10, 20, 30, 40],
                                    "font": "Arial",
                                    "size": 12,
                                    "color": 0
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Call the function with a mock file path
        file_path = Path("test.pdf")
        with patch.object(Path, 'exists', return_value=True):
            result = extract_text_with_layout(file_path)
        
        # Check the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["text"], "Test Text")
        self.assertEqual(result[0]["page"], 1)
        self.assertEqual(result[0]["x0"], 10)
        self.assertEqual(result[0]["y0"], 20)
        self.assertEqual(result[0]["x1"], 30)
        self.assertEqual(result[0]["y1"], 40)
        self.assertEqual(result[0]["font"], "Arial")
        self.assertEqual(result[0]["size"], 12)
        self.assertEqual(result[0]["color"], 0)
        
        # Verify that the document was closed
        mock_doc.close.assert_called_once()
    
    def test_is_pdf_file_with_pdf_extension(self):
        """Test that is_pdf_file returns True for files with .pdf extension and PDF content."""
        file_path = Path("test.pdf")
        
        # Mock the open function to return PDF header
        with patch('builtins.open', unittest.mock.mock_open(read_data=b"%PDF")):
            result = is_pdf_file(file_path)
        
        self.assertTrue(result)
    
    def test_is_pdf_file_with_non_pdf_extension(self):
        """Test that is_pdf_file returns False for files without .pdf extension."""
        file_path = Path("test.txt")
        result = is_pdf_file(file_path)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
