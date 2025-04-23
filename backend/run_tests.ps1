# PowerShell script to run tests for the Healthcare Form Data Extraction PoC backend

# Activate virtual environment if it exists
if (Test-Path -Path ".venv") {
    Write-Host "Activating virtual environment..."
    & .\.venv\Scripts\Activate.ps1
}
else {
    Write-Host "Virtual environment not found. Please run setup.ps1 first."
    exit 1
}

# Run tests with pytest
Write-Host "Running tests..."
python -m pytest tests/ -v
