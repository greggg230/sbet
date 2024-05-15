from typing import List, Dict
from sbet.data.models import NbaGame, NbaMoneyLineBettingOpportunity, NbaTeam
from sbet.data.models.csv_models import Game, Team, MoneyLineBettingOdds


def transform_to_nba_games(games: List[Game], teams: List[Team]) -> List[NbaGame]:
    team_id_to_abbreviation: Dict[int, str] = {team.team_id: team.abbreviation for team in teams}

    nba_games = []
    for game in games:
        home_team_abbreviation = team_id_to_abbreviation.get(game.team_id)
        away_team_abbreviation = team_id_to_abbreviation.get(game.a_team_id)

        if home_team_abbreviation and away_team_abbreviation:
            game_type = "Preseason" if "Preseason" in game.season_type else "Regular Season" if "Regular" in game.season_type else "Playoff"

            nba_game = NbaGame(
                game_id=game.game_id,
                game_date=game.game_date,
                season=game.season,
                game_type=game_type,
                home_team=NbaTeam[home_team_abbreviation],
                away_team=NbaTeam[away_team_abbreviation]
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

        opportunity = NbaMoneyLineBettingOpportunity(
            game=game,
            book_name=odds.book_name,
            away_odds=odds.price1,
            home_odds=odds.price2
        )
        opportunities.append(opportunity)

    return opportunities
