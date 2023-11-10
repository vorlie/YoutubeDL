from pytube import YouTube
import os
import sys
import tkinter.messagebox as messagebox
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import subprocess

ASSETS_PATH = Path(sys._MEIPASS) / "assets" / "frame0"

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

window = Tk()
window.iconbitmap(str(Path(sys._MEIPASS) / "downloadicon.ico"))
window.title("YoutubeDL v2.0.5 - Windows")
window.geometry("850x800")
window.configure(bg = "#1C1C1E")


canvas = Canvas(
    window,
    bg = "#1C1C1E",
    height = 800,
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
    41.0,
    anchor="nw",
    text="YoutubeDL",
    fill="#FFFFFF",
    font=("Helvetica Bold", 36 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    424.0,
    306.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    422.0,
    642.0,
    image=image_image_3
)
output = canvas.create_text(
    54.0,
    567.0,
    anchor="nw",
    text="Output\n",
    fill="#FFFFFF",
    font=("Helvetica", 20 * -1)
)
def update_output_text(text):
    canvas.itemconfigure(output, text=text)
    
def download_soundcloud_track(track_url):
    try:
        result = subprocess.run(['scdl', '-l', track_url], capture_output=True, text=True)
        if result.returncode == 0:
            output_text = result.stderr.strip()
            update_output_text(output_text)  # Call the update_output_text function
            return output_text
        else:
            error_message = result.stderr.strip()
            update_output_text(error_message)  # Call the update_output_text function
            return None
    except FileNotFoundError:
        update_output_text("scdl command not found. Install it with 'pip3 install scdl'")  # Call the update_output_text function
        return None

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

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    424.0,
    658.0,
    image=image_image_6
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

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    689.0,
    439.0,
    image=image_image_9
)

def download_soundcloud_track_get():
    track_url = entry_1.get()
    if not track_url:
        messagebox.showinfo("Warning","No soundcloud URL provided")
        return
    download_soundcloud_track(track_url)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=download_soundcloud_track_get,
    relief="flat"
)
button_1.place(
    x=585.0,
    y=416.0,
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
def download_audio_get():
    video_url = entry_1.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        return
    file_path = download_audio(video_url)

    if file_path:
        messagebox.showinfo("Download Complete", f"Audio saved at: {os.path.abspath(file_path)}")

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=download_audio_get,
    relief="flat"
)
button_2.place(
    x=585.0,
    y=349.0,
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
def download_video_get():
    video_url = entry_1.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        return
    file_path = download_video(video_url)

    if file_path:
        messagebox.showinfo("Download Complete", f"Video saved at: {os.path.abspath(file_path)}")

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=download_video_get,
    relief="flat"
)
button_3.place(
    x=586.0,
    y=282.0,
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
    text="Video Information:",
    fill="#FFFFFF",
    font=("Helvetica Bold", 24 * -1)
)

video_info = canvas.create_text(
    61.0,
    265.0,
    anchor="nw",
    text="Title:\nUploader:\nDuration:\nViews:",
    fill="#FFFFFF",
    font=("Helvetica", 20 * -1)
)
def fetch_video_info():
    video_url = entry_1.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
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

    canvas.itemconfigure(video_info, text=f"Title: {title}\nUploader: {uploader}\nDuration: {length_formatted}\nViews: {views}\nPublished: {publish_date}")

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=fetch_video_info,
    relief="flat"
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
    41.0,
    anchor="nw",
    text="Vorlie",
    fill="#FFFFFF",
    font=("Helvetica Bold", 36 * -1)
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    297.0,
    439.0,
    image=image_image_15
)

dir_text = canvas.create_text(
    61.0,
    425.0,
    anchor="nw",
    text=f"Dir: {save_directory}",
    fill="#FFFFFF",
    font=("Helvetica", 20 * -1)
)
def select_directory():
    global selected_directory
    directory = filedialog.askdirectory(initialdir=selected_directory)
    selected_directory = directory
    canvas.itemconfigure(dir_text, text=f"Dir: {selected_directory}")

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=select_directory,
    relief="flat"
)
button_4.place(
    x=586.0,
    y=214.0,
    width=206.0,
    height=48.0
)
canvas.create_text(
    43.0,
    517.0,
    anchor="nw",
    text="Console Output:",
    fill="#FFFFFF",
    font=("Helvetica Bold", 20 * -1)
)


window.resizable(False, False)
window.mainloop()
