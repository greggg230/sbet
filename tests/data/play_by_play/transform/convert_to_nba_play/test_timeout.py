import unittest
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import Timeout
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayTimeout(unittest.TestCase):

    def setUp(self):
        self.raw_play_timeout_home = Play(
            game_id=1,
            data_set="data_set",
            date="2023-01-01",
            a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
            h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="11:00",
            elapsed="0:00:00",
            play_length="0:00:03",
            play_id=1,
            team="home",
            event_type="timeout",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player=None,
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type=None,
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Timeout by home team"
        )

        self.raw_play_timeout_away = Play(
            game_id=1,
            data_set="data_set",
            date="2023-01-01",
            a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
            h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="11:00",
            elapsed="0:00:00",
            play_length="0:00:03",
            play_id=1,
            team="away",
            event_type="timeout",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player=None,
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type=None,
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Timeout by away team"
        )

    def test_convert_to_nba_play_timeout_home(self):
        nba_play = convert_to_nba_play(self.raw_play_timeout_home)
        expected_play = Timeout(
            play_length=3000,
            play_id=1,
            is_home=True
        )
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_timeout_away(self):
        nba_play = convert_to_nba_play(self.raw_play_timeout_away)
        expected_play = Timeout(
            play_length=3000,
            play_id=1,
            is_home=False
        )
        self.assertEqual(nba_play, expected_play)
