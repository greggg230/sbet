from dataclasses import dataclass


@dataclass(frozen=True)
class GameContext:
    home_team_elo: float
    away_team_elo: float
    away_team_rest_days: int
    home_team_rest_days: int
    home_team_games_played_this_season: int
    away_team_games_played_this_season: int
