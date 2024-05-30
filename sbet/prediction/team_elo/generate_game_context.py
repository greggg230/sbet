from datetime import date
from typing import List, Dict, Optional

from sbet.data.historical.models.transform.game import Game
from sbet.prediction.team_elo.calculate_sports_elo import calculate_sports_elo
from sbet.prediction.team_elo.models.game_context import GameContext
from sbet.prediction.team_elo.models.game_outcome import GameOutcome

INITIAL_ELO = 1500.0


def generate_game_context_for_games(games: List[Game], k: int = 32) -> Dict[Game, GameContext]:
    # Sort games by date
    games.sort(key=lambda game: game.game_date)

    game_contexts = {}
    seasons = set(game.season for game in games)

    for season in seasons:
        season_games = [game for game in games if game.season == season]
        team_elos: dict[str, float] = {}
        games_played: dict[str, int] = {}
        previous_game_dates: dict[str, Optional[date]] = {}

        for game in season_games:
            if game.home_team not in previous_game_dates:
                previous_game_dates[game.home_team] = None
            if game.away_team not in previous_game_dates:
                previous_game_dates[game.away_team] = None
            # Calculate rest days
            home_rest_days = (game.game_date - previous_game_dates[game.home_team]).days if previous_game_dates[
                game.home_team] else 0
            away_rest_days = (game.game_date - previous_game_dates[game.away_team]).days if previous_game_dates[
                game.away_team] else 0

            if game.home_team not in games_played:
                games_played[game.home_team] = 0
            if game.away_team not in games_played:
                games_played[game.away_team] = 0

            if game.home_team not in team_elos:
                team_elos[game.home_team] = INITIAL_ELO
            if game.away_team not in team_elos:
                team_elos[game.away_team] = INITIAL_ELO

            # Generate GameContext
            game_context = GameContext(
                home_team_elo=team_elos[game.home_team],
                away_team_elo=team_elos[game.away_team],
                home_team_rest_days=home_rest_days,
                away_team_rest_days=away_rest_days,
                home_team_games_played_this_season=games_played[game.home_team] + 1,
                away_team_games_played_this_season=games_played[game.away_team] + 1
            )
            game_contexts[game] = game_context

            # Update games played counter
            games_played[game.home_team] += 1
            games_played[game.away_team] += 1

            # Update Elo ratings after the game
            previous_game_dates[game.home_team] = game.game_date
            previous_game_dates[game.away_team] = game.game_date

            game_outcomes = [GameOutcome(
                home_team=g.home_team,
                away_team=g.away_team,
                did_home_team_win=g.home_score > g.away_score
            ) for g in season_games if g.game_date <= game.game_date]
            team_elos = calculate_sports_elo(game_outcomes, k=k)

    return game_contexts
