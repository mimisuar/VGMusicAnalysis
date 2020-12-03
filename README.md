# VGMusicAnalysis
Final project for 21M.383

## Dependencies 
python3.9
music21  
requests  
BeautifulSoup4  
igdb-api-v4 (optional; only for vginfo.py)

## Setting up the environment
Use a virtual environment. Makes life easier. 

After installing and activing the virtual environment,
run this

`pip install music21 requests beautifulsoup4 igdb-api-v4`

it should install all dependencies. 

## Modules

### pyconfig.py

This module holds various variables used by the other modules. Here are the most important:

Writable:  
`cache_name: str` Folder where vgmusic midi files are kept.  
`debug_print: bool` If true, enable some debug print statements. 
`games_file: str` The file where the game information is kept.

Read-only:  
`games: Dict` A dictionary containing information about games, including names, release date, genres, and song lists. 

Methods:  
`verify()` A placeholder, for now. This makes sure that the `games_file` is read and stored into `games`. 

### vgcrawl.py

This module scans vgmusic.com and makes a json file of all the games. No music is downloaded with this script. 

Methods:  
`parse_vgmusic()` Scans vgmusic for songs, and creates the `games_file` json. This probably only needs to run once. Running the script by itself is equivalent to calling this method. 

### vgdownloader.py



### vgmusic.py

###
