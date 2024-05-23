from dataclasses import dataclass


@dataclass(frozen=True)
class FreeThrowState:
    free_throws_remaining: int
    for_home_team: bool
    shooting_team_gets_possession_after: bool
