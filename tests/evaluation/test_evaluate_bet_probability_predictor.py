import unittest
from datetime import date
from unittest.mock import Mock

from sbet.data.historical.models import NbaGame
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity
from sbet.data.historical.models import NbaTeam
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor


class TestEvaluateBetProbabilityPredictor(unittest.TestCase):

    def setUp(self):
        # Mock predictor
        self.predictor = Mock(spec=BetProbabilityPredictor)

        # Mock games
        game1 = NbaGame(
            game_id=101,
            game_date=date(2024, 1, 1),
            season="2023-2024",
            game_type="Regular",
            home_team=NbaTeam.LAL,
            away_team=NbaTeam.GSW,
            home_score=100,
            away_score=90
        )
        game2 = NbaGame(
            game_id=102,
            game_date=date(2024, 1, 2),
            season="2023-2024",
            game_type="Regular",
            home_team=NbaTeam.BOS,
            away_team=NbaTeam.BKN,
            home_score=95,
            away_score=105
        )
        game3 = NbaGame(
            game_id=103,
            game_date=date(2024, 1, 3),
            season="2023-2024",
            game_type="Regular",
            home_team=NbaTeam.MIA,
            away_team=NbaTeam.PHX,
            home_score=110,
            away_score=100
        )
        game4 = NbaGame(
            game_id=104,
            game_date=date(2024, 1, 4),
            season="2023-2024",
            game_type="Regular",
            home_team=NbaTeam.NYK,
            away_team=NbaTeam.DET,
            home_score=80,
            away_score=85
        )
        game5 = NbaGame(
            game_id=105,
            game_date=date(2024, 1, 5),
            season="2023-2024",
            game_type="Regular",
            home_team=NbaTeam.CHI,
            away_team=NbaTeam.MIL,
            home_score=105,
            away_score=110
        )

        # Mock opportunities
        self.opportunity1 = NbaMoneyLineBettingOpportunity(
            game=game1,
            book_name="BookA",
            bet_on_home_team=True,
            price=150
        )
        self.opportunity2 = NbaMoneyLineBettingOpportunity(
            game=game2,
            book_name="BookB",
            bet_on_home_team=False,
            price=-120
        )
        self.opportunity3 = NbaMoneyLineBettingOpportunity(
            game=game3,
            book_name="BookC",
            bet_on_home_team=True,
            price=-130
        )
        self.opportunity4 = NbaMoneyLineBettingOpportunity(
            game=game4,
            book_name="BookD",
            bet_on_home_team=False,
            price=200
        )
        self.opportunity5 = NbaMoneyLineBettingOpportunity(
            game=game5,
            book_name="BookE",
            bet_on_home_team=True,
            price=100
        )

    def test_evaluate_bet_probability_predictor(self):
        # Mock predictor's probability calculation
        self.predictor.calculate_probability_of_bet_win.side_effect = [0.7, 0.4, 0.65, 0.55, 0.6]

        opportunities = [self.opportunity1, self.opportunity2, self.opportunity3, self.opportunity4, self.opportunity5]
        threshold = 0.05

        evaluation = evaluate_bet_probability_predictor(self.predictor, opportunities, threshold)

        # Check the evaluation results
        self.assertAlmostEqual(evaluation.average_profit, 0.817, places=3)
        self.assertEqual(evaluation.number_of_bets_placed, 4)


if __name__ == '__main__':
    unittest.main()
