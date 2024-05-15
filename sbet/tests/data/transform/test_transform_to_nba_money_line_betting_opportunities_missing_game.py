import unittest
from sbet.data.models.csv_models import Team, Game, MoneyLineBettingOdds
from sbet.data.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from typing import List


class TestTransformToNbaMoneyLineBettingOpportunitiesMissingGame(unittest.TestCase):

    def setUp(self):
        self.teams: List[Team] = [
            Team(league_id=0, team_id=1610612737, min_year=1949.0, max_year=2018.0, abbreviation='ATL'),
            Team(league_id=0, team_id=1610612738, min_year=1946.0, max_year=2018.0, abbreviation='BOS')
        ]

        self.games: List[Game] = [
            Game(game_id=20800741, game_date='2009-02-06', matchup='ATL vs. BOS', team_id=1610612737, is_home=True,
                 wl='W',
                 w=29, l=22, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0, fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=111, a_team_id=1610612738, season_year=2008, season_type='Regular Season',
                 season='2008-09'),
            Game(game_id=20800741, game_date='2009-02-06', matchup='ATL vs. BOS', team_id=1610612738, is_home=False,
                 wl='L',
                 w=29, l=22, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0, fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=105, a_team_id=1610612737, season_year=2008, season_type='Regular Season',
                 season='2008-09')
        ]

        self.invalid_betting_odds: List[MoneyLineBettingOdds] = [
            MoneyLineBettingOdds(game_id=99999999, book_name='Book3', book_id=3, team_id=1610612738,
                                 a_team_id=1610612737, price1=100.0, price2=-100.0)
        ]

    def test_transform_to_nba_money_line_betting_opportunities_missing_game(self):
        nba_games = transform_to_nba_games(self.games, self.teams)

        with self.assertRaises(ValueError) as context:
            transform_to_nba_money_line_betting_opportunities(self.invalid_betting_odds, nba_games)

        self.assertEqual(str(context.exception), "Game ID 99999999 not found in game data.")
