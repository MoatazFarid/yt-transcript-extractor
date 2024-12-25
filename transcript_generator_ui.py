import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
from yt_transcript_extractor import (
    process_video_transcript, summarize_text, create_markdown_files, 
    mark_video_processed, check_ffmpeg_installed
)
from video_transcriber import VideoTranscriber

class TranscriptGeneratorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Transcript Generator")
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True)
        
        # YouTube tab
        youtube_frame = ttk.Frame(notebook)
        notebook.add(youtube_frame, text='YouTube Video')
        
        # Local video tab
        local_frame = ttk.Frame(notebook)
        notebook.add(local_frame, text='Local Video')
        
        # Setup YouTube tab
        self.setup_youtube_tab(youtube_frame)
        
        # Setup Local video tab
        self.setup_local_tab(local_frame)
    
    def setup_youtube_tab(self, parent):
        # YouTube URL entry
        self.yt_entry = tk.Entry(parent, width=50)
        self.yt_entry.pack(pady=20)
        
        # YouTube buttons
        button_frame = tk.Frame(parent)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Generate Transcript & Summary", 
                 command=lambda: self.process_youtube(False)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Export Transcript Only", 
                 command=lambda: self.process_youtube(True)).pack(side=tk.LEFT, padx=5)
    
    def setup_local_tab(self, parent):
        # File path display
        self.file_path_var = tk.StringVar()
        tk.Label(parent, textvariable=self.file_path_var, wraplength=400).pack(pady=10)
        
        # Browse button
        tk.Button(parent, text="Browse Video File", 
                 command=self.browse_file).pack(pady=10)
        
        # Process button
        tk.Button(parent, text="Generate Transcript", 
                 command=self.process_local_video).pack(pady=10)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def process_youtube(self, export_only=False):
        if not check_ffmpeg_installed():
            self.show_ffmpeg_instructions()
            return
            
        youtube_link = self.yt_entry.get()
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
    
    def process_local_video(self):
        video_path = self.file_path_var.get()
        if not video_path:
            messagebox.showerror("Input Error", "Please select a video file.")
            return
        
        try:
            transcriber = VideoTranscriber()
            transcript_path = transcriber.process_video(video_path)
            
            messagebox.showinfo("Success", 
                f"Video processed successfully!\n\n"
                f"Transcript saved to: {transcript_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process video: {str(e)}")
    
    def show_ffmpeg_instructions(self):
        message = """FFmpeg is not installed or not found in system PATH. Please follow these steps:

1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract the downloaded file
3. Rename the extracted folder to 'ffmpeg'
4. Move the folder to C:\ drive
5. Add C:\\ffmpeg\\bin to your system PATH
6. Restart your terminal/command prompt

For detailed instructions, visit: https://windowsloop.com/install-ffmpeg-windows-10/"""
        messagebox.showerror("FFmpeg Not Found", message)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TranscriptGeneratorUI()
    app.run() 