"""
Basic tests for the backend.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

import pytest


class TestBasic(unittest.TestCase):
    """Basic test cases for the backend."""
    
    def test_imports(self):
        """Test that the modules can be imported without errors."""
        try:
            # Use a context manager to temporarily suppress import errors
            with patch.dict('sys.modules'):
                # Mock the external dependencies that might cause issues
                for module in ['fitz', 'doctr', 'groq', 'pandera', 'playwright']:
                    sys.modules[module] = MagicMock()
                
                # Try importing our modules
                from config import settings
                from pdf_parser import extract_text_with_layout, is_pdf_file
                from validator import validate, FormData
                
                # If we got here, the imports worked
                self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import error: {str(e)}")
    
    def test_config(self):
        """Test that the config module can be loaded."""
        try:
            # Mock environment variables
            with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
                # Import the module
                from pydantic_settings import BaseSettings
                from config import Settings
                
                # Create a settings object
                settings = Settings()
                
                # Check that it has the expected attributes
                self.assertEqual(settings.groq_api_key, "test_key")
                self.assertTrue(hasattr(settings, 'upload_dir'))
                self.assertTrue(hasattr(settings, 'screenshot_dir'))
        except Exception as e:
            self.fail(f"Config test failed: {str(e)}")


if __name__ == "__main__":
    unittest.main()
