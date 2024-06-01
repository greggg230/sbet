from abc import abstractmethod, ABC
from typing import Optional

from sbet.data.historical.extractor.models.historical_bet_data import HistoricalBetData


class HistoricalBetDataExtractor(ABC):
    csv_file_path: str
    _extracted_data: Optional[HistoricalBetData] = None

    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path

    def extract(self) -> HistoricalBetData:
        if self._extracted_data is None:
            self._extracted_data = self._do_extraction()
        return self._extracted_data

    @abstractmethod
    def _do_extraction(self) -> HistoricalBetData:
        ...
