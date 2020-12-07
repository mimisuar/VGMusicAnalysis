from collections import Counter
import sys
sys.path.append(".")

import vgmusic
from music21 import note, interval, stream
from typing import Dict, Generator, List
import json

class SongDataTracker:
    def __init__(self):
        self.highest_note = 0
        self.lowest_note = 5000
        self.total_note_length = 0.0
        self.note_count = 0
        self.total_rest_length = 0.0
        self.rest_count = 0
        self.range = 0

    def get_notes_to_rests(self) -> float:
        if self.total_rest_length > 0.0:
            return self.total_note_length / self.total_rest_length
        return 0.0

    def get_avg_note(self) -> float:
        if self.note_count > 0:
            return self.total_note_length / self.note_count
        return 0.0

    def get_avg_rest(self) -> float:
        if self.rest_count > 0:
            return self.total_rest_length / self.rest_count
        return 0.0

    def to_dict(self) -> Dict:
        tmp = {
            "highest_note": self.highest_note,
            "lowest_note": self.lowest_note,
            "total_note_length": self.total_note_length,
            "note_count": self.note_count,
            "total_rest_length": self.total_rest_length,
            "rest_count": self.rest_count,
            "range": self.range
        }

        if self.total_rest_length > 0.0:
            tmp["notes_to_rests"] = self.get_notes_to_rests()

        if self.note_count > 0:
            tmp["avg_note_length"] = self.get_avg_note()
        
        if self.rest_count > 0:
            tmp["avg_rest_length"] = self.get_avg_rest()

        return tmp  

    def from_dict(self, inst: Dict):
        self.highest_note = inst.get("highest_note", 0)
        self.lowest_note = inst.get("lowest_note", 0)
        self.total_note_length = inst.get("total_note_length", 0.0)
        self.note_count = inst.get("note_count", 0)
        self.total_rest_length = inst.get("total_rest_length", 0)
        self.rest_count = inst.get("rest_count", 0)
        self.range = inst.get("range", 0)

    def process_stream(self, song_str: stream.Stream):
        new_range = song_str.analyze("ambitus")
        if new_range.semitones > self.range:
            self.range = new_range.semitones

        for gennote in song_str.flat.getElementsByClass(note.GeneralNote):
            if isinstance(gennote, note.Note):
                new_ps = gennote.pitch.ps
                if self.highest_note < new_ps:
                    self.highest_note = new_ps
                if self.lowest_note > new_ps:
                    self.lowest_note = new_ps

                self.total_note_length += gennote.duration.quarterLength
                self.note_count += 1
            elif isinstance(gennote, note.Rest):
                self.total_rest_length += gennote.duration.quarterLength
                self.rest_count += 1

    def compare_stream(self, song_str: stream.Stream) -> float:
        notes_in_range = 0
        note_count = 0
        #for note_obj in song_str.flat.getElementsByClass(note.Note):
        #    if self.lowest_note <= note_obj.pitch.ps <= self.highest_note:
        #        notes_in_range += 1
        #    note_count += 1
        perc_in_range = 0.0

        #sdt = SongDataTracker()
        #sdt.process_stream(song_str)
    
        #range_diff = abs(sdt.range - self.range)
        #range_diff_score = 1.0 - range_diff / 100.0
        #print("{0} -> {1}".format(range_diff, range_diff_score))

        #ntr_diff_score = abs(sdt.get_notes_to_rests() - self.get_notes_to_rests())

        #avg_note_diff = abs(sdt.get_avg_note() - self.get_avg_note())
        #avg_rest_diff = abs(sdt.get_avg_rest() - self.get_avg_rest())

        #scores = [perc_in_range, range_diff_score, ntr_diff_score, avg_note_diff, avg_rest_diff]
        #weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        
        #tmp_sum = 0
        #for i in range(len(scores)):
        #    tmp_sum += scores[i] * weights[i]
        #return tmp_sum
        return 0.0

class GenreDataTracker:
    def __init__(self):
        self.song_trackers: List[SongDataTracker] = []

    def append(self, tracker: SongDataTracker):
        self.song_trackers.append(tracker)

    def get_median_range(self) -> float:
        ranges = [tracker.range for tracker in self.song_trackers]
        size = len(ranges)
        if size == 1:
            return ranges[0]
        elif size == 0:
            return 0
        elif size % 2 == 0:
            return ranges[size // 2]
        else:
            return (ranges[size // 2] + ranges[size // 2 + 1]) / 2.0

    def compare(self, song: stream.Stream) -> float:
        # given a stream, test the probability the stream belonds to this genre. 
        probs = []
        for sdt in self.song_trackers:
            probs.append(sdt.compare_stream(song))
        return sum(probs) / len(probs)

    def to_dict(self):
        tmp = {} 
        
        tmp["tracker_data"] = []
        for tracker in self.song_trackers:
            tmp["tracker_data"].append(tracker.to_dict())

        tmp["median_range"] = self.get_median_range()

        return tmp

    def from_dict(self, inst: Dict):
        tracker_data = inst.get("tracker_data", [])
        for tracker_inst in tracker_data:
            sdt = SongDataTracker()
            sdt.from_dict(tracker_inst)
            self.song_trackers.append(sdt)

def calculate_stats_for_genres():
    genres = {}

    for game in vgmusic.get_games_by_console("nes"):
        
        if len(game.genres) > 0:
            print("Processing {}...".format(game.name))
            for song in game.fetch_all_songs():
                main_tracker = SongDataTracker()
                main_tracker.process_stream(song)

                for genre in game.genres:
                    if genre not in genres:
                        genres[genre] = GenreDataTracker()
                    genres[genre].append(main_tracker)
                break
    
    final_dict = {}
    for genre in genres:
        final_dict[genre] = genres[genre].to_dict()
    with open("test_output/nes.json", "w") as f:
        f.write(json.dumps(final_dict, indent=4))
                

if __name__ == "__main__":
    #calculate_stats_for_genres()
    with open("test_output/nes.json", "r") as f:
        raw_data = json.loads(f.read())
    genres: Dict[str, GenreDataTracker] = {}
    for genre in raw_data:
        gdt = GenreDataTracker()
        gdt.from_dict(raw_data[genre])
        genres[genre] = gdt
    
    final_dict = {}
    for game in vgmusic.get_games_by_console("nes"):
        if "mega_man" not in game.name.lower():
            continue
        print(game.name)
        genres_sum = {}
        genres_total = {}
        for song in game.fetch_all_songs():
            for genre in genres:
                if genre not in genres_sum:
                    genres_sum[genre] = 0.0
                    genres_total[genre] = 0
                genres_sum[genre] += genres[genre].compare(song)
                genres_total[genre] += 1
        genres_avg = []
        for genre in genres_sum:
            genre_data = (
                genre,
                genres_sum[genre] / genres_total[genre]
            )
            genres_avg.append(genre_data)

        def sort_genre_data(genre_data):
            return genre_data[1]

        genres_avg.sort(key=sort_genre_data, reverse=True)
        
        top_3 = genres_avg[0:3]
        final_dict[game.name] = genres_avg

    with open("test_output/megaman.json", "w") as f:
        f.write(json.dumps(final_dict, indent=4))
    
    