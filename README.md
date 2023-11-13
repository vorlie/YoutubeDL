# Requirements
- Windows 10+
- Python 3.12 (Optional)
 - scdl `pip install scdl` (Optional)

> scdl is required only when you want to download songs from soundcloud, if you don't want then you don't need to install it!

# Dependencies
- yt-dlp
- ffmpeg/ffprobe
- scdl (optional)

## Build it yourself
Use [Pyinstaller](https://pypi.org/project/pyinstaller/)
Check the [.spec file](https://github.com/vorlie/YoutubeDL/blob/main/spec-file-example-for-windows.spec) and specify the paths for the required datas. 
Once you do, run `pyinstaller name-of-the-spec-file.spec`

These will append the required files to the .exe
```
datas=[
    ('PATH-TO-THIS-FOLDER\\assets', 'assets'),
    ('PATH-TO-THIS-ICON\\icon.ico', '.'),
    ('PATH-TO-THIS-FOLDER\\dependencies', '.')
]
```

## Gallery
![https://cx.tixte.co/r/preview-ytdl.png](https://cx.tixte.co/r/preview-ytdl.png)
