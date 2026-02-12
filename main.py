import customtkinter as ctk
import threading
from downloader import Downloader
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader & Converter")
        self.geometry("600x450")
        
        self.downloader = Downloader()
        self.video_save_path = ""
        self.audio_save_path = ""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.title_label = ctk.CTkLabel(self, text="YouTube Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter YouTube URL", width=400)
        self.url_entry.grid(row=1, column=0, padx=20, pady=10)

        self.option_frame = ctk.CTkFrame(self)
        self.option_frame.grid(row=2, column=0, padx=20, pady=10)

        self.radio_var = ctk.StringVar(value="video")
        self.video_radio = ctk.CTkRadioButton(self.option_frame, text="Video", variable=self.radio_var, value="video")
        self.video_radio.grid(row=0, column=0, padx=20, pady=10)
        self.video_path_btn = ctk.CTkButton(self.option_frame, text="Select Folder", command=lambda: self.select_folder("video"), width=100)
        self.video_path_btn.grid(row=0, column=1, padx=5, pady=10)

        self.audio_radio = ctk.CTkRadioButton(self.option_frame, text="Audio (MP3)", variable=self.radio_var, value="audio")
        self.audio_radio.grid(row=1, column=0, padx=20, pady=10)
        self.audio_path_btn = ctk.CTkButton(self.option_frame, text="Select Folder", command=lambda: self.select_folder("audio"), width=100)
        self.audio_path_btn.grid(row=1, column=1, padx=5, pady=10)

        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download_thread)
        self.download_button.grid(row=3, column=0, padx=20, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=10)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=5, column=0, padx=20, pady=(0, 20))

    def select_folder(self, type):
        folder = ctk.filedialog.askdirectory()
        if folder:
            if type == "video":
                self.video_save_path = folder
                self.video_path_btn.configure(text="Selected ✔")
            else:
                self.audio_save_path = folder
                self.audio_path_btn.configure(text="Selected ✔")

    def start_download_thread(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a URL!", text_color="red")
            return
        
        self.download_button.configure(state="disabled")
        self.status_label.configure(text="Starting...", text_color="white")
        self.progress_bar.set(0)
        
        mode = self.radio_var.get()
        if mode == "video":
            save_path = self.video_save_path if self.video_save_path else None
        else:
            save_path = self.audio_save_path if self.audio_save_path else None

        thread = threading.Thread(target=self.download_process, args=(url, mode, save_path))
        thread.start()

    def download_process(self, url, mode, save_path):
        
        def update_progress(progress, status):
            self.progress_bar.set(progress)
            self.status_label.configure(text=status)
        
        try:
            if mode == "video":
                success, msg = self.downloader.download_video(url, update_progress, output_path=save_path)
            else:
                success, msg = self.downloader.download_audio(url, format='mp3', progress_callback=update_progress, output_path=save_path)
                
            if success:
                self.status_label.configure(text=msg, text_color="green")
            else:
                self.status_label.configure(text=f"Error: {msg}", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")
        finally:
            self.download_button.configure(state="normal")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
