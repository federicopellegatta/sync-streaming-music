"""This module contains the sync functions between different music streaming services"""
from spotipy.client import Spotify
from ytmusicapi import YTMusic

from cli.bcolors import bcolors
from cli.menu import playlists_checkbox
from cli.operation import Operation
from spotify import get_playlists
from yt_music import sync_playlist


def sync_spotify_to_ytmusic(spotify: Spotify, ytmusic: YTMusic) -> None:
    """
    Syncs all Spotify playlists to the YouTube Music account.

    Parameters
    ----------
    spotify : Spotify
        The Spotify object to use for the API calls.
    ytmusic : YTMusic
        The YTMusic object to use for the API calls.
    """
    print(f"{bcolors.HEADER}{bcolors.BOLD}{bcolors.UNDERLINE}"
          f"{Operation.SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY.value}..."
          f"{bcolors.ENDC}")
    playlists = get_playlists(spotify)

    playlists_to_sync = playlists_checkbox(playlists)
    for playlist in playlists_to_sync:
        sync_playlist(playlist, ytmusic)

    print(f"\n{bcolors.OKGREEN}{bcolors.BOLD}"
          f"{len(playlists_to_sync)} playlist(s) have been synced to your YouTube Music account!"
          f"{bcolors.ENDC}")
