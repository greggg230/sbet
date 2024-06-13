from typing import Dict

from sbet.data.historical.models.transform.bet_type import BetType
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.elo import calculate_win_probability
from sbet.prediction.team_elo.models.game_context import GameContext


class TeamEloProbabilityPredictor(BetProbabilityPredictor):
    underdog_threshold: float
    favorite_threshold: float
    game_contexts: Dict[Game, GameContext]
    home_bias: float

    def __init__(
            self,
            game_contexts: Dict[Game, GameContext],
            underdog_threshold: float,
            favorite_threshold: float,
            home_bias: float = 0.5
    ):
        self.underdog_threshold = underdog_threshold
        self.favorite_threshold = favorite_threshold
        self.game_contexts = game_contexts
        self.home_bias = home_bias

    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        game_context = self.game_contexts[opportunity.game]
        home_team_elo = game_context.home_team_elo
        away_team_elo = game_context.away_team_elo
        expected_home_win_prob = calculate_win_probability(home_team_elo, away_team_elo, winner_bias=self.home_bias)
        return expected_home_win_prob if opportunity.bet_type == BetType.HOME_WIN else 1 - expected_home_win_prob

    def select_opportunity(self, opportunity: MoneyLineBettingOpportunity) -> bool:
        implied_probability = self.convert_moneyline_to_probability(opportunity.price)

        threshold: float
        if implied_probability < 0.5:
            threshold = self.underdog_threshold
        else:
            threshold = self.favorite_threshold

        overlay = self.calculate_probability_of_bet_win(opportunity) - implied_probability

        return overlay > threshold
