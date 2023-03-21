import os
import json
import time
import spotipy
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv


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


if __name__ == "__main__":
    spotify: Spotify = setup_Spotipy()

    playlists = spotify.current_user_playlists()
    for idx, playlist in enumerate(playlists['items']):
        print(playlist['name'])
