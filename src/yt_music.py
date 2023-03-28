"""This module contains  functions to interact with the YoyTube API."""

import os

from dotenv import load_dotenv
from ytmusicapi import YTMusic

from cli.bcolors import bcolors
from playlist import Playlist
from song import Song


def read_file(path: str) -> str:
    """
    Reads a file and returns its content.

    Parameters
    ----------
    path : str
        The path to the file.

    Returns
    -------
    str
        The content of the file.
    """
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()


def setup_ytmusic() -> YTMusic:
    """
    Sets up the YTMusic object for the YouTube Music API.

    Returns
    -------
    YTMusic
        The YTMusic object.
    """
    load_dotenv()

    header_raw = read_file("./header_raw.txt")
    header_json_path = "./resources/headers_auth.json"
    YTMusic.setup(filepath=header_json_path, headers_raw=header_raw)
    ytmusic = YTMusic(header_json_path)
    os.remove(header_json_path)
    return ytmusic


def search_matches(songs: list[Song], ytmusic: YTMusic) -> list[Song]:
    """
    Searches for matches for the given songs on YouTube Music.

    Parameters
    ----------
    songs : list[Song]
        The songs to search for.
    ytmusic : YTMusic
        The YTMusic object to use for the API calls.

    Returns
    -------
    list[Song]
         list of songs with the best match on YouTube Music
    """
    songs_to_sync = []
    for idx, song in enumerate(songs):
        print("Looking for a match for " + str(song))
        search_result: Song = song.get_search_result(ytmusic)
        if search_result is None:
            print(f"{bcolors.WARNING}WARNING: No match found for track nr. {str(idx + 1)}: {str(song)}{bcolors.ENDC}")
        else:
            songs_to_sync.append(search_result)

    return songs_to_sync


def sync_playlist(playlist: Playlist, ytmusic: YTMusic) -> None:
    """
    Syncs the given playlist to the current user's YouTube Music account.

    Parameters
    ----------
    playlist : Playlist
        The playlist to sync.
    ytmusic : YTMusic
        The YTMusic object to use for the API calls.
    """
    print(f"{bcolors.BOLD}\nSearching matches for songs in \"{playlist.name}\" playlist{bcolors.ENDC}")
    # for each song in the Spotify playlist, search for a match on YouTube Music
    songs_to_sync = search_matches(playlist.songs, ytmusic)

    print(f"\nCreating playlist \"{playlist.name}\" in your YouTube Music account...")
    playlist_id = ytmusic.create_playlist(playlist.name, playlist.description)

    print(f"Syncing playlist \"{playlist.name}\" in your YouTube Music account...")
    ytmusic.add_playlist_items(playlist_id, list(map(lambda song: song.id, songs_to_sync)))

    print(f"{bcolors.OKBLUE}\"{playlist.name}\" has been synced to your YouTube Music account!{bcolors.ENDC}")
