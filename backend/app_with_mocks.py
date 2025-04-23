"""
Modified FastAPI application for the Healthcare Form Data Extraction PoC.
Uses mock functionality for problematic components.
"""
import logging
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Mock Settings
class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    groq_api_key: str = Field("mock-api-key", env="GROQ_API_KEY")
    
    # File Paths
    upload_dir: Path = Field(Path("./uploads"), env="UPLOAD_DIR")
    screenshot_dir: Path = Field(Path("./screenshots"), env="SCREENSHOT_DIR")
    
    # Form URLs
    target_form_url: str = Field("https://example.com/healthcare-form", env="TARGET_FORM_URL")
    
    # Server Configuration
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8001, env="PORT")
    debug: bool = Field(True, env="DEBUG")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    def initialize_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)


# Create a global settings instance
settings = Settings()
# Initialize directories
settings.initialize_directories()


# Mock FormData model
class FormData(BaseModel):
    """Pydantic model for healthcare form data."""
    
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


# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Healthcare Form Data Extraction API",
    description="API for extracting data from healthcare forms using OCR and LLM",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for screenshots
app.mount("/screenshots", StaticFiles(directory=str(settings.screenshot_dir)), name="screenshots")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Healthcare Form Data Extraction API"}


@app.post("/api/extract")
async def extract_form_data(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extract data from a healthcare form (PDF or image).
    
    Args:
        file: Uploaded file (PDF or image)
        
    Returns:
        JSON response with extracted data and screenshot URL
    """
    try:
        # Generate a unique ID for this extraction
        extraction_id = str(uuid.uuid4())
        
        # Save the uploaded file
        file_path = await save_upload_file(file, extraction_id)
        
        # Mock data extraction (in a real implementation, this would use the actual components)
        extracted_data = mock_extract_data(file_path)
        
        # Generate mock screenshot URL
        screenshot_url = f"/screenshots/{extraction_id}_screenshot.png"
        
        # Create a mock screenshot file
        create_mock_screenshot(extraction_id)
        
        # Return the response
        return {
            "status": "ok",
            "data": extracted_data,
            "screenshot_url": screenshot_url
        }
    
    except Exception as e:
        logger.error(f"Error processing form: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def save_upload_file(file: UploadFile, file_id: str) -> Path:
    """
    Save an uploaded file to disk.
    
    Args:
        file: Uploaded file
        file_id: Unique ID for the file
        
    Returns:
        Path to the saved file
    """
    # Determine file extension
    file_extension = Path(file.filename).suffix if file.filename else ""
    
    # Create file path
    file_path = settings.upload_dir / f"{file_id}{file_extension}"
    
    # Save the file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return file_path


def mock_extract_data(file_path: Path) -> Dict[str, Any]:
    """
    Mock function to extract data from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing mock extracted data
    """
    # Return mock data
    return {
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


def create_mock_screenshot(extraction_id: str) -> None:
    """
    Create a mock screenshot file.
    
    Args:
        extraction_id: Unique ID for the extraction
    """
    # Create a simple text file as a mock screenshot
    screenshot_path = settings.screenshot_dir / f"{extraction_id}_screenshot.png"
    with open(screenshot_path, "w") as f:
        f.write("This is a mock screenshot file.")


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run(
        "app_with_mocks:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
