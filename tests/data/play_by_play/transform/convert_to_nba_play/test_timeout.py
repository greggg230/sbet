import unittest
from dataclasses import replace

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.plays import Timeout
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayTimeout(unittest.TestCase):
    def setUp(self):
        self.home_team = NbaTeam.GSW
        self.away_team = NbaTeam.MEM
        self.raw_play = Play(
            game_id=42100236, data_set="2021-22 Playoffs", date="2022-05-13",
            a1="Steven Adams", a2="Tyus Jones", a3="Jaren Jackson Jr.", a4="Desmond Bane", a5="Dillon Brooks",
            h1="Kevon Looney", h2="Draymond Green", h3="Andrew Wiggins", h4="Stephen Curry", h5="Klay Thompson",
            period=1, away_score=0, home_score=0, remaining_time="0:10:00", elapsed="0:01:00", play_length="0:00:15",
            play_id=1, team="GSW", event_type="timeout", assist=None, away=None, home=None,
            block=None, entered=None, left=None, num=None, opponent=None, outof=None, player=None,
            points=None, possession=None, reason=None, result=None, steal=None, type=None,
            shot_distance=None, original_x=None, original_y=None, converted_x=None, converted_y=None,
            description="Timeout: Golden State Warriors"
        )
        self.game = Game(
            game_id=42100236,
            date="2022-05-13",
            home_team=self.home_team,
            away_team=self.away_team,
            plays=[self.raw_play]
        )

    def test_convert_to_nba_play_timeout_home(self):
        nba_play = convert_to_nba_play(self.raw_play, self.game)
        expected_play = Timeout(play_length=15000, play_id=1, is_home=True)
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_timeout_away(self):
        raw_play = Play(
            game_id=42100236, data_set="2021-22 Playoffs", date="2022-05-13",
            a1="Steven Adams", a2="Tyus Jones", a3="Jaren Jackson Jr.", a4="Desmond Bane", a5="Dillon Brooks",
            h1="Kevon Looney", h2="Draymond Green", h3="Andrew Wiggins", h4="Stephen Curry", h5="Klay Thompson",
            period=1, away_score=0, home_score=0, remaining_time="0:09:45", elapsed="0:01:15", play_length="0:00:15",
            play_id=2, team="MEM", event_type="timeout", assist=None, away=None, home=None,
            block=None, entered=None, left=None, num=None, opponent=None, outof=None, player=None,
            points=None, possession=None, reason=None, result=None, steal=None, type=None,
            shot_distance=None, original_x=None, original_y=None, converted_x=None, converted_y=None,
            description="Timeout: Memphis Grizzlies"
        )
        another_game = replace(self.game, plays=[raw_play])
        nba_play = convert_to_nba_play(raw_play, another_game)
        expected_play = Timeout(play_length=15000, play_id=2, is_home=False)
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()
