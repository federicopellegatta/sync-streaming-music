"""This module contains the Playlist class and its methods."""

from __future__ import annotations
from dataclasses import dataclass
from spotipy.client import Spotify
from song import Song, get_song_from_spotify_json
from cli.bcolors import bcolors


def get_playlist_from_spotify(json, spotify: Spotify) -> Playlist:
    """
    Creates a Playlist object from a Spotify playlist JSON object.

    Parameters
    ----------
    json : dict
        The JSON object of the playlist.
    spotify : Spotify
        The Spotify object to use for the API calls.

    Returns
    -------
    Playlist
        The Playlist object.
    """
    name = json["name"]
    id = json["id"]
    image = json["images"][0]["url"] if len(json["images"]) > 0 else None
    description = json["description"]
    total_songs = json["tracks"]["total"]
    songs = get_songs_by_playlist_id(id, total_songs, spotify)

    return Playlist(name, id, image, description, songs)


def get_songs_by_playlist_id(playlist_id: str, total_songs: int, spotify: Spotify) -> list[Song]:
    """
    Gets all songs from a Spotify playlist by its ID.

    Parameters
    ----------
    playlist_id : str
        The ID of the playlist.
    total_songs : int
        The total number of songs in the playlist.
    spotify : Spotify
        The Spotify object to use for the API calls.

    Returns
    -------
    list[Song]
        A list of Song objects.
    """
    if total_songs == 0:
        return []

    if total_songs <= 100:
        songs_json = spotify.playlist_items(
            playlist_id, limit=total_songs)['items']

    else:
        # there is a limit of 100 songs per request
        offset = 0
        songs_json = []
        while offset < total_songs:
            songs_json_temp = spotify.playlist_items(
                playlist_id, limit=100, offset=offset)
            songs_json.extend(songs_json_temp["items"])
            offset += 100

    songs = []
    for song in songs_json:
        songs.append(get_song_from_spotify_json(song["track"]))

    if total_songs != len(songs):
        print(f"{bcolors.WARNING}WARNING: Playlist ID {playlist_id}: "
              f"{total_songs} songs were expected, but only {len(songs)} were found{bcolors.ENDC}")

    return songs


@dataclass
class Playlist:
    """
    A class used to represent a playlist.

    Attributes
    ----------
    name : str
        The name of the playlist.
    id : str
        The ID of the playlist.
    image : str
        The URL of the playlist's image.
    description : str
        The description of the playlist.
    songs : list[Song]
        A list of Song objects.
    """

    def __init__(self, name: str, id: str, image: str, description: str, songs=None):
        """
        Parameters
        ----------
        name : str
            The name of the playlist.
        id : str
            The ID of the playlist.
        image : str
            The URL of the playlist's image.
        description : str
            The description of the playlist.
        songs : list[Song], optional
            A list of Song objects. If None, an empty list is used.
        """
        if songs is None:
            songs = []
        self.name: str = name
        self.id: str = id
        self.image: str = image
        self.description: str = description
        self.songs: list[Song] = songs

    def __str__(self):
        return "Playlist{name=" + self.name + \
            ", id=" + self.id + \
            ", image=" + self.image + \
            ", description=" + self.description + "}"
