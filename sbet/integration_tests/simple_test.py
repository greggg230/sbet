import os
import unittest
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.data.parsing import read_teams, read_games, read_money_line_betting_odds
from sbet.data.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from sbet.evaluate import evaluate_bet_probability_predictor
from sbet.data.models import NbaMoneyLineBettingOpportunity


class SimpleBetProbabilityPredictor(BetProbabilityPredictor):
    def calculate_probability_of_bet_win(self, opportunity: NbaMoneyLineBettingOpportunity) -> float:
        return 1.0 if opportunity.bet_on_home_team else 0.0


class TestIntegration(unittest.TestCase):

    def test_integration(self):
        # Construct the absolute paths to the data files
        base_dir = os.path.dirname(os.path.abspath(__file__))
        teams_file = os.path.join(base_dir, '..', 'data', 'resources', 'nba_teams_all.csv')
        games_file = os.path.join(base_dir, '..', 'data', 'resources', 'nba_games_all.csv')
        betting_odds_file = os.path.join(base_dir, '..', 'data', 'resources', 'nba_betting_money_line.csv')

        # Load the data
        teams = read_teams(teams_file)
        games = read_games(games_file)
        betting_odds = read_money_line_betting_odds(betting_odds_file)

        # Transform the data
        nba_games = transform_to_nba_games(games, teams)
        betting_opportunities = transform_to_nba_money_line_betting_opportunities(betting_odds, nba_games)

        # Use the simple predictor
        predictor = SimpleBetProbabilityPredictor()
        threshold = 0.05

        # Evaluate the betting strategy
        average_profitability = evaluate_bet_probability_predictor(predictor, betting_opportunities, threshold)

        # Report the average profitability
        print(f"Average Profitability: {average_profitability}")

        # Assert that the profitability is calculated (not NaN or infinite)
        self.assertTrue(average_profitability is not None)
        self.assertTrue(average_profitability == average_profitability)  # Check for NaN
        self.assertTrue(average_profitability != float('inf'))
        self.assertTrue(average_profitability != float('-inf'))
