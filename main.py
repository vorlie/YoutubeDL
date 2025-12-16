import sys, os, json, re, traceback, subprocess
from urllib.parse import urlparse
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QMessageBox, QHBoxLayout, QFrame, QMenuBar,
    QAction, QDialog, QFormLayout, QDialogButtonBox, QPlainTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QMovie
from yt_dlp import YoutubeDL
from module.utils import get_save_directory
import qdarktheme as qdt

# ----------------------------- DEFAULT CONFIG -----------------------------
DEFAULT_CONFIG = {
    "ffmpeg_path": "ffmpeg",
    "save_directory": os.path.join(os.path.expanduser("~"), "Downloads"),
    "filename_template": "%(title)s [%(id)s].%(ext)s",
    "supported_sites": [
        "youtube.com",
        "youtu.be",
        "music.youtube.com",
        "instagram.com",
    ],
}

# ----------------------------- PATH / CONFIG FILE --------------------------
if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
else:
    exe_dir = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE_PATH = os.path.join(exe_dir, "config.json")

# ----------------------------- HELPERS ------------------------------------

def is_supported_url(url, supported_sites):
    """Robust domain-aware URL check; permissive fallback to let yt-dlp try."""
    try:
        if not url:
            return False
        if not url.lower().startswith(('http://', 'https://')):
            url_to_parse = 'https://' + url
        else:
            url_to_parse = url
        parsed = urlparse(url_to_parse)
        netloc = (parsed.netloc or "").lower().strip()
        if not netloc:
            return url_to_parse.lower().startswith(('http://', 'https://'))
        for s in supported_sites:
            if not s:
                continue
            s = s.strip().lower()
            try:
                s_netloc = urlparse(s).netloc.lower() or s
            except Exception:
                s_netloc = s
            if s_netloc and s_netloc in netloc:
                return True
        return url_to_parse.lower().startswith(('http://', 'https://'))
    except Exception:
        return True

def ffmpeg_available(ffmpeg_path):
    """Return True if ffmpeg executable is available either at given path or on PATH."""
    try:
        if ffmpeg_path and ffmpeg_path.strip() and ffmpeg_path.lower() != 'ffmpeg':
            fp = ffmpeg_path.strip()
            if os.path.isfile(fp) and os.access(fp, os.X_OK):
                return True
            if os.path.isdir(fp):
                candidate = os.path.join(fp, 'ffmpeg')
                if sys.platform.startswith('win'):
                    candidate += '.exe'
                if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                    return True
                return False
            maybe_dir = os.path.dirname(fp)
            if maybe_dir and os.path.isdir(maybe_dir):
                candidate = os.path.join(maybe_dir, 'ffmpeg')
                if sys.platform.startswith('win'):
                    candidate += '.exe'
                if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                    return True
        from shutil import which
        return which('ffmpeg') is not None
    except Exception:
        return False

def ffprobe_available(ffmpeg_path):
    """Return True if ffprobe is available either via the ffmpeg_path or on PATH."""
    try:
        if ffmpeg_path and ffmpeg_path.strip() and ffmpeg_path.lower() != 'ffmpeg':
            fp = ffmpeg_path.strip()
            if os.path.isfile(fp):
                maybe_dir = os.path.dirname(fp)
                probe = os.path.join(maybe_dir, 'ffprobe')
                if sys.platform.startswith('win'):
                    probe += '.exe'
                if os.path.isfile(probe) and os.access(probe, os.X_OK):
                    return True
            if os.path.isdir(fp):
                probe = os.path.join(fp, 'ffprobe')
                if sys.platform.startswith('win'):
                    probe += '.exe'
                if os.path.isfile(probe) and os.access(probe, os.X_OK):
                    return True
        from shutil import which
        return which('ffprobe') is not None
    except Exception:
        return False

# ----------------------------- THREADS ------------------------------------
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


class DownloadWorker(QThread):
    download_complete = pyqtSignal(str)
    download_error = pyqtSignal(str)

    def __init__(self, video_url, ffmpeg_path, directory, filename_template, manual_filename, cookies_file, referer=None):
        super().__init__()
        self.video_url = video_url
        self.ffmpeg_path = ffmpeg_path
        self.directory = directory
        self.filename_template = filename_template
        self.manual_filename = manual_filename
        self.cookies_file = cookies_file
        self.referer = referer

    def run(self):
        try:
            # Compose filename/outtmpl
            filename = (self.manual_filename.strip() if self.manual_filename else self.filename_template)
            if self.manual_filename:
                filename = os.path.basename(filename)
                filename = re.sub(r'[<>:\"/\\|?*\x00-\x1f]', '_', filename)
                if '%(ext)s' not in filename and '%(ext)s' not in self.filename_template:
                    filename = filename + '.%(ext)s'
            outtmpl = os.path.join(self.directory, filename)

            # ALWAYS download merged best video + best audio into single file
            format_str = 'bestvideo+bestaudio/best'

            ydl_opts = {
                'outtmpl': outtmpl,
                'format': format_str,
                'noplaylist': True,
            }

            # Cookies handling
            if self.cookies_file:
                if os.path.exists(self.cookies_file):
                    ydl_opts['cookiefile'] = self.cookies_file
                else:
                    raise Exception(f"Cookies file not found: {self.cookies_file}")

            # Determine ffmpeg_location (directory) if user provided explicit path
            ffmpeg_location = None
            if self.ffmpeg_path and self.ffmpeg_path.strip() and self.ffmpeg_path.lower() != 'ffmpeg':
                if os.path.isfile(self.ffmpeg_path):
                    ffmpeg_location = os.path.dirname(self.ffmpeg_path)
                elif os.path.isdir(self.ffmpeg_path):
                    ffmpeg_location = self.ffmpeg_path
                else:
                    maybe_dir = os.path.dirname(self.ffmpeg_path)
                    if maybe_dir and os.path.isdir(maybe_dir):
                        ffmpeg_location = maybe_dir
            if ffmpeg_location:
                ydl_opts['ffmpeg_location'] = ffmpeg_location

            # Referer header for Instagram (if applicable)
            if 'instagram.com' in (self.video_url or '').lower():
                ydl_opts.setdefault('http_headers', {})
                ydl_opts['http_headers']['Referer'] = 'https://www.instagram.com/'

            # Small logger + progress hook
            class GuiLogger:
                def debug(self, msg): pass
                def info(self, msg): pass
                def warning(self, msg): pass
                def error(self, msg): pass

            def progress_hook(d):
                if d.get('status') == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate')
                    downloaded = d.get('downloaded_bytes', 0)

                    if total:
                        percent = downloaded / total * 100
                        print(f"\rDownloading: {percent:.2f}%  ({downloaded/1024/1024:.2f}MB / {total/1024/1024:.2f}MB)", end="")
                    else:
                        print(f"\rDownloading: {downloaded/1024/1024:.2f}MB", end="")

                elif d.get('status') == 'finished':
                    print("\nDownload finished, merging formats...")

                elif d.get('status') == 'error':
                    print("\nError occurred during download.")


            ydl_opts['logger'] = GuiLogger()
            ydl_opts['progress_hooks'] = [progress_hook]

            # Ensure ffmpeg/ffprobe exist for merging
            if not ffmpeg_available(self.ffmpeg_path):
                raise Exception("FFmpeg not found. A full FFmpeg build (with ffprobe) is required to merge audio and video.")
            if not ffprobe_available(self.ffmpeg_path):
                raise Exception("ffprobe (part of FFmpeg) not found. Required for postprocessing/merging.")

            # Download (yt-dlp will merge when both parts exist)
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.video_url, download=True)
            except Exception as e:
                tb = traceback.format_exc()
                dbg = "\n".join(debug_messages[-25:]) if debug_messages else "<no hook messages>"
                primary_err = f"{type(e).__name__}: {e}\n\nTraceback:\n{tb}\n\nLast hook messages:\n{dbg}"
                # Try a permissive retry with 'best'
                try:
                    ydl_opts_retry = dict(ydl_opts)
                    ydl_opts_retry['format'] = 'best'
                    with YoutubeDL(ydl_opts_retry) as ydl2:
                        info = ydl2.extract_info(self.video_url, download=True)
                except Exception as e2:
                    tb2 = traceback.format_exc()
                    dbg2 = "\n".join(debug_messages[-50:]) if debug_messages else "<no hook messages>"
                    full_err = (
                        f"Primary error:\n{primary_err}\n\n"
                        f"Retry error:\n{type(e2).__name__}: {e2}\n\nTraceback:\n{tb2}\n\n"
                        f"Collected hook messages:\n{dbg2}"
                    )
                    print(full_err, file=sys.stderr)
                    self.download_error.emit(full_err)
                    return

            # Resolve saved path
            saved_path = None
            try:
                if isinstance(info, dict):
                    rd = info.get('requested_downloads')
                    if rd and isinstance(rd, list) and len(rd) > 0:
                        first = rd[0]
                        if isinstance(first, dict):
                            saved_path = first.get('filepath')
                    if not saved_path:
                        saved_path = info.get('_filename') or info.get('filename')
                if not saved_path:
                    try:
                        with YoutubeDL({'outtmpl': outtmpl}) as ydl_tmp:
                            if isinstance(info, dict):
                                saved_path = ydl_tmp.prepare_filename(info)
                    except Exception:
                        pass
            except Exception:
                saved_path = None

            if saved_path and os.path.exists(saved_path):
                self.download_complete.emit(saved_path)
            else:
                self.download_complete.emit(f"Download finished. Saved to {self.directory}")

        except Exception as outer_e:
            tb_outer = traceback.format_exc()
            err_msg = f"{type(outer_e).__name__}: {outer_e}\n\nTraceback:\n{tb_outer}"
            print("DownloadWorker outer error:\n", err_msg, file=sys.stderr)
            self.download_error.emit(err_msg)

# ----------------------------- DIALOGS / HUB --------------------------
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

        Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction...
        """
        self.license_text.setText(license_text)

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = {}
        self.setWindowTitle("Configuration")
        self.setFixedSize(500, 350)
        self.initUI()
        self.load_config()

    def initUI(self):
        layout = QFormLayout()
        self.ffmpeg_path_input = QLineEdit(self)
        self.save_directory_input = QLineEdit(self)
        self.template_string_input = QLineEdit(self)
        self.supported_sites_input = QPlainTextEdit(self)
        self.cookies_file_input = QLineEdit(self)
        cookies_browse = QPushButton("Browse", self)
        cookies_browse.clicked.connect(self.browse_cookies)

        layout.addRow("FFmpeg Path:", self.ffmpeg_path_input)
        layout.addRow("Save Directory:", self.save_directory_input)
        layout.addRow("Filename Template:", self.template_string_input)
        layout.addRow("Supported Sites (one per line):", self.supported_sites_input)
        h = QHBoxLayout()
        h.addWidget(self.cookies_file_input)
        h.addWidget(cookies_browse)
        layout.addRow("Cookies File:", h)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def browse_cookies(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select cookies.txt file", os.path.expanduser("~"), "Text files (*.txt);;All files (*)")
        if file_path:
            self.cookies_file_input.setText(file_path)

    def load_config(self):
        if os.path.exists(CONFIG_FILE_PATH):
            try:
                with open(CONFIG_FILE_PATH, "r", encoding="utf8") as file:
                    self.config = json.load(file)
            except Exception:
                self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = DEFAULT_CONFIG.copy()

        self.ffmpeg_path_input.setText(self.config.get("ffmpeg_path", DEFAULT_CONFIG["ffmpeg_path"]))
        self.save_directory_input.setText(self.config.get("save_directory", DEFAULT_CONFIG["save_directory"]))
        self.template_string_input.setText(self.config.get("filename_template", DEFAULT_CONFIG.get("filename_template", '%(title)s [%(id)s].%(ext)s')))
        self.supported_sites_input.setPlainText("\n".join(self.config.get("supported_sites", DEFAULT_CONFIG["supported_sites"])))
        self.cookies_file_input.setText(self.config.get("cookies_file", ""))

    def get_config(self):
        return {
            "ffmpeg_path": self.ffmpeg_path_input.text(),
            "save_directory": self.save_directory_input.text(),
            "filename_template": self.template_string_input.text(),
            "supported_sites": [line.strip() for line in self.supported_sites_input.toPlainText().splitlines() if line.strip()],
            "cookies_file": self.cookies_file_input.text(),
        }

    def save_config(self):
        config = self.get_config()
        config["ffmpeg_path"] = os.path.normpath(config["ffmpeg_path"])
        config["save_directory"] = os.path.normpath(config["save_directory"])
        config_dir = os.path.dirname(CONFIG_FILE_PATH)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        try:
            with open(CONFIG_FILE_PATH, "w", encoding="utf8") as file:
                json.dump(config, file, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")

# ----------------------------- MAIN HUB ----------------------------------
class MainHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Downloader Hub")
        self.setFixedSize(480, 300)
        self.load_config()
        self.initUI()

    def load_config(self):
        if os.path.exists(CONFIG_FILE_PATH):
            try:
                with open(CONFIG_FILE_PATH, "r", encoding="utf8") as file:
                    self.config = json.load(file)
            except Exception:
                self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = DEFAULT_CONFIG.copy()
        self.ffmpeg_path = self.config.get("ffmpeg_path", DEFAULT_CONFIG["ffmpeg_path"])
        self.save_directory = self.config.get("save_directory", DEFAULT_CONFIG["save_directory"])
        self.supported_sites = self.config.get("supported_sites", DEFAULT_CONFIG["supported_sites"])
        self.filename_template = self.config.get("filename_template", DEFAULT_CONFIG.get("filename_template", '%(title)s [%(id)s].%(ext)s'))
        self.cookies_file = self.config.get("cookies_file", "")

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Paste URL to download (YouTube / Instagram / supported sites):")
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.filename_input = QLineEdit(self)
        self.filename_input.setPlaceholderText("Optional filename (without extension)")

        dir_btn = QPushButton("Select Save Directory", self)
        dir_btn.clicked.connect(self.select_directory)
        self.dir_label = QLabel(f"Save to: {self.save_directory}")

        self.download_button = QPushButton("Download", self)
        self.download_button.setStyleSheet("font-weight: bold; font-size: 14px; padding: 8px;")
        self.download_button.clicked.connect(self.on_download_clicked)

        top_menu = QMenuBar(self)
        file_menu = top_menu.addMenu("File")
        config_action = QAction("Configuration", self)
        config_action.triggered.connect(self.open_config_dialog)
        file_menu.addAction(config_action)
        license_action = QAction("License", self)
        license_action.triggered.connect(self.open_license_dialog)
        file_menu.addAction(license_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        layout.addWidget(label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.filename_input)
        layout.addWidget(dir_btn)
        layout.addWidget(self.dir_label)
        layout.addSpacing(10)
        layout.addWidget(self.download_button)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        self.setMenuBar(top_menu)
        self.setCentralWidget(container)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", self.save_directory)
        if directory:
            self.save_directory = directory
            self.dir_label.setText(f"Save to: {self.save_directory}")

    def on_download_clicked(self):
        video_url = self.url_input.text().strip()
        manual_filename = self.filename_input.text().strip()
        if not video_url:
            QMessageBox.warning(self, "Warning", "Please paste a URL to download.")
            return
        if not is_supported_url(video_url, self.supported_sites):
            # be permissive but warn
            choice = QMessageBox.question(self, "Unknown site", "URL seems outside supported sites. Try anyway?",
                                          QMessageBox.Yes | QMessageBox.No)
            if choice != QMessageBox.Yes:
                return

        # start worker
        self.download_button.setEnabled(False)
        self.download_button.setText("Downloading...")
        self.worker = DownloadWorker(
            video_url,
            self.ffmpeg_path,
            getattr(self, 'save_directory', get_save_directory()),
            self.filename_template,
            manual_filename,
            self.cookies_file
        )
        self.worker.download_complete.connect(self.download_finished)
        self.worker.download_error.connect(self.download_failed)
        self.worker.start()

    def download_finished(self, path_or_msg):
        self.download_button.setEnabled(True)
        self.download_button.setText("Download")
        if isinstance(path_or_msg, str) and os.path.exists(path_or_msg):
            reply = QMessageBox.information(self, "Download Complete", f"Saved to:\n{path_or_msg}\n\nOpen folder?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                folder = os.path.dirname(path_or_msg)
                if sys.platform.startswith('win'):
                    subprocess.Popen(f'explorer "{folder}"')
                elif sys.platform.startswith('darwin'):
                    subprocess.Popen(['open', folder])
                else:
                    subprocess.Popen(['xdg-open', folder])
        else:
            QMessageBox.information(self, "Download", path_or_msg)

    def download_failed(self, error_message):
        self.download_button.setEnabled(True)
        self.download_button.setText("Download")
        QMessageBox.critical(self, "Download Failed", error_message)

    def open_license_dialog(self):
        d = LicenseDialog(self)
        d.exec_()

    def open_config_dialog(self):
        dialog = ConfigDialog(self)
        dialog.load_config()
        if dialog.exec_():
            dialog.save_config()
            self.load_config()

# ----------------------------- APPLICATION ENTRY -------------------------
if __name__ == "__main__":
    try:
        if qdt is not None:
            qdt.enable_hi_dpi()
    except Exception:
        pass

    app = QApplication(sys.argv)
    try:
        if qdt is not None:
            qdt.setup_theme(custom_colors={"primary": "#ff6a82"})
    except Exception:
        pass

    hub = MainHub()
    hub.show()
    exec_fn = getattr(app, "exec_", app.exec)
    sys.exit(exec_fn())
