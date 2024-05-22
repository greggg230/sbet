import unittest
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import Rebound
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.player import Player


class TestConvertToNbaPlayRebound(unittest.TestCase):

    def setUp(self):
        self.raw_play_offensive_rebound = Play(
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
            event_type="rebound",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player="H1",
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type="rebound offensive",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Offensive rebound by H1"
        )

        self.raw_play_defensive_rebound = Play(
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
            event_type="rebound",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player="A1",
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type="rebound defensive",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Defensive rebound by A1"
        )

    def test_convert_to_nba_play_offensive_rebound(self):
        nba_play = convert_to_nba_play(self.raw_play_offensive_rebound)
        expected_play = Rebound(
            play_length=3000,
            play_id=1,
            rebounding_player=Player("H1"),
            is_offensive=True
        )
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_defensive_rebound(self):
        nba_play = convert_to_nba_play(self.raw_play_defensive_rebound)
        expected_play = Rebound(
            play_length=3000,
            play_id=1,
            rebounding_player=Player("A1"),
            is_offensive=False
        )
        self.assertEqual(nba_play, expected_play)
