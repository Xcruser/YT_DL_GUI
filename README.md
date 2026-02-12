# YT_DL_GUI - YouTube Downloader & Converter

A modern, native Windows application to download YouTube videos and extract audio effortlessly. Built with Python, `customtkinter`, and `yt-dlp`.

## Features
- 🎥 **High-Quality Video Downloads**: Automatically fetches the best video and audio streams.
- 🎵 **Audio Extraction**: Convert videos directly to MP3.
- 📂 **Custom Save Locations**: Choose where your files go.
- 🚀 **Standalone Executable**: No need to install Python or dependencies manually (if using the provided `.exe`).
- 🌗 **Modern UI**: Clean, dark-mode interface.

## Quick Start (For Users)

### Option 1: Run the Executable
1.  Go to the **Releases** page (if available) or check the `dist` folder if you built it yourself.
2.  Download `YouTubeDownloader.exe`.
3.  Double-click to run. No installation required!

### Option 2: Run from Source
1.  **Install Python 3.10+**.
2.  **Install FFmpeg** and add it to your system PATH.
3.  Clone this repository:
    ```bash
    git clone https://github.com/Xcruser/YT_DL_GUI.git
    cd YT_DL_GUI
    ```
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the app:
    ```bash
    python main.py
    ```

## Building the Executable (For Developers)
Want to create your own `.exe` file?

1.  Ensure you have `ffmpeg` installed at `C:/Tools/ffmpeg/bin/` (or update `build_app.py` path).
2.  Run the build script:
    ```bash
    python build_app.py
    ```
3.  The executable will be created in the `dist/` folder.

## License
MIT License. Feel free to use and modify!

## Credits
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the powerful downloader engine.
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the beautiful UI.
- [FFmpeg](https://ffmpeg.org/) for media processing.
