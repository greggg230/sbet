from typing import Dict

from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.elo import calculate_win_probability
from sbet.prediction.team_elo.models.game_context import GameContext


class TeamEloProbabilityPredictor(BetProbabilityPredictor):
    game_contexts: Dict[Game, GameContext]
    home_bias: float

    def __init__(self, game_contexts: Dict[Game, GameContext], threshold: float, home_bias: float = 0.5):
        self.threshold = threshold
        self.game_contexts = game_contexts
        self.home_bias = home_bias

    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        game_context = self.game_contexts[opportunity.game]
        home_team_elo = game_context.home_team_elo
        away_team_elo = game_context.away_team_elo
        expected_home_win_prob = calculate_win_probability(home_team_elo, away_team_elo, winner_bias=self.home_bias)
        return expected_home_win_prob if opportunity.bet_on_home_team else 1 - expected_home_win_prob
