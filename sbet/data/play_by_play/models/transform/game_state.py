from dataclasses import dataclass
from typing import Optional, FrozenSet

from frozendict import frozendict

from sbet.data.play_by_play.models.transform.free_throw_state import FreeThrowState
from sbet.data.play_by_play.models.transform.player import Player


@dataclass(frozen=True)
class GameState:
    current_period: int
    home_team_has_possession: bool
    personal_foul_count: frozendict[Player, int]
    ejected_players: FrozenSet[Player]
    home_score: int
    away_score: int
    milliseconds_remaining_in_period: int
    home_team_lineup: FrozenSet[Player]
    away_team_lineup: FrozenSet[Player]
    home_timeouts: int
    away_timeouts: int
    free_throw_state: Optional[FreeThrowState]
    home_team_fouls: int
    away_team_fouls: int
    home_team_fouls_in_last_two_minutes: int
    away_team_fouls_in_last_two_minutes: int
