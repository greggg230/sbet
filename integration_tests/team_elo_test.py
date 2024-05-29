import os
import unittest
from datetime import datetime
from typing import Dict, List
from sbet.data.historical.parsing import read_teams, read_games, read_money_line_betting_odds
from sbet.data.historical.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor
from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity


class TestTeamEloProbabilityPredictorYearly(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        teams_file_path = os.path.join(base_dir, '../sbet', 'data', 'historical', 'resources', 'nba_teams_all.csv')
        games_file_path = os.path.join(base_dir, '../sbet', 'data', 'historical', 'resources', 'nba_games_all.csv')
        betting_odds_file_path = os.path.join(base_dir, '../sbet', 'data', 'historical', 'resources', 'nba_betting_money_line.csv')

        # Read the historical data
        teams = read_teams(teams_file_path)
        games = read_games(games_file_path)
        betting_odds = read_money_line_betting_odds(betting_odds_file_path)

        # Transform the raw game data into NbaGame objects
        nba_games: List[NbaGame] = transform_to_nba_games(games, teams)

        # Filter out games before 2010
        self.nba_games = [
            game for game in nba_games
            if game.game_date.year >= 2010
        ]

        # Transform the raw betting odds data into NbaMoneyLineBettingOpportunity objects
        betting_opportunities: List[NbaMoneyLineBettingOpportunity] = transform_to_nba_money_line_betting_opportunities(betting_odds, self.nba_games)

        # Generate game contexts for all games upfront
        self.game_contexts = generate_game_context_for_games(self.nba_games)

        self.betting_opportunities: dict[NbaGame, NbaMoneyLineBettingOpportunity] = {}

        for betting_opp in betting_opportunities:
            if betting_opp.game not in self.betting_opportunities or betting_opp.price < self.betting_opportunities[betting_opp.game].price:
                self.betting_opportunities[betting_opp.game] = betting_opp

    def test_team_elo_probability_predictor_yearly(self):
        threshold = 0.05  # Example threshold
        total_profit = 0
        year_profits: Dict[int, float] = {}

        for year in range(2010, 2019):
            season_str = f"{year}-{str(year + 1)[-2:]}"
            season_games = [
                game for game in self.nba_games
                if game.season == season_str
            ]

            # Filter betting opportunities for games after 10/31 of the starting year of the season
            start_betting_date = datetime.strptime(f'{year}-11-01', '%Y-%m-%d').date()

            betting_opportunities = [
                self.betting_opportunities[game] for game in season_games if game in self.betting_opportunities and game.game_date >= start_betting_date
            ]

            # Instantiate the TeamEloProbabilityPredictor
            predictor = TeamEloProbabilityPredictor(self.game_contexts)

            # Evaluate the predictor using evaluate_bet_probability_predictor function
            evaluation_result = evaluate_bet_probability_predictor(predictor, list(betting_opportunities), threshold)
            year_profit = evaluation_result.average_profit
            print(f"Year: {year}: {evaluation_result.number_of_bets_placed}")

            year_profits[year] = year_profit
            total_profit += year_profit

        for year, profit in year_profits.items():
            print(f"Year: {year}, Profit: {profit}")

        average_profit = total_profit / len(year_profits)
        print(f"Average Profit: {average_profit}")

        self.assertTrue(average_profit >= 0)


if __name__ == '__main__':
    unittest.main()
