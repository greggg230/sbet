from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Team:
    league_id: int
    team_id: int
    min_year: Optional[float]
    max_year: Optional[float]
    abbreviation: str
