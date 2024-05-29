from typing import List, Dict

from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.prediction.team_elo.calculate_nba_elo import calculate_nba_elo
from sbet.prediction.team_elo.models.game_context import GameContext
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome

INITIAL_ELO = 1500.0


def generate_game_context_for_games(games: List[NbaGame]) -> Dict[NbaGame, GameContext]:
    # Sort games by date
    games.sort(key=lambda game: game.game_date)

    game_contexts = {}
    seasons = set(game.season for game in games)

    for season in seasons:
        season_games = [game for game in games if game.season == season]
        team_elos = {team: INITIAL_ELO for team in NbaTeam}
        games_played = {team: 0 for team in NbaTeam}
        previous_game_dates = {team: None for team in NbaTeam}

        for game in season_games:
            # Calculate rest days
            home_rest_days = (game.game_date - previous_game_dates[game.home_team]).days if previous_game_dates[
                game.home_team] else 0
            away_rest_days = (game.game_date - previous_game_dates[game.away_team]).days if previous_game_dates[
                game.away_team] else 0

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

            game_outcomes = [NbaGameOutcome(
                home_team=g.home_team,
                away_team=g.away_team,
                did_home_team_win=g.home_score > g.away_score
            ) for g in season_games if g.game_date <= game.game_date]
            team_elos = calculate_nba_elo(game_outcomes)

    return game_contexts
