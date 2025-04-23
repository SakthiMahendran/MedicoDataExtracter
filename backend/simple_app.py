"""
Simplified FastAPI application for testing the API structure.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
from pathlib import Path

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

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Healthcare Form Data Extraction API"}

@app.post("/api/extract")
async def extract_form_data(file: UploadFile = File(...)):
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
        
        # In a real implementation, we would:
        # 1. Save the uploaded file
        # 2. Extract text from the file
        # 3. Extract structured data using LLM
        # 4. Validate the extracted data
        # 5. Fill the form and get screenshot
        
        # For now, return mock data
        mock_data = {
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
        
        # Return the response
        return {
            "status": "ok",
            "data": mock_data,
            "screenshot_url": f"/screenshots/{extraction_id}_screenshot.png"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_app:app", host="0.0.0.0", port=8001, reload=True)
