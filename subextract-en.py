import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def select_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(title="Video Dosyalarını Seçin",
                                                  filetypes=[("Video Dosyaları", "*.mp4 *.mkv *.avi")])
    files_label.config(text=f"Seçilen Dosyalar: {len(selected_files)}")

def extract_subtitles():
    if not selected_files:
        messagebox.showwarning("Uyarı", "Lütfen önce dosya(lar) seçin!")
        return
    
    for file in selected_files:
        output_file = file.rsplit('.', 1)[0] + '.srt'
        subprocess.run(['ffmpeg', '-i', file, '-map', '0:s:1', '-c:s', 'srt', output_file], check=True)
    
    messagebox.showinfo("Başarılı", "Altyazılar başarıyla çıkarıldı.")

# GUI Başlat
root = tk.Tk()
root.title("Altyazı Çıkarıcı")
root.geometry("300x150")

selected_files = []

# Seçim butonu
select_button = tk.Button(root, text="Dosya Seç", command=select_files)
select_button.pack(pady=10)

# Seçilen dosyaları göster
files_label = tk.Label(root, text="Seçilen Dosyalar: 0")
files_label.pack(pady=5)

# Başlatma butonu
start_button = tk.Button(root, text="Altyazı Çıkar", command=extract_subtitles)
start_button.pack(pady=10)

root.mainloop()