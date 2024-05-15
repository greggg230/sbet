from typing import List, Dict
from sbet.data.models import NbaGame, NbaTeam
from sbet.data.models.csv_models import Game, Team


def transform_to_nba_games(games: List[Game], teams: List[Team]) -> List[NbaGame]:
    # Create a mapping from team_id to team abbreviation
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
