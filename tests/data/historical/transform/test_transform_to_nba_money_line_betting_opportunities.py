import unittest
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity
from sbet.data.historical.models.csv import Team, Game, MoneyLineBettingOdds
from sbet.data.historical.transform import transform_to_nba_games, transform_to_nba_money_line_betting_opportunities
from typing import List


class TestTransformToNbaMoneyLineBettingOpportunities(unittest.TestCase):

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
                 season='2008-09'),
            Game(game_id=20800701, game_date='2009-01-31', matchup='BOS vs. ATL', team_id=1610612738, is_home=True,
                 wl='L',
                 w=26, l=22, w_pct=0.542, min=240, fgm=17.0, fga=36.0, fg_pct=0.472, fg3m=6.0, fg3a=15.0, fg3_pct=0.400,
                 ftm=14.0, fta=18.0, ft_pct=0.778, oreb=7.0, dreb=30.0, reb=37.0, ast=22.0, stl=6.0, blk=0.0, tov=15.0,
                 pf=22.0, pts=108, a_team_id=1610612737, season_year=2008, season_type='Regular Season',
                 season='2008-09'),
            Game(game_id=20800701, game_date='2009-01-31', matchup='BOS vs. ATL', team_id=1610612737, is_home=False,
                 wl='W',
                 w=26, l=22, w_pct=0.542, min=240, fgm=17.0, fga=36.0, fg_pct=0.472, fg3m=6.0, fg3a=15.0, fg3_pct=0.400,
                 ftm=14.0, fta=18.0, ft_pct=0.778, oreb=7.0, dreb=30.0, reb=37.0, ast=22.0, stl=6.0, blk=0.0, tov=15.0,
                 pf=22.0, pts=110, a_team_id=1610612738, season_year=2008, season_type='Regular Season',
                 season='2008-09')
        ]

        self.money_line_betting_odds: List[MoneyLineBettingOdds] = [
            MoneyLineBettingOdds(game_id=20800741, book_name='Book1', book_id=1, team_id=1610612737,
                                 a_team_id=1610612738, price1=150.0, price2=-150.0),
            MoneyLineBettingOdds(game_id=20800701, book_name='Book2', book_id=2, team_id=1610612738,
                                 a_team_id=1610612737, price1=200.0, price2=-200.0)
        ]

    def test_transform_to_nba_money_line_betting_opportunities(self):
        nba_games = transform_to_nba_games(self.games, self.teams)
        opportunities = transform_to_nba_money_line_betting_opportunities(self.money_line_betting_odds, nba_games)

        self.assertIsInstance(opportunities, List)
        self.assertTrue(all(isinstance(opportunity, NbaMoneyLineBettingOpportunity) for opportunity in opportunities))
        self.assertEqual(len(opportunities), 4)  # 2 games x 2 opportunities per game

        # First game, home bet
        self.assertEqual(opportunities[0].game.game_id, 20800741)
        self.assertEqual(opportunities[0].book_name, 'Book1')
        self.assertTrue(opportunities[0].bet_on_home_team)
        self.assertEqual(opportunities[0].price, -150.0)

        # First game, away bet
        self.assertEqual(opportunities[1].game.game_id, 20800741)
        self.assertEqual(opportunities[1].book_name, 'Book1')
        self.assertFalse(opportunities[1].bet_on_home_team)
        self.assertEqual(opportunities[1].price, 150.0)

        # Second game, home bet
        self.assertEqual(opportunities[2].game.game_id, 20800701)
        self.assertEqual(opportunities[2].book_name, 'Book2')
        self.assertTrue(opportunities[2].bet_on_home_team)
        self.assertEqual(opportunities[2].price, -200.0)

        # Second game, away bet
        self.assertEqual(opportunities[3].game.game_id, 20800701)
        self.assertEqual(opportunities[3].book_name, 'Book2')
        self.assertFalse(opportunities[3].bet_on_home_team)
        self.assertEqual(opportunities[3].price, 200.0)
