from datetime import timedelta
from typing import List, Dict
from collections import defaultdict
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.prediction.team_elo.models.game_context import GameContext
from sbet.prediction.team_elo.calculate_nba_elo import calculate_nba_elo
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome

# Default Elo rating
INITIAL_ELO = 1500.0


def generate_game_context_for_games(games: List[NbaGame]) -> Dict[NbaGame, GameContext]:
    games_sorted = sorted(games, key=lambda game: game.game_date)
    team_last_game_date =  {team: None for team in NbaTeam}
    team_elos = {team: INITIAL_ELO for team in NbaTeam}
    game_contexts = {}

    for game in games_sorted:
        home_team = game.home_team
        away_team = game.away_team

        home_team_rest_days = (game.game_date - team_last_game_date[home_team]).days - 1 if team_last_game_date[home_team] else 0
        away_team_rest_days = (game.game_date - team_last_game_date[away_team]).days - 1 if team_last_game_date[away_team] else 0

        game_contexts[game] = GameContext(
            home_team_elo=team_elos[home_team],
            away_team_elo=team_elos[away_team],
            home_team_rest_days=home_team_rest_days,
            away_team_rest_days=away_team_rest_days
        )

        # Update the last game date for each team
        team_last_game_date[home_team] = game.game_date
        team_last_game_date[away_team] = game.game_date

        # Update Elo ratings after the game
        outcome = NbaGameOutcome(home_team=home_team, away_team=away_team, did_home_team_win=game.home_score > game.away_score)
        team_elos = calculate_nba_elo([outcome], k=32, current_elo=team_elos)

    return game_contexts
