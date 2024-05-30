from abc import ABC, abstractmethod
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity


class BetProbabilityPredictor(ABC):

    @abstractmethod
    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        pass
