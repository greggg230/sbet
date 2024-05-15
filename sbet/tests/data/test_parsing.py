import unittest
from sbet.data.parsing import read_teams, read_games, read_betting_odds
from sbet.data.models import Team, Game, MoneyLineBettingOdds
from typing import List
import tempfile


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.teams_csv_content = """league_id,team_id,min_year,max_year,abbreviation
0,1610612737,1949.0,2018.0,ATL
0,1610612738,1946.0,2018.0,BOS
"""
        self.games_csv_content = """game_id,game_date,matchup,team_id,is_home,wl,w,l,w_pct,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,reb,ast,stl,blk,tov,pf,pts,a_team_id,season_year,season_type,season
20800741,2009-02-06,SAC vs. UTA,1610612762,f,W,29.0,22.0,0.569,240,19.0,40.0,0.475,5.0,16.0,0.313,18.0,26.0,0.692,8.0,24.0,32.0,19.0,5.0,4.0,18.0,26.0,111.0,1610612758,2008,Regular Season,2008-09
20800701,2009-01-31,POR vs. UTA,1610612762,f,L,26.0,22.0,0.542,240,17.0,36.0,0.472,6.0,15.0,0.400,14.0,18.0,0.778,7.0,30.0,37.0,22.0,6.0,0.0,15.0,22.0,108.0,1610612757,2008,Regular Season,2008-09
"""
        self.betting_odds_csv_content = """game_id,book_name,book_id,team_id,a_team_id,price1,price2
41100314,Pinnacle Sports,238,1610612759,1610612760,165.0,-183.0
41100314,5Dimes,19,1610612759,1610612760,165.0,-175.0
"""

        self.temp_teams_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_teams_file.write(self.teams_csv_content)
        self.temp_teams_file.close()

        self.temp_games_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_games_file.write(self.games_csv_content)
        self.temp_games_file.close()

        self.temp_betting_odds_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.temp_betting_odds_file.write(self.betting_odds_csv_content)
        self.temp_betting_odds_file.close()

    def test_read_teams(self):
        teams = read_teams(self.temp_teams_file.name)
        self.assertIsInstance(teams, List)
        self.assertTrue(all(isinstance(team, Team) for team in teams))
        self.assertEqual(len(teams), 2)

        self.assertEqual(teams[0].league_id, 0)
        self.assertEqual(teams[0].team_id, 1610612737)
        self.assertEqual(teams[0].min_year, 1949.0)
        self.assertEqual(teams[0].max_year, 2018.0)
        self.assertEqual(teams[0].abbreviation, 'ATL')

        self.assertEqual(teams[1].league_id, 0)
        self.assertEqual(teams[1].team_id, 1610612738)
        self.assertEqual(teams[1].min_year, 1946.0)
        self.assertEqual(teams[1].max_year, 2018.0)
        self.assertEqual(teams[1].abbreviation, 'BOS')

    def test_read_games(self):
        games = read_games(self.temp_games_file.name)
        self.assertIsInstance(games, List)
        self.assertTrue(all(isinstance(game, Game) for game in games))
        self.assertEqual(len(games), 2)

        self.assertEqual(games[0].game_id, 20800741)
        self.assertEqual(games[0].game_date, '2009-02-06')
        self.assertEqual(games[0].matchup, 'SAC vs. UTA')
        self.assertEqual(games[0].team_id, 1610612762)
        self.assertFalse(games[0].is_home)
        self.assertEqual(games[0].wl, 'W')
        self.assertEqual(games[0].w, 29.0)
        self.assertEqual(games[0].l, 22.0)
        self.assertEqual(games[0].w_pct, 0.569)
        self.assertEqual(games[0].min, 240)
        self.assertEqual(games[0].fgm, 19.0)
        self.assertEqual(games[0].fga, 40.0)
        self.assertEqual(games[0].fg_pct, 0.475)
        self.assertEqual(games[0].fg3m, 5.0)
        self.assertEqual(games[0].fg3a, 16.0)
        self.assertEqual(games[0].fg3_pct, 0.313)
        self.assertEqual(games[0].ftm, 18.0)
        self.assertEqual(games[0].fta, 26.0)
        self.assertEqual(games[0].ft_pct, 0.692)
        self.assertEqual(games[0].oreb, 8.0)
        self.assertEqual(games[0].dreb, 24.0)
        self.assertEqual(games[0].reb, 32.0)
        self.assertEqual(games[0].ast, 19.0)
        self.assertEqual(games[0].stl, 5.0)
        self.assertEqual(games[0].blk, 4.0)
        self.assertEqual(games[0].tov, 18.0)
        self.assertEqual(games[0].pf, 26.0)
        self.assertEqual(games[0].pts, 111.0)
        self.assertEqual(games[0].a_team_id, 1610612758)
        self.assertEqual(games[0].season_year, 2008)
        self.assertEqual(games[0].season_type, 'Regular Season')
        self.assertEqual(games[0].season, '2008-09')

        self.assertEqual(games[1].game_id, 20800701)
        self.assertEqual(games[1].game_date, '2009-01-31')
        self.assertEqual(games[1].matchup, 'POR vs. UTA')
        self.assertEqual(games[1].team_id, 1610612762)
        self.assertFalse(games[1].is_home)
        self.assertEqual(games[1].wl, 'L')
        self.assertEqual(games[1].w, 26.0)
        self.assertEqual(games[1].l, 22.0)
        self.assertEqual(games[1].w_pct, 0.542)
        self.assertEqual(games[1].min, 240)
        self.assertEqual(games[1].fgm, 17.0)
        self.assertEqual(games[1].fga, 36.0)
        self.assertEqual(games[1].fg_pct, 0.472)
        self.assertEqual(games[1].fg3m, 6.0)
        self.assertEqual(games[1].fg3a, 15.0)
        self.assertEqual(games[1].fg3_pct, 0.400)
        self.assertEqual(games[1].ftm, 14.0)
        self.assertEqual(games[1].fta, 18.0)
        self.assertEqual(games[1].ft_pct, 0.778)
        self.assertEqual(games[1].oreb, 7.0)
        self.assertEqual(games[1].dreb, 30.0)
        self.assertEqual(games[1].reb, 37.0)
        self.assertEqual(games[1].ast, 22.0)
        self.assertEqual(games[1].stl, 6.0)
        self.assertEqual(games[1].blk, 0.0)
        self.assertEqual(games[1].tov, 15.0)
        self.assertEqual(games[1].pf, 22.0)
        self.assertEqual(games[1].pts, 108.0)
        self.assertEqual(games[1].a_team_id, 1610612757)
        self.assertEqual(games[1].season_year, 2008)
        self.assertEqual(games[1].season_type, 'Regular Season')
        self.assertEqual(games[1].season, '2008-09')

    def test_read_betting_odds(self):
        betting_odds = read_betting_odds(self.temp_betting_odds_file.name)
        self.assertIsInstance(betting_odds, List)
        self.assertTrue(all(isinstance(odds, MoneyLineBettingOdds) for odds in betting_odds))
        self.assertEqual(len(betting_odds), 2)

        self.assertEqual(betting_odds[0].game_id, 41100314)
        self.assertEqual(betting_odds[0].book_name, 'Pinnacle Sports')
        self.assertEqual(betting_odds[0].book_id, 238)
        self.assertEqual(betting_odds[0].team_id, 1610612759)
        self.assertEqual(betting_odds[0].a_team_id, 1610612760)
        self.assertEqual(betting_odds[0].price1, 165.0)
        self.assertEqual(betting_odds[0].price2, -183.0)

        self.assertEqual(betting_odds[1].game_id, 41100314)
        self.assertEqual(betting_odds[1].book_name, '5Dimes')
        self.assertEqual(betting_odds[1].book_id, 19)
        self.assertEqual(betting_odds[1].team_id, 1610612759)
        self.assertEqual(betting_odds[1].a_team_id, 1610612760)
        self.assertEqual(betting_odds[1].price1, 165.0)
        self.assertEqual(betting_odds[1].price2, -175.0)
