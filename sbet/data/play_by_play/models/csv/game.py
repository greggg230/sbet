from dataclasses import dataclass
from typing import List

from sbet.data.play_by_play.models.csv.play import Play


@dataclass(frozen=True)
class Game:
    game_id: str
    date: str
    home_team: str
    away_team: str
    plays: List[Play]
