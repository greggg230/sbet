from dataclasses import dataclass
from sbet.data.historical.models.transform import NbaGame
from sbet.data.historical.models.transform.bet_type import BetType
from sbet.data.historical.models.transform.game import Game


@dataclass(frozen=True)
class MoneyLineBettingOpportunity:
    game: Game
    book_name: str
    bet_type: BetType
    price: float
