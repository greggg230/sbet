import csv
from typing import List

from sbet.data.models.csv_models.game import Game
from sbet.data.models.csv_models.money_line_betting_odds import MoneyLineBettingOdds
from sbet.data.models.csv_models.team import Team


def read_teams(file_path: str) -> List[Team]:
    teams = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            teams.append(Team(
                league_id=int(row['league_id']),
                team_id=int(row['team_id']),
                min_year=float(row['min_year']),
                max_year=float(row['max_year']),
                abbreviation=row['abbreviation']
            ))
    return teams


def read_games(file_path: str) -> List[Game]:
    games = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            games.append(Game(
                game_id=int(row['game_id']),
                game_date=row['game_date'],
                matchup=row['matchup'],
                team_id=int(row['team_id']),
                is_home=row['is_home'] == 't',
                wl=row['wl'],
                w=float(row['w']),
                l=float(row['l']),
                w_pct=float(row['w_pct']),
                min=float(row['min']),
                fgm=float(row['fgm']),
                fga=float(row['fga']),
                fg_pct=float(row['fg_pct']),
                fg3m=float(row['fg3m']),
                fg3a=float(row['fg3a']),
                fg3_pct=float(row['fg3_pct']),
                ftm=float(row['ftm']),
                fta=float(row['fta']),
                ft_pct=float(row['ft_pct']),
                oreb=float(row['oreb']),
                dreb=float(row['dreb']),
                reb=float(row['reb']),
                ast=float(row['ast']),
                stl=float(row['stl']),
                blk=float(row['blk']),
                tov=float(row['tov']),
                pf=float(row['pf']),
                pts=float(row['pts']),
                a_team_id=int(row['a_team_id']),
                season_year=int(row['season_year']),
                season_type=row['season_type'],
                season=row['season']
            ))
    return games


def read_betting_odds(file_path: str) -> List[MoneyLineBettingOdds]:
    betting_odds = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            betting_odds.append(MoneyLineBettingOdds(
                game_id=int(row['game_id']),
                book_name=row['book_name'],
                book_id=int(row['book_id']),
                team_id=int(row['team_id']),
                a_team_id=int(row['a_team_id']),
                price1=float(row['price1']),
                price2=float(row['price2'])
            ))
    return betting_odds
