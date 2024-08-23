import sys, os, json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, 
    QWidget, QMessageBox, QHBoxLayout, QFrame, QMenuBar, 
    QAction, QDialog, QFormLayout, QDialogButtonBox, QCheckBox, QPlainTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from subprocess import run, DEVNULL
from yt_dlp import YoutubeDL
from module.utils import get_save_directory
import qdarktheme as qdt

class VideoInfoFetcher(QThread):
    info_fetched = pyqtSignal(dict)

    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url

    def run(self):
        ydl_opts = {}
        info = {}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.video_url, download=False)
        except Exception as e:
            info['error'] = str(e)
        self.info_fetched.emit(info)

DEFAULT_CONFIG = {
    "yt_dlp_path": "yt-dlp", 
    "ffmpeg_path": "ffmpeg", 
    "save_directory":  os.path.join(os.path.expanduser("~"), "Downloads"),
    "supported_sites": [
        "https://youtube.com/",
        "https://youtu.be/",
        "https://music.youtube.com/",
        "https://www.youtube.com/",
    ]
}

# Determine if the script is running as a compiled executable or as a script
if getattr(sys, 'frozen', False):
    # If the application is frozen (compiled with PyInstaller), this will be True
    base_path = sys._MEIPASS  # Use this for accessing bundled files, if any
    exe_dir = os.path.dirname(sys.executable)
    print(f"Running as a compiled executable: {exe_dir}")
else:
    # If running as a script, use the directory of the script
    exe_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Running as a script: {exe_dir}")

# Set CONFIG_FILE_PATH to the directory of the executable or script
CONFIG_FILE_PATH = os.path.join(exe_dir, "config.json")

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("License")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.license_text = QLabel(self)
        self.license_text.setWordWrap(True)
        layout.addWidget(self.license_text)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.load_license()

    def load_license(self):
        license_text = """
        MIT License

        Copyright (c) 2024 Charlie (vorlie)

        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """
        self.license_text.setText(license_text)


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = {}
        self.setWindowTitle("Configuration")
        self.setFixedSize(400, 300)
        self.initUI()
        self.load_config()

    def initUI(self):
        layout = QFormLayout()

        self.yt_dlp_path_input = QLineEdit(self)
        self.ffmpeg_path_input = QLineEdit(self)
        self.save_directory_input = QLineEdit(self)
        self.supported_sites_input = QPlainTextEdit(self)

        layout.addRow("yt-dlp Path:", self.yt_dlp_path_input)
        layout.addRow("FFmpeg Path:", self.ffmpeg_path_input)
        layout.addRow("Save Directory:", self.save_directory_input)
        layout.addRow("Supported Sites (one per line):", self.supported_sites_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def load_config(self):
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, "r") as file:
                self.config = json.load(file)
        else:
            self.config = DEFAULT_CONFIG

        self.yt_dlp_path_input.setText(self.config.get("yt_dlp_path", DEFAULT_CONFIG["yt_dlp_path"]))
        self.ffmpeg_path_input.setText(self.config.get("ffmpeg_path", DEFAULT_CONFIG["ffmpeg_path"]))
        self.save_directory_input.setText(self.config.get("save_directory", DEFAULT_CONFIG["save_directory"]))
        self.supported_sites_input.setPlainText("\n".join(self.config.get("supported_sites", DEFAULT_CONFIG["supported_sites"])))

    def get_config(self):
        return {
            "yt_dlp_path": self.yt_dlp_path_input.text(),
            "ffmpeg_path": self.ffmpeg_path_input.text(),
            "save_directory": self.save_directory_input.text(),
            "supported_sites": [line.strip() for line in self.supported_sites_input.toPlainText().splitlines() if line.strip()],
        }

    def save_config(self):
        config = self.get_config()
        
        # Normalize paths based on the operating system
        config["yt_dlp_path"] = os.path.normpath(config["yt_dlp_path"])
        config["ffmpeg_path"] = os.path.normpath(config["ffmpeg_path"])
        config["save_directory"] = os.path.normpath(config["save_directory"])

        # Ensure the directory for the config file exists
        config_dir = os.path.dirname(CONFIG_FILE_PATH)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        
        # Save the config to the file
        try:
            with open(CONFIG_FILE_PATH, "w", encoding="utf8") as file:
                json.dump(config, file, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")
            

class DownloadWorker(QThread):
    download_complete = pyqtSignal(str)
    download_error = pyqtSignal(str)

    def __init__(self, video_url, download_type, yt_dlp_path, ffmpeg_path, directory):
        super().__init__()
        self.video_url = video_url
        self.download_type = download_type
        self.yt_dlp_path = yt_dlp_path
        self.ffmpeg_path = ffmpeg_path
        self.directory = directory

    def run(self):
        try:
            # Check if ffmpeg is in PATH if it's set as "ffmpeg" in config
            if self.ffmpeg_path == "ffmpeg" and not self.is_ffmpeg_in_path():
                raise Exception("FFmpeg not found in PATH. Please add it to PATH or set a custom path in the configuration.")

            if self.download_type == "video":
                run([self.yt_dlp_path, '-P', self.directory, self.video_url])
            elif self.download_type == "audio":
                if self.ffmpeg_path == "ffmpeg":
                    run([self.yt_dlp_path, '-P', self.directory, '--extract-audio', '--audio-format', 'mp3', self.video_url])
                else:
                    run([self.yt_dlp_path, '-P', self.directory, '--ffmpeg-location', self.ffmpeg_path, '--extract-audio', '--audio-format', 'mp3', self.video_url])
            self.download_complete.emit("Download finished! Saved to " + self.directory)
        except Exception as e:
            self.download_error.emit(str(e))

    def is_ffmpeg_in_path(self):
        """Check if ffmpeg is available in the system's PATH by running 'ffmpeg -version'."""
        try:
            result = run(['ffmpeg', '-version'], stdout=DEVNULL, stderr=DEVNULL)
            return result.returncode == 0
        except FileNotFoundError:
            return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.setWindowTitle("YoutubeDL")
        self.setFixedSize(400, 500)
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))

        self.load_config()
        self.initUI()

    def initUI(self):
        self.url_label = QLabel('Enter video URL:', self)
        self.url_input = QLineEdit(self)
        self.url_input.setFixedWidth(371)

        self.info_button = QPushButton('Fetch Info', self)
        self.info_button.clicked.connect(self.fetch_info)

        self.download_video_button = QPushButton('Download Video', self)
        self.download_video_button.clicked.connect(self.download_video)

        self.download_audio_button = QPushButton('Download Audio', self)
        self.download_audio_button.clicked.connect(self.download_audio)

        self.select_directory_button = QPushButton('Select Directory', self)
        self.select_directory_button.clicked.connect(self.select_directory)

        self.thumbnail_label = QLabel(self)
        self.thumbnail_label.setFixedSize(352, 198)
        self.thumbnail_label.setScaledContents(True)
        self.info_display = QLabel('Video info will be shown here', self)
        self.info_display.setWordWrap(True)

        self.loading_gif = QLabel(self)
        self.loading_gif.setFixedSize(20, 20)
        self.loading_movie = QMovie(os.path.join(os.path.dirname(__file__), "loading.gif"))
        self.loading_gif.setMovie(self.loading_movie)
        self.loading_gif.hide()

        self.loading_message = QLabel("Downloading, please wait...", self)
        self.loading_message.setStyleSheet("font-weight: bold; color: #ff6a82;")
        self.loading_message.hide()

        loading_layout = QHBoxLayout()
        loading_layout.addWidget(self.loading_gif)
        loading_layout.addWidget(self.loading_message)
        

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.url_label)
        left_layout.addWidget(self.url_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.info_button)
        buttons_layout.addWidget(self.download_video_button)
        buttons_layout.addWidget(self.download_audio_button)
        left_layout.addLayout(buttons_layout)

        left_layout.addWidget(self.select_directory_button)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #2E2E2E; border: 1px solid #ff6a82; border-radius: 5px;")
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.thumbnail_label)
        info_layout.addWidget(self.info_display)
        info_frame.setLayout(info_layout)

        left_layout.addWidget(info_frame)
        left_layout.addLayout(loading_layout)  
        left_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = self.menu_bar.addMenu("File")

        config_action = QAction("Configuration", self)
        config_action.triggered.connect(self.open_config_dialog)
        file_menu.addAction(config_action)
        
        license_action = QAction("License", self)
        license_action.triggered.connect(self.open_license_dialog)
        file_menu.addAction(license_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_config(self):
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, "r") as file:
                self.config = json.load(file)
        else:
            self.config = DEFAULT_CONFIG

        self.yt_dlp_path = self.config.get("yt_dlp_path", DEFAULT_CONFIG["yt_dlp_path"])
        self.ffmpeg_path = self.config.get("ffmpeg_path", DEFAULT_CONFIG["ffmpeg_path"])
        self.save_directory = self.config.get("save_directory", DEFAULT_CONFIG["save_directory"])
        self.supported_sites = self.config.get("supported_sites", DEFAULT_CONFIG["supported_sites"])

    def fetch_info(self):
        video_url = self.url_input.text()
        if not video_url:
            QMessageBox.warning(self, "Warning", "No URL provided")
            return

        self.info_button.setEnabled(False)
        self.loading_gif.show()
        self.loading_message.setText("Fetching information, please wait...")
        self.loading_message.show()
        self.loading_movie.start()


        self.info_fetcher = VideoInfoFetcher(video_url)
        self.info_fetcher.info_fetched.connect(self.display_info)
        self.info_fetcher.finished.connect(self.on_info_fetched)
        self.info_fetcher.start()

    def display_info(self, info):
        if 'error' in info:
            QMessageBox.critical(self, "Error", info['error'])
            return

        title = info.get('title', 'N/A')
        uploader = info.get('uploader', 'N/A')
        duration = info.get('duration', 0)
        duration_minutes, duration_seconds = divmod(duration, 60)
        duration = f"{duration_minutes}:{duration_seconds:02d}"

        thumbnail_url = info.get('thumbnail', '')

        if thumbnail_url:
            try:
                from urllib.request import urlopen
                image_data = urlopen(thumbnail_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.thumbnail_label.setPixmap(pixmap)
            except Exception as e:
                self.thumbnail_label.setText("Thumbnail not available")

        info_text = f"Title: {title}\nUploader: {uploader}\nDuration: {duration}"
        self.info_display.setText(info_text)


    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.save_directory = directory
            QMessageBox.information(self, "Directory Selected", "Directory selected: " + directory)

    def download_video(self):
        self.start_download("video")

    def download_audio(self):
        self.start_download("audio")

    def start_download(self, download_type):
        video_url = self.url_input.text()
        if not video_url:
            QMessageBox.warning(self, "Warning", "No URL provided")
            return

        if not any(site in video_url for site in self.supported_sites):
            QMessageBox.warning(self, "Warning", "Invalid URL. Only supported sites are allowed.")
            return

        directory = getattr(self, 'save_directory', get_save_directory())
        yt_dlp_path = self.yt_dlp_path
        ffmpeg_path = self.ffmpeg_path

        self.info_button.setEnabled(False)
        self.download_video_button.setEnabled(False)
        self.download_audio_button.setEnabled(False)
        self.loading_gif.show()
        self.loading_message.setText("Downloading, please wait...")
        self.loading_message.show()
        self.loading_movie.start()
        
        self.download_worker = DownloadWorker(video_url, download_type, yt_dlp_path, ffmpeg_path, directory)
        self.download_worker.download_complete.connect(self.on_download_complete)
        self.download_worker.download_error.connect(self.on_download_error)
        self.download_worker.start()

    def on_download_complete(self, message):
        self.reset_ui()
        QMessageBox.information(self, "Download Complete", message)

    def on_download_error(self, error_message):
        self.reset_ui()
        QMessageBox.critical(self, "Error", "Failed to download: " + error_message)

    def on_info_fetched(self):
        self.reset_ui()

    def reset_ui(self):
        self.info_button.setEnabled(True)
        self.download_video_button.setEnabled(True)
        self.download_audio_button.setEnabled(True)
        self.loading_gif.hide()
        self.loading_message.hide()
        self.loading_movie.stop()

    def open_license_dialog(self):
        dialog = LicenseDialog(self)
        dialog.exec_()

    def open_config_dialog(self):
        dialog = ConfigDialog(self)
        dialog.load_config()
        if dialog.exec_():
            dialog.save_config()
            self.load_config()

if __name__ == "__main__":
    qdt.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdt.setup_theme(custom_colors={"primary": "#ff6a82"})
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
