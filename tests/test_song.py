import sys
import unittest

sys.path.insert(0, '../src')

from src.song import Song


class TestSong:
    def test_constructor(self):
        song = Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991)
        assert song.title == "Knockin' On Heaven's Door"
        assert song.artists == ["Guns N' Roses"]
        assert song.album == "Use Your Illusion II"
        assert song.duration == 336
        assert not song.is_explicit
        assert song.year == 1991

    def test_get_search_query(self):
        assert True

    def test_get_search_result(self):
        assert True

    def test_is_similar(self):
        assert True

    def test_is_similar_title(self):
        assert True

    def test_is_similar_artists(self):
        assert True

    def test_is_similar_album(self):
        assert True

    def test_is_live(self):
        assert True

    def test_is_similar_duration(self):
        assert True


if __name__ == "__main__":
    unittest.main()
