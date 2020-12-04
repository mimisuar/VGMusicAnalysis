import vgmusic, vgdownloader, vgconfig
from math import modf
from collections import Counter
from typing import Dict
from music21 import roman, pitch
import json

class ConsoleData:
    def __init__(self, name):
        self.name = name
        self.total_gen_notes = 0 # general notes = notes and rests #
        self.rests = 0
        self.rest_length = 0
        self.counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def inc_gen_notes(self):
        self.total_gen_notes += 1
    
    def inc_pitch_count(self, pitch_class):
        assert 0 <= pitch_class < 12, "Invalid pitch class {}.".format(pitch_class)
        self.counter[pitch_class] += 1

    def inc_rests(self, rest_length):
        self.rests += 1
        self.rest_length += rest_length

    def to_dict(self):
        # prepares a python dictionary with the information need #
        tmp_dict = {
            "general_notes": self.total_gen_notes,
            "rests": self.rests,
            "avg_rest_time": self.rest_length / self.rests
        }

        sum_pitches = sum(self.counter)
        if sum_pitches > 0:
            tmp_averages = [float(x) / sum_pitches for x in self.counter]
            avg_dict = {}
            c_pitch = 0
            p = pitch.Pitch()
            for avg in tmp_averages:
                p.pitchClass = c_pitch
                c_pitch += 1

                avg_dict[p.name] = avg
            tmp_dict["pitch_averages"] = avg_dict

        return tmp_dict

import datetime
start_time = datetime.datetime.now()
vgconfig.verify()
total_console_data = {}
fail_count = 0
for game_name in vgmusic.get_game_names():
    game = vgmusic.get_game(game_name) # game game game name game name game name namen ame
    console = game["console"]
    if console in total_console_data:
        console_data = total_console_data[console]
    else:
        console_data = ConsoleData(console)
        total_console_data[console] = console_data

    for song_name in vgmusic.get_songs_by_game(game_name):
        stream = vgmusic.fetch(game_name, song_name)

        if stream == None:
            #print("Unable to load {0}/{1}".format(game_name, song_name))
            fail_count += 1
            continue
        
        for gen_note in stream.flat.getElementsByClass("GeneralNote"):
            console_data.inc_gen_notes()
            if "Note" in gen_note.classes:
                console_data.inc_pitch_count(gen_note.pitch.pitchClass)
            elif "Rest" in gen_note.classes:
                console_data.inc_rests(gen_note.duration.quarterLength)
        
end_time = datetime.datetime.now()
dt = end_time - start_time
ms = int(dt.total_seconds() * 1000)
print("Took {} ms".format(ms))
print("Failed {} times.".format(fail_count))

# fix data
json_prepped = {}
for key in total_console_data:
    json_prepped[key] = total_console_data[key].to_dict()

with open('file.txt', 'w') as file:
    file.write(json.dumps(json_prepped, indent=4, sort_keys=True))
    # use `json.loads` to do the reverse