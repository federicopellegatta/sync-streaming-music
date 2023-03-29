import json
import sys
import unittest

sys.path.insert(0, '../src')

from src.song import Song, join_artists_names, get_song_from_spotify_json, get_song_from_ytmusic_json
from src.utils.file_utils import get_json_from_file

song1 = Song("Knockin' On Heaven's Door", ["Guns N' Roses"], "Use Your Illusion II", 336, False, 1991)
song2 = Song("Layla (Acoustic Live)", ["Eric Clapton"], "Derek and the Dominos", 480, False, 1970)
song3 = Song("Blowin' in the Wind", ["Bob Dylan"], "The Freewheelin' Bob Dylan", 166, False, 1963)
song4 = Song("Blowin' in the Wind", ["Peter, Paul and Mary"], "Moving", 180, False, 1963)


class TestSong(unittest.TestCase):

    def test_constructor(self):
        assert song1.title == "Knockin' On Heaven's Door"
        assert song1.artists == ["Guns N' Roses"]
        assert song1.album == "Use Your Illusion II"
        assert song1.duration == 336
        assert not song1.is_explicit
        assert song1.year == 1991

    def test_get_search_query(self):
        assert song1.get_search_query() == "Guns N' Roses - Knockin' On Heaven's Door (Use Your Illusion II)"
        assert not song1.get_search_query() == "Guns N' Roses - Knockin' On Heaven's Door Use Your Illusion II"
        assert song3.get_search_query() == "Bob Dylan - Blowin' in the Wind (The Freewheelin' Bob Dylan)"
        assert song4.get_search_query() == "Peter, Paul and Mary - Blowin' in the Wind (Moving)"

    def test_is_similar(self):
        assert not song3.is_similar(song4)
        assert song3.is_similar(song3)

    def test_is_similar_title(self):
        assert song3.is_similar_title(song4.title)
        assert not song3.is_similar_title(song1.title)

    def test_is_similar_artists(self):
        assert song1.is_similar_artists(song1.artists)
        assert not song3.is_similar_artists(song4.artists)
        assert not song3.is_similar_artists(["Bob Dylan", "Peter, Paul and Mary"], is_detailed_search=True)
        assert song3.is_similar_artists(["Bob Dylan", "Peter, Paul and Mary"], is_detailed_search=False)

    def test_is_similar_album(self):
        assert song1.is_similar_album(song1.album)
        assert not song3.is_similar_album(song4.album)

    def test_is_live(self):
        assert song2.is_live()
        assert not song1.is_live()

    def test_is_similar_duration(self):
        assert song1.is_similar_duration(song1.duration)
        assert song1.is_similar_duration(song1.duration + 1)
        assert song1.is_similar_duration(song1.duration - 1)
        assert not song2.is_similar_duration(song2.duration + 10)
        assert not song2.is_similar_duration(song2.duration - 10)

    def test_is_similar_year(self):
        assert song1.is_similar_year(song1.year)
        assert not song1.is_similar_year(song1.year + 1)
        assert not song1.is_similar_year(song1.year - 1)
        assert song1.is_similar_year(None)



def test_join_artists_names():
    assert join_artists_names([]) == ""
    assert join_artists_names(["Bob Dylan"]) == "Bob Dylan"
    assert join_artists_names(["Bob Dylan", "Eric Clapton"]) == "Bob Dylan, Eric Clapton"


def test_get_song_from_spotify_json():
    track_json: json = get_json_from_file("./tests/resources/spotify_track_json_output.json")
    song_from_json: Song = get_song_from_spotify_json(track_json)

    assert song1.is_similar_title(song_from_json.title)
    assert song1.is_similar_artists(song_from_json.artists)
    assert song1.is_similar_album(song_from_json.album)
    assert song1.is_similar_duration(song_from_json.duration)
    assert song1.is_explicit == song_from_json.is_explicit
    assert song1.is_similar_year(song_from_json.year)


def test_get_song_from_ytmusic_json():
    track_json: json = get_json_from_file("./tests/resources/ytmusic_track_json_output.json")
    song_from_json: Song = get_song_from_ytmusic_json(track_json)

    assert song1.is_similar_title(song_from_json.title)
    assert song1.is_similar_artists(song_from_json.artists)
    assert song1.is_similar_album(song_from_json.album)
    assert song1.is_similar_duration(song_from_json.duration)
    assert song1.is_explicit == song_from_json.is_explicit
    assert song1.is_similar_year(song_from_json.year)


if __name__ == "__main__":
    unittest.main()
