from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Game:
    game_id: str | int
    game_date: date
    season: str
    game_type: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
