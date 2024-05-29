# sbet/prediction/team_elo/calculate_home_away_split_nba_elo.py

from typing import List, Dict, Tuple
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.prediction.team_elo.elo import calculate_elo
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome

# Elo rating parameters
INITIAL_ELO = 1500.0


def calculate_home_away_split_nba_elo(game_outcomes: List[NbaGameOutcome], k: float = 32) -> Dict[NbaTeam, Tuple[float, float]]:
    team_elos = {team: (INITIAL_ELO, INITIAL_ELO) for team in NbaTeam}

    for outcome in game_outcomes:
        home_team = outcome.home_team
        away_team = outcome.away_team
        home_team_home_elo, home_team_away_elo = team_elos[home_team]
        away_team_home_elo, away_team_away_elo = team_elos[away_team]

        if outcome.did_home_team_win:
            new_home_elo, new_away_elo = calculate_elo(home_team_home_elo, away_team_away_elo, k)
            team_elos[home_team] = (new_home_elo, home_team_away_elo)
            team_elos[away_team] = (away_team_home_elo, new_away_elo)
        else:
            new_away_elo, new_home_elo = calculate_elo(away_team_away_elo, home_team_home_elo, k)
            team_elos[home_team] = (new_home_elo, home_team_away_elo)
            team_elos[away_team] = (away_team_home_elo, new_away_elo)

    return team_elos
