from abc import ABC, abstractmethod
from sbet.data.models import NbaMoneyLineBettingOpportunity


class BetProbabilityPredictor(ABC):

    @abstractmethod
    def calculate_probability_of_bet_win(self, opportunity: NbaMoneyLineBettingOpportunity) -> float:
        pass
