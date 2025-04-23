"""
Main FastAPI application for the Healthcare Form Data Extraction PoC.
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

from config import settings
from pdf_parser import extract_text_with_layout, is_pdf_file
from ocr_parser import ocr_parser, is_image_file
from llm_extractor import llm_extractor
from validator import validate
from form_filler import fill_form


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

# Create directories if they don't exist
settings.initialize_directories()

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
        
        # Extract text from the file
        text_blocks = await extract_text_from_file(file_path)
        
        # Extract structured data using LLM
        extracted_data = llm_extractor.extract_fields(text_blocks)
        
        # Validate the extracted data
        validated_data = validate(extracted_data)
        
        # Fill the form and get screenshot
        screenshot_path = fill_form(validated_data.dict(), extraction_id)
        
        # Generate screenshot URL
        screenshot_url = f"/screenshots/{screenshot_path.name}" if screenshot_path else None
        
        # Return the response
        return {
            "status": "ok",
            "data": validated_data.dict(),
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


async def extract_text_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract text from a file (PDF or image).
    
    Args:
        file_path: Path to the file
        
    Returns:
        List of text blocks with coordinates
    """
    # Check if the file is a PDF
    if is_pdf_file(file_path):
        return extract_text_with_layout(file_path)
    
    # Check if the file is an image
    elif is_image_file(file_path):
        return ocr_parser.extract_text_from_image(file_path)
    
    # Unsupported file type
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
