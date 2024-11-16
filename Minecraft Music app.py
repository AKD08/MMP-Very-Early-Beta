import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import vlc
import threading
import yt_dlp
import os

# Directory for storing audio files (temporary)
AUDIO_DIR = "minecraft_music"
os.makedirs(AUDIO_DIR, exist_ok=True)

# YouTube playlist URL
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLBO2h-GzDvIYDdNeZs6eAejompnLTZaEq"

class MinecraftMusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Music Player Beta V1.0")
        self.root.geometry("500x400")
        
        self.current_track_index = 0
        self.track_list = []

        # Specify the path to libvlc.dll explicitly
        self.vlc_instance = vlc.Instance('C:\\Program Files\\VideoLAN\\VLC')  # Update the path if needed
        self.player = self.vlc_instance.media_player_new()

        # Event when a track finishes
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.on_track_end)

        # Initialize the status label early in the __init__ method, but it will be updated later.
        self.status_label = None

        self.setup_welcome_screen()

    def setup_welcome_screen(self):
        self.clear_screen()

        # Welcome label
        welcome_label = tk.Label(self.root, text="Welcome", font=("Arial", 24))
        welcome_label.pack(pady=50)

        # Disclaimer label
        disclaimer_label = tk.Label(self.root, text="Disclaimer: may take a while to load", font=("Arial", 12))
        disclaimer_label.pack(pady=10)

        # Start button
        start_button = tk.Button(self.root, text="Start", font=("Arial", 16), command=self.load_player)
        start_button.pack()

    def load_player(self):
        self.clear_screen()

        # Initialize the status label here
        if not self.status_label:
            self.status_label = tk.Label(self.root, text="Loading tracks...", font=("Arial", 14))
            self.status_label.pack(pady=10)

        # Check if music has already been downloaded
        if not self.check_music_folder():
            # Load music from YouTube playlist if music folder is empty
            threading.Thread(target=self.download_tracks, daemon=True).start()
        else:
            # If music already exists, just load it
            self.track_list = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')]
            self.status_label.config(text="Tracks Loaded. Press ▶ to play.")

        # Music disc image
        self.music_disc_img = Image.open("music_disc.png").resize((150, 150))
        self.music_disc_img = ImageTk.PhotoImage(self.music_disc_img)
        music_disc_label = tk.Label(self.root, image=self.music_disc_img)
        music_disc_label.pack(pady=20)

        # Playback controls
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=20)

        prev_button = tk.Button(controls_frame, text="⏮", font=("Arial", 20), command=self.prev_track)
        prev_button.grid(row=0, column=0, padx=10)

        play_button = tk.Button(controls_frame, text="▶", font=("Arial", 20), command=self.play_pause)
        play_button.grid(row=0, column=1, padx=10)

        next_button = tk.Button(controls_frame, text="⏭", font=("Arial", 20), command=self.next_track)
        next_button.grid(row=0, column=2, padx=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_music_folder(self):
        """Checks if the music folder exists and contains audio files."""
        return bool([f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')])

    def download_tracks(self):
        """Downloads audio from YouTube playlist."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{AUDIO_DIR}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(PLAYLIST_URL, download=True)
                self.track_list = [entry['title'] + '.mp3' for entry in info['entries']]

            self.status_label.config(text="Tracks Loaded. Press ▶ to play.")
        except Exception as e:
            self.status_label.config(text="Error loading tracks!")
            messagebox.showerror("Error", str(e))

    def play_pause(self):
        """Toggle play/pause of the current track."""
        if self.player.is_playing():
            self.player.pause()
        else:
            if not self.player.get_media():
                self.play_track()
            else:
                self.player.play()

    def play_track(self):
        """Play the current track."""
        if self.track_list:
            track_path = os.path.join(AUDIO_DIR, self.track_list[self.current_track_index])
            media = self.vlc_instance.media_new(track_path)
            self.player.set_media(media)
            self.player.play()
            self.status_label.config(text=f"Playing: {self.track_list[self.current_track_index]}")

    def next_track(self):
        """Play the next track."""
        if self.track_list:
            self.current_track_index = (self.current_track_index + 1) % len(self.track_list)
            self.play_track()

    def prev_track(self):
        """Play the previous track."""
        if self.track_list:
            self.current_track_index = (self.current_track_index - 1) % len(self.track_list)
            self.play_track()

    def on_track_end(self, event):
        """Automatically play the next track when the current track ends."""
        self.next_track()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftMusicApp(root)
    root.mainloop()
