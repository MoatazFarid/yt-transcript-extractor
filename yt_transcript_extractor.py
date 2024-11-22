import os
from dotenv import load_dotenv
from pytube import YouTube
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
import yt_dlp
import whisper
from datetime import datetime
import subprocess

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# TODO: Implement audio chunking to decrease the number of tokens in each request
def extract_captions(youtube_link):
    try:
        print(f"Processing YouTube link: {youtube_link}")  # Debugging statement
        # Create YouTube object
        yt = YouTube(youtube_link)

        # Check for available captions
        if yt.captions:
            print(f"Available captions: {[caption.code for caption in yt.captions]}")  # Log available captions
            caption = yt.captions.get_by_language_code('en')
            if caption:
                return caption.generate_srt_captions()
            else:
                print("No English captions available.")
                return None
        else:
            print("No captions available for this video.")
            return None
        
    except Exception as e:
        return f"Error extracting captions: {str(e)}"

def audio_to_text(audio_file):
    try:
        model = whisper.load_model("base")  # You can choose a different model size if needed
        result = model.transcribe(audio_file)
        return result['text']
    except Exception as e:
        return f"Error converting audio to text: {str(e)}"

def summarize_text(full_text):
    try:
        print(f"Summarizing text: {full_text[:50]}...")  # Debugging statement
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Please summarize the following text:\n\n{full_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing text: {str(e)}"

def create_markdown_files(video_id, full_text, summary):
    # Create output folder
    output_folder = create_output_folder(video_id)
    
    # Use video ID for file naming
    safe_id = "".join(c for c in video_id if c.isalnum() or c in ("_", "-")).rstrip()

    # Save full text file in output folder
    full_text_path = os.path.join(output_folder, f'{safe_id}_full_text.md')
    with open(full_text_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    # Save summary file in output folder 
    summary_path = os.path.join(output_folder, f'{safe_id}_summary.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)

def check_video_processed(video_id):
    processed_videos_file = 'processed_videos.txt'
    if os.path.exists(processed_videos_file):
        with open(processed_videos_file, 'r', encoding='utf-8') as f:
            processed_videos = f.read().splitlines()
            return video_id in processed_videos
    return False

def mark_video_processed(video_id):
    with open('processed_videos.txt', 'a', encoding='utf-8') as f:
        f.write(video_id + '\n')

def create_output_folder(video_id):
    """Create a dated output folder for a video"""
    today_date = datetime.now().date().isoformat()
    folder_name = f"{video_id}_{today_date}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def check_audio_exists(temp_audio_path):
    """Check if the audio file or its WAV version exists"""
    wav_path = f"{temp_audio_path}"
    return os.path.exists(wav_path)

def download_audio(youtube_link, temp_audio_path):
    """Download audio from YouTube link"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_audio_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'keepvideo': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])

def save_transcript_file(output_folder, video_id, video, youtube_link, transcript, detected_lang=None):
    """Save transcript to a formatted md file"""
    output_file = os.path.join(output_folder, f'{video_id}_transcriptOnly.md')
    print(f"Saving transcript to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    return output_file

def check_ffmpeg_installed():
    """Check if FFmpeg is installed and accessible"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def process_video_transcript(youtube_link, output_folder=None):
    """Process video and return transcript. Core logic separated from UI."""
    video = YouTube(youtube_link)
    video_id = video.video_id
    detected_lang = None
    
    if not output_folder:
        output_folder = create_output_folder(video_id)
    
    # Try getting captions first
    transcript = extract_captions(youtube_link)
    
    # If no captions available, use whisper
    if transcript is None:
        print("No captions found. Converting audio to text with language detection...")
        temp_audio_path = os.path.join(output_folder, 'temp_audio.wav')
        
        if check_audio_exists(temp_audio_path):
            print("Using existing audio file...")
        else:
            print("Downloading audio file...")
            download_audio(youtube_link, temp_audio_path)
        
        model = whisper.load_model("base", device="cpu")
        result = model.transcribe(f"{temp_audio_path}", fp16=False)
        transcript = result["text"]
        detected_lang = result["language"]
        print(f"Detected language: {detected_lang}")
    
    # Save and return transcript
    output_file = save_transcript_file(
        output_folder, 
        video_id, 
        video, 
        youtube_link, 
        transcript, 
        detected_lang
    )
    
    return {
        'transcript': transcript,
        'video_id': video_id,
        'output_file': output_file,
        'detected_lang': detected_lang
    }

if __name__ == "__main__":
    youtube_link = input("Enter YouTube link: ")
    yt = YouTube(youtube_link)
    video_id = yt.video_id
    video_language = yt.captions.get_by_language_code('en').name if yt.captions else "Unknown"

    print(f"Video Language: {video_language}")

    if check_video_processed(video_id):
        print(f"The video '{video_id}' has already been processed.")
    else:
        full_text = extract_captions(youtube_link)
        
        if full_text is None:
            # If no captions, attempt to download audio and convert to text
            try:
                print("Attempting to download audio and convert to text...")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'audio.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',  # Keep as wav format
                        'preferredquality': '192',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_link])
                full_text = audio_to_text('audio.wav')  # Use wav file for recognition
            except Exception as e:
                print(f"Error downloading audio: {str(e)}")
                full_text = "Error downloading audio."

        if "Error" in full_text:
            print(full_text)
        else:
            summary = summarize_text(full_text)
            if "Error" in summary:
                print(summary)
            else:
                create_markdown_files(video_id, full_text, summary)
                mark_video_processed(video_id)
