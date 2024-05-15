from dataclasses import dataclass
from .nba_game import NbaGame


@dataclass(frozen=True)
class NbaMoneyLineBettingOpportunity:
    game: NbaGame
    book_name: str
    away_odds: float
    home_odds: float
