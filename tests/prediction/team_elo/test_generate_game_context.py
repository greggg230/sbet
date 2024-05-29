import unittest
from datetime import date
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games
from sbet.prediction.team_elo.models.game_context import GameContext


class TestGenerateGameContextForGames(unittest.TestCase):

    def setUp(self):
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
                game_date=date(2024, 1, 4),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.LAL,
                away_team=NbaTeam.GSW,
                home_score=95,
                away_score=105
            ),
            NbaGame(
                game_id=3,
                game_date=date(2024, 1, 7),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.GSW,
                away_team=NbaTeam.LAL,
                home_score=110,
                away_score=100
            ),
            NbaGame(
                game_id=4,
                game_date=date(2025, 1, 1),
                season="2024-2025",
                game_type="Regular",
                home_team=NbaTeam.GSW,
                away_team=NbaTeam.LAL,
                home_score=95,
                away_score=85
            ),
            NbaGame(
                game_id=5,
                game_date=date(2025, 1, 4),
                season="2024-2025",
                game_type="Regular",
                home_team=NbaTeam.LAL,
                away_team=NbaTeam.GSW,
                home_score=100,
                away_score=110
            )
        ]

    def test_generate_game_context_for_games(self):
        expected_contexts = {
            self.games[0]: GameContext(home_team_elo=1500.0, away_team_elo=1500.0, home_team_rest_days=0, away_team_rest_days=0, home_team_games_played_this_season=1, away_team_games_played_this_season=1),
            self.games[1]: GameContext(home_team_elo=1484.0, away_team_elo=1516.0, home_team_rest_days=3, away_team_rest_days=3, home_team_games_played_this_season=2, away_team_games_played_this_season=2),
            self.games[2]: GameContext(home_team_elo=1530.5305, away_team_elo=1469.4695, home_team_rest_days=3, away_team_rest_days=3, home_team_games_played_this_season=3, away_team_games_played_this_season=3),
            self.games[3]: GameContext(home_team_elo=1500.0, away_team_elo=1500.0, home_team_rest_days=0, away_team_rest_days=0, home_team_games_played_this_season=1, away_team_games_played_this_season=1),
            self.games[4]: GameContext(home_team_elo=1484.0, away_team_elo=1516.0, home_team_rest_days=3, away_team_rest_days=3, home_team_games_played_this_season=2, away_team_games_played_this_season=2)
        }

        game_contexts = generate_game_context_for_games(self.games)

        for game in self.games:
            with self.subTest(game=game):
                self.assertIn(game, game_contexts)
                self.assertAlmostEqual(game_contexts[game].home_team_elo, expected_contexts[game].home_team_elo, places=5)
                self.assertAlmostEqual(game_contexts[game].away_team_elo, expected_contexts[game].away_team_elo, places=5)
                self.assertEqual(game_contexts[game].home_team_rest_days, expected_contexts[game].home_team_rest_days)
                self.assertEqual(game_contexts[game].away_team_rest_days, expected_contexts[game].away_team_rest_days)
                self.assertEqual(game_contexts[game].home_team_games_played_this_season, expected_contexts[game].home_team_games_played_this_season)
                self.assertEqual(game_contexts[game].away_team_games_played_this_season, expected_contexts[game].away_team_games_played_this_season)


if __name__ == '__main__':
    unittest.main()
