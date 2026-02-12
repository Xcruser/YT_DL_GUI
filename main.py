import customtkinter as ctk
import threading
from downloader import Downloader
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Media Downloader & Converter v2.0")
        self.geometry("900x500")
        
        self.downloader = Downloader()
        self.video_save_path = ""
        self.audio_save_path = ""
        self.local_file_path = ""

        # Set grid layout 1x2 (Sidebar and Main Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MediaDL 🚀", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_yt = ctk.CTkButton(self.sidebar_frame, text="📺  YouTube Download", 
                                    fg_color="transparent", text_color=("gray10", "gray90"),
                                    hover_color=("gray70", "gray30"), anchor="w",
                                    command=self.show_yt_view)
        self.btn_yt.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_local = ctk.CTkButton(self.sidebar_frame, text="📂  Local Conversion", 
                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                       hover_color=("gray70", "gray30"), anchor="w",
                                       command=self.show_local_view)
        self.btn_local.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.appearance_label = ctk.CTkLabel(self.sidebar_frame, text="🌓  Appearance:", anchor="w")
        self.appearance_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_menu.set("Dark")

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # -- YouTube View --
        self.view_yt = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_yt.grid_columnconfigure(0, weight=1)
        
        self.yt_heading = ctk.CTkLabel(self.view_yt, text="YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold"))
        self.yt_heading.grid(row=0, column=0, padx=20, pady=(10, 20))

        self.url_entry = ctk.CTkEntry(self.view_yt, placeholder_text="Paste YouTube URL here...", width=500, height=40)
        self.url_entry.grid(row=1, column=0, padx=20, pady=10)

        self.yt_card = ctk.CTkFrame(self.view_yt)
        self.yt_card.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.yt_card.grid_columnconfigure(1, weight=1)

        self.radio_var = ctk.StringVar(value="video")
        self.video_radio = ctk.CTkRadioButton(self.yt_card, text="Video", variable=self.radio_var, value="video", command=self.update_yt_format_options)
        self.video_radio.grid(row=0, column=0, padx=20, pady=15)
        
        self.video_path_btn = ctk.CTkButton(self.yt_card, text="Set Folder", command=lambda: self.select_folder("video"), width=120)
        self.video_path_btn.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        self.audio_radio = ctk.CTkRadioButton(self.yt_card, text="Audio", variable=self.radio_var, value="audio", command=self.update_yt_format_options)
        self.audio_radio.grid(row=1, column=0, padx=20, pady=15)
        
        self.audio_path_btn = ctk.CTkButton(self.yt_card, text="Set Folder", command=lambda: self.select_folder("audio"), width=120)
        self.audio_path_btn.grid(row=1, column=1, padx=20, pady=15, sticky="e")

        self.yt_format_var = ctk.StringVar(value="mp4")
        self.yt_format_menu = ctk.CTkOptionMenu(self.view_yt, values=["mp4", "mkv"], variable=self.yt_format_var, width=150)
        self.yt_format_menu.grid(row=3, column=0, padx=20, pady=10)

        self.download_button = ctk.CTkButton(self.view_yt, text="Start Download", command=self.start_download_thread, height=40, font=ctk.CTkFont(weight="bold"))
        self.download_button.grid(row=4, column=0, padx=40, pady=20, sticky="ew")

        # -- Local View --
        self.view_local = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_local.grid_columnconfigure(0, weight=1)

        self.local_heading = ctk.CTkLabel(self.view_local, text="Media Converter", font=ctk.CTkFont(size=20, weight="bold"))
        self.local_heading.grid(row=0, column=0, padx=20, pady=(10, 20))

        self.local_file_btn = ctk.CTkButton(self.view_local, text="Choose Media File (Video/Audio)", command=self.select_local_file, height=60, font=ctk.CTkFont(size=14))
        self.local_file_btn.grid(row=1, column=0, padx=40, pady=20, sticky="ew")

        self.format_card = ctk.CTkFrame(self.view_local)
        self.format_card.grid(row=2, column=0, padx=40, pady=10, sticky="ew")
        
        self.format_label = ctk.CTkLabel(self.format_card, text="Target Format:")
        self.format_label.grid(row=0, column=0, padx=20, pady=15)

        self.format_var = ctk.StringVar(value="mp3")
        self.format_menu = ctk.CTkOptionMenu(self.format_card, values=["mp3", "wav", "flac", "m4a"], variable=self.format_var)
        self.format_menu.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        self.convert_button = ctk.CTkButton(self.view_local, text="Convert Now", command=self.start_conversion_thread, height=40, font=ctk.CTkFont(weight="bold"))
        self.convert_button.grid(row=3, column=0, padx=40, pady=20, sticky="ew")

        # --- Shared Footer (Progress & Status) ---
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.footer_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self.footer_frame, height=10)
        self.progress_bar.grid(row=0, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.footer_frame, text="Ready", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 10))

        # Show initial view
        self.show_yt_view()

    def show_yt_view(self):
        self.view_local.grid_forget()
        self.view_yt.grid(row=0, column=0, sticky="nsew")
        self.btn_yt.configure(fg_color=("gray75", "gray25"))
        self.btn_local.configure(fg_color="transparent")

    def show_local_view(self):
        self.view_yt.grid_forget()
        self.view_local.grid(row=0, column=0, sticky="nsew")
        self.btn_local.configure(fg_color=("gray75", "gray25"))
        self.btn_yt.configure(fg_color="transparent")

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    def select_folder(self, type):
        folder = ctk.filedialog.askdirectory()
        if folder:
            if type == "video":
                self.video_save_path = folder
                self.video_path_btn.configure(text=f"Save: {os.path.basename(folder)}")
            else:
                self.audio_save_path = folder
                self.audio_path_btn.configure(text=f"Save: {os.path.basename(folder)}")

    def select_local_file(self):
        file = ctk.filedialog.askopenfilename(filetypes=[
            ("Media files", "*.mp4 *.mkv *.avi *.mov *.wmv *.mp3 *.wav *.flac *.aac *.m4a *.ogg"),
            ("Video files", "*.mp4 *.mkv *.avi *.mov *.wmv"),
            ("Audio files", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg"),
            ("All files", "*.*")
        ])
        if file:
            self.local_file_path = file
            self.local_file_btn.configure(text=f"Selected: {os.path.basename(file)}")

    def start_download_thread(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a URL!", text_color="red")
            return
        
        self.download_button.configure(state="disabled")
        self.status_label.configure(text="Initializing download...", text_color=("gray10", "gray90"))
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

    def start_conversion_thread(self):
        if not self.local_file_path:
            self.status_label.configure(text="Please select a file!", text_color="red")
            return
        
        self.convert_button.configure(state="disabled")
        self.status_label.configure(text="Processing file...", text_color=("gray10", "gray90"))
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
                self.status_label.configure(text=f"Finished: {msg}", text_color="green")
            else:
                self.status_label.configure(text=f"Failed: {msg}", text_color="red")
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
