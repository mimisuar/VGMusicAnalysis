import json
cache_name = "vgmusic_downloads"
games_file = "games.json"
debug_print = True
games = None

# backwards compatability. This function was used back when the game database was a python dictionary :puke:
# now its a very lovely json file!
def verify(): 
    global games
    if games == None:
        with open(games_file) as file:
            games = json.loads(file.read())
        

#if __name__ == "__main__":
#    try:
#        verify()
#        print("This file is configured correctly!")
#    except AssertionError as e:
#        print("Failed to verify.")
#        print(str(e))

