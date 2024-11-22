import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
from yt_transcript_extractor import (
    process_video_transcript, summarize_text, create_markdown_files, 
    mark_video_processed, check_ffmpeg_installed
)

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
    """Handle video processing from UI"""
    if not check_ffmpeg_installed():
        show_ffmpeg_instructions()
        return
        
    youtube_link = entry.get()
    if not youtube_link:
        messagebox.showerror("Input Error", "Please enter a YouTube link.")
        return

    try:
        # Process video and get transcript
        result = process_video_transcript(youtube_link)
        
        # Handle export-only mode
        if export_only:
            messagebox.showinfo("Success", 
                f"Transcript exported successfully to:\n{result['output_file']}")
            return

        # Generate summary and create files
        try:
            summary = summarize_text(result['transcript'])
            create_markdown_files(result['video_id'], result['transcript'], summary)
            mark_video_processed(result['video_id'])
            
            messagebox.showinfo("Success", 
                f"Processing completed successfully!\n\n"
                f"Video ID: {result['video_id']}\n"
                f"Transcript: {result['output_file']}")
                
        except Exception as e:
            messagebox.showerror("Processing Error", f"Error during text processing: {str(e)}")
            
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
