from dataclasses import dataclass
from typing import List

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play


@dataclass(frozen=True)
class Game:
    game_id: int
    date: str
    home_team: NbaTeam
    away_team: NbaTeam
    plays: List[Play]
