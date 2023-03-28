"""This module contains the Song class and its methods."""

from __future__ import annotations

from dataclasses import dataclass

from ytmusicapi import YTMusic

from utils.string_utils import get_string_before_dash, remove_parenthesis_content, string_similarity


def join_artists_names(artists: list[str]) -> str:
    """
    Joins a list of artists names into a single string.

    Parameters
    ----------
    artists : list[str]
        The list of artists names.

    Returns
    -------
    str
        The joined string.
    """
    return ", ".join(artists)


def get_song_from_ytmusic_json(args) -> Song:
    """
    Creates a Song object from a YTMusic song1 JSON object.

    Parameters
    ----------
    args : dict
        The JSON object of the song1.

    Returns
    -------
    Song
        The Song object.
    """
    title = args["title"]
    artist = list(map(lambda a: a["name"], args["artists"]))
    album = args["album"]["name"] if args["album"] is not None else None
    duration = args["duration_seconds"]
    is_explicit = args["isExplicit"]
    year = args["year"]
    id = args["videoId"]

    return Song(title, artist, album, duration, is_explicit, year, id)


def get_song_from_spotify_json(args) -> Song:
    """
    Creates a Song object from a Spotify song1 JSON object.

    Parameters
    ----------
    args : dict
        The JSON object of the song1.

    Returns
    -------
    Song
        The Song object.
    """
    title = args["name"]
    artist = list(map(lambda a: a["name"], args["artists"]))
    album = args["album"]["name"]
    duration = args["duration_ms"] / 1000 if args["duration_ms"] is not None else None
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
    """
    This class represents a song1.

    Attributes
    ----------
    id : str
        The ID of the song1.
    title : str
        The title of the song1.
    artists : list[str]
        The list of artists names.
    album : str
        The album name.
    duration : int
        The duration of the song1 in seconds.
    is_explicit : bool
        Whether the song1 is explicit or not.
    year : int
        The year of the song1.
    id : str
        The ID of the song1.
    """

    def __init__(self, title: str, artists: list[str], album: str, duration: int = None, is_explicit: bool = False,
                 year: int = None, id: str = None):
        """
        The constructor for the Song class.

        Parameters
        ----------
        title : str
            The title of the song1.
        artists : list[str]
            The list of artists names.
        album : str
            The album name.
        duration : int, optional
            The duration of the song1 in seconds, by default None
        is_explicit : bool, optional
            Whether the song1 is explicit or not, by default False
        year : int, optional
            The year of the song1, by default None
        id : str, optional
            The ID of the song1 on Spotify or YouTube Music service, by default None
        """
        self.id: str = id
        self.title: str = title
        self.artists: list[str] = artists
        self.album: str = album
        self.duration: int = duration
        self.is_explicit: bool = is_explicit
        self.year: int = year

    def get_search_query(self) -> str:
        """
        Returns the search query for the song1.

        Returns
        -------
        str
            The search query.

        Examples
        --------
        >>> song1 = Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991)
        >>> song1.get_search_query()
        'Guns N' Roses - Knockin' On Heaven's Door (Use Your Illusion II)'
        """
        return join_artists_names(self.artists) + " - " + self.title + " (" + self.album + ")"

    def get_search_result(self, ytmusic: YTMusic) -> Song:
        """
        Returns the best search result on YouTube Music for the song1.

        Parameters
        ----------
        ytmusic : YTMusic
            The YTMusic object.

        Returns
        -------
        Song
            The best search result on YouTube Music.
        """
        search_results = ytmusic.search(
            query=self.get_search_query(), filter="songs")

        best_result = next(
            (get_song_from_ytmusic_json(res) for res in search_results if
             self.is_similar(get_song_from_ytmusic_json(res), True)), None)

        if best_result is None:
            best_result = next(
                (get_song_from_ytmusic_json(res) for res in search_results if
                 self.is_similar(get_song_from_ytmusic_json(res), False)), None)

        return best_result

    def is_similar(self, other: Song, is_detailed_search: bool = True) -> bool:
        """
        Returns whether the song1 is similar to another song1.

        Parameters
        ----------
        other : Song
            The other song1.
        is_detailed_search : bool, optional
            Whether the search is detailed or not, by default True

        Returns
        -------
        bool
            Whether the song1 is similar to another song1.
        """
        return (self.is_similar_title(other.title, is_detailed_search) and
                self.is_similar_artists(other.artists, is_detailed_search) and
                self.is_similar_album(other.album, is_detailed_search) and
                self.is_live() == other.is_live() and
                self.is_similar_duration(other.duration) and
                self.is_explicit == other.is_explicit and
                (self.year == other.year if self.year is not None and other.year is not None else True))

    def is_similar_title(self, title: str, is_detailed_search: bool = True) -> bool:
        """
        Returns whether the song1 title is similar to another song1 title.

        Parameters
        ----------
        title : str
            The other song1 title.
        is_detailed_search : bool, optional
            Whether the search is detailed or not, by default True

        Returns
        -------
        bool
            Whether the song1 title is similar to another song1 title.
        """
        self_title = self.title if is_detailed_search else remove_parenthesis_content(
            get_string_before_dash(self.title))
        other_title = title if is_detailed_search else remove_parenthesis_content(
            get_string_before_dash(title))

        return string_similarity(self_title, other_title) > 0.8

    def is_similar_artists(self, artists: list[str], is_detailed_search: bool = True) -> bool:
        """
        Returns whether the song1 artists are similar to another song1 artists.

        Parameters
        ----------
        artists : list[str]
            The other song1 artists.
        is_detailed_search : bool, optional
            Whether the search is detailed or not, by default True.
            If True, the artists names must be in the same order.
            If False, the first artist name must be the same.

        Returns
        -------
        bool
            Whether the song1 artists are similar to another song1 artists.

        Examples
        --------
        >>> song1 = Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991)
        >>> song1.is_similar_artists(["Guns N' Roses"], True)
        True
        >>> song1.is_similar_artists(["Guns N' Roses"], False)
        True
        >>> song1.is_similar_artists(["Guns N' Roses", "Axl Rose"], True)
        False
        >>> song1.is_similar_artists(["Guns N' Roses", "Axl Rose"], False)
        True
        """
        if is_detailed_search:
            return all(map(lambda a: string_similarity(a[0], a[1]) > 0.8, zip(self.artists, artists))) if len(
                self.artists) == len(artists) else False

        return self.artists[0] == artists[0]

    def is_similar_album(self, album: str, is_detailed_search: bool = True) -> bool:
        """
        Returns whether the song1 album is similar to another song1 album.

        Parameters
        ----------
        album : str
            The other song1 album.
        is_detailed_search : bool, optional
            Whether the search is detailed or not, by default True.

        Returns
        -------
        bool
            Whether the song1 album is similar to another song1 album.
        """
        return string_similarity(remove_parenthesis_content(self.album),
                                 remove_parenthesis_content(album)) > 0.5 if is_detailed_search else True

    def is_live(self) -> bool:
        """
        Returns whether the song1 is a live version.

        Returns
        -------
        bool
            Whether the song1 is a live version.
        """
        return "live" in self.title.lower()

    def is_similar_duration(self, duration: int) -> bool:
        """
        Returns True if the duration of the song1 is within 10 seconds of the other song1 duration.

        Parameters
        ----------
        duration : int
            The other song1 duration in seconds.

        Returns
        -------
        bool
            Whether the song1 duration is similar to another song1 duration.
        """
        return abs(self.duration - duration) < 10 if self.duration is not None and duration is not None else True

    def __str__(self):
        return join_artists_names(self.artists) + " - " + self.title + " (" + self.album + ")"
