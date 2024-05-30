from dataclasses import dataclass


@dataclass(frozen=True)
class ScottfreeGameCsvRow:
    season: str
    date: str
    away_team: str
    away_score: str
    away_point_spread: str
    away_point_spread_line: str
    away_money_line: str
    home_team: str
    home_score: str
    home_point_spread: str
    home_point_spread_line: str
    home_money_line: str
    over_under: str
    over_line: str
    under_line: str
