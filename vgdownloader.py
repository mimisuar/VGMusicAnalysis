# a module that helps with download files from vgmusic.com :)
import requests
import os
import vgconfig as config
from typing import Tuple, List

def print2(text) -> None:
    """
    Shoulda done this a long time ago.
    """
    if config.debug_print:
        print(text)

def mkdir(dir_name: str) -> None:
    try:
        os.mkdir(dir_name)
    except Exception as e:
        #print(dir_name + " exists. Skipping.")
        pass

def download_all_music() -> None:
    """ 
    Attempts to download music files from vgmusic.com. Configure in games.json.
    """
    config.verify()
    #config.debug_print = False

    process_count = 0
    failed_count = 0
    mkdir(config.cache_name)
    for game_name in config.games:
        new_base = config.cache_name + "/" + game_name
        mkdir(new_base)
        game = config.games[game_name]
        for song_name in game["songs"]:
            process_count += 1
            output_file = new_base + "/" + song_name + ".mid"
            if os.path.isfile(output_file):
                print2(game_name + "/" + song_name + " skipped.")
                continue
            
            
            song_url = game["songs"][song_name]
            try:
                #song = converter.parse(song_url)
                #song.write(fp=output_file, fmt="midi")
                response = requests.get(song_url)
                if response.status_code == requests.codes.ok:
                    with open(output_file, "wb") as midifile:
                        midifile.write(response.content)
                else:
                    response.raise_for_status()

                print2(game_name + "/" + song_name + " downloaded.")
            except Exception as e:
                failed_count += 1
                print("Failed to get " + game_name + "/" + song_name + ":\n" + str(e))
    
    #config.debug_print = True
    print2("Processed {} songs.".format(process_count))
    if failed_count > 0:
        print2("Failed {} times.".format(failed_count))

if __name__ == "__main__":
    download_all_music()