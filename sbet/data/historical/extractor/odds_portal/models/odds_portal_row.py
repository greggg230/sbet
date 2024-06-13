from dataclasses import dataclass


@dataclass(frozen=True)
class OddsPortalRow:
    home_team: str
    away_team: str
    date_start_timestamp: int
    home_score: int
    away_score: int
    home_moneyline_price: float
    draw_moneyline_price: float
    away_moneyline_price: float
