"""
Form filler module for generating visual representations of healthcare forms with extracted data.
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import io
import base64

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from config import settings


class FormVisualizer:
    """Creates visual representations of healthcare forms with extracted data."""
    
    def __init__(self, screenshot_dir: Path):
        """
        Initialize the form visualizer.
        
        Args:
            screenshot_dir: Directory to save visualizations
        """
        self.screenshot_dir = screenshot_dir
        self.logger = logging.getLogger(__name__)
    
    def create_form_visualization(self, data: Dict[str, Any], form_id: str) -> Optional[Path]:
        """
        Create a visual representation of a healthcare form with the extracted data.
        
        Args:
            data: Dictionary containing form data
            form_id: Unique identifier for the form
            
        Returns:
            Path to the visualization if successful, None otherwise
        """
        if not PIL_AVAILABLE:
            self.logger.error("PIL not available, cannot create form visualization")
            return self._create_text_fallback(data, form_id)
        
        screenshot_path = self.screenshot_dir / f"{form_id}_screenshot.png"
        
        try:
            # Create a blank image
            width, height = 1000, 1400
            image = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            # Try to load fonts
            try:
                title_font = ImageFont.truetype("arial.ttf", 24)
                header_font = ImageFont.truetype("arial.ttf", 18)
                normal_font = ImageFont.truetype("arial.ttf", 14)
            except IOError:
                # Fallback to default font
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                normal_font = ImageFont.load_default()
            
            # Draw form header
            draw.rectangle([(0, 0), (width, 80)], fill=(66, 133, 244))
            draw.text((20, 20), "HEALTHCARE PATIENT INFORMATION FORM", fill=(255, 255, 255), font=title_font)
            draw.text((20, 50), f"Form ID: {form_id}", fill=(255, 255, 255), font=normal_font)
            
            # Draw form sections
            y_pos = 100
            
            # Patient Information Section
            self._draw_section_header(draw, "Patient Information", 20, y_pos, header_font)
            y_pos += 30
            
            fields = [
                ("Patient Name:", data.get("patient_name", "N/A")),
                ("Date of Birth:", data.get("date_of_birth", "N/A")),
                ("Gender:", data.get("gender", "N/A")),
                ("Address:", data.get("address", "N/A")),
                ("Phone Number:", data.get("phone_number", "N/A")),
                ("Email:", data.get("email", "N/A"))
            ]
            
            for label, value in fields:
                y_pos = self._draw_field(draw, label, str(value), 40, y_pos, normal_font)
                y_pos += 10
            
            # Insurance Information Section
            y_pos += 20
            self._draw_section_header(draw, "Insurance Information", 20, y_pos, header_font)
            y_pos += 30
            
            insurance_fields = [
                ("Insurance Provider:", data.get("insurance_provider", "N/A")),
                ("Insurance ID:", data.get("insurance_id", "N/A"))
            ]
            
            for label, value in insurance_fields:
                y_pos = self._draw_field(draw, label, str(value), 40, y_pos, normal_font)
                y_pos += 10
            
            # Medical Information Section
            y_pos += 20
            self._draw_section_header(draw, "Medical Information", 20, y_pos, header_font)
            y_pos += 30
            
            # Medical History
            y_pos = self._draw_list_field(draw, "Medical History:", data.get("medical_history", []), 40, y_pos, normal_font)
            y_pos += 20
            
            # Current Medications
            y_pos = self._draw_list_field(draw, "Current Medications:", data.get("current_medications", []), 40, y_pos, normal_font)
            y_pos += 20
            
            # Allergies
            y_pos = self._draw_list_field(draw, "Allergies:", data.get("allergies", []), 40, y_pos, normal_font)
            y_pos += 20
            
            # Appointment Information Section
            y_pos += 20
            self._draw_section_header(draw, "Appointment Information", 20, y_pos, header_font)
            y_pos += 30
            
            appointment_fields = [
                ("Primary Complaint:", data.get("primary_complaint", "N/A")),
                ("Appointment Date:", data.get("appointment_date", "N/A")),
                ("Doctor:", data.get("doctor_name", "N/A"))
            ]
            
            for label, value in appointment_fields:
                y_pos = self._draw_field(draw, label, str(value), 40, y_pos, normal_font)
                y_pos += 10
            
            # Draw footer
            draw.rectangle([(0, height-40), (width, height)], fill=(240, 240, 240))
            draw.text((20, height-30), "Generated by Healthcare Form Data Extraction PoC", fill=(100, 100, 100), font=normal_font)
            
            # Save the image
            image.save(screenshot_path)
            
            return screenshot_path
        
        except Exception as e:
            self.logger.error(f"Error creating form visualization: {str(e)}")
            return self._create_text_fallback(data, form_id)
    
    def _draw_section_header(self, draw, text, x, y, font):
        """Draw a section header with a line underneath."""
        draw.text((x, y), text, fill=(66, 133, 244), font=font)
        draw.line([(x, y + 25), (x + 500, y + 25)], fill=(200, 200, 200), width=1)
    
    def _draw_field(self, draw, label, value, x, y, font):
        """Draw a field with label and value."""
        draw.text((x, y), label, fill=(100, 100, 100), font=font)
        
        # Handle multiline values
        if "\n" in value:
            lines = value.split("\n")
            line_height = font.getsize("A")[1] + 5
            for i, line in enumerate(lines):
                draw.text((x + 200, y + (i * line_height)), line, fill=(0, 0, 0), font=font)
            return y + (len(lines) * line_height)
        else:
            draw.text((x + 200, y), value, fill=(0, 0, 0), font=font)
            return y + 25
    
    def _draw_list_field(self, draw, label, values, x, y, font):
        """Draw a field with a list of values."""
        draw.text((x, y), label, fill=(100, 100, 100), font=font)
        
        if not values:
            draw.text((x + 200, y), "None", fill=(0, 0, 0), font=font)
            return y + 25
        
        line_height = font.getsize("A")[1] + 5
        for i, value in enumerate(values):
            draw.text((x + 200, y + (i * line_height)), f"• {value}", fill=(0, 0, 0), font=font)
        
        return y + (len(values) * line_height)
    
    def _create_text_fallback(self, data: Dict[str, Any], form_id: str) -> Optional[Path]:
        """Create a simple text file as a fallback."""
        screenshot_path = self.screenshot_dir / f"{form_id}_screenshot.txt"
        
        try:
            with open(screenshot_path, "w") as f:
                f.write(f"HEALTHCARE FORM DATA - ID: {form_id}\n\n")
                
                # Patient Information
                f.write("PATIENT INFORMATION\n")
                f.write(f"Patient Name: {data.get('patient_name', 'N/A')}\n")
                f.write(f"Date of Birth: {data.get('date_of_birth', 'N/A')}\n")
                f.write(f"Gender: {data.get('gender', 'N/A')}\n")
                f.write(f"Address: {data.get('address', 'N/A')}\n")
                f.write(f"Phone Number: {data.get('phone_number', 'N/A')}\n")
                f.write(f"Email: {data.get('email', 'N/A')}\n\n")
                
                # Insurance Information
                f.write("INSURANCE INFORMATION\n")
                f.write(f"Insurance Provider: {data.get('insurance_provider', 'N/A')}\n")
                f.write(f"Insurance ID: {data.get('insurance_id', 'N/A')}\n\n")
                
                # Medical Information
                f.write("MEDICAL INFORMATION\n")
                f.write("Medical History:\n")
                for item in data.get('medical_history', []):
                    f.write(f"- {item}\n")
                
                f.write("\nCurrent Medications:\n")
                for item in data.get('current_medications', []):
                    f.write(f"- {item}\n")
                
                f.write("\nAllergies:\n")
                for item in data.get('allergies', []):
                    f.write(f"- {item}\n")
                
                # Appointment Information
                f.write("\nAPPOINTMENT INFORMATION\n")
                f.write(f"Primary Complaint: {data.get('primary_complaint', 'N/A')}\n")
                f.write(f"Appointment Date: {data.get('appointment_date', 'N/A')}\n")
                f.write(f"Doctor: {data.get('doctor_name', 'N/A')}\n")
            
            return screenshot_path
        
        except Exception as e:
            self.logger.error(f"Error creating text fallback: {str(e)}")
            return None


# Create a singleton instance
form_visualizer = FormVisualizer(screenshot_dir=settings.screenshot_dir)


def fill_form(data: Dict[str, Any], form_id: str) -> Optional[Path]:
    """
    Create a visual representation of a healthcare form with the extracted data.
    
    Args:
        data: Dictionary containing form data
        form_id: Unique identifier for the form
        
    Returns:
        Path to the visualization if successful, None otherwise
    """
    return form_visualizer.create_form_visualization(data, form_id)
