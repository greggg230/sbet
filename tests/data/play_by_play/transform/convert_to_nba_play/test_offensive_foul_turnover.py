import unittest

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.turnover import OffensiveFoulTurnover
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayOffensiveFoulTurnover(unittest.TestCase):

    def setUp(self):
        self.raw_play_offensive_foul_turnover = Play(
            game_id=42100236,
            data_set='2021-22 Playoffs',
            date='2022-05-13',
            a1='Steven Adams', a2='Tyus Jones', a3='Jaren Jackson Jr.', a4='Desmond Bane', a5='Dillon Brooks',
            h1='Kevon Looney', h2='Draymond Green', h3='Andrew Wiggins', h4='Stephen Curry', h5='Klay Thompson',
            period=1,
            away_score=4,
            home_score=5,
            remaining_time='0:09:33',
            elapsed='0:02:27',
            play_length='0:00:00',
            play_id=21,
            team='GSW',
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
            player='Kevon Looney',
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type='offensive foul',
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description='Looney Offensive Foul Turnover (P1.T1)'
        )

    def test_convert_to_nba_play_offensive_foul_turnover(self):
        nba_play = convert_to_nba_play(self.raw_play_offensive_foul_turnover, NbaTeam.GSW, NbaTeam.MEM)
        self.assertIsInstance(nba_play, OffensiveFoulTurnover)
        self.assertEqual(nba_play.play_length, 0)
        self.assertEqual(nba_play.play_id, 21)


if __name__ == '__main__':
    unittest.main()
