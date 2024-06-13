from abc import ABC, abstractmethod
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity


class BetProbabilityPredictor(ABC):
    threshold: float

    @abstractmethod
    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        pass

    def select_opportunity(self, opportunity: MoneyLineBettingOpportunity) -> bool:
        implied_probability = self.convert_moneyline_to_probability(opportunity.price)
        return self.calculate_probability_of_bet_win(opportunity) - implied_probability > self.threshold

    def convert_moneyline_to_probability(self, moneyline: float) -> float:
        if moneyline > 0:
            return 100 / (moneyline + 100)
        else:
            return -moneyline / (-moneyline + 100)
