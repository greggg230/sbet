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
            try:
                team = Team(
                    league_id=int(row['league_id']),
                    team_id=int(row['team_id']),
                    min_year=float(row['min_year']) if row['min_year'] else None,
                    max_year=float(row['max_year']) if row['max_year'] else None,
                    abbreviation=row['abbreviation']
                )
                teams.append(team)
            except ValueError as e:
                print(f"Skipping row due to error: {e}")
    return teams

def read_games(file_path: str) -> List[Game]:
    games: List[Game] = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row: dict
        for row in reader:
            try:
                game = Game(
                    game_id=int(row['game_id']),
                    game_date=row['game_date'],
                    matchup=row['matchup'],
                    team_id=int(row['team_id']),
                    is_home=row['is_home'].lower() == 't',
                    wl=row['wl'],
                    w=int(row['w']) if row['w'] else None,
                    l=int(row['l']) if row['l'] else None,
                    w_pct=float(row['w_pct']) if row['w_pct'] else None,
                    min=int(row['min']) if row['min'] else None,
                    fgm=float(row['fgm']) if row['fgm'] else None,
                    fga=float(row['fga']) if row['fga'] else None,
                    fg_pct=float(row['fg_pct']) if row['fg_pct'] else None,
                    fg3m=float(row['fg3m']) if row['fg3m'] else None,
                    fg3a=float(row['fg3a']) if row['fg3a'] else None,
                    fg3_pct=float(row['fg3_pct']) if row['fg3_pct'] else None,
                    ftm=float(row['ftm']) if row['ftm'] else None,
                    fta=float(row['fta']) if row['fta'] else None,
                    ft_pct=float(row['ft_pct']) if row['ft_pct'] else None,
                    oreb=float(row['oreb']) if row['oreb'] else None,
                    dreb=float(row['dreb']) if row['dreb'] else None,
                    reb=float(row['reb']) if row['reb'] else None,
                    ast=float(row['ast']) if row['ast'] else None,
                    stl=float(row['stl']) if row['stl'] else None,
                    blk=float(row['blk']) if row['blk'] else None,
                    tov=float(row['tov']) if row['tov'] else None,
                    pf=float(row['pf']) if row['pf'] else None,
                    pts=int(row['pts']) if row['pts'] else None,
                    a_team_id=int(row['a_team_id']),
                    season_year=int(row['season_year']),
                    season_type=row['season_type'],
                    season=row['season']
                )
                games.append(game)
            except ValueError as e:
                print(f"Skipping row due to error: {e}")
    return games


def read_money_line_betting_odds(file_path: str) -> List[MoneyLineBettingOdds]:
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
