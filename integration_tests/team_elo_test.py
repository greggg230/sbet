import os
import unittest
from datetime import datetime, date

from sbet.data.historical.parsing import read_teams, read_games, read_money_line_betting_odds
from sbet.data.historical.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor, PredictorEvaluation
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor


class TestTeamEloProbabilityPredictor(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        teams_file_path = os.path.join(base_dir, '../sbet', 'data', 'historical', 'resources', 'nba_teams_all.csv')
        games_file_path = os.path.join(base_dir, '../sbet', 'data', 'historical', 'resources', 'nba_games_all.csv')
        betting_odds_file_path = os.path.join(base_dir, '../sbet', 'data', 'historical', 'resources',
                                              'nba_betting_money_line.csv')

        # Read the historical data
        self.teams = read_teams(teams_file_path)
        self.games = read_games(games_file_path)
        self.betting_odds = read_money_line_betting_odds(betting_odds_file_path)

        # Transform the raw game data into NbaGame objects
        self.nba_games = transform_to_nba_games(self.games, self.teams)

    def test_team_elo_probability_predictor_yearly(self):
        threshold = 0.4  # Threshold for evaluating the strategy
        start_year = 2010
        end_year = 2018

        total_profit = 0
        total_bets_placed = 0
        num_years = end_year - start_year + 1

        for year in range(start_year, end_year + 1):
            start_date = date(year, 10, 20)
            end_date = date(year, 12, 31)
            filtered_games = [
                game for game in self.nba_games
                if start_date <= game.game_date <= end_date
            ]

            game_outcomes = [
                NbaGameOutcome(
                    home_team=game.home_team,
                    away_team=game.away_team,
                    did_home_team_win=game.home_score > game.away_score
                )
                for game in filtered_games
            ]

            start_betting_date = date(year + 1, 1, 1)
            end_betting_date = date(year + 1, 4, 13)
            nba_money_line_betting_opportunities = transform_to_nba_money_line_betting_opportunities(self.betting_odds, self.nba_games)
            betting_opportunities = [
                opportunity for opportunity in nba_money_line_betting_opportunities
                if start_betting_date <= opportunity.game.game_date <= end_betting_date
            ]

            # Instantiate the TeamEloProbabilityPredictor
            predictor = TeamEloProbabilityPredictor(game_outcomes)

            # Evaluate the predictor using evaluate_bet_probability_predictor function
            evaluation = evaluate_bet_probability_predictor(predictor, betting_opportunities, threshold)
            total_profit += evaluation.average_profit * evaluation.number_of_bets_placed
            total_bets_placed += evaluation.number_of_bets_placed

            print(f'Year: {year}, Profit: {evaluation.average_profit}, Bets Placed: {evaluation.number_of_bets_placed}')

        average_profit = total_profit / total_bets_placed if total_bets_placed > 0 else 0.0
        print(f'Average Profit: {average_profit}')


if __name__ == '__main__':
    unittest.main()
