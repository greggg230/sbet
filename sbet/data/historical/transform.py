from datetime import datetime
from typing import List, Dict, Optional
from sbet.data.historical.models import NbaGame, NbaMoneyLineBettingOpportunity, NbaTeam
from sbet.data.historical.models import Game, Team, MoneyLineBettingOdds


def transform_to_nba_games(games: List[Game], teams: List[Team]) -> List[NbaGame]:
    team_id_to_abbreviation: Dict[int, str] = {team.team_id: team.abbreviation for team in teams}
    game_pairs: Dict[int, Dict[str, Optional[Game]]] = {}

    for game in games:
        if game.game_id not in game_pairs:
            game_pairs[game.game_id] = {"home": None, "away": None}

        if game.is_home:
            game_pairs[game.game_id]["home"] = game
        else:
            game_pairs[game.game_id]["away"] = game

    nba_games = []
    for game_id, pair in game_pairs.items():
        home_game = pair["home"]
        away_game = pair["away"]

        if home_game and away_game and home_game.game_date:
            home_team_abbreviation = team_id_to_abbreviation.get(home_game.team_id)
            away_team_abbreviation = team_id_to_abbreviation.get(away_game.team_id)

            if home_team_abbreviation and away_team_abbreviation:
                game_type = "Preseason" if "Preseason" in home_game.season_type else "Regular Season" if "Regular" in home_game.season_type else "Playoff"

                try:
                    game_date = datetime.strptime(home_game.game_date, '%Y-%m-%d').date()
                except ValueError:
                    # Skip if the date format is incorrect
                    continue

                nba_game = NbaGame(
                    game_id=home_game.game_id,
                    game_date=game_date,
                    season=home_game.season,
                    game_type=game_type,
                    home_team=NbaTeam[home_team_abbreviation],
                    away_team=NbaTeam[away_team_abbreviation],
                    home_score=home_game.pts,
                    away_score=away_game.pts
                )
                nba_games.append(nba_game)

    return nba_games


def transform_to_nba_money_line_betting_opportunities(
    money_line_betting_odds: List[MoneyLineBettingOdds],
    nba_games: List[NbaGame]
) -> List[NbaMoneyLineBettingOpportunity]:
    game_id_to_nba_game: Dict[int, NbaGame] = {game.game_id: game for game in nba_games}

    opportunities = []
    for odds in money_line_betting_odds:
        game = game_id_to_nba_game.get(odds.game_id)
        if game is None:
            raise ValueError(f"Game ID {odds.game_id} not found in game data.")

        opportunity_home = NbaMoneyLineBettingOpportunity(
            game=game,
            book_name=odds.book_name,
            bet_on_home_team=True,
            price=odds.price2
        )
        opportunities.append(opportunity_home)

        opportunity_away = NbaMoneyLineBettingOpportunity(
            game=game,
            book_name=odds.book_name,
            bet_on_home_team=False,
            price=odds.price1
        )
        opportunities.append(opportunity_away)

    return opportunities
