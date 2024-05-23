import unittest

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import Foul
from sbet.data.play_by_play.models.transform.player import Player


class TestConvertToNbaPlayFoul(unittest.TestCase):

    def setUp(self):
        self.raw_play_foul = Play(
            game_id=1,
            data_set="test",
            date="2022-01-01",
            a1="A1",
            a2="A2",
            a3="A3",
            a4="A4",
            a5="A5",
            h1="H1",
            h2="H2",
            h3="H3",
            h4="H4",
            h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="0:11:00",
            elapsed="0:01:00",
            play_length="0:00:20",
            play_id=1,
            team="home",
            event_type="foul",
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
            type="personal",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Personal foul on H1"
        )

        self.raw_play_offensive_foul = Play(
            game_id=1,
            data_set="test",
            date="2022-01-01",
            a1="A1",
            a2="A2",
            a3="A3",
            a4="A4",
            a5="A5",
            h1="H1",
            h2="H2",
            h3="H3",
            h4="H4",
            h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="0:10:00",
            elapsed="0:02:00",
            play_length="0:00:20",
            play_id=2,
            team="home",
            event_type="foul",
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
            type="offensive",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Offensive foul on H1"
        )

    def test_convert_to_nba_play_foul(self):
        nba_play = convert_to_nba_play(self.raw_play_foul, NbaTeam.ATL, NbaTeam.BKN)
        expected_play = Foul(play_length=20000, play_id=1, foul_type="personal", committed_by=Player("H1"), is_offensive=False)
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_offensive_foul(self):
        nba_play = convert_to_nba_play(self.raw_play_offensive_foul, NbaTeam.ATL, NbaTeam.BKN)
        expected_play = Foul(play_length=20000, play_id=2, foul_type="offensive", committed_by=Player("H1"), is_offensive=True)
        self.assertEqual(nba_play, expected_play)
