import unittest

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import FieldGoalAttempt
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayFieldGoalAttempt(unittest.TestCase):

    def setUp(self):
        self.raw_play_field_goal_attempt = Play(
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
            play_length="0:00:20",
            play_id=1,
            team="home",
            event_type="shot",
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
            points=2,
            possession=None,
            reason=None,
            result="made",
            steal=None,
            type=None,
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Made shot"
        )

    def test_convert_to_nba_play_field_goal_attempt(self):
        nba_play = convert_to_nba_play(self.raw_play_field_goal_attempt, NbaTeam.ATL, NbaTeam.BKN)
        expected_play = FieldGoalAttempt(
            play_length=20000,
            play_id=1,
            shot_made=True,
            points=2
        )
        self.assertEqual(nba_play, expected_play)
