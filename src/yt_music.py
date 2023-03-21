from ytmusicapi import YTMusic
import pandas as pd
import os
from song import Song
from utils.bcolors import bcolors
from utils.string_utils import title_case
from dotenv import load_dotenv


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def setup_YTMusic() -> YTMusic:
    load_dotenv()

    header_raw = os.getenv('HEADER_RAW')
    header_json_path = "./resources/headers_auth.json"
    YTMusic.setup(filepath=header_json_path, headers_raw=header_raw)
    ytmusic = YTMusic(header_json_path)
    os.remove(header_json_path)
    return ytmusic


def search_matches(df: pd.DataFrame, ytmusic: YTMusic) -> list:
    songs_to_sync = []
    for index, row in df.iterrows():
        song = Song.get_song_from_csv_row(row)

        print("Looking for matches for " + str(song))
        search_result = song.get_search_result(ytmusic)
        if (search_result is None):
            print(
                f"{bcolors.WARNING}WARNING: No match found for track nr. {str(index + 1)}: {str(song)}{bcolors.ENDC}")
        else:
            songs_to_sync.append(search_result)

    return songs_to_sync


def sync_playlists(ytmusic: YTMusic, playlists_dir: str) -> None:
    for filename in os.scandir(playlists_dir):
        if not filename.is_file() or not filename.name.endswith('.csv'):
            print(
                f"{bcolors.FAIL}Warning: Skipping {filename.name}...{bcolors.ENDC}")
            continue
        else:
            playlist_name = title_case(filename.name[:-4])
            print(
                f"{bcolors.HEADER}Reading {filename.name}...{bcolors.ENDC}")

            df = pd.read_csv(playlists_dir + filename.name).reset_index()
            songs_to_sync = search_matches(df, ytmusic)

            print(
                f"{bcolors.OKCYAN}{len(songs_to_sync)}/{len(df.index)} result(s) have been found for the playlist {playlist_name}{bcolors.ENDC}")

            print("Creating playlist " + playlist_name + "...")
            playlistId = ytmusic.create_playlist(
                playlist_name, "Playlist description")

            print("Syncing playlist " + playlist_name + "...")
            ytmusic.add_playlist_items(playlistId, map(
                lambda song: song["videoId"], songs_to_sync))

            print(
                f"{bcolors.OKGREEN}The {playlist_name} playlist has been synced!{bcolors.ENDC}")
