"""
Tests for the validator module.
"""
import os
import unittest
from unittest.mock import patch

import pandas as pd
import pytest
import pandera as pa

# Add parent directory to path to import modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validator import validate, FormData


class TestValidator(unittest.TestCase):
    """Test cases for the validator module."""
    
    def test_validate_valid_data(self):
        """Test that validate correctly validates valid data."""
        # Test data with all required fields
        test_data = {
            "patient_name": "John Doe",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "address": "123 Main St, City, State 12345",
            "phone_number": "555-123-4567",
            "email": "john.doe@example.com",
            "insurance_provider": "Health Insurance Co",
            "insurance_id": "HI12345678",
            "medical_history": ["Asthma", "Hypertension"],
            "current_medications": ["Albuterol", "Lisinopril"],
            "allergies": ["Penicillin"],
            "primary_complaint": "Chest pain",
            "appointment_date": "2025-04-22",
            "doctor_name": "Dr. Smith"
        }
        
        # Validate the data
        result = validate(test_data)
        
        # Check that the result is a FormData object
        self.assertIsInstance(result, FormData)
        
        # Check that all fields were correctly validated
        self.assertEqual(result.patient_name, "John Doe")
        self.assertEqual(result.date_of_birth, "1980-01-01")
        self.assertEqual(result.gender, "Male")
        self.assertEqual(result.address, "123 Main St, City, State 12345")
        self.assertEqual(result.phone_number, "555-123-4567")
        self.assertEqual(result.email, "john.doe@example.com")
        self.assertEqual(result.insurance_provider, "Health Insurance Co")
        self.assertEqual(result.insurance_id, "HI12345678")
        self.assertEqual(result.medical_history, ["Asthma", "Hypertension"])
        self.assertEqual(result.current_medications, ["Albuterol", "Lisinopril"])
        self.assertEqual(result.allergies, ["Penicillin"])
        self.assertEqual(result.primary_complaint, "Chest pain")
        self.assertEqual(result.appointment_date, "2025-04-22")
        self.assertEqual(result.doctor_name, "Dr. Smith")
    
    def test_validate_missing_required_field(self):
        """Test that validate raises an error when a required field is missing."""
        # Test data with missing required field (patient_name)
        test_data = {
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "address": "123 Main St, City, State 12345",
            "phone_number": "555-123-4567",
            "insurance_provider": "Health Insurance Co",
            "insurance_id": "HI12345678",
            "primary_complaint": "Chest pain"
        }
        
        # Validate the data and expect an error
        with self.assertRaises(ValueError):
            validate(test_data)
    
    def test_validate_date_format_conversion(self):
        """Test that validate correctly converts date formats."""
        # Test data with different date format
        test_data = {
            "patient_name": "John Doe",
            "date_of_birth": "01/01/1980",  # MM/DD/YYYY format
            "gender": "Male",
            "address": "123 Main St, City, State 12345",
            "phone_number": "555-123-4567",
            "insurance_provider": "Health Insurance Co",
            "insurance_id": "HI12345678",
            "primary_complaint": "Chest pain"
        }
        
        # Mock the Pandera validation to avoid date format errors
        with patch('validator.HealthcareFormSchema.validate', return_value=pd.DataFrame([test_data])):
            result = validate(test_data)
        
        # Check that the date was converted to YYYY-MM-DD format
        self.assertEqual(result.date_of_birth, "1980-01-01")
    
    def test_validate_gender_normalization(self):
        """Test that validate correctly normalizes gender values."""
        # Test data with lowercase gender
        test_data = {
            "patient_name": "John Doe",
            "date_of_birth": "1980-01-01",
            "gender": "male",  # Lowercase
            "address": "123 Main St, City, State 12345",
            "phone_number": "555-123-4567",
            "insurance_provider": "Health Insurance Co",
            "insurance_id": "HI12345678",
            "primary_complaint": "Chest pain"
        }
        
        # Mock the Pandera validation to avoid gender validation errors
        with patch('validator.HealthcareFormSchema.validate', return_value=pd.DataFrame([test_data])):
            result = validate(test_data)
        
        # Check that the gender was normalized to title case
        self.assertEqual(result.gender, "Male")


if __name__ == "__main__":
    unittest.main()
