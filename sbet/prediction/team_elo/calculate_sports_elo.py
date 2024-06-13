from typing import List, Dict, Optional
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.prediction.team_elo.elo import calculate_elo
from sbet.prediction.team_elo.models.game_outcome import GameOutcome

# Elo rating parameters
INITIAL_ELO = 1500.0


def calculate_sports_elo(
    game_outcomes: List[GameOutcome],
    k: float = 32,
    current_elo: Optional[Dict[str, float]] = None,
    margin_of_victory_gradient: float = 1,
    home_bias: float = 0.5
) -> Dict[str, float]:
    if current_elo is None:
        current_elo = {}

    team_elos = {}

    if current_elo is not None:
        team_elos.update(current_elo)

    for outcome in game_outcomes:
        home_team = outcome.home_team
        away_team = outcome.away_team

        if home_team not in team_elos:
            team_elos[home_team] = current_elo.get(home_team, INITIAL_ELO)
        if away_team not in team_elos:
            team_elos[away_team] = current_elo.get(away_team, INITIAL_ELO)

        home_team_elo = team_elos[home_team]
        away_team_elo = team_elos[away_team]

        margin_of_victory = abs(outcome.home_score - outcome.away_score)

        effective_k = min(margin_of_victory_gradient * k * margin_of_victory, k)

        if margin_of_victory > 0:
            if outcome.did_home_team_win:
                new_home_elo, new_away_elo = calculate_elo(home_team_elo, away_team_elo, effective_k, winner_bias=home_bias)
            else:
                new_away_elo, new_home_elo = calculate_elo(away_team_elo, home_team_elo, effective_k, winner_bias=home_bias)

            team_elos[home_team] = new_home_elo
            team_elos[away_team] = new_away_elo

    return team_elos
