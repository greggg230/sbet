from dataclasses import dataclass
from sbet.data.historical.models.transform import NbaGame
from sbet.data.historical.models.transform.game import Game


@dataclass(frozen=True)
class MoneyLineBettingOpportunity:
    game: Game
    book_name: str
    bet_on_home_team: bool
    price: float
