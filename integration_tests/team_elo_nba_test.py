import csv
import multiprocessing.context
import os
from multiprocessing import Pool
from pickle import load, dump
from typing import Dict, List, Tuple, Callable, Optional

from frozendict import frozendict

from sbet.data.historical.extractor.base import HistoricalBetDataExtractor
from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.extractor.models.historical_bet_data import HistoricalBetData
from sbet.data.historical.extractor.scottfree.extractor import ScottfreeHistoricalBetDataExtractor
from sbet.data.historical.models.transform.game import Game
from sbet.evaluation.evaluate import evaluate_bet_probability_predictor
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games_recursive, \
    generate_game_context_for_games_recursive_regenerate
from sbet.prediction.team_elo.models.game_context import GameContext
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def test_predictor(
    extracted_data: HistoricalBetData,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    make_season_fn: Callable[[int], str],
    season_years: List[int],
    season_months: List[int],
    betting_months: List[int],
    verbose: bool = True,
    write_report: bool = False,
) -> (float, float):
    betting_opportunities: frozendict[Game, GameBettingOpportunities] = extracted_data.money_line_data

    total_profit = 0
    total_bets = 0
    year_profits: Dict[str, float] = {}

    all_details = []

    by_month = {i: [] for i in range(1, 13)}

    for season_year in season_years:
        season = make_season_fn(season_year)
        season_games = [
            game for game in extracted_data.games
            if game.season == season
        ]

        betting_months_and_years = []

        for month in betting_months:
            if month < season_months[0]:
                year = season_year + 1
            else:
                year = season_year
            betting_months_and_years.append((month, year))


        # Filter betting opportunities for games after 10/31 of the starting year of the season
        betting_opportunities_list = [
            betting_opportunities[game] for game in season_games
            if (game.game_date.month, game.game_date.year) in betting_months_and_years
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
            print(f"Season: {season}: {evaluation_result.number_of_bets_placed} * {evaluation_result.average_profit} = {evaluation_result.number_of_bets_placed * evaluation_result.average_profit}")

        year_profits[season] = year_profit
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
        with open('output.csv', 'w', newline='') as f:
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
                    detail.bet_type.value,
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
    extracted_data: HistoricalBetData,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
) -> Tuple[float, float]:
    return test_predictor(
        extracted_data,
        predictor,
        game_contexts,
        season_months=[10, 11, 12, 1, 2, 3, 4, 5, 6],
        betting_months=[12, 1, 2, 3, 4, 5, 6],
        season_years=[2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022],
        make_season_fn=lambda year: f"{year}-{str(year + 1)[-2:]}",
        verbose=verbose,
        write_report=write_report,
    )


def test_ncaab_predictor(
    extracted_data: HistoricalBetData,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
) -> Tuple[float, float]:
    return test_predictor(
        extracted_data,
        predictor,
        game_contexts,
        season_months=[11, 12, 1, 2, 3, 4],
        betting_months=[12, 1, 2, 3, 4],
        season_years=[2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023],
        make_season_fn=lambda year: f"{year}-{str(year + 1)[-2:]}",
        verbose=verbose,
        write_report=write_report,
    )


def test_nhl_predictor(
        extracted_data: HistoricalBetData,
        predictor: BetProbabilityPredictor,
        game_contexts: Dict[Game, GameContext],
        verbose: bool = True,
        write_report: bool = False,
) -> Tuple[float, float]:
    return test_predictor(
        extracted_data,
        predictor,
        game_contexts,
        season_months=[10, 11, 12, 1, 2, 3, 4, 5, 6],
        betting_months=[12, 1, 2, 3, 4, 5, 6],
        season_years=[2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022],
        make_season_fn=lambda year: f"{year}-{str(year + 1)[-2:]}",
        verbose=verbose,
        write_report=write_report,
    )


def test_nfl_predictor(
    extracted_data: HistoricalBetData,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    betting_month_and_day_start: Tuple[int, int] = (10, 1)
) -> Tuple[float, float]:
    return test_predictor(
        extracted_data,
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
    extracted_data: HistoricalBetData,
    predictor: BetProbabilityPredictor,
    game_contexts: Dict[Game, GameContext],
    verbose: bool = True,
    write_report: bool = False,
    year_start: int = 2007,
    year_end: int = 2022,
    betting_month_and_day_start: Tuple[int, int] = (5, 1)
) -> Tuple[float, float]:
    return test_predictor(
        extracted_data,
        predictor,
        game_contexts,
        verbose,
        write_report,
        year_start=year_start,
        year_end=year_end,
        betting_month_and_day_start=betting_month_and_day_start,
        make_season_fn=lambda year: f"{year}"
    )


def cache_contexts(prefix: str, params: Tuple, context: dict[Game, GameContext]) -> None:
    path = os.path.join(BASE_DIR, "context_cache", prefix, f"{str(hash(params)).replace('-', 'n')}.pickle")
    with open(path, 'wb') as f:
        dump(context, f)


def check_context_cache(prefix: str, params: Tuple) -> Optional[dict[Game, GameContext]]:
    path = os.path.join(BASE_DIR, "context_cache", prefix, f"{str(hash(params)).replace('-', 'n')}.pickle")
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            return load(f)


def process_context_with_thresholds(
    bet_data: HistoricalBetData,
    k: float,
    recursions: int,
    margin_of_victory_gradient: float,
    home_bias: float,
    k_decay_factor: float,
    context_generator: Callable[..., dict[Game, GameContext]],
    underdog_thresholds: List[float],
    favorite_thresholds: List[float],
    test_fn: Callable[..., Tuple[float, float]],
    cache_prefix: str
) -> dict[Tuple, Tuple[float, float]]:
    params = (k, recursions, margin_of_victory_gradient, home_bias, k_decay_factor)
    maybe_cached_result = check_context_cache(cache_prefix, params)

    contexts: dict[Game, GameContext]
    if maybe_cached_result is not None:
        contexts = maybe_cached_result
    else:
        contexts = context_generator(
            bet_data.games,
            k=k,
            recursions=recursions,
            margin_of_victory_gradient=margin_of_victory_gradient,
            home_bias=home_bias,
            k_decay_factor=k_decay_factor
        )
        cache_contexts(cache_prefix, params, contexts)

    output: dict[Tuple, Tuple[float, float]] = {}

    for u in underdog_thresholds:
        for f in favorite_thresholds:
            predictor = TeamEloProbabilityPredictor(contexts, underdog_threshold=u, favorite_threshold=f, home_bias=home_bias)
            output[(k, recursions, margin_of_victory_gradient, u, f, home_bias, k_decay_factor, context_generator)] = test_fn(bet_data, predictor, contexts, verbose=False)

    return output


def space_explorer(
        extractor: HistoricalBetDataExtractor,
        k: List[float],
        recursions: List[int],
        margin_of_victory_gradient: List[float],
        underdog_threshold: List[float],
        favorite_threshold: List[float],
        home_bias: List[float],
        k_decay_factor: List[float],
        context_generators: List[Callable[..., dict[Game, GameContext]]],
        test_fn: Callable,
        cache_prefix: str,
        total_value_threshold: float = 0) -> None:
    extracted = extractor.extract()
    futures = []
    with Pool(processes=20) as pool:
        for k_ in k:
            for r in recursions:
                for m in margin_of_victory_gradient:
                    for kd in k_decay_factor:
                        for h in home_bias:
                            for context_generator in context_generators:
                                futures.append(pool.apply_async(
                                    process_context_with_thresholds,
                                    (extracted, k_, r, m, h, kd, context_generator, underdog_threshold, favorite_threshold, test_fn, cache_prefix),
                                    callback=lambda x: print(f"Done: {x}"),
                                    error_callback=lambda e: print(f"Failed: {e}")
                                ))

        params: Tuple
        results: Tuple[float, float]
        full_list: List[Tuple[Tuple, Tuple[float, float]]] = []

        for future in futures:
            future.wait(timeout=60)

        for future in futures:
            try:
                result = future.get(timeout=60)
            except multiprocessing.context.TimeoutError:
                continue
            for params, results in result.items():
                full_list.append((params, results))

    filtered_list = sorted([item for item in full_list if item[1][0] * item[1][1] > total_value_threshold], key=lambda x: -(x[1][0] * x[1][1]))[:50]

    for combo, results in filtered_list:
        value, bets_placed = results
        print(f"{combo} {value} ({bets_placed}) = {value * bets_placed}")


def explore_nhl():
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nhl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        k=[3, 4, 5, 7, 8, 9, 10],
        recursions=[1],
        margin_of_victory_gradient=[0],
        underdog_threshold=[0.16, 0.165, 0.17, 0.175],
        favorite_threshold=[0.1, 0.2, 0.3, 0.35, 0.4],
        home_bias=[0.52, 0.53, 0.54],
        k_decay_factor=[80, 95, 100, 105],
        test_fn=test_nhl_predictor,
        context_generators=[generate_game_context_for_games_recursive_regenerate],
        total_value_threshold=-8,
        cache_prefix="nhl"
    )


def explore_nba():
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nba.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        k=[140, 142, 143, 144, 145],
        recursions=[2, 3, 4, 7],
        margin_of_victory_gradient=[1],
        underdog_threshold=[0.235, 0.24, 0.245, 0.25],
        favorite_threshold=[0.3, 0.31, 0.315, 0.32],
        home_bias=[0.56, 0.57, 0.575],
        k_decay_factor=[43, 45, 46, 47],
        context_generators=[generate_game_context_for_games_recursive_regenerate],
        test_fn=test_nba_predictor,
        cache_prefix="nba"
    )


def explore_ncaab():
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'ncaab.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        k=[55, 75, 90],
        recursions=[2, 3],
        margin_of_victory_gradient=[0.05, 0.5, 1],
        underdog_threshold=[0.425, 0.43, 0.44, 0.45],
        favorite_threshold=[0.4],
        home_bias=[0.575, 0.6],
        k_decay_factor=[15, 20, 30, 35],
        context_generators=[generate_game_context_for_games_recursive_regenerate],
        test_fn=test_ncaab_predictor,
        cache_prefix="ncaab"
    )


def explore_nfl():
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nfl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        [2, 5, 7, 10, 20, 30, 40],
        [0, 1, 5],
        [1],
        [0.15, 0.2, 0.22, 0.28, 0.3, 0.32],
        [0.57, 0.6, 0.65],
        [0, 25, 50],
        test_nfl_predictor,
        total_value_threshold=-5
    )


def explore_mlb():
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'mlb.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    space_explorer(
        extractor,
        [2, 5, 7, 10],
        [0, 1, 5],
        [1],
        [0.1, 0.15, 0.2, 0.22, 0.25, 0.28],
        [0.57, 0.6],
        [0, 50, 200, 400, 600],
        [generate_game_context_for_games_recursive],
        test_mlb_predictor,
        total_value_threshold=-5
    )


def create_context_and_predictor(
        extractor: HistoricalBetDataExtractor,
        k: float,
        r: int,
        m: float,
        h: float,
        ut: float,
        ft: float,
        kd: float,
        cache_prefix: str
) -> Tuple[dict[Game, GameContext], TeamEloProbabilityPredictor]:
    extracted = extractor.extract()

    params = (k, r, m, h, kd)
    maybe_cached_result = check_context_cache(cache_prefix, params)

    contexts: dict[Game, GameContext]
    if maybe_cached_result is not None:
        contexts = maybe_cached_result
    else:
        contexts = generate_game_context_for_games_recursive_regenerate(
            extracted.games,
            k=k,
            recursions=r,
            margin_of_victory_gradient=m,
            home_bias=h,
            k_decay_factor=kd
        )
        cache_contexts(cache_prefix, params, contexts)

    predictor = TeamEloProbabilityPredictor(contexts, underdog_threshold=ut, favorite_threshold=ft, home_bias=h)

    return contexts, predictor


def test_single_nba_case(k: float, r: int, m: float, ut: float, ft: float, h: float, kd: float) -> None:
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nba.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    contexts, predictor = create_context_and_predictor(extractor, k=k, r=r, m=m, h=h, ut=ut, ft=ft, kd=kd, cache_prefix="nba")

    test_nba_predictor(extractor.extract(), predictor, contexts, write_report=True)


def test_single_ncaab_case(k: float, r: int, m: float, ut: float, ft: float, h: float, kd: float) -> None:
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'ncaab.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)

    contexts, predictor = create_context_and_predictor(extractor, k=k, r=r, m=m, h=h, ut=ut, ft=ft, kd=kd, cache_prefix="ncaab")

    test_ncaab_predictor(extractor.extract(), predictor, contexts, write_report=True)


def test_single_nhl_case(k: float, r: int, m: float, ut: float, ft: float, h: float, kd: int) -> None:
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nhl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
    contexts, predictor = create_context_and_predictor(extractor, k=k, r=r, m=m, h=h, ut=ut, ft=ft, kd=kd, cache_prefix="nhl")

    test_nhl_predictor(extractor.extract(), predictor, contexts, write_report=True)


def test_single_nfl_case(k: float, r: int, m: float, t: float, h: float, kd: int) -> None:
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'nfl.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
    contexts, predictor = create_context_and_predictor(extractor, k, r, m, h, t, kd)

    test_nfl_predictor(extractor, predictor, contexts)


def test_single_mlb_case(k: float, r: int, m: float, t: float, h: float, kd: int) -> None:
    scottfree_path = os.path.join(BASE_DIR, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources',
                                  'mlb.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(scottfree_path)
    contexts, predictor = create_context_and_predictor(extractor, k, r, m, h, t, kd)

    test_mlb_predictor(extractor, predictor, contexts)


# Example usage
if __name__ == '__main__':
    #test_single_nba_case(144, 7, 1, 0.24, 0.315, 0.57, 45)
    #test_single_nfl_case(1, 5, 1, 0.18, 0.57, 80)
    #explore_nhl()
    #test_single_nhl_case(9, 1,  0, 0.165, 0.1, 0.53, 100)
    #explore_nba()
    #explore_ncaab()
    #test_single_ncaab_case(75, 3, 1, 0.425, 0.4,  0.6, 20)

    #check_context_cache((115, 7, 2, 0.57, 50))

    #explore_nfl()
    #test_single_nfl_case(20, 0, 0, 0.22, 0.57, 0)
    #test_single_nfl_case(40, 0, 0, 0.28, 0.57, 0)
    #explore_mlb()
    #test_single_mlb_case(2, 0, 0, .22, 0.6, 0)
