import sys
import unittest

sys.path.insert(0, '../src')

from src.song import Song


class TestSong(unittest.TestCase):
    song1 = Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991)
    song2 = Song("Layla (Acoustic Live)", ["Eric Clapton"], "Derek and the Dominos", 480, False, 1970)
    song3 = Song("Blowin' in the Wind", ["Bob Dylan"], "The Freewheelin' Bob Dylan", 166, False, 1963)
    song4 = Song("Blowin' in the Wind", ["Peter, Paul and Mary"], "Moving", 180, False, 1963)

    def test_constructor(self):
        assert self.song1.title == "Knockin' On Heaven's Door"
        assert self.song1.artists == ["Guns N' Roses"]
        assert self.song1.album == "Use Your Illusion II"
        assert self.song1.duration == 336
        assert not self.song1.is_explicit
        assert self.song1.year == 1991

    def test_get_search_query(self):
        assert self.song1.get_search_query() == "Guns N' Roses - Knockin' On Heaven's Door (Use Your Illusion II)"
        assert not self.song1.get_search_query() == "Guns N' Roses - Knockin' On Heaven's Door Use Your Illusion II"
        assert self.song3.get_search_query() == "Bob Dylan - Blowin' in the Wind (The Freewheelin' Bob Dylan)"
        assert self.song4.get_search_query() == "Peter, Paul and Mary - Blowin' in the Wind (Moving)"

    def test_is_similar(self):
        assert not self.song3.is_similar(self.song4)
        assert self.song3.is_similar(self.song3)

    def test_is_similar_title(self):
        assert self.song3.is_similar_title(self.song4.title)
        assert not self.song3.is_similar_title(self.song1.title)

    def test_is_similar_artists(self):
        assert self.song1.is_similar_artists(self.song1.artists)
        assert not self.song3.is_similar_artists(self.song4.artists)
        assert not self.song3.is_similar_artists(["Bob Dylan", "Peter, Paul and Mary"], is_detailed_search=True)
        assert self.song3.is_similar_artists(["Bob Dylan", "Peter, Paul and Mary"], is_detailed_search=False)

    def test_is_similar_album(self):
        assert self.song1.is_similar_album(self.song1.album)
        assert not self.song3.is_similar_album(self.song4.album)

    def test_is_live(self):
        assert self.song2.is_live()
        assert not self.song1.is_live()

    def test_is_similar_duration(self):
        assert self.song1.is_similar_duration(self.song1.duration)
        assert self.song1.is_similar_duration(self.song1.duration + 1)
        assert self.song1.is_similar_duration(self.song1.duration - 1)
        assert not self.song2.is_similar_duration(self.song2.duration + 10)
        assert not self.song2.is_similar_duration(self.song2.duration - 10)


if __name__ == "__main__":
    unittest.main()
