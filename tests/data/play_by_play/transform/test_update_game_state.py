import unittest

from frozendict import frozendict

from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Substitution, PeriodStart, PeriodEnd, Timeout, Foul, JumpBall
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoul
)
from sbet.data.play_by_play.update_game_state import update_game_state, UnrecognizedPlayException


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
            home_team_lineup=frozenset({Player("Home Player 1"), Player("Home Player 2")}),
            away_team_lineup=frozenset({Player("Away Player 1"), Player("Away Player 2")}),
            home_timeouts=3,
            away_timeouts=3
        )

    def test_field_goal_attempt_made(self):
        play = FieldGoalAttempt(play_length=5000, play_id="1", description="Made 3-point shot", shot_made=True, points=3)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_score, 3)
        self.assertEqual(updated_state.away_score, 0)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 715000)

    def test_field_goal_attempt_missed(self):
        play = FieldGoalAttempt(play_length=5000, play_id="2", description="Missed shot", shot_made=False, points=0)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_score, 0)
        self.assertEqual(updated_state.away_score, 0)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 715000)

    def test_substitution(self):
        play = Substitution(play_length=2000, play_id="3", description="Substitution",
                            home_team_lineup=frozenset({Player("Home Player 1"), Player("Home Player 3")}),
                            away_team_lineup=frozenset({Player("Away Player 1"), Player("Away Player 3")}))
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_team_lineup, frozenset({Player("Home Player 1"), Player("Home Player 3")}))
        self.assertEqual(updated_state.away_team_lineup, frozenset({Player("Away Player 1"), Player("Away Player 3")}))
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_period_start(self):
        play = PeriodStart(play_length=0, play_id="4", description="Start of period", period_number=2)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.current_period, 2)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 720000)

    def test_period_end(self):
        play = PeriodEnd(play_length=0, play_id="5", description="End of period", period_number=1)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 0)

    def test_timeout_home(self):
        play = Timeout(play_length=1000, play_id="6", description="Timeout", is_home=True)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_timeouts, 2)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 719000)

    def test_timeout_away(self):
        play = Timeout(play_length=1000, play_id="7", description="Timeout", is_home=False)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.away_timeouts, 2)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 719000)

    def test_foul(self):
        player = Player("Player A")
        play = Foul(play_length=3000, play_id="8", description="Foul", foul_type="personal", committed_by=player)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.personal_foul_count[player], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 717000)

    def test_jump_ball(self):
        play = JumpBall(play_length=5000, play_id="9", description="Jump ball", home_player=Player("Home Player 1"), away_player=Player("Away Player 1"), did_home_team_win=True)
        updated_state = update_game_state(self.initial_state, play)
        self.assertTrue(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 715000)

    def test_steal(self):
        play = Steal(play_length=4000, play_id="10", description="Steal", stolen_from=Player("Away Player 1"), stolen_by=Player("Home Player 1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 716000)

    def test_shot_clock_violation(self):
        play = ShotClockViolation(play_length=24000, play_id="11", description="Shot clock violation")
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 696000)

    def test_out_of_bounds_turnover(self):
        play = OutOfBoundsTurnover(play_length=3000, play_id="12", description="Out of bounds", player=Player("Home Player 1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 717000)

    def test_offensive_foul(self):
        fouling_player = Player("Player B")
        fouled_player = Player("Player C")
        play = OffensiveFoul(play_length=3000, play_id="13", description="Offensive foul", fouling_player=fouling_player, fouled_player=fouled_player)
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.personal_foul_count[fouling_player], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 717000)

    def test_unrecognized_play_exception(self):
        class UnknownPlay(NbaPlay):
            pass
        play = UnknownPlay(play_length=5000, play_id="14", description="Unknown play")
        with self.assertRaises(UnrecognizedPlayException):
            update_game_state(self.initial_state, play)


if __name__ == '__main__':
    unittest.main()
