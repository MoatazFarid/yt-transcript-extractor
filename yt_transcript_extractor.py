import os
from dotenv import load_dotenv
from pytube import YouTube
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
import yt_dlp
import whisper

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
        # Load the whisper model
        model = whisper.load_model("base")  # You can choose a different model size if needed

        # Transcribe the audio file
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
    # Use video ID for file naming
    safe_id = "".join(c for c in video_id if c.isalnum() or c in ("_", "-")).rstrip()
    
    with open(f'{safe_id}_full_text.md', 'w', encoding='utf-8') as f:
        f.write(full_text)

    with open(f'{safe_id}_summary.md', 'w', encoding='utf-8') as f:
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
