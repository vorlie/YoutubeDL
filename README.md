# IMPORTANT!!
If your antivirus is gonna complain about the .exe, you can ignore it! It's false positive I tried everything I could to make it not complain! 
If you are sceptical, read the code..
- 3/69 [VirusTotal result](https://www.virustotal.com/gui/file/33c355e4989ab3164d1bfca6c576fa95e9f8f6c0e80d5e7a606138df9c49f20e/detection)

# Requirements
- Windows 10+

# Dependencies
- yt-dlp
- ffmpeg/ffprobe

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
![https://i.vorlie.pl/r/YoutubeDL_297067489.png](hhttps://i.vorlie.pl/r/YoutubeDL_297067489.png)
