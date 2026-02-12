import customtkinter as ctk
import threading
from downloader import Downloader
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Media Downloader & Converter v1.1.1")
        self.geometry("600x450")
        
        self.downloader = Downloader()
        self.video_save_path = ""
        self.audio_save_path = ""
        self.local_file_path = ""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.title_label = ctk.CTkLabel(self, text="Media Downloader & Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tabview initialization
        self.tabview = ctk.CTkTabview(self, width=500, height=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=10)
        self.tabview.add("YouTube")
        self.tabview.add("Local")

        # --- YouTube Tab ---
        self.tab_yt = self.tabview.tab("YouTube")
        self.tab_yt.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.tab_yt, placeholder_text="Enter YouTube URL", width=400)
        self.url_entry.grid(row=0, column=0, padx=20, pady=10)

        self.yt_option_frame = ctk.CTkFrame(self.tab_yt)
        self.yt_option_frame.grid(row=1, column=0, padx=20, pady=10)

        self.radio_var = ctk.StringVar(value="video")
        self.video_radio = ctk.CTkRadioButton(self.yt_option_frame, text="Video", variable=self.radio_var, value="video", command=self.update_yt_format_options)
        self.video_radio.grid(row=0, column=0, padx=20, pady=10)
        self.video_path_btn = ctk.CTkButton(self.yt_option_frame, text="Select Folder", command=lambda: self.select_folder("video"), width=100)
        self.video_path_btn.grid(row=0, column=1, padx=5, pady=10)

        self.audio_radio = ctk.CTkRadioButton(self.yt_option_frame, text="Audio", variable=self.radio_var, value="audio", command=self.update_yt_format_options)
        self.audio_radio.grid(row=1, column=0, padx=20, pady=10)
        self.audio_path_btn = ctk.CTkButton(self.yt_option_frame, text="Select Folder", command=lambda: self.select_folder("audio"), width=100)
        self.audio_path_btn.grid(row=1, column=1, padx=5, pady=10)

        self.yt_format_var = ctk.StringVar(value="mp4")
        self.yt_format_menu = ctk.CTkOptionMenu(self.tab_yt, values=["mp4", "mkv"], variable=self.yt_format_var)
        self.yt_format_menu.grid(row=3, column=0, padx=20, pady=10)

        self.download_button = ctk.CTkButton(self.tab_yt, text="Download", command=self.start_download_thread)
        self.download_button.grid(row=4, column=0, padx=20, pady=10)

        # --- Local Tab ---
        self.tab_local = self.tabview.tab("Local")
        self.tab_local.grid_columnconfigure(0, weight=1)

        self.local_label = ctk.CTkLabel(self.tab_local, text="Convert local Media (Video/Audio)")
        self.local_label.grid(row=0, column=0, padx=20, pady=10)

        self.local_file_btn = ctk.CTkButton(self.tab_local, text="Select Media File", command=self.select_local_file)
        self.local_file_btn.grid(row=1, column=0, padx=20, pady=10)

        self.format_label = ctk.CTkLabel(self.tab_local, text="Select Target Format:")
        self.format_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.format_var = ctk.StringVar(value="mp3")
        self.format_menu = ctk.CTkOptionMenu(self.tab_local, values=["mp3", "wav", "flac", "m4a"], variable=self.format_var)
        self.format_menu.grid(row=3, column=0, padx=20, pady=10)

        self.convert_button = ctk.CTkButton(self.tab_local, text="Convert Now", command=self.start_conversion_thread)
        self.convert_button.grid(row=4, column=0, padx=20, pady=10)

        # --- Footer (Progress & Status) ---
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=2, column=0, padx=20, pady=10)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 20))

    def select_folder(self, type):
        folder = ctk.filedialog.askdirectory()
        if folder:
            if type == "video":
                self.video_save_path = folder
                self.video_path_btn.configure(text=f"Folder: {os.path.basename(folder)}")
            else:
                self.audio_save_path = folder
                self.audio_path_btn.configure(text=f"Folder: {os.path.basename(folder)}")

    def select_local_file(self):
        file = ctk.filedialog.askopenfilename(filetypes=[
            ("Media files", "*.mp4 *.mkv *.avi *.mov *.wmv *.mp3 *.wav *.flac *.aac *.m4a *.ogg"),
            ("Video files", "*.mp4 *.mkv *.avi *.mov *.wmv"),
            ("Audio files", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg"),
            ("All files", "*.*")
        ])
        if file:
            self.local_file_path = file
            self.local_file_btn.configure(text=f"File: {os.path.basename(file)}")

    def start_download_thread(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a URL!", text_color="red")
            return
        
        self.download_button.configure(state="disabled")
        self.status_label.configure(text="Starting...", text_color="white")
        self.progress_bar.set(0)
        
        mode = self.radio_var.get()
        format_val = self.yt_format_var.get()
        
        if mode == "video":
            save_path = self.video_save_path if self.video_save_path else None
        else:
            save_path = self.audio_save_path if self.audio_save_path else None

        thread = threading.Thread(target=self.download_process, args=(url, mode, save_path, format_val))
        thread.start()

    def download_process(self, url, mode, save_path, format_val):
        
        def update_progress(progress, status):
            self.progress_bar.set(progress)
            self.status_label.configure(text=status)
        
        try:
            if mode == "video":
                success, msg = self.downloader.download_video(url, update_progress, output_path=save_path, target_ext=format_val)
            else:
                success, msg = self.downloader.download_audio(url, format=format_val, progress_callback=update_progress, output_path=save_path)
                
            if success:
                self.status_label.configure(text=msg, text_color="green")
            else:
                self.status_label.configure(text=f"Error: {msg}", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")
        finally:
            self.download_button.configure(state="normal")
            # Don't reset progress immediately so user can see 100%

    def start_conversion_thread(self):
        if not self.local_file_path:
            self.status_label.configure(text="Please select a file!", text_color="red")
            return
        
        self.convert_button.configure(state="disabled")
        self.status_label.configure(text="Starting conversion...", text_color="white")
        self.progress_bar.set(0)
        
        target_format = self.format_var.get()

        thread = threading.Thread(target=self.conversion_process, args=(self.local_file_path, target_format))
        thread.start()

    def conversion_process(self, input_path, target_format):
        def update_progress(progress, status):
            self.progress_bar.set(progress)
            self.status_label.configure(text=status)

        try:
            success, msg = self.downloader.convert_local_media(input_path, target_format=target_format, progress_callback=update_progress)
            if success:
                self.status_label.configure(text=f"Success: {msg}", text_color="green")
            else:
                self.status_label.configure(text=f"Error: {msg}", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")
        finally:
            self.convert_button.configure(state="normal")

    def update_yt_format_options(self):
        mode = self.radio_var.get()
        if mode == "video":
            self.yt_format_menu.configure(values=["mp4", "mkv"])
            self.yt_format_var.set("mp4")
        else:
            self.yt_format_menu.configure(values=["mp3", "wav", "flac", "m4a"])
            self.yt_format_var.set("mp3")

if __name__ == "__main__":
    app = App()
    app.mainloop()
