import sys
import unittest

sys.path.insert(0, '../src')

from src.playlist import Playlist
from src.song import Song

playlist = Playlist("My Playlist", "Playlist id", "My Playlist Image URL", "My Playlist Description", [
    Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991),
    Song("Layla (Acoustic Live)", ["Eric Clapton"], "Derek and the Dominos", 480, False, 1970),
    Song("Blowin' in the Wind", ["Bob Dylan"], "The Freewheelin' Bob Dylan", 166, False, 1963),
    Song("Blowin' in the Wind", ["Peter, Paul and Mary"], "Moving", 180, False, 1963)
])


class TestPlaylist(unittest.TestCase):
    def test_constructor(self):
        assert playlist.name == "My Playlist"
        assert playlist.id == "Playlist id"
        assert playlist.description == "My Playlist Description"
        assert playlist.image == "My Playlist Image URL"
        assert playlist.songs == [
            Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991),
            Song("Layla (Acoustic Live)", ["Eric Clapton"], "Derek and the Dominos", 480, False, 1970),
            Song("Blowin' in the Wind", ["Bob Dylan"], "The Freewheelin' Bob Dylan", 166, False, 1963),
            Song("Blowin' in the Wind", ["Peter, Paul and Mary"], "Moving", 180, False, 1963)
        ]


if __name__ == '__main__':
    unittest.main()
