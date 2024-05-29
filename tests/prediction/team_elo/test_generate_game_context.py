import unittest
from datetime import date
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games
from sbet.prediction.team_elo.models.game_context import GameContext


class TestGenerateGameContextForGames(unittest.TestCase):

    def setUp(self):
        self.initial_elo = 1500.0
        self.k = 32
        self.games = [
            NbaGame(
                game_id=1,
                game_date=date(2024, 1, 1),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.GSW,
                away_team=NbaTeam.LAL,
                home_score=100,
                away_score=90
            ),
            NbaGame(
                game_id=2,
                game_date=date(2024, 1, 3),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.LAL,
                away_team=NbaTeam.GSW,
                home_score=90,
                away_score=100
            ),
            NbaGame(
                game_id=3,
                game_date=date(2024, 1, 5),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.GSW,
                away_team=NbaTeam.LAL,
                home_score=110,
                away_score=100
            )
        ]

    def test_generate_game_context_for_games(self):
        game_contexts = generate_game_context_for_games(self.games)

        # Check if the returned value is a dictionary
        self.assertIsInstance(game_contexts, dict)
        self.assertEqual(len(game_contexts), len(self.games))

        # Define expected GameContexts for each game
        expected_contexts = {
            self.games[0]: GameContext(
                home_team_elo=1500.0,
                away_team_elo=1500.0,
                home_team_rest_days=0,
                away_team_rest_days=0
            ),
            self.games[1]: GameContext(
                home_team_elo=1484,
                away_team_elo=1516,
                home_team_rest_days=1,
                away_team_rest_days=1
            ),
            self.games[2]: GameContext(
                home_team_elo=1530.5304984710244,
                away_team_elo=1469.4695015289756,
                home_team_rest_days=1,
                away_team_rest_days=1
            )
        }

        # Verify each game context
        for game, expected_context in expected_contexts.items():
            with self.subTest(game=game):
                context = game_contexts[game]
                self.assertEqual(context, expected_context)

    def _calculate_expected_elos(self, home_elo, away_elo, home_team_won):
        expected_win_prob_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
        if home_team_won:
            new_home_elo = home_elo + self.k * (1 - expected_win_prob_home)
            new_away_elo = away_elo - self.k * (1 - expected_win_prob_home)
        else:
            new_home_elo = home_elo - self.k * expected_win_prob_home
            new_away_elo = away_elo + self.k * expected_win_prob_home
        return new_home_elo, new_away_elo


if __name__ == '__main__':
    unittest.main()
