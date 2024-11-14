# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt

# Create requirements.txt if it doesn't exist
if (-Not (Test-Path requirements.txt)) {
    pip freeze > requirements.txt
}

Write-Host "Setup complete. Virtual environment created and packages installed."
