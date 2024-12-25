# Transcript Generator

A powerful application that generates transcripts from both YouTube videos and local video files. The application uses OpenAI's Whisper model for local video transcription and YouTube's API for online videos.

## Features

- **YouTube Video Processing**
  - Extract transcripts from YouTube videos
  - Generate text summaries
  - Export in Markdown format
  - Support for multiple languages

- **Local Video Processing**
  - Convert MP4 videos to transcripts
  - Automatic MP4 to MP3 conversion
  - Timestamped transcripts in Markdown format
  - Organized output in timestamped directories

## Prerequisites

- Python 3.8 or higher
- FFmpeg installed and added to system PATH
- Windows/Linux/MacOS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/transcript_generator.git
cd transcript_generator
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
   - **Windows**: 
     1. Download from https://www.gyan.dev/ffmpeg/builds/
     2. Extract and rename folder to 'ffmpeg'
     3. Move to C:\ drive
     4. Add C:\ffmpeg\bin to system PATH
   - **Linux**: `sudo apt-get install ffmpeg`
   - **MacOS**: `brew install ffmpeg`

## Usage

1. Start the application:
```bash
python transcript_generator_ui.py
```

2. The application has two main features:

### YouTube Video Transcription
1. Select the "YouTube Video" tab
2. Paste the YouTube video URL
3. Choose either:
   - "Generate Transcript & Summary" for full processing
   - "Export Transcript Only" for just the transcript
4. Wait for processing to complete
5. Find the output files in the generated timestamp directory

### Local Video Transcription
1. Select the "Local Video" tab
2. Click "Browse Video File" to select an MP4 file
3. Click "Generate Transcript"
4. Wait for processing to complete
5. Find the transcript in the generated timestamp directory

## Output Format

### YouTube Videos
- `video_id_transcript.md`: Full transcript
- `video_id_summary.md`: Text summary
- Files are organized in a directory with the video ID

### Local Videos
- `filename_transcript.md`: Transcript with timestamps
- Organized in directories named `filename_YYYYMMDD_HHMMSS`
- Timestamps for each segment of speech

## Troubleshooting

1. **FFmpeg Error**:
   - Ensure FFmpeg is properly installed
   - Verify system PATH includes FFmpeg
   - Restart application after installation

2. **Memory Issues**:
   - Close other applications
   - For large videos, ensure sufficient free memory
   - Consider using a machine with more RAM

3. **File Access Errors**:
   - Run the application with appropriate permissions
   - Ensure write access to the output directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI's Whisper model for transcription
- YouTube API for video processing
- MoviePy for video conversion
- All other open-source contributors
