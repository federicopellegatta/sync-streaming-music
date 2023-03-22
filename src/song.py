from __future__ import annotations
from dataclasses import dataclass
from utils.string_utils import string_similarity, remove_parenthesis_content, get_string_before_dash
from ytmusicapi import YTMusic


def join_artists_names(artists: list[str]) -> str:
    return ", ".join(artists)


def get_song_from_ytmusic_json(args) -> Song:
    title = args["title"]
    artist = list(map(lambda a: a["name"], args["artists"]))
    album = args["album"]["name"] if args["album"] is not None else None
    duration = args["duration_seconds"]
    is_explicit = args["isExplicit"]
    year = args["year"]
    id = args["videoId"]

    return Song(title, artist, album, duration, is_explicit, year, id)


def get_song_from_spotify_json(args) -> Song:
    title = args["name"]
    artist = list(map(lambda a: a["name"], args["artists"]))
    album = args["album"]["name"]
    duration = args["duration_ms"] / \
        1000 if args["duration_ms"] is not None else None
    is_explicit = args["explicit"]

    match args["album"]["release_date_precision"]:
        case "day" | "month":
            year = args["album"]["release_date"].split("-")[0]
        case "year":
            year = args["album"]["release_date"]
        case _:
            year = None

    id = args["id"]

    return Song(title, artist, album, duration, is_explicit, year, id)


@dataclass
class Song:

    def __init__(self, title: str, artists: list[str], album: str, duration: int = None, is_explicit: bool = False, year: int = None, id: str = None):
        self.id: str = id
        self.title: str = title
        self.artists: list[str] = artists
        self.album: str = album
        self.duration: int = duration
        self.is_explicit: bool = is_explicit
        self.year: int = year

    @classmethod
    def get_song_from_csv_row(cls, args) -> Song:
        title = args["Track Name"]
        artist = args["Artist Name(s)"]
        album = args["Album Name"]
        duration = args["Track Duration (ms)"]
        is_explicit = args["Explicit"]
        year = args["Album Release Date"].split(
            "-")[0] if args["Album Release Date"] is not None else None

        song = cls(title, artist, album,
                   duration, is_explicit, year)
        return song

    def get_search_query(self) -> str:
        return join_artists_names(self.artists) + " - " + self.title + " (" + self.album + ")"

    def get_search_result(self, ytmusic: YTMusic) -> Song:
        search_results = ytmusic.search(
            query=self.get_search_query(), filter="songs")

        best_result = next(
            (get_song_from_ytmusic_json(res) for res in search_results if self.is_similar(get_song_from_ytmusic_json(res), True)), None)

        if (best_result is None):
            best_result = next(
                (get_song_from_ytmusic_json(res) for res in search_results if self.is_similar(get_song_from_ytmusic_json(res), False)), None)

        return best_result

    def is_similar(self, other: Song, is_detailed_search: bool = True) -> bool:
        return (self.is_similar_title(other.title, is_detailed_search) and
                self.is_similar_artists(other.artists, is_detailed_search) and
                self.is_similar_album(other.album, is_detailed_search) and
                self.is_live() == other.is_live() and
                self.is_similar_duration(other.duration) and
                self.is_explicit == other.is_explicit and
                (self.year == other.year if self.year is not None and other.year is not None else True))

    def is_similar_title(self, title: str, is_detailed_search: bool = True) -> bool:
        self_title = self.title if is_detailed_search else remove_parenthesis_content(
            get_string_before_dash(self.title))
        other_title = title if is_detailed_search else remove_parenthesis_content(
            get_string_before_dash(title))

        return string_similarity(self_title, other_title) > 0.8

    def is_similar_artists(self, artists: list[str], is_detailed_search: bool = True) -> bool:
        if (is_detailed_search):
            if len(self.artists) != len(artists):
                return False
            else:
                return all(map(lambda a: string_similarity(a[0], a[1]) > 0.8, zip(self.artists, artists)))
        else:
            return self.artists[0] == artists[0]

    def is_similar_album(self, album: str, is_detailed_search: bool = True) -> bool:
        return string_similarity(remove_parenthesis_content(self.album), remove_parenthesis_content(album)) > 0.5 if is_detailed_search else True

    def is_live(self, title: str = None) -> bool:
        return "live" in title.lower() if title is not None else "live" in self.title.lower()

    def is_similar_duration(self, duration: int) -> bool:
        """
        Returns true if the duration of the song is within 10 seconds of the result
        """
        return abs(self.duration - duration) < 10 if self.duration is not None and duration is not None else True

    def __str__(self):
        return join_artists_names(self.artists) + " - " + self.title + " (" + self.album + ")"
