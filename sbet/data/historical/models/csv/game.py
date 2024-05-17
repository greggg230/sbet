from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    game_id: int
    game_date: str
    matchup: str
    team_id: int
    is_home: bool
    wl: str
    w: int
    l: int
    w_pct: float
    min: int
    fgm: float
    fga: float
    fg_pct: float
    fg3m: float
    fg3a: float
    fg3_pct: float
    ftm: float
    fta: float
    ft_pct: float
    oreb: float
    dreb: float
    reb: float
    ast: float
    stl: float
    blk: float
    tov: float
    pf: float
    pts: int
    a_team_id: int
    season_year: int
    season_type: str
    season: str
