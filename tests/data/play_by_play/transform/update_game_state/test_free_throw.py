import unittest
from dataclasses import replace
from frozendict import frozendict
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import FreeThrow
from sbet.data.play_by_play.models.transform.game_state import GameState, FreeThrowState
from sbet.data.play_by_play.update_game_state import update_game_state


class TestUpdateGameStateFreeThrow(unittest.TestCase):

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

    def test_free_throw_made(self):
        state = replace(self.initial_state, free_throw_state=FreeThrowState(free_throws_remaining=1, for_home_team=True, shooting_team_gets_possession_after=False))
        play = FreeThrow(play_length=1000, play_id=3, shot_made=True)
        updated_state = update_game_state(state, play)
        self.assertEqual(updated_state.home_score, 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 719000)
        self.assertIsNone(updated_state.free_throw_state)
        self.assertFalse(updated_state.home_team_has_possession)

    def test_free_throw_missed(self):
        state = replace(self.initial_state, free_throw_state=FreeThrowState(free_throws_remaining=1, for_home_team=True, shooting_team_gets_possession_after=False))
        play = FreeThrow(play_length=1000, play_id=3, shot_made=False)
        updated_state = update_game_state(state, play)
        self.assertEqual(updated_state.home_score, 0)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 719000)
        self.assertIsNone(updated_state.free_throw_state)
        self.assertTrue(updated_state.home_team_has_possession)

    def test_free_throw_made_with_more_remaining(self):
        state = replace(self.initial_state, free_throw_state=FreeThrowState(free_throws_remaining=2, for_home_team=True, shooting_team_gets_possession_after=False))
        play = FreeThrow(play_length=1000, play_id=3, shot_made=True)
        updated_state = update_game_state(state, play)
        self.assertEqual(updated_state.home_score, 1)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 719000)
        self.assertIsNotNone(updated_state.free_throw_state)
        self.assertEqual(updated_state.free_throw_state.free_throws_remaining, 1)
        self.assertTrue(updated_state.home_team_has_possession)

    def test_free_throw_missed_with_more_remaining(self):
        state = replace(self.initial_state, free_throw_state=FreeThrowState(free_throws_remaining=2, for_home_team=True, shooting_team_gets_possession_after=False))
        play = FreeThrow(play_length=1000, play_id=3, shot_made=False)
        updated_state = update_game_state(state, play)
        self.assertEqual(updated_state.home_score, 0)
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 719000)
        self.assertIsNotNone(updated_state.free_throw_state)
        self.assertEqual(updated_state.free_throw_state.free_throws_remaining, 1)
        self.assertTrue(updated_state.home_team_has_possession)


if __name__ == '__main__':
    unittest.main()
