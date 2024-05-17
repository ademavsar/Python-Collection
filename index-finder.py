import tkinter as tk
from tkinter import filedialog
import re
import os
import pyperclip
import json

# Pencere konumunu kaydetmek için kullanılan dosya
WINDOW_POSITION_FILE = "window_position.json"

def load_window_position():
    try:
        with open(WINDOW_POSITION_FILE, "r") as file:
            position = json.load(file)
            return position.get("x"), position.get("y")
    except FileNotFoundError:
        return None, None

def save_window_position(x, y):
    with open(WINDOW_POSITION_FILE, "w") as file:
        json.dump({"x": x, "y": y}, file)

def on_close():
    x = pencere.winfo_x()
    y = pencere.winfo_y()
    save_window_position(x, y)
    pencere.destroy()

def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mkv *.mp4 *.webm")])
    if file_path:
        video_path.set(file_path)
        display_video_path.set(os.path.basename(file_path))
        print(f"Video dosyası seçildi: {os.path.basename(file_path)}")

def select_subtitle():
    file_path = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])
    if file_path:
        subtitle_path.set(file_path)
        display_subtitle_path.set(os.path.basename(file_path))
        print(f"Altyazı dosyası seçildi: {os.path.basename(file_path)}")

def start_processing():
    lines = input_screen.get("1.0", "end-1c").strip().split('\n')
    all_indices = []
    not_found_words = []
    if video_path.get() and subtitle_path.get() and lines:
        try:
            with open(subtitle_path.get(), "r", encoding="utf-8") as file:
                content = file.read()
            blocks = re.split(r'\n\n+', content)
            for line in lines:
                parts = line.split()
                word = ' '.join(part for part in parts if not part.startswith('+') and not part.startswith('-'))
                offsets = [int(x) for x in parts if x.startswith('+') or x.startswith('-') and x.lstrip('+-').isdigit()]
                indices = set()
                found = False
                for block in blocks:
                    block_lines = block.split('\n')
                    try:
                        index = int(block_lines[0])
                    except ValueError:
                        continue
                    text = ' '.join(block_lines[2:])
                    if word.lower() in text.lower():
                        found = True
                        indices.add(index)
                        for offset in offsets:
                            new_index = index + offset
                            if new_index > 0:
                                indices.add(new_index)
                if found:
                    if offsets:
                        min_index = min(indices)
                        max_index = max(indices)
                        all_indices.append(f"{min_index} {max_index}")
                    else:
                        all_indices.append(' '.join(map(str, indices)))
                else:
                    not_found_words.append(word)
            if all_indices:
                joined_indices = ', '.join(all_indices)
                command = f"./script.sh {display_video_path.get()} {display_subtitle_path.get()} {joined_indices}"
                output_screen.delete(1.0, tk.END)
                output_screen.insert(tk.END, command)

                command2 = f'./script.sh "{display_video_path.get()}" "{display_subtitle_path.get()}" {joined_indices}'
                output_screen2.delete(1.0, tk.END)
                output_screen2.insert(tk.END, command2)
            else:
                output_screen.delete(1.0, tk.END)
                output_screen.insert(tk.END, "Kelime bulunamadı.")
                output_screen2.delete(1.0, tk.END)
                output_screen2.insert(tk.END, "Kelime bulunamadı.")
            if not_found_words:
                not_found_screen.delete(1.0, tk.END)
                not_found_screen.insert(tk.END, '\n'.join(not_found_words))
            else:
                not_found_screen.delete(1.0, tk.END)
                not_found_screen.insert(tk.END, "Tüm kelimeler bulundu.")
        except Exception as e:
            output_screen.delete(1.0, tk.END)
            output_screen.insert(tk.END, f"Hata: {str(e)}")
            output_screen2.delete(1.0, tk.END)
            output_screen2.insert(tk.END, f"Hata: {str(e)}")

def copy_to_clipboard(output_widget):
    text = output_widget.get("1.0", "end-1c").strip()
    pyperclip.copy(text)
    print("Metin panoya kopyalandı.")

# Pencere oluşturma ve tema ayarları
pencere = tk.Tk()
pencere.title("Video ve Altyazı İşleme GUI")
pencere.geometry("800x1000")
x, y = load_window_position()
if x is not None and y is not None:
    pencere.geometry(f"+{x}+{y}")

# Siyah tema
pencere.configure(bg="#1c1c1c")

video_path = tk.StringVar()
subtitle_path = tk.StringVar()
display_video_path = tk.StringVar()
display_subtitle_path = tk.StringVar()

btn_style = {"bg": "#444444", "fg": "white", "activebackground": "#666666", "activeforeground": "white"}
text_style = {"bg": "#2b2b2b", "fg": "white", "insertbackground": "white"}

frame = tk.Frame(pencere, bg="#1c1c1c")
frame.pack(pady=10)
tk.Button(frame, text="Video Seç", command=select_video, **btn_style).pack(side="left", padx=5)
tk.Button(frame, text="Altyazı Seç", command=select_subtitle, **btn_style).pack(side="left", padx=5)
tk.Button(frame, text="Başlat", command=start_processing, **btn_style).pack(side="left", padx=5)

input_screen = tk.Text(pencere, height=10, width=70, **text_style)
input_screen.pack(pady=10)
tk.Button(pencere, text="Panoya Kopyala", command=lambda: copy_to_clipboard(input_screen), **btn_style).pack(pady=10)

output_screen = tk.Text(pencere, height=5, width=70, **text_style)
output_screen.pack(pady=10)
tk.Button(pencere, text="Panoya Kopyala", command=lambda: copy_to_clipboard(output_screen), **btn_style).pack(pady=10)

output_screen2 = tk.Text(pencere, height=5, width=70, **text_style)
output_screen2.pack(pady=10)
tk.Button(pencere, text="Panoya Kopyala", command=lambda: copy_to_clipboard(output_screen2), **btn_style).pack(pady=10)

not_found_screen = tk.Text(pencere, height=5, width=70, **text_style)
not_found_screen.pack(pady=10)

pencere.protocol("WM_DELETE_WINDOW", on_close)

pencere.mainloop()
