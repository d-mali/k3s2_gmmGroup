import tkinter as tk
from tkinter import messagebox
import os
import time
import soundfile as sf
import numpy as np
import simpleaudio as sa

def ensure_directories():
    base_dir = 'tmp'
    audio_dir = os.path.join(base_dir, 'audio')
    text_dir = os.path.join(base_dir, 'text')
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)
    return base_dir, audio_dir, text_dir

def generate_audio_from_text(text, audio_path, text_path):
    with open(text_path, "w") as text_file:
        text_file.write(text)
    
    sample_rate = 22050
    duration = 5.0
    t = np.linspace(0., duration, int(sample_rate * duration))
    audio = 0.5 * np.sin(2. * np.pi * 220. * t)
    sf.write(audio_path, audio, sample_rate)
    print(f"Audio and text saved: {audio_path}, {text_path}")

def on_generate_button_click():
    input_text = text_entry.get("1.0", "end-1c")
    if not input_text.strip():
        messagebox.showwarning("Input Error", "Please enter some text.")
        return
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    audio_path = os.path.join(audio_dir, f"audio_{timestamp}.wav")
    text_path = os.path.join(text_dir, f"text_{timestamp}.txt")
    
    generate_audio_from_text(input_text, audio_path, text_path)
    list_generated_files()

def clear_files():
    for folder in [audio_dir, text_dir]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    list_generated_files()

def list_generated_files():
    for widget in file_frame.winfo_children():
        widget.destroy()

    audio_files = sorted(os.listdir(audio_dir))
    text_files = sorted(os.listdir(text_dir))
    
    for audio_file, text_file in zip(audio_files, text_files):
        if audio_file.endswith('.wav') and text_file.endswith('.txt'):
            file_label = tk.Label(file_frame, text=audio_file)
            file_label.pack(side=tk.TOP, fill=tk.X)
            play_button = tk.Button(file_frame, text="Play *not working*", command=lambda af=audio_file: play_audio(af))
            play_button.pack(side=tk.TOP)

def play_audio(audio_file):
    audio_path = os.path.join(audio_dir, audio_file)
    wave_obj = sa.WaveObject.from_wave_file(audio_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

base_dir, audio_dir, text_dir = ensure_directories()

root = tk.Tk()
root.title("Text-to-Speech Generator")

text_label = tk.Label(root, text="Enter text for speech generation:")
text_label.pack(pady=10)
text_entry = tk.Text(root, height=10, width=50)
text_entry.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

clear_button = tk.Button(button_frame, text="Clear Files", command=clear_files, bg="red", fg="white")
clear_button.pack(side=tk.LEFT, padx=10)

generate_button = tk.Button(button_frame, text="Generate Audio", command=on_generate_button_click, bg="green", fg="white")
generate_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Play *not working*", command="", bg="green", fg="white")
clear_button.pack(side=tk.LEFT, padx=10)

file_frame = tk.Frame(root)
file_frame.pack(pady=10)

list_generated_files()

root.mainloop()
