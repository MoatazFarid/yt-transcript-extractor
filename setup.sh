#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Create requirements.txt if it doesn't exist
if [ ! -f requirements.txt ]; then
    pip freeze > requirements.txt
fi

echo "Setup complete. Virtual environment created and packages installed."
