import os
from moviepy.editor import VideoFileClip
import whisper
from datetime import datetime

class VideoTranscriber:
    def __init__(self):
        # Initialize the Whisper model (using the base model for faster processing)
        self.model = whisper.load_model("base")
        
    def create_output_directory(self, video_name):
        """
        Create a timestamped directory for outputs
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = f"{video_name}_{timestamp}"
        os.makedirs(dir_name, exist_ok=True)
        return dir_name
        
    def convert_mp4_to_mp3(self, video_path, output_dir):
        """
        Convert an MP4 file to MP3 format
        """
        try:
            # Get the filename without extension
            filename = os.path.splitext(os.path.basename(video_path))[0]
            # Create output path for MP3
            output_path = os.path.join(output_dir, f"{filename}.mp3")
            
            # Load the video file
            video = VideoFileClip(video_path)
            # Extract the audio
            audio = video.audio
            # Write the audio file
            audio.write_audiofile(output_path)
            # Close the video to free up resources
            video.close()
            
            return output_path
        except Exception as e:
            raise Exception(f"Error converting video to audio: {str(e)}")

    def transcribe_audio(self, audio_path, output_dir):
        """
        Transcribe an audio file using Whisper and save as markdown
        """
        try:
            # Transcribe the audio file
            result = self.model.transcribe(audio_path)
            
            # Get the base filename
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            
            # Create output paths for different formats
            transcript_path = os.path.join(output_dir, f"{base_name}_transcript.md")
            
            # Format the transcript in markdown
            markdown_content = f"# Transcript: {base_name}\n\n"
            markdown_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            markdown_content += "## Content\n\n"
            
            # Add segments with timestamps if available
            if 'segments' in result:
                for segment in result['segments']:
                    start_time = str(datetime.utcfromtimestamp(segment['start']).strftime('%H:%M:%S'))
                    markdown_content += f"[{start_time}] {segment['text']}\n\n"
            else:
                markdown_content += result["text"]
            
            # Save the markdown transcript
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            return transcript_path
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")

    def process_video(self, video_path):
        """
        Process a video file: convert to audio and transcribe
        """
        try:
            # Get video filename without extension
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            
            # Create output directory
            output_dir = self.create_output_directory(video_name)
            
            # Convert video to audio
            print("Converting video to audio...")
            audio_path = self.convert_mp4_to_mp3(video_path, output_dir)
            
            # Transcribe the audio
            print("Transcribing audio...")
            transcript_path = self.transcribe_audio(audio_path, output_dir)
            
            # Clean up the temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return transcript_path
        except Exception as e:
            raise Exception(f"Error processing video: {str(e)}")

# Example usage:
if __name__ == "__main__":
    transcriber = VideoTranscriber()
    # Replace with your video path
    video_path = "path/to/your/video.mp4"
    transcript_path = transcriber.process_video(video_path)
    print(f"Transcript saved to: {transcript_path}") 