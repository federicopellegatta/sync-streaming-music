from __future__ import annotations
from dataclasses import dataclass
from utils.string_utils import string_similarity, remove_parenthesis_content, get_string_before_dash
from ytmusicapi import YTMusic


@dataclass
class Song:

    def __init__(self, track: str, artist: str, album: str, duration: int = None, is_explicit: bool = False, year: int = None):
        self.track: str = track
        self.artist: str = artist
        self.album: str = album
        self.duration: int = duration / \
            1000 if duration is not None else None
        self.is_explicit: bool = is_explicit
        self.year: int = year

    @classmethod
    def get_song_from_csv_row(cls, args) -> Song:
        track = args["Track Name"]
        artist = args["Artist Name(s)"]
        album = args["Album Name"]
        duration = args["Track Duration (ms)"]
        is_explicit = args["Explicit"]
        year = args["Album Release Date"].split(
            "-")[0] if args["Album Release Date"] is not None else None

        song = cls(track, artist, album,
                   duration, is_explicit, year)
        return song

    def get_search_query(self) -> str:
        return self.artist + " - " + self.track + " (" + self.album + ")"

    def get_search_result(self, ytmusic: YTMusic) -> Song:
        search_results = ytmusic.search(
            query=self.get_search_query(), filter="songs")

        best_result = next(
            (res for res in search_results if self.is_result_similar(res, True)), None)

        if (best_result is None):
            best_result = next(
                (res for res in search_results if self.is_result_similar(res, False)), None)

        return best_result

    def is_result_similar(self, result: Song, is_detailed_search: bool = True) -> bool:
        return (self.is_similar_track_name(result["title"], is_detailed_search) and
                self.is_similar_artist(result["artists"], is_detailed_search) and
                self.is_similar_album(result["album"]["name"], is_detailed_search) and
                self.is_live() == self.is_live(result["title"]) and
                self.is_similar_duration(result["duration"]) and
                self.is_explicit == result["isExplicit"] and
                (self.year == result["year"] if self.year is not None and result["year"] is not None else True))

    def is_similar_track_name(self, track: str, is_detailed_search: bool = True) -> bool:
        self_track = self.track if is_detailed_search else remove_parenthesis_content(
            get_string_before_dash(self.track))
        other_track = track if is_detailed_search else remove_parenthesis_content(
            get_string_before_dash(track))

        return string_similarity(self_track, other_track) > 0.8

    def is_similar_artist(self, artists: str, is_detailed_search: bool = True) -> bool:
        self_artist = self.artist if is_detailed_search else self.artist.split(",")[
            0]
        other_artist = self.join_artists_names(
            artists) if is_detailed_search else artists[0]["name"]
        return string_similarity(self_artist, other_artist) > 0.8

    def join_artists_names(self, artists: list) -> str:
        return ", ".join(map(lambda artist: artist["name"] if type(artist) is dict else artist, artists))

    def is_similar_album(self, album: str, is_detailed_search: bool = True) -> bool:
        return string_similarity(remove_parenthesis_content(self.album), remove_parenthesis_content(album)) > 0.5 if is_detailed_search else True

    def is_live(self, track: str = None) -> bool:
        return "live" in track.lower() if track is not None else "live" in self.track.lower()

    def is_similar_duration(self, duration_str: str) -> bool:
        """
        Returns true if the duration of the song is within 10 seconds of the result
        """
        duration_split = duration_str.split(":")
        duration = int(duration_split[0])*60 + int(duration_split[1])
        return abs(self.duration - duration) < 10 if self.duration is not None and duration is not None else True

    def __str__(self):
        return self.artist + " - " + self.track + " (" + self.album + ")"
