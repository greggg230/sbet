import unittest
from dataclasses import replace

from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.plays import FreeThrow
from sbet.data.historical.models.transform.nba_team import NbaTeam


class TestConvertToNbaPlayFreeThrow(unittest.TestCase):

    def setUp(self):
        self.raw_play_free_throw = Play(
            game_id=1,
            data_set="",
            date="2022-01-01",
            a1="PlayerA1",
            a2="PlayerA2",
            a3="PlayerA3",
            a4="PlayerA4",
            a5="PlayerA5",
            h1="PlayerH1",
            h2="PlayerH2",
            h3="PlayerH3",
            h4="PlayerH4",
            h5="PlayerH5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="12:00:00",
            elapsed="0:00:00",
            play_length="0:00:00",
            play_id=1,
            team="GSW",
            event_type="free throw",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player="PlayerH1",
            points=1,
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
            description="Free Throw 1 of 1 by PlayerH1"
        )

        self.game = Game(
            game_id=1,
            date="2022-01-01",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[]
        )

    def test_convert_to_nba_play_free_throw_made(self):
        self.game = replace(self.game, plays=[self.raw_play_free_throw])
        nba_play = convert_to_nba_play(self.raw_play_free_throw, self.game)
        self.assertEqual(nba_play, FreeThrow(play_length=0, play_id=1, shot_made=True))

    def test_convert_to_nba_play_free_throw_missed(self):
        play = replace(self.raw_play_free_throw, result="missed")
        self.game = replace(self.game, plays=[play])
        nba_play = convert_to_nba_play(play, self.game)
        self.assertEqual(nba_play, FreeThrow(play_length=0, play_id=1, shot_made=False))


if __name__ == '__main__':
    unittest.main()
