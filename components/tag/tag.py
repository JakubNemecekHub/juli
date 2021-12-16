""" ??? Funkce, které dáme soubor a ona nám vrátí vybrané tagy ??? """

import os

import music_tag
import mutagen


def get_tags(path: str):
    # Get tags
    TAG_NAMES = ["artist", "album", "tracknumber", "tracktitle"] # Přidat duration
    tags = music_tag.load_file(path)
    song = {key: tags[key].value for key in TAG_NAMES if tags[key].value}   # Copy only existing tags
    if len(song) == len(TAG_NAMES):
        # All tags found
        filled_tracknumber = str(song['tracknumber']).zfill(2)
        song_id = f"{song['artist']} - {song['album']} - {filled_tracknumber} - {song['tracktitle']}"
    if not song:
        # At least one tag missing
        full_name = os.path.basename(path)
        song_id = os.path.splitext(full_name)[0]
    song["path"] = path
    # Add duration, in milliseconds
    file = mutagen.File(path)
    song["duration"] = int(file.info.length) * 1000
    # Return song_id and song
    return song_id, song
