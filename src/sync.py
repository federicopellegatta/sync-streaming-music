from cli.bcolors import bcolors
from ytmusicapi import YTMusic
from spotipy.client import Spotify
from cli.operation import Operation


def sync_spotify_to_ytmusic(spotify: Spotify, ytmusic: YTMusic):
    print(f"{bcolors.HEADER}{bcolors.BOLD}{bcolors.UNDERLINE}{Operation.SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY.value}...{bcolors.ENDC}")
    playlists = get_playlists(spotify)

    playlists_to_sync = playlists_checkbox(playlists)
    for playlist in playlists_to_sync:
        sync_playlist(playlist, ytmusic)

    print(f"\n{bcolors.OKGREEN}{bcolors.BOLD}{len(playlists_to_sync)} playlist(s) have been synced to your YouTube Music account!{bcolors.ENDC}")
