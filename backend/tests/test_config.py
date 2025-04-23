"""
Tests for the config module.
"""
import os
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path to import modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Settings


class TestConfig(unittest.TestCase):
    """Test cases for the config module."""
    
    def test_settings_defaults(self):
        """Test that Settings has the expected default values."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            settings = Settings()
            
            # Check default values
            self.assertEqual(settings.groq_api_key, "test_key")
            self.assertEqual(settings.upload_dir, Path("./uploads"))
            self.assertEqual(settings.screenshot_dir, Path("./screenshots"))
            self.assertEqual(settings.target_form_url, "https://example.com/healthcare-form")
            self.assertEqual(settings.host, "0.0.0.0")
            self.assertEqual(settings.port, 8001)
            self.assertEqual(settings.debug, True)
    
    def test_initialize_directories(self):
        """Test that initialize_directories creates the necessary directories."""
        with patch.dict(os.environ, {"GROQ_API_KEY": "test_key"}):
            settings = Settings()
            
            # Mock the mkdir method
            with patch.object(Path, 'mkdir') as mock_mkdir:
                settings.initialize_directories()
                
                # Check that mkdir was called for both directories
                self.assertEqual(mock_mkdir.call_count, 2)
                mock_mkdir.assert_any_call(parents=True, exist_ok=True)


if __name__ == "__main__":
    unittest.main()
