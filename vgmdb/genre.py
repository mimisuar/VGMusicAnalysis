GENREDATA = [{"id":4,"name":"Fighting"},{"id":5,"name":"Shooter"},{"id":7,"name":"Music"},{"id":8,"name":"Platform"},
{"id":9,"name":"Puzzle"},{"id":10,"name":"Racing"},{"id":11,"name":"Real Time Strategy (RTS)"},
{"id":12,"name":"Role-playing (RPG)"},{"id":13,"name":"Simulator"},{"id":14,"name":"Sport"},{"id":15,"name":"Strategy"},
{"id":16,"name":"Turn-based strategy (TBS)"},{"id":24,"name":"Tactical"},{"id":26,"name":"Quiz/Trivia"},{"id":25,"name":"Hack and slash/Beat 'em up"},
{"id":30,"name":"Pinball"},{"id":31,"name":"Adventure"},{"id":33,"name":"Arcade"},{"id":34,"name":"Visual Novel"},{"id":32,"name":"Indie"},
{"id":35,"name":"Card & Board Game"},{"id":36,"name":"MOBA"},{"id":2,"name":"Point-and-click"}]

class Genre:
    def __init__(self, id):
        self.id = id
        self.name = ""

        for genre_info in GENREDATA:
            if genre_info["id"] == id:
                self.name = genre_info["name"]
                break
        else:
            raise Exception("Invalid genre id {}.".format(self.id))