from dataclasses import dataclass
from sbet.data.historical.models import NbaGame


@dataclass(frozen=True)
class NbaMoneyLineBettingOpportunity:
    game: NbaGame
    book_name: str
    bet_on_home_team: bool
    price: float
