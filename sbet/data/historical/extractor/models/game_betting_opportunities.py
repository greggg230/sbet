from dataclasses import dataclass
from typing import Optional

from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity


@dataclass(frozen=True)
class GameBettingOpportunities:
    home: Optional[MoneyLineBettingOpportunity]
    away: Optional[MoneyLineBettingOpportunity]
    draw: Optional[MoneyLineBettingOpportunity]
