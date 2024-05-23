import unittest
from dataclasses import replace

from frozendict import frozendict

from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import Foul
from sbet.data.play_by_play.update_game_state import update_game_state


class TestUpdateGameStateFoul(unittest.TestCase):

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

    def test_foul_offensive(self):
        play = Foul(play_length=2000, play_id=2, foul_type="personal", committed_by=Player("H1"), is_offensive=True)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.personal_foul_count[Player("H1")], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)
        self.assertIsNone(updated_state.free_throw_state)

    def test_foul_defensive_non_bonus(self):
        play = Foul(play_length=2000, play_id=2, foul_type="personal", committed_by=Player("A1"), is_offensive=False)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.personal_foul_count[Player("A1")], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)
        self.assertEqual(updated_state.away_team_fouls, 1)
        self.assertIsNone(updated_state.free_throw_state)

    def test_foul_defensive_bonus(self):
        state = replace(self.initial_state, away_team_fouls=5)
        play = Foul(play_length=2000, play_id=2, foul_type="personal", committed_by=Player("A1"), is_offensive=False)
        updated_state = update_game_state(state, play)
        self.assertEqual(updated_state.personal_foul_count[Player("A1")], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)
        self.assertEqual(updated_state.away_team_fouls, 6)
        self.assertIsNotNone(updated_state.free_throw_state)
        self.assertEqual(updated_state.free_throw_state.free_throws_remaining, 2)
        self.assertTrue(updated_state.free_throw_state.for_home_team)

    def test_shooting_foul(self):
        play = Foul(play_length=2000, play_id=12, foul_type="shooting", committed_by=Player("A1"), is_offensive=False)
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.personal_foul_count[Player("A1")], 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)
        self.assertIsNotNone(updated_state.free_throw_state)
        self.assertEqual(updated_state.free_throw_state.free_throws_remaining, 2)
        self.assertTrue(updated_state.free_throw_state.for_home_team)


if __name__ == '__main__':
    unittest.main()