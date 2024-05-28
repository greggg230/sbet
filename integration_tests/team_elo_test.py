import os
import unittest
from datetime import datetime

from sbet.data.historical.parsing import read_teams, read_games, read_money_line_betting_odds
from sbet.data.historical.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
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
        teams = read_teams(teams_file_path)
        games = read_games(games_file_path)
        betting_odds = read_money_line_betting_odds(betting_odds_file_path)

        # Transform the raw game data into NbaGame objects
        nba_games = transform_to_nba_games(games, teams)

        # Filter games between October 20, 2015 and December 31, 2015
        start_date = datetime.strptime('2015-10-20', '%Y-%m-%d').date()
        end_date = datetime.strptime('2015-12-31', '%Y-%m-%d').date()
        filtered_games = [
            game for game in nba_games
            if start_date <= game.game_date <= end_date
        ]

        # Convert filtered games into NbaGameOutcome objects
        self.game_outcomes = [
            NbaGameOutcome(
                home_team=game.home_team,
                away_team=game.away_team,
                did_home_team_win=game.home_score > game.away_score
            )
            for game in filtered_games
        ]

        # Identify betting opportunities between January 1, 2016 and April 13, 2016
        start_betting_date = datetime.strptime('2016-01-01', '%Y-%m-%d').date()
        end_betting_date = datetime.strptime('2016-04-13', '%Y-%m-%d').date()
        nba_money_line_betting_opportunities = transform_to_nba_money_line_betting_opportunities(betting_odds, nba_games)
        self.betting_opportunities = [
            opportunity for opportunity in nba_money_line_betting_opportunities
            if start_betting_date <= opportunity.game.game_date <= end_betting_date
        ]

    def test_team_elo_probability_predictor(self):
        # Instantiate the TeamEloProbabilityPredictor
        predictor = TeamEloProbabilityPredictor(self.game_outcomes)

        # Evaluate the predictor using evaluate_bet_probability_predictor function
        threshold = 0.15  # Example threshold
        profit = evaluate_bet_probability_predictor(predictor, self.betting_opportunities, threshold)

        # Assert profit (placeholder assertion, replace with actual expected profit range)
        print(profit)
        self.assertTrue(profit >= 0)


if __name__ == '__main__':
    unittest.main()
