from pytube import YouTube
import os
import sys
import tkinter.messagebox as messagebox
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
import threading
import subprocess
import ffmpeg
import yt_dlp
import requests
import webbrowser

ASSETS_PATH = Path(sys._MEIPASS) / "assets" 
#ASSETS_PATH = "assets"

dependencies_path = Path(sys._MEIPASS)
#dependencies_path = "dependencies" 

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

save_directory = os.path.expanduser("~\\Downloads\\")
selected_directory = ""

current_version = "v2.1.0" 
github_repository = "vorlie/YoutubeDL"  

def check_for_updates():
    try:
        api_url = f"https://api.github.com/repos/{github_repository}/releases/latest"
        response = requests.get(api_url)
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            if latest_version != current_version:
                release_url = response.json()["html_url"]
                download_url = response.json()["assets"][0]["browser_download_url"]
                up = Toplevel()
                up.title("Update Available")
                up.geometry("300x150")
                up.configure(bg = "#000000")
                up.resizable(False, False)
                up.iconbitmap("icon.ico")
                Label(up, text=f"Current version: {current_version}\nUpdate available: {latest_version}", bg = "#000000", fg = "#FFFFFF", anchor="w").pack()
                Button(up, text="Check out the update", command=lambda: webbrowser.open(release_url), bg = "#000000", fg = "#FFFFFF", anchor="w").pack()
                Button(up, text="Download new version", command=lambda: webbrowser.open(download_url), bg = "#000000", fg = "#FFFFFF", anchor="w").pack()
                Button(up, text="Close", command=up.destroy, bg="#000000", fg="#FFFFFF", anchor="w").pack()
            else:
                pass
        else:
            messagebox.showerror("Error", "Failed to check for updates.")
    except requests.RequestException:
        messagebox.showerror("Error", "Failed to check for updates.")

def select_directory():
    global selected_directory
    directory = filedialog.askdirectory(initialdir=selected_directory)
    selected_directory = directory.replace("/", "\\")
    messagebox.showinfo("Directory Selected", "Directory selected: " + selected_directory)

def on_startup():
    update_check = threading.Thread(target=check_for_updates,)
    update_check.start()

window = Tk()
window.iconbitmap(str(Path(sys._MEIPASS) / "icon.ico"))
#window.iconbitmap("icon.ico")
window.title("YoutubeDL")
window.geometry("850x505")
window.configure(bg = "#000000")

def download_video(video_url):
    directory = selected_directory or save_directory
    if directory:
        try:
            subprocess.run([f'{dependencies_path}/yt-dlp.exe', '-P', directory, video_url])
            messagebox.showinfo("Download Complete", "Video download finished! Saved to " + directory)
        except Exception as e:
            print("Failed to download video:", e)
        finally:
            window.config(cursor="")
    else:
        return None

def download_audio(video_url):
    directory = selected_directory or save_directory
    if directory:
        try:
            subprocess.run([f'{dependencies_path}/yt-dlp.exe', '-P', directory, '--ffmpeg-location', dependencies_path, '--extract-audio', '--audio-format', 'mp3', video_url])
            messagebox.showinfo("Download Complete", "Audio download finished! Saved to " + directory)
        except Exception as e:
            print("Failed to download audio:", e)
        finally:
            window.config(cursor="")
    else:
        return None

canvas = Canvas(
    window,
    bg = "#000000",
    height = 505,
    width = 850,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    424.0,
    61.0,
    image=image_image_1
)

canvas.create_text(
    325.0,
    35.0,
    anchor="nw",
    text="YoutubeDL",
    fill="#FFFFFF",
    font=("Montserrat Bold", 36 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    424.0,
    306.0,
    image=image_image_2
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    297.0,
    171.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    297.0,
    305.0,
    image=image_image_5
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    313.0,
    171.0,
    image=image_image_7
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    307.0,
    171.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#5856D6",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=101.0,
    y=160.0,
    width=412.0,
    height=21.0
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    77.0,
    171.0,
    image=image_image_8
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=select_directory,
    relief="flat",
    cursor="hand2"
)
button_1.place(
    x=585.0,
    y=349.0,
    width=207.0,
    height=48.0
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    689.0,
    372.0,
    image=image_image_10
)

def start_audio_download():
    video_url = entry_1.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        return
    window.config(cursor="wait")
    download_thread = threading.Thread(target=download_audio, args=(video_url,))
    download_thread.start()

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=start_audio_download,
    relief="flat",
    cursor="hand2"
)
button_2.place(
    x=586.0,
    y=282.0,
    width=204.0,
    height=48.0
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    689.0,
    305.0,
    image=image_image_11
)
def start_video_download():
    video_url = entry_1.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        return
    window.config(cursor="wait")
    download_thread = threading.Thread(target=download_video, args=(video_url,))
    download_thread.start()

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=start_video_download,
    relief="flat",
    cursor="hand2"
)    
button_3.place(
    x=586.0,
    y=214.0,
    width=204.0,
    height=48.0
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    689.0,
    238.0,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    689.0,
    171.0,
    image=image_image_13
)

canvas.create_text(
    61.0,
    221.0,
    anchor="nw",
    text="Information:",
    fill="#FFFFFF",
    font=("Montserrat Bold", 24 * -1)
)

video_info = canvas.create_text(
    61.0,
    257.0,
    anchor="nw",
    text="!",
    fill="#FFFFFF",
    font=("Montserrat", 20 * -1)
)

title_text = canvas.create_text(
    61.0,
    425.0,
    anchor="nw",
    text=f"!",
    fill="#FFFFFF",
    font=("Montserrat", 20 * -1)
)

def fetch_video_info():
    video_url = entry_1.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        window.config(cursor="")
        return
    ydl_opts = {}
    if video_url.startswith("https://soundcloud.com"):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                title = info_dict.get('title')
                uploader = info_dict.get('uploader')
                repost_count = info_dict.get('repost_count')
                like_count = info_dict.get('like_count')
                genre = info_dict.get('genre')

                duration_seconds = info_dict.get('duration')
                duration_minutes, duration_seconds = divmod(duration_seconds, 60)
                duration = f"{int(duration_minutes)}:{int(duration_seconds):02d}"
                canvas.itemconfigure(video_info, text=f"Author: {uploader}\nDuration: {duration}\nReposts: {repost_count}\nLikes: {like_count}\nGenre: {genre}")
                max_chars = 64

                def truncate_title(title):
                    if len(title) > max_chars:
                        truncated_title = title[:max_chars-3] + "..."
                    else:
                        truncated_title = title
                    return truncated_title

                canvas.itemconfigure(title_text, text=f"Title: {truncate_title(title)}")
        except Exception as e:
            print(f"Error fetching video info: {e}")
            return
        finally:
            window.config(cursor="")
    else:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False) # Extract the video information
                title = info.get('title', None) # Get the video title
                likes = info.get('like_count', None) # Get the number of likes
                views = info.get('view_count', None) # Get the number of views
                uploader = info.get('uploader', None) # Get the uploader
                duration = info.get('duration', None) # Get the duration
                length_minutes = duration // 60 # Get the duration in minutes
                length_seconds = duration % 60 # Get the duration in seconds
                length_formatted = f"{length_minutes}:{length_seconds:02d}" # Format the duration

                canvas.itemconfigure(video_info, text=f"Uploader: {uploader}\nDuration: {length_formatted}\nViews: {views}\nLikes: {likes}")
                max_chars = 64

                def truncate_title(title):
                    if len(title) > max_chars:
                        truncated_title = title[:max_chars-3] + "..."
                    else:
                        truncated_title = title
                    return truncated_title

                canvas.itemconfigure(title_text, text=f"Title: {truncate_title(title)}")
        except Exception as e:
            print(f"Error fetching video info: {e}")
            return
        finally:
            window.config(cursor="")
def start_fetching_info():
    window.config(cursor="wait")
    info_thread = threading.Thread(target=fetch_video_info)
    info_thread.start()

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=start_fetching_info,
    relief="flat",
    cursor="hand2"
)
button_5.place(
    x=586.0,
    y=148.0,
    width=204.0,
    height=48.0
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    78.0,
    62.0,
    image=image_image_14
)

canvas.create_text(
    125.0,
    35.0,
    anchor="nw",
    text="Vorlie",
    fill="#FFFFFF",
    font=("Montserrat Bold", 36 * -1)
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    425.0,
    439.0,
    image=image_image_15
)

on_startup()
window.resizable(False, False)
window.mainloop()