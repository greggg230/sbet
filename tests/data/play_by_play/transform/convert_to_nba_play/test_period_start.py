import unittest
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import PeriodStart
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.player import Player


class TestConvertToNbaPlayPeriodStart(unittest.TestCase):

    def setUp(self):
        self.raw_play_period_start = Play(
            game_id=1,
            data_set="2021-22 Playoffs",
            date="2022-05-13",
            a1="Steven Adams", a2="Tyus Jones", a3="Jaren Jackson Jr.", a4="Desmond Bane", a5="Dillon Brooks",
            h1="Kevon Looney", h2="Draymond Green", h3="Andrew Wiggins", h4="Stephen Curry", h5="Klay Thompson",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="12:00",
            elapsed="0:00:00",
            play_length="0:00:00",
            play_id=1,
            team="",
            event_type="start of period",
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
            description="Start of period"
        )

    def test_convert_to_nba_play_period_start(self):
        nba_play = convert_to_nba_play(self.raw_play_period_start)
        expected_play = PeriodStart(
            play_length=0,
            play_id=1,
            period_number=1,
            home_team_lineup=frozenset({
                Player("Kevon Looney"),
                Player("Draymond Green"),
                Player("Andrew Wiggins"),
                Player("Stephen Curry"),
                Player("Klay Thompson")
            }),
            away_team_lineup=frozenset({
                Player("Steven Adams"),
                Player("Tyus Jones"),
                Player("Jaren Jackson Jr."),
                Player("Desmond Bane"),
                Player("Dillon Brooks")
            })
        )
        self.assertEqual(nba_play, expected_play)
