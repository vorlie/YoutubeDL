# Requirements
- MacOS 11.7.10 and newer.
- scdl
- ffmpeg
> If scdl is not installed, install it using (pip3 install scdl).

> If ffmpeg is not installed, visit [this page](https://evermeet.cx/ffmpeg/) and download the latest package and extract it to /usr/local/bin/

# Important!
Refer to the scdl instructions [https://github.com/flyingrub/scdl/wiki/Installation-Instruction](https://github.com/flyingrub/scdl/wiki/Installation-Instruction)
to make soundcloud downloader working

Config [source](https://github.com/flyingrub/scdl/blob/master/scdl/scdl.cfg):
```cfg
[scdl]
client_id = 
auth_token =
path = .
name_format = {title}
playlist_name_format = {playlist[title]}_{title}
```


## Features
- Paste youtube/soundcloud link
- Select video or audio (mp4/mp3)
- Select folder (Default: **MacOS:** `/Users/~/Downloads`)
- Video info viewer
- And of course download it
  
# Libraries used to make this possible
- [PyTube](https://pypi.org/project/pytube/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

## Build it yourself
Use [Pyinstaller](https://pypi.org/project/pyinstaller/)


## Gallery

[![1](https://cx.tixte.co/r/youtubedl-macos.png)](https://cx.tixte.co/r/youtubedl-macos.png)
