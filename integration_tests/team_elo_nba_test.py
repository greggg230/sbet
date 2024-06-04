import csv
import os
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Tuple, Callable

from frozendict import frozendict

from sbet.data.historical.extractor.base import HistoricalBetDataExtractor
from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.extractor.scottfree.extractor import ScottfreeHistoricalBetDataExtractor
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games_recursive
from sbet.prediction.team_elo.models.game_context import GameContext
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor


def test_predictor(
    data_extractor: HistoricalBetDataExtractor,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    make_season_fn: Callable[[int], str] = lambda year: f"{year}-{str(year + 1)[-2:]}",
    betting_month_and_day_start: Tuple[int, int] = (12, 15)
) -> (float, float):
    extracted_data = data_extractor.extract()

    nba_games = [
        game for game in extracted_data.games
        if game.game_date.year >= year_start
    ]

    betting_opportunities: frozendict[Game, GameBettingOpportunities] = extracted_data.money_line_data

    total_profit = 0
    total_bets = 0
    year_profits: Dict[int, float] = {}

    all_details = []

    by_month = {i: [] for i in range(1, 13)}

    for year in range(year_start, year_end + 1):
        season_str = make_season_fn(year)
        season_games = [
            game for game in nba_games
            if game.season == season_str
        ]

        # Filter betting opportunities for games after 10/31 of the starting year of the season
        month, day = betting_month_and_day_start
        start_betting_date = date(year, month, day)

        betting_opportunities_list = [
            betting_opportunities[game] for game in season_games
            if game in betting_opportunities and game.game_date >= start_betting_date
        ]
        all_opportunities = [opportunity.home for opportunity in betting_opportunities_list if opportunity.home] + [opportunity.away for opportunity in betting_opportunities_list if opportunity.away]

        # Evaluate the predictor using evaluate_bet_probability_predictor function
        evaluation_result = evaluate_bet_probability_predictor(
            predictor,
            all_opportunities,
            write_report,
            frozendict(game_contexts)
        )
        year_profit = evaluation_result.average_profit
        if verbose:
            print(f"Year: {year}: {evaluation_result.number_of_bets_placed} * {evaluation_result.average_profit} = {evaluation_result.number_of_bets_placed * evaluation_result.average_profit}")

        year_profits[year] = year_profit
        total_profit += year_profit
        total_bets += evaluation_result.number_of_bets_placed

        for month, details in evaluation_result.details_by_month.items():
            by_month[month].append(details.average_profit)

        all_details.extend(evaluation_result.details)

    if verbose:
        for month, month_items in by_month.items():
            avg = (sum(month_items) / len(month_items)) if len(month_items) > 0 else 0
            print(f"{month}: {avg} {month_items}")

    average_profit = total_profit / len(year_profits)
    bets_per_season = total_bets / len(year_profits)

    if write_report:
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

    if verbose:
        print(f"{average_profit} * {bets_per_season} = {average_profit * bets_per_season}")

    return average_profit, bets_per_season


def test_nba_predictor(
    data_extractor: HistoricalBetDataExtractor,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    betting_month_and_day_start: Tuple[int, int] = (12, 15)
) -> Tuple[float, float]:
    return test_predictor(
        data_extractor,
        predictor,
        game_contexts,
        verbose,
        write_report,
        year_start=year_start,
        year_end=year_end,
        betting_month_and_day_start=betting_month_and_day_start,
        make_season_fn=lambda year: f"{year}-{str(year + 1)[-2:]}"
    )


def test_nhl_predictor(
    data_extractor: HistoricalBetDataExtractor,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    betting_month_and_day_start: Tuple[int, int] = (12, 15)
) -> Tuple[float, float]:
    return test_predictor(
        data_extractor,
        predictor,
        game_contexts,
        verbose,
        write_report,
        year_start=year_start,
        year_end=year_end,
        betting_month_and_day_start=betting_month_and_day_start,
        make_season_fn=lambda year: f"{year}-{str(year + 1)[-2:]}"
    )


def test_nfl_predictor(
    data_extractor: HistoricalBetDataExtractor,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    betting_month_and_day_start: Tuple[int, int] = (10, 1)
) -> Tuple[float, float]:
    return test_predictor(
        data_extractor,
        predictor,
        game_contexts,
        verbose,
        write_report,
        year_start=year_start,
        year_end=year_end,
        betting_month_and_day_start=betting_month_and_day_start,
        make_season_fn=lambda year: f"{year}-{str(year + 1)[-2:]}"
    )


def test_mlb_predictor(
    data_extractor: HistoricalBetDataExtractor,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    betting_month_and_day_start: Tuple[int, int] = (5, 1)
) -> Tuple[float, float]:
    return test_predictor(
        data_extractor,
        predictor,
        game_contexts,
        verbose,
        write_report,
        year_start=year_start,
        year_end=year_end,
        betting_month_and_day_start=betting_month_and_day_start,
        make_season_fn=lambda year: f"{year}"
    )


def space_explorer(
        extractor: HistoricalBetDataExtractor,
        k: List[float],
        recursions: List[int],
        margin_of_victory_gradient: List[float],
        threshold: List[float],
        home_bias: List[float],
        k_decay_factor: List[float],
        test_fn: Callable,
        total_value_threshold: float = 8) -> None:
    profitable_combos = []
    extracted = extractor.extract()
    counter = 0
    total_count = len(k) * len(recursions) * len(margin_of_victory_gradient) * len(threshold) * len(home_bias) * len(k_decay_factor)
    for k_ in k:
        for r in recursions:
            for m in margin_of_victory_gradient:
                for kd in k_decay_factor:
                    contexts = generate_game_context_for_games_recursive(
                        extracted.games,
                        k=k_,
                        recursions=r,
                        margin_of_victory_gradient=m,
                        k_decay_factor=kd
                    )
                    for h in home_bias:
                        for t in threshold:
                            params = (k_, r, m, t, h, kd)
                            predictor = TeamEloProbabilityPredictor(contexts, threshold=t, home_bias=h)

                            counter += 1
                            if counter % 100 == 0:
                                print(f"{counter / total_count * 100}%")

                            value, bets_placed = test_fn(extractor, predictor, contexts, verbose=False)

                            total_value = value * bets_placed

                            if total_value < total_value_threshold:
                                continue

                            profitable_combos.append((value, bets_placed, params))

    for value, bets_placed, combo in sorted(profitable_combos, key=lambda x: -(x[0] * x[1]))[:50]:
        print(f"{combo} -> {value} ({bets_placed}) = {value * bets_placed}")


base_dir = os.path.dirname(os.path.abspath(__file__))


def explore_nhl():
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nhl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        [1, 1.5, 1.75, 2, 2.25, 2.5],
        [0, 1],
        [0],
        [0.1, 0.135, 0.15, 0.175, 0.2],
        [0.51, 0.53, 0.55, 0.6],
        [0, 100, 200, 570],
        total_value_threshold=3.5
    )


class CompositePredictor(BetProbabilityPredictor):
    def __init__(self, threshold: float, *predictors: BetProbabilityPredictor):
        if len(predictors) == 0:
            raise ValueError("Must pass at least one predictor to CompositePredictor.")

        self.threshold = threshold
        self.predictors = list(predictors)

    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        evaluations = [predictor.calculate_probability_of_bet_win(opportunity) for predictor in self.predictors]
        return sum(evaluations) / len(evaluations)

    def select_opportunity(self, opportunity: MoneyLineBettingOpportunity) -> bool:
        return all([predictor.select_opportunity(opportunity) for predictor in self.predictors])


def explore_nba():
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nba.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        [1, 2, 3, 5],
        [0, 1, 2, 5, 10],
        [0, 1,  2],
        [0.18, 0.2, 0.22],
        [0.53, 0.55, 0.57],
        [80, 100, 120, 160],
        test_nba_predictor
    )


def explore_nfl():
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nfl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        [2, 5, 7, 10, 20, 30, 40],
        [0, 1, 5],
        [0],
        [0.15, 0.2, 0.22, 0.28, 0.3, 0.32],
        [0.57, 0.6, 0.65],
        [0, 25, 50],
        test_nfl_predictor,
        total_value_threshold=-5
    )


def explore_mlb():
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'mlb.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        [2, 5, 7, 10],
        [0, 1, 5],
        [0],
        [0.1, 0.15, 0.2, 0.22, 0.25, 0.28],
        [0.57, 0.6],
        [0, 50, 200, 400, 600],
        test_mlb_predictor,
        total_value_threshold=-5
    )


def create_context_and_predictor(
        extractor: HistoricalBetDataExtractor, k: float, r: int, m: float, h: float, t: float, kd: float
) -> Tuple[dict[Game, GameContext], TeamEloProbabilityPredictor]:
    extracted = extractor.extract()
    contexts = generate_game_context_for_games_recursive(extracted.games, k=k, recursions=r,
                                                         margin_of_victory_gradient=m, k_decay_factor=kd)

    predictor = TeamEloProbabilityPredictor(contexts, threshold=t, home_bias=h)

    return contexts, predictor


def test_single_nba_case(k: float, r: int, m: float, t: float, h: float, kd: float) -> None:
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nba.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    contexts1, predictor1 = create_context_and_predictor(extractor, k, r, m, h, t, kd)
    contexts2, predictor2 = create_context_and_predictor(extractor, 1, 2, 2, 0.55, 0.2, 160)

    predictor = CompositePredictor(t, predictor1, predictor2)

    test_nba_predictor(extractor, predictor, contexts1)


@dataclass(frozen=True)
class PredictorParams:
    k: float
    r: int
    m: float
    h: float
    kd: float


def test_single_nhl_case(k: float, r: int, m: float, t: float, h: float, kd: int) -> None:
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nhl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
    contexts1, predictor1 = create_context_and_predictor(extractor, k, r, m, h, t, kd)
    contexts2, predictor2 = create_context_and_predictor(extractor, 1, 2, 2, 0.55, 0.2, 160)

    predictor = CompositePredictor(t, predictor1, predictor2)

    test_predictor(extractor, predictor1, contexts1)


def test_single_nfl_case(k: float, r: int, m: float, t: float, h: float, kd: int) -> None:
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nfl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
    contexts, predictor = create_context_and_predictor(extractor, k, r, m, h, t, kd)

    test_nfl_predictor(extractor, predictor, contexts)


def test_single_mlb_case(k: float, r: int, m: float, t: float, h: float, kd: int) -> None:
    scottfree_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'mlb.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
    contexts, predictor = create_context_and_predictor(extractor, k, r, m, h, t, kd)

    test_mlb_predictor(extractor, predictor, contexts)


def consensus_nba(extractor: HistoricalBetDataExtractor, t: float, *parameters: PredictorParams):
    data = [
        create_context_and_predictor(extractor, param.k, param.r, param.m, param.h, param.kd)
        for param in parameters
    ]



# Example usage
if __name__ == '__main__':
    #test_single_nba_case(1, 5, 1, 0.18, 0.57, 80)
    #test_single_nfl_case(1, 5, 1, 0.18, 0.57, 80)
    #explore_nhl()
    #test_single_nhl_case(2.5, 0, 0, 0.15, 0.53)
    #explore_nba()
    #explore_nfl()
    #test_single_nfl_case(20, 0, 0, 0.22, 0.57, 0)
    #test_single_nfl_case(40, 0, 0, 0.28, 0.57, 0)
    explore_mlb()
    #test_single_mlb_case(2, 0, 0, .22, 0.6, 0)
