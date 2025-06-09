import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ftplib import FTP
from datetime import datetime


# Configuration
WATCH_FOLDER = "your_local_folder"
FTP_HOST = "ftp.your_server.com"
FTP_USER = "ftp_username"
FTP_PASS = "ftp_password"
FTP_REMOTE_BASE = "/"
BATCH_INTERVAL = 1  # seconds


class FTPUploader:
    
    def __init__(self, host, user, passwd, remote_base):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.remote_base = remote_base
        self.saves = 0

    def upload(self, local_file, relative_path):
        # Get current date/time formatted as desired
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with FTP(self.host) as ftp:
                ftp.set_pasv(True)
                ftp.login(self.user, self.passwd)
                remote_dir = os.path.join(self.remote_base, os.path.dirname(relative_path)).replace('\\', '/')
                filename = os.path.basename(local_file)
                ftp.cwd(remote_dir)
                with open(local_file, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                # Print with timestamp
                print(f"{current_time} - Uploaded {local_file} to {remote_dir}/{filename}")
                self.saves += 1
                # Clear terminal every 12 uploads
                if self.saves % 12 == 0:
                    os.system('clear')  # or 'cls' on Windows
        except Exception as e:
            print(f"Failed to upload {local_file}: {e}")

class BatchHandler(FileSystemEventHandler):
    def __init__(self, uploader, base_folder):
        self.uploader = uploader
        self.base_folder = base_folder
        self.changed_files = set()
        self.lock = threading.Lock()
        self.timer = None
        self.saves = 0

    def on_modified(self, event):
        if not event.is_directory:
            self._add_event(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._add_event(event.src_path)

    def _add_event(self, file_path):
        filename = os.path.basename(file_path)
        if filename.endswith('.kate-swp'):
            return
        with self.lock:
            self.changed_files.add(file_path)
            # Reset timer each time a new change occurs
            if self.timer:
                self.timer.cancel()
            self.timer = threading.Timer(BATCH_INTERVAL, self.process_batch)
            self.timer.start()

    def process_batch(self):
        with self.lock:
            files_to_upload = list(self.changed_files)
            self.changed_files.clear()
        for file_path in files_to_upload:
            relative_path = os.path.relpath(file_path, self.base_folder)
            self.uploader.upload(file_path, relative_path)
        self.timer = None

if __name__ == "__main__":
    uploader = FTPUploader(FTP_HOST, FTP_USER, FTP_PASS, FTP_REMOTE_BASE)
    event_handler = BatchHandler(uploader, WATCH_FOLDER)
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=True)

    print(f"Monitoring {WATCH_FOLDER} and subfolders for changes...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
