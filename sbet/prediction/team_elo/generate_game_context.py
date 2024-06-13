import math
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
                home_team=game.home_team,
                away_team=game.away_team,
                did_home_team_win=game.home_score > game.away_score
            )]

            effective_k = math.ceil(k * (1 - (games_played[game.home_team] / 200)))

            team_elos = calculate_sports_elo(game_outcomes, k=effective_k, current_elo=team_elos)

    return game_contexts


def generate_game_context_for_games_recursive(
        games: List[Game],
        k: float = 32,
        recursions: int = 1,
        margin_of_victory_gradient: float = 0,
        k_decay_factor: float = 570,
        home_bias: float = 0.5
) -> Dict[Game, GameContext]:
    # Sort games by date
    games.sort(key=lambda game: game.game_date)

    game_contexts = {}
    seasons = set(game.season for game in games)

    for season in seasons:
        season_games = [game for game in games if game.season == season]
        team_elos: dict[str, float] = {}
        games_played: dict[str, int] = {}
        previous_game_dates: dict[str, Optional[date]] = {}

        processed_outcomes: List[GameOutcome] = []

        current_date: Optional[date] = None
        days_into_season = 0

        for game in season_games:
            if k_decay_factor == 0:
                effective_k = k
            else:
                discount = max(1 - (min(k_decay_factor, days_into_season) / k_decay_factor), 1 / k_decay_factor)
                effective_k = k * discount

            if current_date is None:
                current_date = game.game_date
                days_into_season = 1
            elif current_date < game.game_date:
                days_into_season += 1
                # Re-run Elo again for all previous games, using the new Elo ratings.
                for i in range(recursions):
                    team_elos = calculate_sports_elo(
                        processed_outcomes,
                        k=effective_k,
                        current_elo=team_elos,
                        margin_of_victory_gradient=margin_of_victory_gradient,
                        home_bias=home_bias
                    )
                current_date = game.game_date

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

            game_outcome = GameOutcome(
                home_team=game.home_team,
                away_team=game.away_team,
                home_score=game.home_score,
                away_score=game.away_score,
                did_home_team_win=game.home_score > game.away_score
            )

            processed_outcomes.append(game_outcome)

            team_elos = calculate_sports_elo(
                [game_outcome],
                k=effective_k,
                current_elo=team_elos,
                margin_of_victory_gradient=margin_of_victory_gradient,
                home_bias=home_bias
            )

    return game_contexts


def generate_elos(
        games: List[Game],
        iterations: int,
        k: float,
        home_bias: float,
        margin_of_victory_gradient: float,
        k_decay_factor: float = 0
) -> Dict[str, float]:
    sorted_games = sorted(games, key=lambda game: game.game_date)
    teams = set([game.home_team for game in sorted_games] + [game.away_team for game in sorted_games])
    elos = {team: INITIAL_ELO for team in teams}

    unique_dates = sorted(list(set([game.game_date for game in sorted_games])))

    for i in range(iterations):
        day_counter = 0
        for udate in unique_dates:
            if k_decay_factor == 0:
                effective_k = k
            else:
                discount = max(1 - (day_counter / k_decay_factor), 1 / k_decay_factor)
                effective_k = k * discount

            todays_games = [game for game in sorted_games if game.game_date == udate]

            outcomes = [
                GameOutcome(
                    home_team=game.home_team,
                    away_team=game.away_team,
                    home_score=game.home_score,
                    away_score=game.away_score,
                    did_home_team_win=game.home_score > game.away_score
                )
                for game in todays_games
            ]
            elos = calculate_sports_elo(
                outcomes,
                effective_k,
                current_elo=elos,
                margin_of_victory_gradient=margin_of_victory_gradient,
                home_bias=home_bias
            )

            day_counter += 1

    return elos


def generate_elos_v2(
        games: List[Game],
        iterations: int,
        k: float,
        home_bias: float,
        margin_of_victory_gradient: float,
        k_decay_factor: float = 0
) -> Dict[str, float]:
    sorted_games = sorted(games, key=lambda game: game.game_date)
    teams = set([game.home_team for game in sorted_games] + [game.away_team for game in sorted_games])
    elos = {team: INITIAL_ELO for team in teams}

    unique_dates = sorted(list(set([game.game_date for game in sorted_games])))

    for i in range(iterations):
        day_counter = 0
        for udate in unique_dates:
            if k_decay_factor == 0:
                effective_k = k
            else:
                discount = max(1 - (day_counter / k_decay_factor), 1 / k_decay_factor)
                effective_k = k * discount

            todays_games = [game for game in sorted_games if game.game_date == udate]

            outcomes = [
                GameOutcome(
                    home_team=game.home_team,
                    away_team=game.away_team,
                    home_score=game.home_score,
                    away_score=game.away_score,
                    did_home_team_win=game.home_score > game.away_score
                )
                for game in todays_games
            ]
            elos = calculate_sports_elo(
                outcomes,
                effective_k,
                current_elo=elos,
                margin_of_victory_gradient=margin_of_victory_gradient,
                home_bias=home_bias
            )

            day_counter += 1

    return elos


def generate_game_context_for_games_recursive_regenerate(
        games: List[Game],
        k: float = 32,
        recursions: int = 1,
        margin_of_victory_gradient: float = 0,
        home_bias: float = 0.5,
        k_decay_factor: float = 0
) -> Dict[Game, GameContext]:
    # Sort games by date
    games.sort(key=lambda game: game.game_date)

    game_contexts = {}
    seasons = set(game.season for game in games)
    team_elos: dict[str, float] = {}

    for season in seasons:
        season_games = [game for game in games if game.season == season]

        current_date = None

        for game in season_games:
            if current_date is None or current_date < game.game_date:
                current_date = game.game_date
                previous_games = [sgame for sgame in season_games if sgame.game_date < game.game_date]

                team_elos = generate_elos(
                    previous_games,
                    recursions,
                    k,
                    home_bias=home_bias,
                    margin_of_victory_gradient=margin_of_victory_gradient,
                    k_decay_factor=k_decay_factor
                )

            # Generate GameContext
            game_context = GameContext(
                home_team_elo=team_elos.get(game.home_team, INITIAL_ELO),
                away_team_elo=team_elos.get(game.away_team, INITIAL_ELO),
                home_team_rest_days=0,
                away_team_rest_days=0,
                home_team_games_played_this_season=0,
                away_team_games_played_this_season=0
            )

            game_contexts[game] = game_context

    return game_contexts
