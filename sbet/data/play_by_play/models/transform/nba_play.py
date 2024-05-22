from dataclasses import dataclass


@dataclass(frozen=True)
class NbaPlay:
    play_length: int
    play_id: int
