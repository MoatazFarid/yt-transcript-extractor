# yt-transcript-extractor

This application extracts captions from YouTube videos. If captions are not available, it downloads the audio and converts it to text using OpenAI's Whisper model.

<details>
<summary>✨ Features</summary>

- Extracts available captions/subtitles from YouTube videos
- Falls back to audio transcription using OpenAI Whisper if captions aren't available
- Supports multiple languages (when available through YouTube)
- Outputs transcripts in plain text format
- Simple and intuitive user interface
</details>

## 🚀 Setup Instructions

1. Clone the repository
2. Navigate to the project directory
3. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. Run the setup script:
   <details>
   <summary>Setup Commands</summary>

   ```bash
   # For Bash
   bash setup.sh

   # For PowerShell
   .\setup.ps1
   ```
   </details>

5. Activate the virtual environment:
   <details>
   <summary>Activation Commands</summary>

   ```bash
   # For Bash
   source venv/bin/activate

   # For PowerShell
   .\venv\Scripts\Activate.ps1
   ```
   </details>

## 💻 Usage

1. Start the application:
   ```bash
   python yt_transcript_extractor_ui.py
   ```
2. Enter a YouTube URL when prompted
3. Wait for the transcript to be generated
4. The output will be saved as a text file

Example:
```bash
# Extract captions from a YouTube video
python yt_transcript_extractor_ui.py
# When prompted, enter: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## 🛠️ TODO and Future Work

- [ ] Implement audio chunking to decrease token usage
- [ ] Create a Dockerfile for containerization
- [ ] Add command-line arguments support
- [ ] Add batch processing capabilities

## YouTube Content Analyzer

The `youtube_content_analyzer.py` script analyzes YouTube video transcripts and generates Simon Sinek style content analysis.

### Features

- 📝 Extracts and processes YouTube video transcripts
- 🔍 Analyzes content using OpenAI's GPT models
- 💡 Generates detailed content analysis in Simon Sinek's style
- 💾 Saves both raw transcripts and analyzed content

### Prerequisites

1. OpenAI API key (set in `.env` file)
2. Python packages:
   ```bash
   pip install youtube_transcript_api python-dotenv
   ```

### Usage

#### Method 1: Using Environment Variables

```bash
# Set your OpenAI API key and video ID in .env file
OPENAI_API_KEY=your_api_key_here
YOUTUBE_VIDEO_ID=video_id_here

# Run the script
python youtube_content_analyzer.py
```

#### Method 2: Direct Input

```python
from youtube_content_analyzer import YouTubeContentAnalyzer

# Initialize analyzer
analyzer = YouTubeContentAnalyzer(api_key="your_openai_api_key")

# Analyze video
analysis = analyzer.analyze_video(
    video_id="video_id_here",
    chunk_size=1000,  # Optional: adjust text chunk size
    save_output=True  # Optional: save results to files
)

# Access results
print(f"Transcript: {analysis.transcript}")
print(f"Analysis points: {analysis.points}")
print(f"Output files: {analysis.raw_output_path}, {analysis.summary_path}")
```

### Output Files

The analyzer generates two files in the `output` directory:
- `{video_id}_transcript.txt`: Raw video transcript
- `{video_id}_analysis.md`: Detailed content analysis in markdown format

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `api_key` | OpenAI API key | Required |
| `model` | OpenAI model to use | "gpt-4" |
| `chunk_size` | Text chunk size for processing | 1000 |
| `save_output` | Save results to files | True |
| `output_dir` | Directory for output files | "output" |
