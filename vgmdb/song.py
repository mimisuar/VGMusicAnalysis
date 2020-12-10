from __future__ import annotations
import requests, os

DEFAULT_DOWNLOAD_FOLDER = "vgmusic_downloads"

class Song:
    def __init__(self, game_name: str, song_title: str, song_url: str):
        self.game_name = game_name
        self.song_title = song_title
        self.song_url = song_url

    def get_filename(self):
        return "{0}/{1}/{2}.mid".format(DEFAULT_DOWNLOAD_FOLDER, self.game_name, self.song_title)

    def download(self):
        if not os.path.isdir(DEFAULT_DOWNLOAD_FOLDER):
            os.mkdir(DEFAULT_DOWNLOAD_FOLDER)
        if not os.path.isdir(DEFAULT_DOWNLOAD_FOLDER + "/" + self.game_name):
            os.mkdir(DEFAULT_DOWNLOAD_FOLDER + "/" + self.game_name)

        song_data = requests.get(self.song_url)
        with open(self.get_filename(), "wb") as f:
            f.write(song_data.content)

    def fetch(self):
        file_name = self.get_filename()
        if os.path.isfile(file_name):
            return file_name
        
        # try to download the song 
        self.download()
        return file_name
        
        