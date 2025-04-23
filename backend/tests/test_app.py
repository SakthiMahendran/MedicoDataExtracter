"""
Tests for the FastAPI application.
"""
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path to import modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestApp(unittest.TestCase):
    """Test cases for the FastAPI application."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test that the root endpoint returns the expected response."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Healthcare Form Data Extraction API"})
    
    @patch('app.save_upload_file')
    @patch('app.extract_text_from_file')
    @patch('app.llm_extractor.extract_fields')
    @patch('app.validate')
    @patch('app.fill_form')
    def test_extract_form_data_endpoint(self, mock_fill_form, mock_validate, mock_extract_fields, 
                                       mock_extract_text, mock_save_file):
        """Test that the extract_form_data endpoint returns the expected response."""
        # Mock the file upload
        test_file = MagicMock()
        test_file.filename = "test.pdf"
        
        # Set up the mock return values
        mock_save_file.return_value = Path("uploads/test.pdf")
        mock_extract_text.return_value = [{"text": "Test Text", "page": 1}]
        mock_extract_fields.return_value = {
            "patient_name": "John Doe",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "address": "123 Main St",
            "phone_number": "555-123-4567",
            "insurance_provider": "Health Insurance Co",
            "insurance_id": "HI12345678",
            "primary_complaint": "Chest pain"
        }
        
        # Mock the validated data
        mock_validated_data = MagicMock()
        mock_validated_data.dict.return_value = {
            "patient_name": "John Doe",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "address": "123 Main St",
            "phone_number": "555-123-4567",
            "insurance_provider": "Health Insurance Co",
            "insurance_id": "HI12345678",
            "primary_complaint": "Chest pain"
        }
        mock_validate.return_value = mock_validated_data
        
        # Mock the screenshot path
        mock_fill_form.return_value = Path("screenshots/test_screenshot.png")
        
        # Make the request
        with patch('builtins.open', unittest.mock.mock_open(read_data=b"test")):
            response = self.client.post(
                "/api/extract",
                files={"file": ("test.pdf", b"test", "application/pdf")}
            )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["screenshot_url"], "/screenshots/test_screenshot.png")
        
        # Check that all the mock functions were called
        mock_save_file.assert_called_once()
        mock_extract_text.assert_called_once()
        mock_extract_fields.assert_called_once()
        mock_validate.assert_called_once()
        mock_fill_form.assert_called_once()
    
    @patch('app.save_upload_file')
    def test_extract_form_data_endpoint_error(self, mock_save_file):
        """Test that the extract_form_data endpoint handles errors correctly."""
        # Mock the file upload
        test_file = MagicMock()
        test_file.filename = "test.pdf"
        
        # Make the save_upload_file function raise an exception
        mock_save_file.side_effect = Exception("Test error")
        
        # Make the request
        with patch('builtins.open', unittest.mock.mock_open(read_data=b"test")):
            response = self.client.post(
                "/api/extract",
                files={"file": ("test.pdf", b"test", "application/pdf")}
            )
        
        # Check the response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Test error")


if __name__ == "__main__":
    unittest.main()
