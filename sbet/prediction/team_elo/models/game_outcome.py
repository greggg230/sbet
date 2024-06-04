from dataclasses import dataclass


@dataclass(frozen=True)
class GameOutcome:
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    did_home_team_win: bool
