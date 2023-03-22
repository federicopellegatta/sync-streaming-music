import os
import spotipy
from spotipy.client import Spotify
from dotenv import load_dotenv
from cli.bcolors import bcolors


from playlist import Playlist, get_playlist_from_spotify


def setup_Spotipy() -> Spotify:
    load_dotenv()
    client_id: str = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret: str = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri: str = os.getenv('SPOTIPY_REDIRECT_URI')

    # maybe add playlist-modify-public playlist-modify-private
    scope = "playlist-read-private playlist-read-collaborative user-library-read"

    # spotify authentication
    oauth = spotipy.SpotifyOAuth(client_id, client_secret, redirect_uri, scope)
    return spotipy.Spotify(auth_manager=oauth)


def get_playlists(spotify: Spotify) -> list[Playlist]:
    current_user = spotify.current_user()
    print(
        f"{bcolors.OKCYAN}Searching for {current_user['display_name']}'s playlists...{bcolors.ENDC}")

    playlists_json = spotify.current_user_playlists()
    number_of_playlists = playlists_json['total']
    print(f"{bcolors.BOLD}Found {number_of_playlists} playlist(s):{bcolors.ENDC}")

    right_justify = len(str(number_of_playlists))
    playlists = []
    for idx, playlist_json in enumerate(playlists_json['items']):
        playlist = get_playlist_from_spotify(playlist_json, spotify)
        print(
            f"{str(idx + 1).rjust(right_justify)}. {playlist.name} ({len(playlist.songs)} songs)")
        playlists.append(playlist)

    return playlists
