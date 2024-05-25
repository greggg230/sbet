import unittest
from dataclasses import replace

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.turnover import Steal
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlaySteal(unittest.TestCase):

    def setUp(self):
        self.raw_play_steal = Play(
            game_id=42100236,
            data_set='2021-22 Playoffs',
            date='2022-05-13',
            a1='Steven Adams', a2='Tyus Jones', a3='Jaren Jackson Jr.', a4='Desmond Bane', a5='Dillon Brooks',
            h1='Kevon Looney', h2='Draymond Green', h3='Andrew Wiggins', h4='Stephen Curry', h5='Klay Thompson',
            period=1,
            away_score=4,
            home_score=5,
            remaining_time='0:08:51',
            elapsed='0:03:09',
            play_length='0:00:09',
            play_id=28,
            team='MEM',
            event_type='turnover',
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player='Steven Adams',
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal='Draymond Green',
            type='bad pass',
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description='Green STEAL (1 STL): Adams Bad Pass Turnover (P1.T1)'
        )

        self.game = Game(
            game_id=42100236,
            date="2022-05-13",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[]
        )

    def test_convert_to_nba_play_steal(self):
        self.game = replace(self.game, plays=[self.raw_play_steal])
        nba_play = convert_to_nba_play(self.raw_play_steal, self.game)
        self.assertIsInstance(nba_play, Steal)
        self.assertEqual(nba_play.play_length, 9000)
        self.assertEqual(nba_play.play_id, 28)
        self.assertEqual(nba_play.stolen_from, Player('Steven Adams'))
        self.assertEqual(nba_play.stolen_by, Player('Draymond Green'))


if __name__ == '__main__':
    unittest.main()
