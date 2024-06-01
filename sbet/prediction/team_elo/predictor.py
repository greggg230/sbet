from typing import Dict

from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.models.game_context import GameContext


class TeamEloProbabilityPredictor(BetProbabilityPredictor):
    def __init__(self, game_contexts: Dict[Game, GameContext]):
        self.game_contexts = game_contexts

    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        game_context = self.game_contexts[opportunity.game]
        home_team_elo = game_context.home_team_elo
        away_team_elo = game_context.away_team_elo
        expected_home_win_prob = .969 / (1 + 10 ** ((away_team_elo - home_team_elo) / 400))
        return expected_home_win_prob if opportunity.bet_on_home_team else 1 - expected_home_win_prob
