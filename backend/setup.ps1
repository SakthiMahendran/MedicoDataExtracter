# PowerShell script to set up the development environment
# for the Healthcare Form Data Extraction PoC backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
Write-Host "Installing Playwright browsers..."
python -m playwright install

# Create necessary directories
Write-Host "Creating necessary directories..."
if (-not (Test-Path -Path "uploads")) {
    New-Item -Path "uploads" -ItemType Directory
}

if (-not (Test-Path -Path "screenshots")) {
    New-Item -Path "screenshots" -ItemType Directory
}

# Check if .env file exists, copy from .env.example if not
if (-not (Test-Path -Path ".env")) {
    Write-Host "Creating .env file from .env.example..."
    if (Test-Path -Path "../.env.example") {
        Copy-Item -Path "../.env.example" -Destination ".env"
        Write-Host "Please edit the .env file to set your GROQ_API_KEY and other settings."
    }
    else {
        Write-Host "Warning: .env.example not found. Please create a .env file manually."
    }
}

Write-Host "Setup complete! You can now run the FastAPI server with:"
Write-Host "uvicorn app:app --reload --port 8001"
