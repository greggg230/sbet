from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Play:
    game_id: int
    data_set: str
    date: str
    a1: str
    a2: str
    a3: str
    a4: str
    a5: str
    h1: str
    h2: str
    h3: str
    h4: str
    h5: str
    period: int
    away_score: int
    home_score: int
    remaining_time: str
    elapsed: str
    play_length: str
    play_id: int
    team: str
    event_type: str
    assist: Optional[str]
    away: Optional[str]
    home: Optional[str]
    block: Optional[str]
    entered: Optional[str]
    left: Optional[str]
    num: Optional[str]
    opponent: Optional[str]
    outof: Optional[str]
    player: Optional[str]
    points: Optional[int]
    possession: Optional[str]
    reason: Optional[str]
    result: Optional[str]
    steal: Optional[str]
    type: Optional[str]
    shot_distance: Optional[int]
    original_x: Optional[int]
    original_y: Optional[int]
    converted_x: Optional[float]
    converted_y: Optional[float]
    description: str
