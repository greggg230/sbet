import csv
import os
import unittest
from datetime import datetime
from typing import Dict

from frozendict import frozendict

from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.extractor.scottfree.extractor import ScottfreeHistoricalBetDataExtractor
from sbet.data.historical.models.transform.game import Game
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor


class TestTeamEloProbabilityPredictorYearly(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources', 'mlb.csv')

        extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
        extracted_data = extractor.extract()

        # Filter out games before 2010
        self.mlb_games = [
            game for game in extracted_data.games
            if game.game_date.year >= 2010
        ]

        # Generate game contexts for all games upfront
        self.game_contexts = generate_game_context_for_games(self.mlb_games, 250)

        self.betting_opportunities: frozendict[Game, GameBettingOpportunities] = extracted_data.money_line_data

    def test_team_elo_probability_predictor_yearly(self):
        threshold = 0.05  # Example threshold
        total_profit = 0
        year_profits: Dict[int, float] = {}

        all_details = []

        for year in range(2014, 2024):
            season_str = f"{year}"
            season_games = [
                game for game in self.mlb_games
                if game.season == season_str
            ]

            start_betting_date = datetime.strptime(f'{year}-04-15', '%Y-%m-%d').date()

            betting_opportunities = [
                self.betting_opportunities[game] for game in season_games if game in self.betting_opportunities and game.game_date >= start_betting_date
            ]
            all_opportunities = [opportunity.home for opportunity in betting_opportunities if opportunity.home] + [opportunity.away for opportunity in betting_opportunities if opportunity.away]

            # Instantiate the TeamEloProbabilityPredictor
            predictor = TeamEloProbabilityPredictor(self.game_contexts)

            # Evaluate the predictor using evaluate_bet_probability_predictor function
            evaluation_result = evaluate_bet_probability_predictor(predictor, all_opportunities, threshold, self.game_contexts)
            year_profit = evaluation_result.average_profit
            print(f"Year: {year}: {evaluation_result.number_of_bets_placed} / {evaluation_result.number_of_bets_skipped}")

            year_profits[year] = year_profit
            total_profit += year_profit

            all_details.extend(evaluation_result.details)

        for year, profit in year_profits.items():
            print(f"Year: {year}, Profit: {profit}")

        average_profit = total_profit / len(year_profits)
        print(f"Average Profit: {average_profit}")

        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([
                'date',
                'season',
                'home_team',
                'away_team',
                'home_elo',
                'away_elo',
                'is_betting_on_home',
                'expected_probability_of_win',
                'bet_price',
                'bet_taken',
                'inferred_bet_probability',
                'bet_won',
                'net_winnings'
            ])

            for detail in all_details:
                writer.writerow([
                    detail.date.strftime('%Y-%m-%d'),
                    detail.season,
                    detail.home_team,
                    detail.away_team,
                    detail.home_elo,
                    detail.away_elo,
                    detail.is_betting_on_home,
                    detail.expected_probability_of_win,
                    detail.bet_price,
                    detail.bet_taken,
                    detail.inferred_bet_probability,
                    detail.bet_won,
                    detail.net_winnings
                ])

        self.assertTrue(average_profit >= 0)


if __name__ == '__main__':
    unittest.main()
