from pytube import YouTube
import os
import sys
import tkinter.messagebox as messagebox
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess

ASSETS_PATH = Path(sys._MEIPASS) / "assets"
#ASSETS_PATH = "assets"
save_directory = os.path.expanduser("~\\Downloads")
selected_directory = ""

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x330")
        self.title("YoutubeDL v2.0.3 - Windows")
        self.resizable(True, True)
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        def select_directory():
            global selected_directory
            directory = filedialog.askdirectory(initialdir=selected_directory)
            selected_directory = directory.replace("/", "\\")
            self.folder_label3.configure(text=f"Selected: {selected_directory}")


        self.folder_label = ctk.CTkLabel(self, text="YoutubeDL by vorlie", font=('Arial Black', 20))
        self.folder_label.grid(row=1,column=0,padx=0, pady=10)

        self.folder_label2 = ctk.CTkLabel(self, text="Video Info:", font=('Arial Black', 20))
        self.folder_label2.grid(row=1,column=2,padx=0, pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Paste your youtube link here", width=270)
        self.entry.grid(row=2,column=0,padx=20, pady=5)

        def audio_callback(choice):
            print("optionmenu dropdown clicked:", choice)

        self.audio_var = ctk.StringVar(value="Audio (.mp3)")
        self.audio = ctk.CTkOptionMenu(self, values=["Video 720p (.mp4)", "Audio (.mp3)"], command=audio_callback, variable=self.audio_var, width=270)
        self.audio.grid(row=3, column=0,pady=5)

        def fetch_video_info():
            video_url = self.entry.get()
            if not video_url:
                print("No video URL provided")
                return

            yt = YouTube(video_url)
            try:
                title = yt.title
                uploader = yt.author
                views = yt.views
                publish_date = yt.publish_date
                length_seconds = yt.length
                length_minutes = length_seconds // 60
                length_seconds = length_seconds % 60
                length_formatted = f"{length_minutes}:{length_seconds:02d}"
            except Exception as e:
                print(f"Error fetching video info: {e}")
                return
            

            self.video_title.configure(text=f"Title: {title}\nUploader: {uploader}")
            self.video_stats.configure(text=f"Duration: {length_formatted}\nViews: {views} \nPublished: {publish_date}")

        self.fetch_button = ctk.CTkButton(self, text="Fetch Video Info", command=fetch_video_info, width=270)
        self.fetch_button.grid(row=4, column=0, pady=5)

        self.button = ctk.CTkButton(self, text="Select Folder", command=select_directory, width=270)
        self.button.grid(row=5, column=0,pady=5)

        def download():
            video_url = self.entry.get()
            is_audio = self.audio_var.get()

            if not video_url:
                messagebox.showerror("Error", "Please provide a YouTube link")
                return

            if is_audio == "Audio (.mp3)":
                file_path = download_audio(video_url)
            else:
                file_path = download_video(video_url)

            if file_path:
                messagebox.showinfo("Download Complete", f"File saved at: {os.path.abspath(file_path)}")

        self.button = ctk.CTkButton(self, text="Download", command=download, width=270)
        self.button.grid(row=6, column=0, pady=5)

        self.folder_label3 = ctk.CTkLabel(self, text=f"Default: {save_directory}")
        self.folder_label3.grid(row=7,column=0)

        self.video_title = ctk.CTkLabel(self, text="No title/uploader")
        self.video_title.grid(row=2,column=2)

        self.video_stats = ctk.CTkLabel(self, text="No stats")
        self.video_stats.grid(row=3,column=2)

app = App()
app.mainloop()