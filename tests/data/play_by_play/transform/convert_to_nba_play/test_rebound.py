import unittest

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import Rebound
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.player import Player


class TestConvertToNbaPlayRebound(unittest.TestCase):

    def setUp(self):
        self.raw_play_offensive_rebound = Play(
            game_id=42100236,
            data_set='2021-22 Playoffs',
            date='2022-05-13',
            a1='Steven Adams', a2='Tyus Jones', a3='Jaren Jackson Jr.', a4='Desmond Bane', a5='Dillon Brooks',
            h1='Kevon Looney', h2='Draymond Green', h3='Andrew Wiggins', h4='Stephen Curry', h5='Klay Thompson',
            period=1,
            away_score=7,
            home_score=13,
            remaining_time='0:06:49',
            elapsed='0:05:11',
            play_length='0:00:02',
            play_id=41,
            team='GSW',
            event_type='rebound',
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
            type='rebound offensive',
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description='Looney REBOUND (Off:2 Def:1)'
        )

        self.raw_play_team_rebound = Play(
            game_id=42100236,
            data_set='2021-22 Playoffs',
            date='2022-05-13',
            a1='Steven Adams', a2='Tyus Jones', a3='Jaren Jackson Jr.', a4='Desmond Bane', a5='Dillon Brooks',
            h1='Kevon Looney', h2='Draymond Green', h3='Andrew Wiggins', h4='Stephen Curry', h5='Klay Thompson',
            period=1,
            away_score=7,
            home_score=13,
            remaining_time='0:06:49',
            elapsed='0:05:11',
            play_length='0:00:00',
            play_id=49,
            team='MEM',
            event_type='rebound',
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
            type='team rebound',
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description='Grizzlies Rebound'
        )

        self.raw_play_defensive_rebound = Play(
            game_id=42100236,
            data_set='2021-22 Playoffs',
            date='2022-05-13',
            a1='Steven Adams', a2='Tyus Jones', a3='Jaren Jackson Jr.', a4='Desmond Bane', a5='Dillon Brooks',
            h1='Kevon Looney', h2='Draymond Green', h3='Andrew Wiggins', h4='Stephen Curry', h5='Klay Thompson',
            period=1,
            away_score=7,
            home_score=13,
            remaining_time='0:06:49',
            elapsed='0:05:11',
            play_length='0:00:02',
            play_id=45,
            team='GSW',
            event_type='rebound',
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
            type='rebound defensive',
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description='Looney REBOUND (Off:2 Def:2)'
        )

    def test_convert_to_nba_play_offensive_rebound(self):
        nba_play = convert_to_nba_play(self.raw_play_offensive_rebound, NbaTeam.GSW, NbaTeam.MEM)
        self.assertIsInstance(nba_play, Rebound)
        self.assertEqual(nba_play.play_length, 2000)
        self.assertEqual(nba_play.play_id, 41)
        self.assertEqual(nba_play.rebounding_player, Player("Kevon Looney"))
        self.assertTrue(nba_play.is_offensive)

    def test_convert_to_nba_play_team_rebound(self):
        nba_play = convert_to_nba_play(self.raw_play_team_rebound, NbaTeam.GSW, NbaTeam.MEM)
        self.assertIsInstance(nba_play, Rebound)
        self.assertEqual(nba_play.play_length, 0)
        self.assertEqual(nba_play.play_id, 49)
        self.assertIsNone(nba_play.rebounding_player)
        self.assertTrue(nba_play.is_offensive)

    def test_convert_to_nba_play_defensive_rebound(self):
        nba_play = convert_to_nba_play(self.raw_play_defensive_rebound, NbaTeam.GSW, NbaTeam.MEM)
        self.assertIsInstance(nba_play, Rebound)
        self.assertEqual(nba_play.play_length, 2000)
        self.assertEqual(nba_play.play_id, 45)
        self.assertEqual(nba_play.rebounding_player, Player("Kevon Looney"))
        self.assertFalse(nba_play.is_offensive)
