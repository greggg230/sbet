# fouls.py

from abc import ABC
from dataclasses import dataclass
from typing import Optional

from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType


@dataclass(frozen=True)
class Foul(NbaPlay, ABC):
    pass


@dataclass(frozen=True)
class OffensiveFoul(Foul):
    fouling_player: Player


@dataclass(frozen=True)
class PersonalFoul(Foul):
    fouling_player: Player


@dataclass(frozen=True)
class ShootingFoul(Foul):
    fouling_player: Player
    field_goal_type: FieldGoalType
    field_goal_made: bool


@dataclass(frozen=True)
class TechnicalFoul(Foul):
    fouling_player: Optional[Player]
    is_home_team: bool


@dataclass(frozen=True)
class FlagrantFoul(Foul):
    fouling_player: Player
