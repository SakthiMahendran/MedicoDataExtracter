"""
LLM extractor module for extracting structured data from text using Groq's Llama-3.1 model.
"""
import json
from typing import Dict, Any, List, Optional

import groq
from pydantic import BaseModel, Field

from config import settings


class HealthcareFormFields(BaseModel):
    """Schema for healthcare form fields to be extracted."""
    patient_name: str
    date_of_birth: str
    gender: str
    address: str
    phone_number: str
    email: Optional[str] = None
    insurance_provider: str
    insurance_id: str
    medical_history: Optional[List[str]] = Field(default_factory=list)
    current_medications: Optional[List[str]] = Field(default_factory=list)
    allergies: Optional[List[str]] = Field(default_factory=list)
    primary_complaint: str
    appointment_date: Optional[str] = None
    doctor_name: Optional[str] = None


class LLMExtractor:
    """LLM-based extractor using Groq's Llama-3.1 model."""
    
    def __init__(self, api_key: str):
        """
        Initialize the LLM extractor with Groq API key.
        
        Args:
            api_key: Groq API key
        """
        self.client = groq.Client(api_key=api_key)
        self.model = "llama-3.1-70b-instant"  # Using the latest Llama-3.1 70B model
    
    def extract_fields(self, text_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract structured fields from text blocks using LLM.
        
        Args:
            text_blocks: List of text blocks with coordinates
            
        Returns:
            Dictionary containing extracted fields
        """
        # Combine all text blocks into a single string
        combined_text = self._combine_text_blocks(text_blocks)
        
        # Create system message for extraction
        system_message = """
        # Your Purpose
        You are a healthcare form data extraction assistant. Your task is to extract specific fields from healthcare form text and return them in a structured JSON format.

        # Instructions
        1. Carefully analyze the provided healthcare form text.
        2. Extract all requested fields accurately.
        3. For fields not explicitly found in the text, use reasonable inference based on context.
        4. For list fields (medical_history, current_medications, allergies), separate items properly.
        5. Format dates in YYYY-MM-DD format when possible.
        6. Return ONLY the JSON object without any additional text, explanations, or markdown formatting.

        # Output Format
        Your response must be a valid JSON object containing exactly these fields:
        {
          "patient_name": "Full name of the patient",
          "date_of_birth": "Patient's date of birth (YYYY-MM-DD)",
          "gender": "Patient's gender",
          "address": "Patient's full address",
          "phone_number": "Patient's phone number",
          "email": "Patient's email address (or null if not available)",
          "insurance_provider": "Name of the insurance provider",
          "insurance_id": "Insurance ID or policy number",
          "medical_history": ["List of medical history items"],
          "current_medications": ["List of current medications"],
          "allergies": ["List of allergies"],
          "primary_complaint": "Patient's primary complaint or reason for visit",
          "appointment_date": "Date of appointment (YYYY-MM-DD or null if not available)",
          "doctor_name": "Name of the doctor (or null if not available)"
        }
        """
        
        # Call Groq API with JSON mode enabled
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Extract the healthcare form data from the following text:\n\n{combined_text}"}
                ],
                response_format={"type": "json_object"},  # Enable JSON mode
                temperature=0.1,  # Low temperature for more deterministic results
                max_tokens=2048
            )
            
            # Parse JSON directly from response
            json_str = response.choices[0].message.content
            extracted_data = json.loads(json_str)
            
            # Ensure required fields have string values
            required_fields = ['patient_name', 'date_of_birth', 'gender', 'address', 
                              'phone_number', 'insurance_provider', 'insurance_id', 
                              'primary_complaint']
            
            for field in required_fields:
                if field not in extracted_data or extracted_data[field] is None:
                    extracted_data[field] = "Unknown"
            
            # Ensure list fields are lists
            list_fields = ['medical_history', 'current_medications', 'allergies']
            for field in list_fields:
                if field not in extracted_data or extracted_data[field] is None:
                    extracted_data[field] = []
            
            # Validate against our schema
            validated_data = HealthcareFormFields(**extracted_data).dict()
            return validated_data
            
        except Exception as e:
            # If extraction fails, log the error and return a structured error response
            import logging
            logging.error(f"LLM extraction failed: {str(e)}")
            
            # Get sample text from the input to use in the fallback
            sample_text = ""
            if text_blocks and len(text_blocks) > 0:
                sample_text = " ".join([block.get("text", "") for block in text_blocks[:5]])
                if len(sample_text) > 50:
                    sample_text = sample_text[:50] + "..."
            
            # Return a fallback structure with string values for required fields
            return {
                "patient_name": "Unable to extract - API error",
                "date_of_birth": "Unknown",
                "gender": "Unknown",
                "address": "Unable to extract - API error",
                "phone_number": "Unknown",
                "email": None,
                "insurance_provider": "Unknown",
                "insurance_id": "Unknown",
                "medical_history": [],
                "current_medications": [],
                "allergies": [],
                "primary_complaint": f"Error in extraction: {str(e)}. Sample text: {sample_text}",
                "appointment_date": None,
                "doctor_name": None
            }
    
    def _combine_text_blocks(self, text_blocks: List[Dict[str, Any]]) -> str:
        """
        Combine text blocks into a single string, sorted by position.
        
        Args:
            text_blocks: List of text blocks with coordinates
            
        Returns:
            Combined text string
        """
        # Sort blocks by page, then y-coordinate (top to bottom), then x-coordinate (left to right)
        sorted_blocks = sorted(
            text_blocks,
            key=lambda block: (block.get("page", 0), block.get("y0", 0), block.get("x0", 0))
        )
        
        # Combine text with page and position information for better context
        result_text = ""
        current_page = None
        
        for block in sorted_blocks:
            page = block.get("page", 0)
            if page != current_page:
                result_text += f"\n--- PAGE {page} ---\n"
                current_page = page
            
            result_text += block["text"] + " "
        
        return result_text


# Create a singleton instance
llm_extractor = LLMExtractor(api_key=settings.groq_api_key)
