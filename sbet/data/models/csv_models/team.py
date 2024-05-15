from dataclasses import dataclass


@dataclass(frozen=True)
class Team:
    league_id: int
    team_id: int
    min_year: float
    max_year: float
    abbreviation: str
