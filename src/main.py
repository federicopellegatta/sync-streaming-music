from cli.bcolors import bcolors
from spotify import get_playlists, setup_Spotipy
from yt_music import setup_YTMusic, sync_playlist
from cli.menu import main_menu, playlists_checkbox
from cli.operation import Operation


if __name__ == "__main__":
    spotify = setup_Spotipy()
    ytmusic = setup_YTMusic()

    playlists_dir = 'resources/playlists/'

    operation: Operation = main_menu()

    match operation:

        case Operation.SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY:
            print(
                f"{bcolors.HEADER}{bcolors.BOLD}{bcolors.UNDERLINE}{Operation.SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY.value}...{bcolors.ENDC}")
            playlists = get_playlists(spotify)

            playlists_to_sync = playlists_checkbox(playlists)
            for playlist in playlists_to_sync:
                sync_playlist(playlist, ytmusic)

            print(
                f"\n{bcolors.OKGREEN}{bcolors.BOLD}{len(playlists_to_sync)} playlist(s) have been synced to your YouTube Music account!{bcolors.ENDC}")

        case Operation.SYNC_SPOTIFY_PLAYLISTS_WITH_YOUTUBE:
            print(
                f"{bcolors.HEADER}{bcolors.BOLD}{bcolors.UNDERLINE}{Operation.SYNC_SPOTIFY_PLAYLISTS_WITH_YOUTUBE.value}...{bcolors.ENDC}")
            print(f"{bcolors.WARNING}Not implemented yet...{bcolors.ENDC}")

        case _:
            print("Invalid operation")
