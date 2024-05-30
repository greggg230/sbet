from dataclasses import dataclass
from typing import List

from frozendict import frozendict

from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.models.transform.game import Game


@dataclass(frozen=True)
class HistoricalBetData:
    games: List[Game]
    money_line_data: frozendict[Game, GameBettingOpportunities]