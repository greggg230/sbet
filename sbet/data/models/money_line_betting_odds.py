from dataclasses import dataclass


@dataclass(frozen=True)
class MoneyLineBettingOdds:
    game_id: int
    book_name: str
    book_id: int
    team_id: int
    a_team_id: int
    price1: float
    price2: float
