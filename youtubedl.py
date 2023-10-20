import tkinter.messagebox as messagebox
from tkinter import filedialog
import customtkinter as ctk
from pytube import YouTube
import os
import sys

save_directory = os.path.expanduser("~\Downloads")
selected_directory = ""

def download_video(video_url):
    video = YouTube(video_url)
    video = video.streams.get_highest_resolution()

    try:
        directory = selected_directory or save_directory
        if directory:
            file_path = video.download(directory)
        else:
            return None
    except:
        print("Failed to download video")
        return None

    print("Video was downloaded successfully")
    return file_path

def download_audio(video_url):
    video = YouTube(video_url)
    audio = video.streams.filter(only_audio=True).first()

    try:
        directory = selected_directory or save_directory
        if directory:
            file_path = audio.download(directory)
            # Change the file extension to mp3
            new_file_path = file_path[:-4] + ".mp3"
            os.rename(file_path, new_file_path)
        else:
            return None
    except:
        print("Failed to download audio")
        return None

    print("Audio was downloaded successfully")
    return new_file_path

def find_by_relative_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("310x250")
        self.title("YoutubeDL v2.0.0")
        self.iconbitmap("./icon.ico")
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("./theme.json")

        def select_directory():
            global selected_directory
            directory = filedialog.askdirectory(initialdir=selected_directory)
            selected_directory = directory.replace("/", "\\")
            self.folder_label.configure(text=f"Selected: {selected_directory}")

        self.folder_label = ctk.CTkLabel(self, text="YoutubeDL by vorlie", font=('Arial Black', 20))
        self.folder_label.grid(row=1,column=0,padx=0, pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Paste your youtube link here", width=270)
        self.entry.grid(row=2,column=0,padx=20, pady=5)

        self.folder_label = ctk.CTkLabel(self, text=f"Default: {save_directory}")
        self.folder_label.grid(row=6,column=0,padx=0)

        def audio_callback(choice):
            print("optionmenu dropdown clicked:", choice)

        self.audio_var = ctk.StringVar(value="Audio (.mp3)")
        self.audio = ctk.CTkOptionMenu(self, values=["Video 720p (.mp4)", "Audio (.mp3)"], command=audio_callback, variable=self.audio_var, width=270)
        self.audio.grid(row=3, column=0,pady=5)
        # Use CTkButton instead of tkinter Button
        self.button = ctk.CTkButton(self, text="Select Folder", command=select_directory, width=270)
        self.button.grid(row=4, column=0,pady=5)

        def download():
            video_url = self.entry.get()
            is_audio = self.audio_var.get()

            if not video_url:
                messagebox.showerror("Error", "Please provide a YouTube link")
                return

            if is_audio:
                file_path = download_audio(video_url)
            else:
                file_path = download_video(video_url)

            if file_path:
                messagebox.showinfo("Download Complete", f"File saved at: {os.path.abspath(file_path)}")


        self.button = ctk.CTkButton(self, text="Download", command=download, width=270)
        self.button.grid(row=5, column=0, pady=5)

app = App()
app.mainloop()