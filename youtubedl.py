import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from pytube import YouTube
import os
import webbrowser

SAVE_DIRECTORY = os.path.expanduser("~\Downloads")
selected_directory = ""

def open_link(event):
    webbrowser.open("https://vorlie.pl")

def select_directory():
    global selected_directory
    directory = filedialog.askdirectory(initialdir=selected_directory)
    selected_directory = directory
    return directory

def apply_icon(w):
    try:
        icon = tk.PhotoImage(data=icondata)
        w.iconphoto(True, icon)
    except Exception as e:
        print("Could not load icon due to:\n  ",e)

def download_video(video_url):
    video = YouTube(video_url)
    video = video.streams.get_highest_resolution()

    try:
        directory = selected_directory or SAVE_DIRECTORY
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
        directory = selected_directory or SAVE_DIRECTORY
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

def main():
    root = tk.Tk()
    apply_icon(root)
    root.configure(background='#222222')
    root.geometry('330x250')
    root.title("Youtube Downloader")
    root.resizable(False, False)  # Disable window resizing

    style = ttk.Style()
    style.configure("TRadiobutton", background='#222222', foreground='#FFFFFF', indicatorbackground='#616161')

    link_label = tk.Label(root, text="Paste your youtube link here:", fg='#FFFFFF', bg='#222222', anchor='w')
    link_label.pack(fill='none')

    link_entry = tk.Entry(root, width=50)
    link_entry.pack(fill='none')

    audio_var = tk.BooleanVar()
    audio_var.set(False)

    video_radio = ttk.Radiobutton(root, text="Video (.mp4)", variable=audio_var, value=False)
    video_radio.pack(fill='none')

    audio_radio = ttk.Radiobutton(root, text="Audio (.mp3)", variable=audio_var, value=True)
    audio_radio.pack(fill='none')

    folder_label = tk.Label(root, text=f"Default directory: {SAVE_DIRECTORY}", fg='#c8c8c8', bg='#222222', anchor='w')
    folder_label.pack(fill='none')

    blank_label = tk.Label(root, text=" ", fg='#FFFFFF', bg='#222222', anchor='w')
    blank_label.pack(fill='none')

    folder_button = tk.Button(root, text="Select Folder", command=select_directory, fg='#FFFFFF', bg='#333333', highlightbackground='#ff8181', width=15, cursor="hand2")
    folder_button.pack(fill='none')
    
    def download():
        video_url = link_entry.get()
        is_audio = audio_var.get()

        if not video_url:
            messagebox.showerror("Error", "Please provide a YouTube link")
            return

        if is_audio:
            file_path = download_audio(video_url)
        else:
            file_path = download_video(video_url)

        if file_path:
            messagebox.showinfo("Download Complete", f"File saved at: {os.path.abspath(file_path)}")

    download_button = tk.Button(root, text="Download", command=download, fg='#FFFFFF', bg='#333333', highlightcolor='#616161', width=15, cursor="hand2")
    download_button.pack(fill='none')
    
    blank_label = tk.Label(root, text=" ", fg='#FFFFFF', bg='#222222', anchor='w')
    blank_label.pack(fill='none')

    footer_label = tk.Label(root, text="Made by vorlie", fg='#616161', bg='#222222', anchor='w', cursor="hand2")
    footer_label.pack(fill='none')
    footer_label.bind("<Button-1>", open_link)

    root.mainloop()

icondata = '''
R0lGODlhQABAAIUAACMhIwAAAIw57iEhIe4lkq0y0M8rrzUmS0wkTEshN3s68Usqc7kuumojUJM0
1XIsjm4nbK0jbCEhIcAvwHE20I0iWVosh4slbSAgIBwcHCAgICAgICsrK64pkcknj5UqlNQjerov
wOEooW0yslwxpz4pY58wupcuqFYwmQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAEALAAAAABAAEAAQAj/AAMI
HEiwoMGDCBMqXBiAwwYAECNKnEixosWLFzdwKDgAo8UECRpUAEGgpMmTJUFUaADSY8UBBDtiTIAA
wYUOBnIaECFCpwEPFxo0uODBp1EPDRAkcAkA5kCZExFAKEC1qtWqHx5AWIBAIoIFEB58uEq2wAkE
B17GrHjggAUBcOPKnQvXwYgRDujqlUthQVqKTgVCZdq2sOHDiBMzhRh4oITFkCNflLBQwkPJmDFu
oIzwcWaKIEMv/TyRs2DINCugXM36ZIWWixsP9orgg9HbPiHUrAkB9+0ONTHKrojggYPjZak6KODA
Atq/bRFYWL48OfIHaAGvvdh2AQW4CvaK/98bXkDfthcbcyDNHvLGhBkGaGifWcOADAwPZpAwoL//
/wAGKOCA/UmAX34CYUDfghFhgNB8DEYIkQYckRaaSBVEoGEEFawUGmnDRRZSBK2VSEAELEkWoks1
XWDiiyV5UIFSsW1nEQIN4OSbT0HVNNSOBnygW1cerSjRAbUxoGQIEzTp5ARKRpkURDhGqeSTE4Rg
5QfBqfUUcQ8kd9UDXBFJ2wJhilkVdl6eRtEBC+Q1nlzNLWDnAtPNOdcDf01k5JFwfqfnoOKdZ9Gf
bHWHAgUUKODoo5BGKqkCFJDgF3rC2ShhhI0FMNum7HVKkIKgZuYggqimquqqrLbqagDxQf9Y6kX2
HcgQqbNGdmpnuZJmmqa9YtbpesGy956bFoqmLGwgArvYhRGQxBoIKH4orLMegdQAiTCaVO1okCE6
EwLcdotSBDSGi21FNDUgrbmrVavul9n62IGJHmjoAUo8eZuuS+JG1K6OQAYl1I87DslUwADURDCQ
BgzJG8QMXNBleutKxQDEOjGgG0gac2wAcGZqR29UCzCgJlVaKlkyAlGuXEAIuh2KbXEym6DVxRHx
9oAJMtdsMrIRIZnmyg6QmV3RXxkncwFsDu0pmMfNmZcDXBn21dVWC4BdnxGJi+QIhNZlgZ15lo01
2GGvCyfZZcc9lwWY+rkuAG1ZIKjchJ5Vx3bbJ1vUHQmNTmr44Y9aWnebUxPWVgl3Ri755JKXUNjC
dzueGGLNOlYse78GIOvnkVFYkEOkR6YRQrimjtGuCVnmOkWbrbofgbjnPqCBr/buu0EBAQA7
'''

if __name__ == '__main__':
    main()