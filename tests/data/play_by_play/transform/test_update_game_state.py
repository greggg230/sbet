import unittest


from frozendict import frozendict
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Foul, JumpBall, PeriodStart, Rebound, Substitution, Timeout
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoul
)
from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.update_game_state import update_game_state


class TestUpdateGameState(unittest.TestCase):

    def setUp(self):
        self.initial_state = GameState(
            current_period=1,
            home_team_has_possession=True,
            personal_foul_count=frozendict(),
            ejected_players=frozenset(),
            home_score=0,
            away_score=0,
            milliseconds_remaining_in_period=720000,
            home_team_lineup=frozenset({Player("H1"), Player("H2"), Player("H3"), Player("H4"), Player("H5")}),
            away_team_lineup=frozenset({Player("A1"), Player("A2"), Player("A3"), Player("A4"), Player("A5")}),
            home_timeouts=7,
            away_timeouts=7
        )

    def test_field_goal_attempt(self):
        play = FieldGoalAttempt(play_length=2000, play_id=1, shot_made=True, points=2)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_score, 2)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_foul(self):
        play = Foul(play_length=2000, play_id=2, foul_type="personal", committed_by=Player("H1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.personal_foul_count[Player("H1")], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_jump_ball(self):
        play = JumpBall(play_length=2000, play_id=3, home_player=Player("H1"), away_player=Player("A1"), did_home_team_win=True)
        updated_state = update_game_state(self.initial_state, play)
        self.assertTrue(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_period_start(self):
        play = PeriodStart(play_length=0, play_id=4, period_number=2)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.current_period, 2)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 720000)

    def test_rebound_offensive(self):
        play = Rebound(play_length=2000, play_id=5, rebounding_player=Player("H1"), is_offensive=True)
        updated_state = update_game_state(self.initial_state, play)
        self.assertTrue(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_rebound_defensive(self):
        play = Rebound(play_length=2000, play_id=5, rebounding_player=Player("A1"), is_offensive=False)
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_substitution(self):
        play = Substitution(play_length=2000, play_id=6, home_team_lineup=frozenset({Player("H1"), Player("H2"), Player("H3"), Player("H4"), Player("H6")}), away_team_lineup=frozenset({Player("A1"), Player("A2"), Player("A3"), Player("A4"), Player("A5")}))
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_team_lineup, frozenset({Player("H1"), Player("H2"), Player("H3"), Player("H4"), Player("H6")}))
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_timeout(self):
        play = Timeout(play_length=2000, play_id=7, is_home=True)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_timeouts, 6)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_steal(self):
        play = Steal(play_length=2000, play_id=8, stolen_from=Player("A1"), stolen_by=Player("H1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertTrue(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_shot_clock_violation(self):
        play = ShotClockViolation(play_length=2000, play_id=9)
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_out_of_bounds_turnover(self):
        play = OutOfBoundsTurnover(play_length=2000, play_id=10, player=Player("H1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)

    def test_offensive_foul(self):
        play = OffensiveFoul(play_length=2000, play_id=11, fouling_player=Player("H1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)
