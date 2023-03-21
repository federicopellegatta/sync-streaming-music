from cli.bcolors import bcolors
from yt_music import setup_YTMusic, sync_playlists
from cli.menu import menu
from cli.operation import Operation


if __name__ == "__main__":
    ytmusic = setup_YTMusic()

    playlists_dir = 'resources/playlists/'

    operation: Operation = menu()

    match operation:
        case Operation.GET_SPOTIFY_PLAYLISTS:
            print(f"{bcolors.OKBLUE}Getting Spotify playlists...{bcolors.ENDC}")
            print(f"{bcolors.WARNING}Not implemented yet...{bcolors.ENDC}")

        case Operation.SYNC_YOUTUBE_PLAYLISTS_FROM_CSV:
            print(
                f"{bcolors.OKBLUE}Syncing YouTube playlists from CSV files...{bcolors.ENDC}")
            sync_playlists(ytmusic, playlists_dir)

        case Operation.SYNC_YOUTUBE_PLAYLISTS_WITH_SPOTIFY:
            print(
                f"{bcolors.OKBLUE}Syncing YouTube playlists with Spotify...{bcolors.ENDC}")
            print(f"{bcolors.WARNING}Not implemented yet...{bcolors.ENDC}")

        case _:
            print("Invalid operation")
