import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from dotenv import load_dotenv
from pytube import YouTube  # Importing YouTube class
import yt_dlp
import whisper
from yt_transcript_extractor import extract_captions, audio_to_text, summarize_text, create_markdown_files, check_video_processed, mark_video_processed
import warnings
import subprocess

# warnings.filterwarnings("ignore", category=FutureWarning)
# warnings.filterwarnings("ignore", category=UserWarning)

# Load environment variables from .env file
load_dotenv()

def create_output_folder(video_id):
    today_date = datetime.now().date().isoformat()
    folder_name = f"{video_id}_{today_date}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def check_audio_exists(temp_audio_path):
    """Check if the audio file or its WAV version exists"""
    wav_path = f"{temp_audio_path}.wav"
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

def export_transcript(youtube_link, output_folder=None):
    """
    Exports the transcript of a YouTube video to a text file with automatic language detection.
    Returns the path to the saved transcript file.
    """
    try:
        # this is the object that contains the video information
        video = YouTube(youtube_link)
        video_id = video.video_id
        detected_lang = None
        
        # Create output folder if not provided
        if not output_folder:
            output_folder = f"transcripts_{datetime.now().strftime('%Y%m%d')}"
            os.makedirs(output_folder, exist_ok=True)
        
        # Try getting captions first
        transcript = extract_captions(youtube_link)
        
        # If no captions available, use whisper with language detection
        if transcript is None:
            print("No captions found. Converting audio to text with language detection...")
            temp_audio_path = f'{output_folder}/temp_audio.wav'
            
            # Check if audio file already exists
            if check_audio_exists(temp_audio_path):
                print("Using existing audio file...")
            else:
                print("Downloading audio file...")
                download_audio(youtube_link, temp_audio_path)
            
            # Use whisper model with auto language detection 
            # device="cpu" is used to avoid the warning about fp16 being deprecated
            model = whisper.load_model("base", device="cpu")
            # fp16=False is used to avoid the warning about fp16 being deprecated
            result = model.transcribe(f"{temp_audio_path}", fp16=False)

            transcript = result["text"]
            detected_lang = result["language"]
            print(f"Detected language: {detected_lang}")
            
        
        # Save transcript to file
        output_file = os.path.join(output_folder, f'{video_id}_transcript.txt')
        print(f"Saving transcript to: {output_file}")
        with open(output_file, 'w+', encoding='utf-8') as f:
            f.write(transcript)
        
        return output_file
    
    except Exception as e:
        raise Exception(f"Error exporting transcript: {str(e)}")

def check_ffmpeg_installed():
    """Check if FFmpeg is installed and accessible"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False

def show_ffmpeg_instructions():
    """Show FFmpeg installation instructions"""
    message = """FFmpeg is not installed or not found in system PATH. Please follow these steps:

1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract the downloaded file
3. Rename the extracted folder to 'ffmpeg'
4. Move the folder to C:\ drive
5. Add C:\\ffmpeg\\bin to your system PATH
6. Restart your terminal/command prompt

For detailed instructions, visit: https://windowsloop.com/install-ffmpeg-windows-10/"""
    messagebox.showerror("FFmpeg Not Found", message)

def process_video(export_only=False):
    """Process YouTube video for transcript and optional summary"""
    if not check_ffmpeg_installed():
        show_ffmpeg_instructions()
        return
        
    youtube_link = entry.get()
    if not youtube_link:
        messagebox.showerror("Input Error", "Please enter a YouTube link.")
        return

    try:
        # Handle export-only mode
        if export_only:
            output_file = export_transcript(youtube_link)
            messagebox.showinfo("Success", f"Transcript exported successfully to:\n{output_file}")
            return

        # Process video for both transcript and summary
        video = YouTube(youtube_link)
        video_id = video.video_id
        output_folder = create_output_folder(video_id)

        # Try getting captions first
        full_text = extract_captions(youtube_link)
        
        # If no captions, use whisper
        if full_text is None:
            try:
                print("No captions found. Attempting to download audio and convert to text...")
                temp_audio_path = os.path.join(output_folder, 'temp_audio.wav')
                
                # Check if audio file already exists
                if check_audio_exists(temp_audio_path):
                    print("Using existing audio file...")
                else:
                    print("Downloading audio file...")
                    download_audio(youtube_link, temp_audio_path)
                
                # Convert audio to text using whisper
                model = whisper.load_model("base", device="cpu")
                result = model.transcribe(f"{temp_audio_path}", fp16=False)
                full_text = result["text"]
                detected_lang = result["language"]
                print(f"Detected language: {detected_lang}")
                
            except Exception as e:
                messagebox.showerror("Audio Processing Error", f"Error processing audio: {str(e)}")
                return

        # Process the text
        if full_text:
            try:
                # Generate summary
                summary = summarize_text(full_text)
                
                # Create output files
                create_markdown_files(video_id, full_text, summary)
                mark_video_processed(video_id)
                
                messagebox.showinfo("Success", 
                    f"Processing completed successfully!\n\n"
                    f"Video ID: {video_id}\n"
                    f"Output folder: {output_folder}")
            except Exception as e:
                messagebox.showerror("Processing Error", f"Error during text processing: {str(e)}")
        else:
            messagebox.showerror("Error", "Could not extract text from the video.")
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process video: {str(e)}")

# Create the main application window
root = tk.Tk()
root.title("YouTube Transcript Extractor")

# Create and place the input field and button
entry = tk.Entry(root, width=50)
entry.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button_process = tk.Button(button_frame, text="Generate Transcript & Summary", 
                          command=lambda: process_video(False))
button_process.pack(side=tk.LEFT, padx=5)

button_export = tk.Button(button_frame, text="Export Transcript Only", 
                         command=lambda: process_video(True))
button_export.pack(side=tk.LEFT, padx=5)

# Start the application
root.mainloop()
