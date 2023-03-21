from yt_music import setup_YTMusic, sync_playlists


if __name__ == "__main__":
    ytmusic = setup_YTMusic()

    playlists_dir = 'resources/playlists/'

    sync_playlists(ytmusic, playlists_dir)
