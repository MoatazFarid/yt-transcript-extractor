from typing import Optional, List
from dataclasses import dataclass
from youtube_transcript_api import YouTubeTranscriptApi
from sinek_style_analyzer import create_analyzer, Point
import os
from dotenv import load_dotenv

@dataclass
class VideoAnalysis:
    video_id: str
    transcript: str
    points: List[Point]
    raw_output_path: Optional[str] = None
    summary_path: Optional[str] = None

class YouTubeContentAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize the YouTube content analyzer.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use (default: gpt-4)
        """
        self.analyzer = create_analyzer(
            api_key=api_key,
            model=model
        )

    def get_transcript(self, video_id: str) -> str:
        """Retrieve and format YouTube video transcript."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([entry['text'] for entry in transcript_list])
        except Exception as e:
            raise ValueError(f"Failed to get transcript for video {video_id}: {str(e)}")

    def analyze_video(
        self, 
        video_id: str, 
        chunk_size: int = 1000,
        save_output: bool = True,
        output_dir: str = "output"
    ) -> VideoAnalysis:
        """Analyze a YouTube video and generate Simon Sinek style content.
        
        Args:
            video_id: YouTube video ID
            chunk_size: Size of text chunks for processing
            save_output: Whether to save output to files
            output_dir: Directory to save output files
        
        Returns:
            VideoAnalysis object containing results
        """
        # Get transcript
        transcript = self.get_transcript(video_id)
        
        # Process transcript to get points
        points = self.analyzer.process_transcript(transcript, chunk_size)
        
        # Generate detailed content
        points = self.analyzer.generate_detailed_content(points)
        
        # Create analysis object
        analysis = VideoAnalysis(
            video_id=video_id,
            transcript=transcript,
            points=points
        )
        
        # Save output if requested
        if save_output:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save raw transcript
            raw_path = os.path.join(output_dir, f"{video_id}_transcript.txt")
            with open(raw_path, "w", encoding='utf-8') as f:
                f.write(transcript)
            analysis.raw_output_path = raw_path
            
            # Save analyzed content
            summary_path = os.path.join(output_dir, f"{video_id}_analysis.md")
            self.analyzer.save_to_file(points, summary_path)
            analysis.summary_path = summary_path
            
        return analysis

def create_analyzer_from_env() -> YouTubeContentAnalyzer:
    """Create analyzer using environment variables."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return YouTubeContentAnalyzer(api_key)

# Example usage
if __name__ == "__main__":
    # Create analyzer from environment variables
    analyzer = create_analyzer_from_env()
    
    # Get video ID from environment or input
    video_id = os.getenv('YOUTUBE_VIDEO_ID')
    if not video_id:
        video_id = input("Enter YouTube video ID: ")
    
    try:
        # Analyze video
        analysis = analyzer.analyze_video(video_id)
        print(f"Analysis complete!")
        print(f"Raw transcript saved to: {analysis.raw_output_path}")
        print(f"Analysis saved to: {analysis.summary_path}")
        
    except Exception as e:
        print(f"Error analyzing video: {str(e)}") 