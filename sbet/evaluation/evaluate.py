from dataclasses import dataclass
from typing import List
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity


@dataclass
class PredictorEvaluation:
    average_profit: float
    number_of_bets_placed: int


def evaluate_bet_probability_predictor(
    predictor: BetProbabilityPredictor,
    opportunities: List[NbaMoneyLineBettingOpportunity],
    threshold: float
) -> PredictorEvaluation:
    total_profit = 0.0
    placed_bets = 0

    for opportunity in opportunities:
        win_probability = predictor.calculate_probability_of_bet_win(opportunity)
        implied_probability = convert_moneyline_to_probability(opportunity.price)

        if opportunity.bet_on_home_team:
            bet_won = opportunity.game.home_score > opportunity.game.away_score
        else:
            bet_won = opportunity.game.home_score < opportunity.game.away_score

        if win_probability - implied_probability > threshold:
            placed_bets += 1
            if bet_won:
                if opportunity.price > 0:
                    total_profit += opportunity.price / 100
                else:
                    total_profit += 100 / abs(opportunity.price)
            else:
                total_profit -= 1

    average_profit = total_profit / placed_bets if placed_bets > 0 else 0.0
    return PredictorEvaluation(average_profit=average_profit, number_of_bets_placed=placed_bets)


def convert_moneyline_to_probability(moneyline: float) -> float:
    if moneyline > 0:
        return 100 / (moneyline + 100)
    else:
        return -moneyline / (-moneyline + 100)
