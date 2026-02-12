import PyInstaller.__main__
import customtkinter
import os

# Get customtkinter path to include its data
ctk_path = os.path.dirname(customtkinter.__file__)

print("Building YouTube Downloader...")
print(f"CustomTkinter path: {ctk_path}")

PyInstaller.__main__.run([
    'main.py',
    '--name=YouTubeDownloader',
    '--onefile',
    '--windowed',
    f'--add-data={ctk_path};customtkinter',
    '--add-binary=C:/Tools/ffmpeg/bin/ffmpeg.exe;.',
    '--add-binary=C:/Tools/ffmpeg/bin/ffprobe.exe;.',
    '--clean',
    '--noconfirm',
])

print("Build complete! Check the 'dist' folder.")
