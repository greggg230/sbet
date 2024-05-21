from dataclasses import dataclass
from typing import FrozenSet
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.turnover import Turnover, Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoul


@dataclass(frozen=True)
class FieldGoalAttempt(NbaPlay):
    shot_made: bool
    points: int


@dataclass(frozen=True)
class Substitution(NbaPlay):
    home_team_lineup: FrozenSet[Player]
    away_team_lineup: FrozenSet[Player]


@dataclass(frozen=True)
class PeriodStart(NbaPlay):
    period_number: int


@dataclass(frozen=True)
class PeriodEnd(NbaPlay):
    period_number: int


@dataclass(frozen=True)
class Timeout(NbaPlay):
    is_home: bool


@dataclass(frozen=True)
class Foul(NbaPlay):
    foul_type: str
    committed_by: Player


@dataclass(frozen=True)
class JumpBall(NbaPlay):
    home_player: Player
    away_player: Player
    did_home_team_win: bool
