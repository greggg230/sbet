import unittest
from datetime import date
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.data.historical.models.transform import NbaGame
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor
from sbet.prediction.team_elo.generate_game_context import GameContext


class TestTeamEloProbabilityPredictor(unittest.TestCase):

    def setUp(self):
        # Mock game contexts
        self.game_contexts = {
            NbaGame(
                game_id=1,
                game_date=date(2024, 1, 1),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.LAL,
                away_team=NbaTeam.GSW,
                home_score=100,
                away_score=90
            ): GameContext(
                home_team_elo=1500.0,
                away_team_elo=1500.0,
                home_team_rest_days=2,
                away_team_rest_days=3,
                home_team_games_played_this_season=10,
                away_team_games_played_this_season=10
            ),
            NbaGame(
                game_id=2,
                game_date=date(2024, 1, 2),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.BOS,
                away_team=NbaTeam.BKN,
                home_score=95,
                away_score=105
            ): GameContext(
                home_team_elo=1520.0,
                away_team_elo=1480.0,
                home_team_rest_days=3,
                away_team_rest_days=2,
                home_team_games_played_this_season=12,
                away_team_games_played_this_season=11
            ),
        }

        # Mock opportunities
        self.opportunity1 = NbaMoneyLineBettingOpportunity(
            game=NbaGame(
                game_id=1,
                game_date=date(2024, 1, 1),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.LAL,
                away_team=NbaTeam.GSW,
                home_score=100,
                away_score=90
            ),
            book_name="BookA",
            bet_on_home_team=True,
            price=150
        )
        self.opportunity2 = NbaMoneyLineBettingOpportunity(
            game=NbaGame(
                game_id=2,
                game_date=date(2024, 1, 2),
                season="2023-2024",
                game_type="Regular",
                home_team=NbaTeam.BOS,
                away_team=NbaTeam.BKN,
                home_score=95,
                away_score=105
            ),
            book_name="BookB",
            bet_on_home_team=False,
            price=-120
        )

    def test_calculate_probability_of_bet_win(self):
        predictor = TeamEloProbabilityPredictor(self.game_contexts)

        # Test first opportunity
        win_prob_opportunity1 = predictor.calculate_probability_of_bet_win(self.opportunity1)
        expected_win_prob_opportunity1 = 1 / (1 + 10 ** ((1500.0 - 1500.0) / 400))
        self.assertAlmostEqual(win_prob_opportunity1, expected_win_prob_opportunity1, places=5)

        # Test second opportunity
        win_prob_opportunity2 = predictor.calculate_probability_of_bet_win(self.opportunity2)
        expected_win_prob_opportunity2 = 1 / (1 + 10 ** ((1480.0 - 1520.0) / 400))
        self.assertAlmostEqual(win_prob_opportunity2, 1 - expected_win_prob_opportunity2, places=5)


if __name__ == '__main__':
    unittest.main()
