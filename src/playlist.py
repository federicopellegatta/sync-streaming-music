from __future__ import annotations
from dataclasses import dataclass
from song import Song
from spotipy.client import Spotify
from cli.bcolors import bcolors


def get_songs_by_playlist_id(playlist_id: str, total_songs: int, spotify: Spotify) -> list[Song]:
    if total_songs == 0:
        return []

    elif total_songs <= 100:
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
        songs.append(Song.get_song_from_json(song["track"]))

    if (total_songs != len(songs)):
        print(f"{bcolors.WARNING}WARNING: Playlist ID {playlist_id}: {total_songs} songs were expected, but only {len(songs)} were found{bcolors.ENDC}")

    return songs


@ dataclass
class Playlist:

    def __init__(self, name: str, id: str, image: str, description: str, songs: list[Song] = []):
        self.name: str = name
        self.id: str = id
        self.image: str = image
        self.description: str = description
        self.songs: list[Song] = songs

    @ classmethod
    def get_playlist_from_json(cls, args, spotify: Spotify) -> Playlist:
        json = args[1]

        name = json["name"]
        id = json["id"]
        image = json["images"][0]["url"] if len(json["images"]) > 0 else None
        description = json["description"]
        total_songs = json["tracks"]["total"]
        songs = get_songs_by_playlist_id(id, total_songs, spotify)

        playlist = cls(name, id, image, description, songs)
        return playlist

    def __str__(self):
        return "Playlist{name=" + self.name + ", id=" + self.id + ", image=" + self.image + ", description=" + self.description + "}"
