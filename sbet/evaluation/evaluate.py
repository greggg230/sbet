from dataclasses import dataclass
from datetime import date
from typing import List

from frozendict import frozendict

from sbet.data.historical.models.transform.bet_type import BetType
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.game_result import GameResult
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.models.game_context import GameContext


@dataclass(frozen=True)
class PredictorEvaluationDetail:
    date: date
    season: str
    home_team: str
    away_team: str
    home_elo: float
    away_elo: float
    bet_type: BetType
    expected_probability_of_win: float
    bet_price: float
    bet_taken: bool
    inferred_bet_probability: float
    bet_won: bool
    net_winnings: float


@dataclass(frozen=True)
class MonthDetails:
    average_profit: float
    number_of_bets_placed: int


@dataclass(frozen=True)
class PredictorEvaluation:
    average_profit: float
    number_of_bets_placed: int
    number_of_bets_skipped: int
    details: frozenset[PredictorEvaluationDetail]
    details_by_month: dict[int, MonthDetails]


def evaluate_bet_probability_predictor(
    predictor: BetProbabilityPredictor,
    opportunities: List[MoneyLineBettingOpportunity],
    create_report: bool = False,
    contexts: frozendict[Game, GameContext] = frozendict({})
) -> PredictorEvaluation:
    total_profit = 0.0
    placed_bets = 0
    bets_skipped = 0

    details: List[PredictorEvaluationDetail] = []
    bets_by_month: dict[int, List[float]] = {i: [] for i in range(1, 13)}

    for opportunity in opportunities:
        if opportunity.bet_type == BetType.HOME_WIN:
            bet_won = opportunity.game.result == GameResult.HOME_WINS
        elif opportunity.bet_type == BetType.AWAY_WIN:
            bet_won = opportunity.game.result == GameResult.AWAY_WINS
        else:
            bet_won = opportunity.game.result == GameResult.DRAW

        bet_taken = predictor.select_opportunity(opportunity)
        net_winnings: float

        if bet_taken:
            placed_bets += 1
            if bet_won:
                if opportunity.price > 0:
                    net_winnings = opportunity.price / 100
                    total_profit += net_winnings
                else:
                    net_winnings = 100 / abs(opportunity.price)
                    total_profit += net_winnings
            else:
                net_winnings = -1
                total_profit -= 1
            bets_by_month[opportunity.game.game_date.month].append(net_winnings)
        else:
            net_winnings = 0
            bets_skipped += 1

        if create_report:
            context = contexts[opportunity.game]
            win_probability = predictor.calculate_probability_of_bet_win(opportunity)
            implied_probability = convert_moneyline_to_probability(opportunity.price)
            details.append(PredictorEvaluationDetail(
                date=opportunity.game.game_date,
                season=opportunity.game.season,
                home_team=opportunity.game.home_team,
                away_team=opportunity.game.away_team,
                home_elo=context.home_team_elo,
                away_elo=context.away_team_elo,
                bet_type=opportunity.bet_type,
                expected_probability_of_win=win_probability,
                bet_price=opportunity.price,
                bet_taken=bet_taken,
                inferred_bet_probability=implied_probability,
                bet_won=bet_won,
                net_winnings=net_winnings
            ))

    average_profit = total_profit / placed_bets if placed_bets > 0 else 0.0

    details_by_month = {}
    for month, month_bets in bets_by_month.items():
        details_by_month[month] = MonthDetails(
            average_profit=(sum(month_bets) / len(month_bets)) if len(month_bets) else 0,
            number_of_bets_placed=len(month_bets)
        )

    return PredictorEvaluation(
        average_profit=average_profit,
        number_of_bets_placed=placed_bets,
        number_of_bets_skipped=bets_skipped,
        details=frozenset(details),
        details_by_month=details_by_month
    )


def convert_moneyline_to_probability(moneyline: float) -> float:
    if moneyline > 0:
        return 100 / (moneyline + 100)
    else:
        return -moneyline / (-moneyline + 100)
