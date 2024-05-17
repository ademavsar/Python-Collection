import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def select_video():
    global video_path
    video_path = filedialog.askopenfilename(title="Select video file", filetypes=[("MP4 files", "*.mp4")])

def select_subtitle():
    global subtitle_path
    subtitle_path = filedialog.askopenfilename(title="Select subtitle file", filetypes=[("Subtitle files", "*.srt")])

def embed_subtitles():
    if not video_path or not subtitle_path:
        return  # Eğer dosya yolları belirlenmemişse işlemi iptal et
    output_path = filedialog.asksaveasfilename(title="Save video as", defaultextension=".mp4")
    command = [
        "ffmpeg", "-i", video_path, "-i", subtitle_path,
        "-c", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", output_path
    ]
    subprocess.run(command, shell=True)

root = tk.Tk()
root.title("Subtitle Embedder")
root.geometry("300x400")

select_video_button = tk.Button(root, text="Select Video", command=select_video)
select_video_button.pack(pady=20)

select_subtitle_button = tk.Button(root, text="Select Subtitle", command=select_subtitle)
select_subtitle_button.pack(pady=20)

start_embedding_button = tk.Button(root, text="Start Embedding", command=embed_subtitles)
start_embedding_button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
