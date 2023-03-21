import os
import spotipy
from spotipy.client import Spotify
from dotenv import load_dotenv
from cli.bcolors import bcolors


from playlist import Playlist


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
        f"{bcolors.HEADER}Searching for {current_user['display_name']}'s playlists...{bcolors.ENDC}")

    playlists_json = spotify.current_user_playlists()
    print(
        f"{bcolors.OKBLUE}Found {playlists_json['total']} playlist(s){bcolors.ENDC}")
    playlists = []
    for playlist_json in enumerate(playlists_json['items']):
        playlist = Playlist.get_playlist_from_json(playlist_json, spotify)
        print(f"Found playlist {playlist.name} ({len(playlist.songs)} songs)")
        playlists.append(playlist)

    return playlists


if __name__ == "__main__":
    spotify: Spotify = setup_Spotipy()
    playlists = get_playlists(spotify)
