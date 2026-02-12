import yt_dlp
import os
import sys
import subprocess
import re

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

    def download_video(self, url, progress_callback=None, output_path=None, target_ext="mp4"):
        """Downloads the best available video in the specified extension."""
        path = output_path if output_path else self.output_path
        if not os.path.exists(path):
            os.makedirs(path)
            
        # Select format based on extension
        if target_ext == "mp4":
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else: # mkv
            format_str = 'bestvideo+bestaudio/best'

        ydl_opts = {
            'format': format_str,
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'progress_hooks': [lambda d: self._progress_hook(d, progress_callback)],
            'noplaylist': True,
            'ffmpeg_location': self._get_ffmpeg_location(),
            'merge_output_format': target_ext,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True, f"Download as {target_ext.upper()} complete!"
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
            return True, f"Audio ({format.upper()}) download complete!"
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

    def convert_local_video(self, input_path, target_format="mp3", progress_callback=None, output_path=None):
        """Converts a local video file to various audio formats using FFmpeg."""
        if not output_path:
            output_path = os.path.splitext(input_path)[0] + f".{target_format}"
        
        ffmpeg_exe = os.path.join(self._get_ffmpeg_location(), "ffmpeg.exe") if self._get_ffmpeg_location() else "ffmpeg"
        
        # Command to extract duration first for progress calculation
        probe_cmd = [
            os.path.join(self._get_ffmpeg_location(), "ffprobe.exe") if self._get_ffmpeg_location() else "ffprobe",
            "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_path
        ]
        
        try:
            duration = float(subprocess.check_output(probe_cmd).decode().strip())
        except:
            duration = 1.0 # Fallback

        # Base CMD for extraction/conversion
        cmd = [ffmpeg_exe, "-i", input_path, "-vn", "-y"]

        if target_format == "mp3":
            cmd += ["-ar", "44100", "-ac", "2", "-b:a", "192k"]
        elif target_format == "wav":
            cmd += ["-ar", "44100", "-ac", "2"]
        elif target_format == "flac":
            cmd += ["-compression_level", "5"]
        elif target_format == "m4a":
            cmd += ["-c:a", "aac", "-b:a", "192k"]
        
        cmd += [output_path]

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
            
            for line in process.stdout:
                if "time=" in line:
                    # Extract time=HH:MM:SS.ms
                    time_match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                    if time_match:
                        h, m, s = map(float, time_match.groups())
                        current_time = h * 3600 + m * 60 + s
                        progress = min(current_time / duration, 0.99)
                        if progress_callback:
                            progress_callback(progress, f"Converting... {int(progress*100)}%")

            process.wait()
            if process.returncode == 0:
                if progress_callback:
                    progress_callback(1.0, f"Conversion to {target_format.upper()} complete!")
                return True, f"Saved as: {os.path.basename(output_path)}"
            else:
                return False, f"FFmpeg failed with code {process.returncode}"
        except Exception as e:
            return False, str(e)
