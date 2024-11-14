import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from dotenv import load_dotenv
from pytube import YouTube  # Importing YouTube class
import yt_dlp
import whisper
from yt_transcript_extractor import extract_captions, audio_to_text, summarize_text, create_markdown_files, check_video_processed, mark_video_processed

# Load environment variables from .env file
load_dotenv()

def create_output_folder(video_id):
    today_date = datetime.now().date().isoformat()
    folder_name = f"{video_id}_{today_date}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def process_video():
    youtube_link = entry.get()
    if not youtube_link:
        messagebox.showerror("Input Error", "Please enter a YouTube link.")
        return

    video_id = YouTube(youtube_link).video_id
    output_folder = create_output_folder(video_id)

    full_text = extract_captions(youtube_link)
    if full_text is None:
        try:
            print("Attempting to download audio and convert to text...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{output_folder}/audio.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',  # Keep as wav format
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_link])
            full_text = audio_to_text(f'{output_folder}/audio.wav')
        except Exception as e:
            messagebox.showerror("Download Error", f"Error downloading audio: {str(e)}")
            return

    if "Error" in full_text:
        messagebox.showerror("Transcription Error", full_text)
    else:
        summary = summarize_text(full_text)
        if "Error" in summary:
            messagebox.showerror("Summarization Error", summary)
        else:
            create_markdown_files(video_id, full_text, summary)
            mark_video_processed(video_id)
            messagebox.showinfo("Success", "Transcription and summarization completed successfully.")

# Create the main application window
root = tk.Tk()
root.title("YouTube Transcript Extractor")

# Create and place the input field and button
entry = tk.Entry(root, width=50)
entry.pack(pady=20)

button = tk.Button(root, text="Generate Transcript", command=process_video)
button.pack(pady=10)

# Start the application
root.mainloop()
