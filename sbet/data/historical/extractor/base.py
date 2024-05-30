from abc import abstractmethod, ABC

from sbet.data.historical.extractor.models.historical_bet_data import HistoricalBetData


class HistoricalBetDataExtractor(ABC):

    @abstractmethod
    def extract(self) -> HistoricalBetData:
        ...
