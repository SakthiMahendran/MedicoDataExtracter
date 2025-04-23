# Healthcare Form Data Extraction PoC

A proof-of-concept application for extracting structured data from healthcare forms using OCR, LLM extraction, and form visualization.

![Healthcare Form Data Extraction](https://img.shields.io/badge/PoC-Healthcare%20Form%20Data%20Extraction-blue)
![Llama 3.1](https://img.shields.io/badge/LLM-Llama%203.1%2070B-green)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Data Extraction Process](#data-extraction-process)
- [JSON Data Format](#json-data-format)
- [API Reference](#api-reference)
- [Setup Instructions](#setup-instructions)
- [Quick Start](#quick-start)
- [Development](#development)
- [Future Enhancements](#future-enhancements)

## Overview

This application extracts structured data from healthcare forms (PDF or images) using a combination of OCR, advanced LLM processing, and data validation. It provides a modern React-based UI for uploading forms and viewing extracted data.

## Features

- **PDF Processing**: Extract text with layout preservation using PyMuPDF
- **OCR Capabilities**: Process scanned documents and images using docTR
- **AI-Powered Extraction**: Extract structured data using Groq's Llama 3.1 70B model
- **Data Validation**: Validate and sanitize extracted data with Pandera and Pydantic
- **Form Visualization**: Generate visual representations of completed forms
- **Modern UI**: React-based interface with Material UI components
- **API-First Design**: RESTful API for easy integration with other systems

## Technology Stack

### Backend (Python 3.11)

- **FastAPI 0.95** – Modern, high-performance web framework
- **Uvicorn 0.22** – ASGI server for FastAPI
- **PyMuPDF 1.25** – PDF processing library for text and layout extraction
- **docTR 0.7** – Document Text Recognition for OCR on scanned images
- **Groq SDK 1.4** – API client for Llama 3.1 model access
- **Llama 3.1 70B** – State-of-the-art large language model for structured data extraction
- **Pandera 0.20** – Statistical data validation
- **Pydantic 2.1** – Data validation and settings management
- **PIL/Pillow** – Image processing for form visualization

### Frontend (Vite + React 18)

- **Vite 4.x** – Next-generation frontend build tool
- **React 18** – UI library with hooks and concurrent rendering
- **Material UI 5.14** – Comprehensive component library
- **Axios 1.4** – Promise-based HTTP client
- **React Dropzone** – Drag-and-drop file upload
- **React Syntax Highlighter** – JSON data formatting and display

## Architecture

The application follows a clean, modular architecture:

```
monolith_data_extractor/
├── backend/                  # Python FastAPI backend
│   ├── app_compatible.py     # Main FastAPI application
│   ├── config.py             # Configuration management
│   ├── pdf_parser.py         # PDF text extraction
│   ├── ocr_parser.py         # Image OCR processing
│   ├── llm_extractor.py      # LLM-based data extraction
│   ├── validator.py          # Data validation
│   ├── form_filler.py        # Form visualization
│   └── tests/                # Unit tests
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── App.jsx           # Main application component
│   │   └── main.jsx          # Application entry point
│   └── public/               # Static assets
└── run_app.cmd               # Script to run both frontend and backend
```

## Data Extraction Process

1. **Document Upload**: User uploads a healthcare form (PDF or image)
2. **Text Extraction**: 
   - For PDFs: Extract text with layout information using PyMuPDF
   - For Images: Perform OCR using docTR
3. **LLM Processing**: Send extracted text to Llama 3.1 70B model via Groq API
4. **Data Structuring**: Extract structured data in JSON format
5. **Validation**: Validate data against predefined schema
6. **Visualization**: Generate visual representation of the form with extracted data
7. **Result Delivery**: Return structured data and form visualization to the user

## JSON Data Format

The application extracts the following structured data from healthcare forms:

```json
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
```

### Field Details

- **Required Fields**: patient_name, date_of_birth, gender, address, phone_number, insurance_provider, insurance_id, primary_complaint
- **Optional Fields**: email, appointment_date, doctor_name
- **List Fields**: medical_history, current_medications, allergies

## API Reference

### Extract Form Data

```
POST /api/extract
```

**Request:**
- Content-Type: multipart/form-data
- Body: file (PDF, JPEG, PNG, or TIFF)

**Response:**
```json
{
  "status": "ok",
  "data": {
    // Extracted form data in the format shown above
  },
  "screenshot_url": "/screenshots/{id}_screenshot.png"
}
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Node.js 18.x or higher
- Groq API key (for LLM access)

### Backend Setup

```bash
# Navigate to backend source
cd monolith_data_extractor/backend

# Create and activate a Python virtual environment
python -m venv .venv
# On Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Install project dependencies
pip install -r requirements.txt

# Copy example env vars and edit as needed
cp ../.env.example .env    # <- set GROQ_API_KEY
```

### Frontend Setup

```bash
# Navigate to frontend
cd monolith_data_extractor/frontend

# Install Node dependencies
npm install
```

## Quick Start

The easiest way to run the application is using the provided script:

```bash
# From the project root
.\run_app.cmd
```

This script will:
1. Start the backend server (FastAPI + Uvicorn)
2. Start the frontend development server (Vite)
3. Open the application in your default browser
4. Provide an easy way to stop all servers when done

Alternatively, you can start the servers manually:

**Backend:**
```bash
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app_compatible:app --reload --port 8001
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Development

For detailed development information, see:
- `development_plan_for_backend.txt` - Backend implementation details
- `development_plan_for_frontend.txt` - Frontend implementation details

## Future Enhancements

- **Multi-form Support**: Add templates for different healthcare form types
- **Authentication**: Add user authentication and authorization
- **Document Storage**: Implement secure storage for processed documents
- **Batch Processing**: Support for processing multiple forms at once
- **Export Options**: Add export to PDF, CSV, and other formats
- **Integration APIs**: Connectors for EHR/EMR systems
