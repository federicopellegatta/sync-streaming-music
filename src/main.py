from cli.bcolors import bcolors
from spotify import setup_Spotipy
from sync import sync_spotify_to_ytmusic
from yt_music import setup_YTMusic
from cli.menu import main_menu
from cli.operation import Operation


if __name__ == "__main__":
    spotify = setup_Spotipy()
    ytmusic = setup_YTMusic()

    playlists_dir = 'resources/playlists/'

    operation: Operation = main_menu()

    match operation:

        case Operation.SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY:
            sync_spotify_to_ytmusic(spotify, ytmusic)

        case Operation.SYNC_SPOTIFY_PLAYLISTS_WITH_YOUTUBE:
            print(
                f"{bcolors.HEADER}{bcolors.BOLD}{bcolors.UNDERLINE}{Operation.SYNC_SPOTIFY_PLAYLISTS_WITH_YOUTUBE.value}...{bcolors.ENDC}")
            print(f"{bcolors.WARNING}Not implemented yet...{bcolors.ENDC}")

        case _:
            print("Invalid operation")
