# YouTubeDL

## Overview

YouTubeDL is a graphical user interface for managing YouTube video and audio downloads using `yt-dlp`. It provides a simple and user-friendly way to fetch video information and download media files.

## Project Structure

The project directory contains:
- `module/`: Directory containing utility functions.
   - `utils.py`: Source code for utility functions.
- `resources/`: Directory containing images and other resources.
   - `loading.gif`: Loading animation GIF file.
- `.gitignore`: Git ignore rules.
- `main.py`: Source code for the GUI application.
- `config.json`: Configuration file for the application. 
   - The application will create it if it doesn't exist.
- `icon.ico`: Icon for the application.
- `LICENSE`: License information.
- `README.md`: This file.
- `requirements.txt`: List of Python dependencies.
- `YoutubeDL.spec`: PyInstaller spec file for the GUI application.

## Downloading the Executable

The compiled executable for Windows is not included in the repository. Instead, you can download it from the GitHub Releases page:

- **[Download YoutubeDL](https://github.com/vorlie/YoutubeDL/releases/download/v3.1/YoutubeDL-win64.zip)**

## YoutubeDL.exe (GUI)

### Features

- **Fetch Video Information:** Retrieve and display video details such as title, uploader, duration, and thumbnail.
- **Download Video and Audio:** Download videos or audio from supported YouTube URLs.
   - It should be always targetting the highest quality.
- **Custom Configuration:** Set paths for `yt-dlp` and `ffmpeg` binaries, and manage supported sites.
- **Loading Indicators:** Visual feedback with a loading animation during long operations.


### Installation

1. **Download the archive**:
    - [YouTubeDL-win64.zip](https://github.com/vorlie/YoutubeDL/releases/download/v3.1/YouTubeDL-win64.zip)

2. **Extract the archive**:
    - Extract the downloaded `YouTubeDL-win64.zip`.
    
3. **Run the Application**: 
    - Open the archive that you just extracted.
    - Double-click the extracted `.exe` file to start the application.

## Development

To contribute to the development or modify the application:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/vorlie/YoutubeDL.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd <path-to-project-directory>
    ```

3. **Install Dependencies**:

    Ensure you have Python and pip installed. Then install the required Python packages:

    ```bash
    pip install -r requirements.txt --ignore-requires-python
    ```

4. **Run the Application**:

    ```bash
    python main.py
    ```

5. **Build the Executable**:

    Use PyInstaller to bundle the application into a standalone executable.

    If you do not have PyInstaller installed:

    ```bash
    pip install pyinstaller==6.6.0
    ```

    Build the executable:

    ```bash
    pyinstaller YoutubeDL.spec
    ```

6. **Test the Executable**:

    The built executable will be located in the `dist/` directory. Test it to ensure it works as expected.

## Thanks

A special thanks to the following projects and contributors that made this tool possible:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: A powerful YouTube video downloader that is used for fetching video and audio content.
- **[FFmpeg](https://ffmpeg.org/download.html)**: A comprehensive multimedia framework used for handling audio, video, and other multimedia files and streams.
- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)**: A set of Python bindings for the Qt application framework, which provides the GUI capabilities for this application.
- **[qdarktheme](https://pypi.org/project/pyqtdarktheme/)**: A library for applying dark themes to PyQt5 applications, enhancing the visual appeal of the interface.

Your work and contributions are greatly appreciated!


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
