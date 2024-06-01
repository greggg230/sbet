import csv
import os
from datetime import datetime
from typing import Dict, Type

from frozendict import frozendict

from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.extractor.base import HistoricalBetDataExtractor
from sbet.data.historical.models.transform.game import Game
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.models.game_context import GameContext


def test_predictor(
    data_extractor: HistoricalBetDataExtractor,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    threshold: float = 0.25,
    k: int = 50
) -> None:
    extracted_data = data_extractor.extract()

    # Filter out games before 2010
    nba_games = [
        game for game in extracted_data.games
        if game.game_date.year >= 2010
    ]

    betting_opportunities: frozendict[Game, GameBettingOpportunities] = extracted_data.money_line_data

    total_profit = 0
    year_profits: Dict[int, float] = {}

    all_details = []

    by_month = {i: [] for i in range(1, 13)}

    for year in range(2010, 2023):
        season_str = f"{year}-{str(year + 1)[-2:]}"
        season_games = [
            game for game in nba_games
            if game.season == season_str
        ]

        # Filter betting opportunities for games after 10/31 of the starting year of the season
        start_betting_date = datetime.strptime(f'{year}-12-01', '%Y-%m-%d').date()

        betting_opportunities_list = [
            betting_opportunities[game] for game in season_games
            if game in betting_opportunities and game.game_date >= start_betting_date and game.game_date.month != 2
        ]
        all_opportunities = [opportunity.home for opportunity in betting_opportunities_list if opportunity.home] + [opportunity.away for opportunity in betting_opportunities_list if opportunity.away]

        # Evaluate the predictor using evaluate_bet_probability_predictor function
        evaluation_result = evaluate_bet_probability_predictor(predictor, all_opportunities, threshold, True, frozendict(game_contexts))
        year_profit = evaluation_result.average_profit
        print(f"Year: {year}: {evaluation_result.number_of_bets_placed} / {evaluation_result.number_of_bets_skipped}")

        year_profits[year] = year_profit
        total_profit += year_profit

        for month, details in evaluation_result.details_by_month.items():
            by_month[month].append(details.average_profit)

        all_details.extend(evaluation_result.details)

    for year, profit in year_profits.items():
        print(f"Year: {year}, Profit: {profit}")

    for month, month_items in by_month.items():
        avg = (sum(month_items) / len(month_items)) if len(month_items) > 0 else 0
        print(f"{month}: {avg} {month_items}")

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


# Example usage
if __name__ == '__main__':
    from sbet.data.historical.extractor.scottfree.extractor import ScottfreeHistoricalBetDataExtractor
    from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor

    base_dir = os.path.dirname(os.path.abspath(__file__))
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources', 'nba.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    extracted = extractor.extract()

    contexts = generate_game_context_for_games(extracted.games, k=150)

    predictor = TeamEloProbabilityPredictor(contexts)

    test_predictor(extractor, predictor, contexts, threshold=0.3)
