import unittest
import os
from typing import List
from frozendict import frozendict
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.parsing import parse_plays
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.update_game_state import update_game_state
from integration_tests.play_by_play.expected_plays import expected_plays
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay


class TestIntegrationPlayByPlay(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, 'data', '[2022-05-13]-0042100236-MEM@GSW.csv')
        self.plays: List[Play] = parse_plays(self.file_path)

    def test_integration_play_by_play(self):
        nba_plays: List[NbaPlay] = [convert_to_nba_play(play) for play in self.plays[:len(expected_plays)]]

        initial_state = GameState(
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

        current_state = initial_state

        expected: NbaPlay
        actual: NbaPlay
        play: Play

        for expected, actual, play in zip(expected_plays, nba_plays, self.plays[:len(expected_plays)]):
            with self.subTest(play_id=actual.play_id):
                self.assertEqual(expected, actual)

                # Update game state
                current_state = update_game_state(current_state, actual)

                # Consistency checks
                self.assertEqual(current_state.home_score, play.home_score)
                self.assertEqual(current_state.away_score, play.away_score)

                # Check lineups
                expected_home_lineup = frozenset({Player(play.h1), Player(play.h2), Player(play.h3), Player(play.h4), Player(play.h5)})
                expected_away_lineup = frozenset({Player(play.a1), Player(play.a2), Player(play.a3), Player(play.a4), Player(play.a5)})
                self.assertEqual(current_state.home_team_lineup, expected_home_lineup)
                self.assertEqual(current_state.away_team_lineup, expected_away_lineup)

                # Check period
                self.assertEqual(current_state.current_period, play.period)

                # Check remaining time
                remaining_time_parts = play.remaining_time.split(":")
                expected_remaining_time = (int(remaining_time_parts[0]) * 3600 + int(remaining_time_parts[1]) * 60 + int(remaining_time_parts[2])) * 1000
                self.assertEqual(current_state.milliseconds_remaining_in_period, expected_remaining_time)
