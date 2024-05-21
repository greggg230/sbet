from dataclasses import dataclass
from frozendict import frozendict
from typing import FrozenSet
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
