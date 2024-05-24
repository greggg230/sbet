from abc import ABC
from dataclasses import dataclass

from sbet.data.play_by_play.models.transform.player import Player

from sbet.data.play_by_play.models.transform.nba_play import NbaPlay


@dataclass(frozen=True)
class Turnover(NbaPlay, ABC):
    pass


@dataclass(frozen=True)
class Steal(Turnover):
    stolen_from: Player
    stolen_by: Player


@dataclass(frozen=True)
class ShotClockViolation(Turnover):
    pass


@dataclass(frozen=True)
class OutOfBoundsTurnover(Turnover):
    player: Player


@dataclass(frozen=True)
class OffensiveFoulTurnover(NbaPlay):
    pass


@dataclass(frozen=True)
class TravelingTurnover(Turnover):
    player: Player
