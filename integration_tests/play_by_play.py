import unittest
import os
from sbet.data.play_by_play.parsing import parse_plays
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, PeriodStart, Foul, JumpBall, Rebound
)
from sbet.data.play_by_play.models.transform.player import Player


class TestIntegrationPlayByPlay(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, 'play_by_play_data', '[2022-05-13]-0042100236-MEM@GSW.csv')
        self.plays = parse_plays(self.file_path)

    def test_integration_play_by_play(self):
        expected_plays = [
            PeriodStart(play_length=0, play_id=1, period_number=1),
            JumpBall(play_length=0, play_id=2, home_player=Player("Kevon Looney"), away_player=Player("Steven Adams"), did_home_team_win=False),
            FieldGoalAttempt(play_length=20000, play_id=3, shot_made=False, points=0),
            Rebound(play_length=3000, play_id=4, rebounding_player=None, is_offensive=True),
            Foul(play_length=0, play_id=5, foul_type="loose ball", committed_by=Player("Draymond Green")),
            FieldGoalAttempt(play_length=6000, play_id=6, shot_made=False, points=0),
            Rebound(play_length=2000, play_id=7, rebounding_player=Player("Draymond Green"), is_offensive=False),
            FieldGoalAttempt(play_length=22000, play_id=8, shot_made=False, points=0),
            Rebound(play_length=2000, play_id=9, rebounding_player=Player("Tyus Jones"), is_offensive=False),
            FieldGoalAttempt(play_length=13000, play_id=10, shot_made=True, points=2)
        ]

        nba_plays = [convert_to_nba_play(play) for play in self.plays[:10]]

        for expected, actual in zip(expected_plays, nba_plays):
            with self.subTest(play_id=actual.play_id):
                self.assertEqual(expected, actual)

