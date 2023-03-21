from enum import Enum


class Operation(Enum):
    GET_SPOTIFY_PLAYLISTS = 'Get Spotify playlists'
    SYNC_YOUTUBE_PLAYLISTS_FROM_CSV = 'Create YouTube playlist from CSV files'
    SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY = 'Sync YouTube Music playlists from Spotify'
