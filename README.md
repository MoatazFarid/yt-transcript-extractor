# yt-transcript-extractor

This application extracts captions from YouTube videos. If captions are not available, it downloads the audio and converts it to text using OpenAI's Whisper model.

## Setup Instructions

1. Clone the repository.
2. Navigate to the project directory.
3. Create a `.env` file based on the `.env.example` template:
   - Copy `.env.example` to `.env` and fill in your OpenAI API key.
4. Run the setup script:
   - For Bash:
     ```bash
     bash setup.sh
     ```
   - For PowerShell:
     ```powershell
     .\setup.ps1
     ```
5. Activate the virtual environment:
   - For Bash:
     ```bash
     source venv/bin/activate
     ```
   - For PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
6. Run the application:
   ```bash
   python yt_transcript_extractor.py
   ```

## Usage

Enter the YouTube link when prompted to extract captions.
