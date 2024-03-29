import tkinter.messagebox as messagebox
from os import path as ospath
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
from threading import Thread
from subprocess import run
from yt_dlp import YoutubeDL
from requests import get, RequestException
from webbrowser import open

ASSETS_PATH = "./assets"
dependencies_path = "./binaries" 
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
save_directory = ospath.expanduser("~\\Downloads\\")
selected_directory = ""
current_version = "v2.1.3" 
github_repository = "vorlie/YoutubeDL"  
supported_sites = ["https://youtube.com/","https://youtu.be/","https://soundcloud.com/","https://music.youtube.com/","https://www.youtube.com/","https://www.soundcloud.com/"]

def check_for_updates():
    try:
        api_url = f"https://api.github.com/repos/{github_repository}/releases/latest"
        response = get(api_url)
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            if latest_version > current_version:
                release_url = response.json()["html_url"]
                download_url = response.json()["assets"][0]["browser_download_url"]
                up = Toplevel()
                up.title("Update Available")
                up.geometry("300x150")
                up.configure(bg = "#000000")
                up.resizable(False, False)
                up.iconbitmap("icon.ico")
                Label(up, text=f"Current version: {current_version}\nUpdate available: {latest_version}", bg = "#000000", fg = "#FFFFFF", anchor="w").pack()
                Button(up, text="Whats new", command=lambda: open(release_url), bg = "#000000", fg = "#FFFFFF", anchor="w").pack()
                Button(up, text="Download", command=lambda: open(download_url), bg = "#000000", fg = "#FFFFFF", anchor="w").pack()
                Button(up, text="Close", command=up.destroy, bg="#000000", fg="#FFFFFF", anchor="w").pack()
            else:
                pass
        else:
            messagebox.showerror("Error", "Failed to check for updates.")
    except RequestException:
        messagebox.showerror("Error", "Failed to check for updates.")

def select_directory():
    global selected_directory
    directory = filedialog.askdirectory(initialdir=selected_directory)
    selected_directory = directory.replace("/", "\\")
    messagebox.showinfo("Directory Selected", "Directory selected: " + selected_directory)

def on_startup():
    update_check = Thread(target=check_for_updates,)
    update_check.start()
def fetch_video_info():
    video_url = link_entry.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        window.config(cursor="")
        return
    ydl_opts = {}
    if video_url.startswith("https://soundcloud.com"):
        try:
            with YoutubeDL(ydl_opts) as ydl:
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
    elif video_url.startswith("https://www.youtube.com") or video_url.startswith("https://youtu.be") or video_url.startswith("https://music.youtube.com") or video_url.startswith("https://youtube.com"):
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title = info.get('title', None) 
                likes = info.get('like_count', None) 
                views = info.get('view_count', None) 
                uploader = info.get('uploader', None) 
                duration = info.get('duration', None) 
                length_minutes = duration // 60 
                length_seconds = duration % 60 
                length_formatted = f"{length_minutes}:{length_seconds:02d}" 
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
    else:
        messagebox.showinfo("Warning", "Invalid URL. Only youtube/soundcloud URLs are supported.")
        window.config(cursor="")
        return

def download_video(video_url):
    directory = selected_directory or save_directory
    if directory:
        try:
            run([f'{dependencies_path}/yt-dlp.exe', '-P', directory, video_url])
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
            run([f'{dependencies_path}/yt-dlp.exe', '-P', directory, '--ffmpeg-location', dependencies_path, '--extract-audio', '--audio-format', 'mp3', video_url])
            messagebox.showinfo("Download Complete", "Audio download finished! Saved to " + directory)
        except Exception as e:
            print("Failed to download audio:", e)
        finally:
            window.config(cursor="")
    else:
        return None

window = Tk()
window.iconbitmap("./icon.ico")
window.title(f"YoutubeDL {current_version}")
window.geometry("850x505")
window.configure(bg = "#000000")
canvas = Canvas(window,bg = "#000000",height = 505,width = 850,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
header_asset = PhotoImage(file=relative_to_assets("image_1.png"))
header = canvas.create_image(424.0,61.0,image=header_asset)
canvas.create_text(325.0,35.0,anchor="nw",text="YoutubeDL",fill="#FFFFFF",font=("Montserrat Bold", 36 * -1))

user_area_bg_asset = PhotoImage(file=relative_to_assets("image_2.png"))
user_area_bg = canvas.create_image(424.0,306.0,image=user_area_bg_asset)

info_bg_asset = PhotoImage(file=relative_to_assets("image_5.png"))
info_bg = canvas.create_image(297.0,305.0,image=info_bg_asset)

link_entry_bg_asset = PhotoImage(file=relative_to_assets("image_4.png"))
link_entry_bg = canvas.create_image(297.0,171.0,image=link_entry_bg_asset)
link_entry_fg_asset = PhotoImage(file=relative_to_assets("image_7.png"))
link_entry_fg = canvas.create_image(313.0,171.0,image=link_entry_fg_asset)
link_entry = Entry(bd=0,bg="#5856D6",fg="#000716",highlightthickness=0)
link_entry.place(x=101.0,y=160.0,width=412.0,height=21.0)

pen_img_asset = PhotoImage(file=relative_to_assets("image_8.png"))
pen_img = canvas.create_image(77.0,171.0,image=pen_img_asset)

sl_fld_btn_asset = PhotoImage(file=relative_to_assets("button_1.png"))
sl_fld_btn = Button(image=sl_fld_btn_asset,borderwidth=0,highlightthickness=0,command=select_directory,relief="flat",cursor="hand2")
sl_fld_btn.place(x=585.0,y=349.0,width=207.0,height=48.0)

btn_bg_1_asset = PhotoImage(file=relative_to_assets("image_10.png"))
btn_bg_1 = canvas.create_image(689.0,372.0,image=btn_bg_1_asset)

def start_audio_download():
    video_url = link_entry.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube/soundcloud URL provided")
        return
    if not any(site in video_url for site in supported_sites):
        messagebox.showinfo("Warning", "Invalid URL. Only youtube/soundcloud URLs are supported.")
        return
    window.config(cursor="wait")
    download_thread = Thread(target=download_audio, args=(video_url,))
    download_thread.start()

dl_aud_btn_asset = PhotoImage(file=relative_to_assets("button_2.png"))
dl_aud_btn = Button(image=dl_aud_btn_asset,borderwidth=0,highlightthickness=0,command=start_audio_download,relief="flat",cursor="hand2")
dl_aud_btn.place(x=586.0,y=282.0,width=204.0,height=48.0)

btn_bg_2_asset = PhotoImage(file=relative_to_assets("image_11.png"))
btn_bg_2 = canvas.create_image(689.0,305.0,image=btn_bg_2_asset)

def start_video_download():
    video_url = link_entry.get()
    if not video_url:
        messagebox.showinfo("Warning","No youtube URL provided")
        return
    if not any(site in video_url for site in supported_sites):
        messagebox.showinfo("Warning", "Invalid URL. Only youtube/soundcloud URLs are supported.")
        return
    window.config(cursor="wait")
    download_thread = Thread(target=download_video, args=(video_url,))
    download_thread.start()

dl_vid_btn_asset = PhotoImage(file=relative_to_assets("button_3.png"))
dl_vid_btn = Button(image=dl_vid_btn_asset,borderwidth=0,highlightthickness=0,command=start_video_download,relief="flat",cursor="hand2")    
dl_vid_btn.place(x=586.0,y=214.0,width=204.0,height=48.0)

btn_bg_3_asset = PhotoImage(file=relative_to_assets("image_12.png"))
btn_bg_3 = canvas.create_image(689.0,238.0,image=btn_bg_3_asset)

btn_bg_4_asset = PhotoImage(file=relative_to_assets("image_13.png"))
btn_bg_4 = canvas.create_image(689.0,171.0,image=btn_bg_4_asset)

canvas.create_text(61.0,221.0,anchor="nw",text="Information:",fill="#FFFFFF",font=("Montserrat Bold", 24 * -1))
video_info = canvas.create_text(61.0,257.0,anchor="nw",text="!",fill="#FFFFFF",font=("Montserrat", 20 * -1))
title_text = canvas.create_text(61.0,425.0,anchor="nw",text=f"!",fill="#FFFFFF",font=("Montserrat", 20 * -1))

def start_fetching_info():
    window.config(cursor="wait")
    info_thread = Thread(target=fetch_video_info)
    info_thread.start()

fetch_info_asset = PhotoImage(file=relative_to_assets("button_5.png"))
fetch_info_btn = Button(image=fetch_info_asset,borderwidth=0,highlightthickness=0,command=start_fetching_info,relief="flat",cursor="hand2")
fetch_info_btn.place(x=586.0,y=148.0,width=204.0,height=48.0)

logo_asset = PhotoImage(file=relative_to_assets("image_14.png"))
logo = canvas.create_image(78.0,62.0,image=logo_asset)

canvas.create_text(125.0,35.0,anchor="nw",text="Vorlie",fill="#FFFFFF",font=("Montserrat Bold", 36 * -1))

title_bg_asset = PhotoImage(file=relative_to_assets("image_15.png"))
title_bg = canvas.create_image(425.0,439.0,image=title_bg_asset)

on_startup()
window.resizable(False, False)
window.mainloop()