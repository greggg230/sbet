import unittest
import os
from sbet.data.play_by_play.parsing import parse_plays
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, PeriodStart, Foul, JumpBall, Rebound, Timeout
)
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.turnover import OutOfBoundsTurnover, Steal, OffensiveFoulTurnover
from sbet.data.play_by_play.update_game_state import update_game_state
from sbet.data.play_by_play.models.transform.game_state import GameState
from frozendict import frozendict


class TestIntegrationPlayByPlay(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, 'play_by_play_data', '[2022-05-13]-0042100236-MEM@GSW.csv')
        self.plays = parse_plays(self.file_path)
        self.initial_state = GameState(
            current_period=1,
            home_team_has_possession=False,
            personal_foul_count=frozendict(),
            ejected_players=frozenset(),
            home_score=0,
            away_score=0,
            milliseconds_remaining_in_period=720000,  # 12 minutes in milliseconds
            home_team_lineup=frozenset(),
            away_team_lineup=frozenset(),
            home_timeouts=7,
            away_timeouts=7
        )

    def test_integration_play_by_play(self):
        expected_plays = [
            PeriodStart(
                play_length=0,
                play_id=1,
                period_number=1,
                home_team_lineup=frozenset({Player("Kevon Looney"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry"), Player("Klay Thompson")}),
                away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Jaren Jackson Jr."), Player("Desmond Bane"), Player("Dillon Brooks")})
            ),
            JumpBall(play_length=0, play_id=2, home_player=Player("Kevon Looney"), away_player=Player("Steven Adams"), did_home_team_win=False),
            FieldGoalAttempt(play_length=20000, play_id=3, shot_made=False, points=0),
            Rebound(play_length=3000, play_id=4, rebounding_player=None, is_offensive=True),
            Foul(play_length=0, play_id=5, foul_type="loose ball", committed_by=Player("Draymond Green")),
            FieldGoalAttempt(play_length=6000, play_id=6, shot_made=False, points=0),
            Rebound(play_length=2000, play_id=7, rebounding_player=Player("Draymond Green"), is_offensive=False),
            FieldGoalAttempt(play_length=22000, play_id=8, shot_made=False, points=0),
            Rebound(play_length=2000, play_id=9, rebounding_player=Player("Tyus Jones"), is_offensive=False),
            FieldGoalAttempt(play_length=13000, play_id=10, shot_made=True, points=2),
            FieldGoalAttempt(play_length=15000, play_id=11, shot_made=False, points=0),
            Rebound(play_length=3000, play_id=12, rebounding_player=Player("Steven Adams"), is_offensive=False),
            FieldGoalAttempt(play_length=6000, play_id=13, shot_made=True, points=2),
            FieldGoalAttempt(play_length=15000, play_id=14, shot_made=True, points=3),
            FieldGoalAttempt(play_length=17000, play_id=15, shot_made=False, points=0),
            Rebound(play_length=3000, play_id=16, rebounding_player=Player("Kevon Looney"), is_offensive=False),
            FieldGoalAttempt(play_length=3000, play_id=17, shot_made=True, points=2),
            FieldGoalAttempt(play_length=9000, play_id=18, shot_made=False, points=0),
            Rebound(play_length=3000, play_id=19, rebounding_player=Player("Draymond Green"), is_offensive=False),
            Foul(play_length=5000, play_id=20, foul_type="offensive", committed_by=Player("Kevon Looney")),
            OffensiveFoulTurnover(play_length=0, play_id=21),
            FieldGoalAttempt(play_length=19000, play_id=22, shot_made=False, points=0),
            Rebound(play_length=3000, play_id=23, rebounding_player=Player("Klay Thompson"), is_offensive=False),
            FieldGoalAttempt(play_length=2000, play_id=24, shot_made=False, points=0),
            Rebound(play_length=2000, play_id=25, rebounding_player=Player("Klay Thompson"), is_offensive=True),
            FieldGoalAttempt(play_length=5000, play_id=26, shot_made=False, points=0),
            Rebound(play_length=2000, play_id=27, rebounding_player=Player("Steven Adams"), is_offensive=False),
            Steal(play_length=9000, play_id=28, stolen_from=Player("Steven Adams"), stolen_by=Player("Draymond Green")),
            FieldGoalAttempt(play_length=4000, play_id=29, shot_made=True, points=3),
            Timeout(play_length=1000, play_id=30, is_home=False)
        ]

        game_state = self.initial_state
        for play, expected in zip(self.plays[:30], expected_plays):
            nba_play = convert_to_nba_play(play)
            game_state = update_game_state(game_state, nba_play)
            with self.subTest(play_id=play.play_id):
                self.assertEqual(expected, nba_play)
                # Check score consistency
                self.assertEqual(game_state.home_score, play.home_score)
                self.assertEqual(game_state.away_score, play.away_score)
                # Check lineup consistency
                self.assertEqual(
                    game_state.home_team_lineup,
                    frozenset(Player(p) for p in [play.h1, play.h2, play.h3, play.h4, play.h5])
                )
                self.assertEqual(
                    game_state.away_team_lineup,
                    frozenset(Player(p) for p in [play.a1, play.a2, play.a3, play.a4, play.a5])
                )
                # Check period consistency
                self.assertEqual(game_state.current_period, play.period)
                # Check time remaining consistency
                h, m, s = map(int, play.remaining_time.split(':'))
                expected_remaining_time = (h * 3600 + m * 60 + s) * 1000
                self.assertEqual(game_state.milliseconds_remaining_in_period, expected_remaining_time)
