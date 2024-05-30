from dataclasses import dataclass


@dataclass(frozen=True)
class GameOutcome:
    home_team: str
    away_team: str
    did_home_team_win: bool
