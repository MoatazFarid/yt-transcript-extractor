# Changelog

All notable changes to the Transcript Generator project will be documented in this file.

## [v2.0.0] - 2024-03-19

### Added
- Local video transcription support using OpenAI's Whisper model
- New tabbed interface with separate tabs for YouTube and local video processing
- Markdown output format for transcripts with timestamps
- Automatic directory organization with timestamped folders
- Support for MP4 to MP3 conversion

### Changed
- Restructured the application to use a modular design
- Enhanced UI with ttk widgets for a more modern look
- Improved error handling and user feedback
- Updated file organization system

### Dependencies
- Added `moviepy` for video processing
- Added `whisper` for local video transcription
- Updated requirements.txt with new dependencies

## [v1.0.0] - 2023-11-21

### Initial Release
- YouTube video transcript extraction
- Text summarization
- Markdown file generation
- Basic UI for YouTube video processing 