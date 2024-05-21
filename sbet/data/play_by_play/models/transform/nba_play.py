from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class NbaPlay(ABC):
    play_length: int
    play_id: str
    description: str
