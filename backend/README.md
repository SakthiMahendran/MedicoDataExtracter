# Healthcare Form Data Extraction PoC - Backend

This directory contains the backend implementation for the Healthcare Form Data Extraction Proof of Concept.

## Overview

The backend is built with FastAPI and provides an API endpoint for extracting structured data from healthcare forms (PDF or images) using OCR and LLM technologies. It also includes functionality for form automation using Playwright.

## Architecture

The backend is organized into several modules:

- `app.py`: FastAPI application with the `/api/extract` endpoint
- `config.py`: Environment variable management using Pydantic
- `pdf_parser.py`: PDF text extraction with PyMuPDF
- `ocr_parser.py`: Image text extraction with docTR
- `llm_extractor.py`: Structured data extraction using Groq/Llama-3
- `validator.py`: Data validation with Pandera and Pydantic
- `form_filler.py`: Form automation with Playwright

## Setup

### Prerequisites

- Python 3.11 or higher
- A Groq API key for LLM access

### Installation

1. Run the setup script to create a virtual environment and install dependencies:

```powershell
# On Windows (PowerShell)
.\setup.ps1
```

2. Edit the `.env` file to set your Groq API key and other settings:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Running the Server

Start the FastAPI server:

```powershell
# Make sure the virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Start the server
uvicorn app:app --reload --port 8001
```

The API will be available at http://localhost:8001

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

### Endpoints

#### `GET /`

Returns a simple message to verify that the API is running.

#### `POST /api/extract`

Extracts structured data from a healthcare form (PDF or image).

**Request:**
- Content-Type: multipart/form-data
- Body: file (PDF or image)

**Response:**
```json
{
  "status": "ok",
  "data": {
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
  },
  "screenshot_url": "/screenshots/12345678-1234-1234-1234-123456789012_screenshot.png"
}
```

## Testing

Run the tests using the provided script:

```powershell
# On Windows (PowerShell)
.\run_tests.ps1
```

This will run all the unit tests in the `tests` directory.

## Directory Structure

- `uploads/`: Directory for storing uploaded files
- `screenshots/`: Directory for storing form automation screenshots
- `tests/`: Unit tests for the backend modules

## Next Steps

After successfully implementing and testing the backend, the next step is to develop the frontend according to the development plan.
