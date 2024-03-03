# IMPORTANT!!
If your antivirus is gonna complain about the .exe, you can ignore it! It's false positive I tried everything I could to make it not complain! 

It's not signed because I am not spending hundreds of money on this. 

And since it was compiled using Pyinstaller, I can't do anything about it.

If you are skeptical, read the code..

# Requirements
- Windows 10+ or Ubuntu 22.04 based OS

## Build it yourself
Use [Pyinstaller](https://pypi.org/project/pyinstaller/)
Check the [.spec file](https://github.com/vorlie/YoutubeDL/blob/main/spec-file-example-for-windows.spec). 
Once you do, run `pyinstaller name-of-the-spec-file.spec` 
> Make sure you have the `./binaries`, `./assets` and `./icon.ico` in the same path as the .exe or .py file. Otherwise it will not open.
