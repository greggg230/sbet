import unittest

from frozendict import frozendict

from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import Substitution
from sbet.data.play_by_play.update_game_state import update_game_state


class TestUpdateGameStateSubstitution(unittest.TestCase):

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

    def test_substitution(self):
        play = Substitution(play_length=2000, play_id=6, home_team_lineup=frozenset({Player("H1"), Player("H2"), Player("H3"), Player("H4"), Player("H6")}), away_team_lineup=frozenset({Player("A1"), Player("A2"), Player("A3"), Player("A4"), Player("A5")}))
        updated_state = update_game_state(self.initial_state, play)
        self.assertEqual(updated_state.home_team_lineup, frozenset({Player("H1"), Player("H2"), Player("H3"), Player("H4"), Player("H6")}))
        self.assertEqual(updated_state.milliseconds_remaining_in_period, 718000)


if __name__ == '__main__':
    unittest.main()
