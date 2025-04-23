"""
Validator module for validating extracted healthcare form data.
Uses Pandera for DataFrame validation and Pydantic for type validation.
"""
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

import pandas as pd
import pandera as pa
from pydantic import BaseModel, Field, validator


# Pandera schema for DataFrame validation
class HealthcareFormSchema(pa.SchemaModel):
    """Pandera schema for validating healthcare form data."""
    
    patient_name: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Patient's full name"
    )
    
    date_of_birth: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Patient's date of birth"
    )
    
    gender: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Patient's gender"
    )
    
    address: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Patient's full address"
    )
    
    phone_number: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Patient's phone number"
    )
    
    email: pa.typing.Series[str] = pa.Field(
        nullable=True,
        coerce=True,
        description="Patient's email address"
    )
    
    insurance_provider: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Name of the insurance provider"
    )
    
    insurance_id: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Insurance ID or policy number"
    )
    
    primary_complaint: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Patient's primary complaint or reason for visit"
    )
    
    appointment_date: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Date of appointment"
    )
    
    doctor_name: pa.typing.Series[str] = pa.Field(
        nullable=True,  # Allow null values for error cases
        coerce=True,
        description="Name of the doctor"
    )
    
    class Config:
        """Pandera schema configuration."""
        coerce = True
        strict = False


# Pydantic model for type validation
class MedicalItem(BaseModel):
    """Model for medical items like history, medications, allergies."""
    name: str
    details: Optional[str] = None


class FormData(BaseModel):
    """Pydantic model for validated healthcare form data."""
    
    patient_name: str = "Unable to extract"
    date_of_birth: str = "Unknown"
    gender: str = "Unknown"
    address: str = "Unable to extract"
    phone_number: str = "Unknown"
    email: Optional[str] = None
    insurance_provider: str = "Unknown"
    insurance_id: str = "Unknown"
    medical_history: List[Union[str, MedicalItem]] = Field(default_factory=list)
    current_medications: List[Union[str, MedicalItem]] = Field(default_factory=list)
    allergies: List[Union[str, MedicalItem]] = Field(default_factory=list)
    primary_complaint: str = "Unable to extract"
    appointment_date: Optional[str] = None
    doctor_name: Optional[str] = None
    
    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender field."""
        if not v or v == "Unknown":
            return "Unknown"
        valid_genders = ["Male", "Female", "Other", "Prefer not to say"]
        if v.title() in valid_genders:
            return v.title()
        return v
    
    @validator('date_of_birth', 'appointment_date')
    def validate_date_format(cls, v):
        """Validate date format."""
        if not v:
            return None if v is None else v
        
        # Basic format check (more sophisticated validation could be added)
        if not isinstance(v, str):
            return "Unknown" if v == 'date_of_birth' else None
        
        try:
            # Try to parse the date
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            # If date format is invalid, try to fix it or return as is
            return v


def validate_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Validate data using Pandera schema.
    
    Args:
        data: Dictionary containing form data
        
    Returns:
        Validated DataFrame
    """
    # Convert dictionary to DataFrame
    df = pd.DataFrame([data])
    
    try:
        # Validate with Pandera schema
        validated_df = HealthcareFormSchema.validate(df)
        return validated_df
    except pa.errors.SchemaError as e:
        # Log validation errors
        print(f"Validation error: {str(e)}")
        
        # Return original data for fallback
        return df


def validate(data: Dict[str, Any]) -> FormData:
    """
    Validate extracted form data.
    
    Args:
        data: Dictionary containing extracted form data
        
    Returns:
        Validated FormData object
    """
    # Handle None values for required string fields
    for field in ['patient_name', 'date_of_birth', 'gender', 'address', 'phone_number', 
                 'insurance_provider', 'insurance_id', 'primary_complaint']:
        if field in data and data[field] is None:
            data[field] = "Unknown"
    
    # Convert list fields to proper format
    for list_field in ['medical_history', 'current_medications', 'allergies']:
        if list_field in data:
            if data[list_field] is None:
                data[list_field] = []
            elif isinstance(data[list_field], str):
                # Convert string to list if needed
                if data[list_field]:
                    data[list_field] = [item.strip() for item in data[list_field].split(',')]
                else:
                    data[list_field] = []
    
    try:
        # Validate with Pydantic model
        validated_data = FormData(**data)
        return validated_data
    except Exception as e:
        # Log validation errors
        print(f"Pydantic validation error: {str(e)}")
        
        # Create a minimal valid object for fallback
        return FormData(
            patient_name="Error in validation",
            date_of_birth="Unknown",
            gender="Unknown",
            address="Error in validation",
            phone_number="Unknown",
            insurance_provider="Unknown",
            insurance_id="Unknown",
            primary_complaint=f"Error in validation: {str(e)}"
        )
