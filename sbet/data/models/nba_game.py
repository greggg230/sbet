from dataclasses import dataclass
from sbet.data.models.nba_team import NbaTeam


@dataclass(frozen=True)
class NbaGame:
    game_id: int
    game_date: str
    season: str
    game_type: str
    home_team: NbaTeam
    away_team: NbaTeam
    home_score: int
    away_score: int
