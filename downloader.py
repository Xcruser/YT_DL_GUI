import yt_dlp
import os
import sys

class Downloader:
    def __init__(self, output_path="downloads"):
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def _get_ffmpeg_location(self):
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        return None

    def get_video_info(self, url):
        """Fetches video information without downloading."""
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get('title', 'Unknown Title'),
                    "thumbnail": info.get('thumbnail', None),
                    "duration": info.get('duration', 0),
                    "uploader": info.get('uploader', 'Unknown Uploader')
                }
        except Exception as e:
            print(f"Error fetching info: {e}")
            return None

    def download_video(self, url, progress_callback=None, output_path=None):
        """Downloads the best available video."""
        path = output_path if output_path else self.output_path
        if not os.path.exists(path):
            os.makedirs(path)
            
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: self._progress_hook(d, progress_callback)],
            'noplaylist': True,
            'ffmpeg_location': self._get_ffmpeg_location(),
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True, "Download complete!"
        except Exception as e:
            return False, str(e)

    def download_audio(self, url, format='mp3', progress_callback=None, output_path=None):
        """Downloads and extracts audio in the specified format."""
        path = output_path if output_path else self.output_path
        if not os.path.exists(path):
            os.makedirs(path)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192',
            }],
            'progress_hooks': [lambda d: self._progress_hook(d, progress_callback)],
            'noplaylist': True,
            'ffmpeg_location': self._get_ffmpeg_location(),
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True, "Download complete!"
        except Exception as e:
            return False, str(e)

    def _progress_hook(self, d, callback):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%', '')
                progress = float(p) / 100
                if callback:
                    callback(progress, "Downloading...")
            except:
                pass
        elif d['status'] == 'finished':
            if callback:
                callback(1.0, "Processing...")
