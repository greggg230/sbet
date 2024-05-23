import unittest

from frozendict import frozendict

from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoulTurnover
)
from sbet.data.play_by_play.update_game_state import update_game_state


class TestUpdateGameStateTurnover(unittest.TestCase):

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
            away_timeouts=7,
            home_team_fouls=0,
            away_team_fouls=0,
            home_team_fouls_in_last_two_minutes=0,
            away_team_fouls_in_last_two_minutes=0,
            free_throw_state=None
        )

    def test_steal(self):
        play = Steal(play_length=2000, play_id=8, stolen_from=Player("A1"), stolen_by=Player("H1"))
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
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
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)

    def test_offensive_foul_turnover(self):
        play = OffensiveFoulTurnover(play_length=2000, play_id=11)
        updated_state = update_game_state(self.initial_state, play)
        self.assertFalse(updated_state.home_team_has_possession)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)


if __name__ == '__main__':
    unittest.main()
