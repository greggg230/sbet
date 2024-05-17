import unittest
import tempfile
from sbet.data.historical.models import Game
from sbet.data.historical.parsing import read_games
from typing import List


class TestReadGames(unittest.TestCase):

    def setUp(self):
        self.csv_data = """game_id,game_date,matchup,team_id,is_home,wl,w,l,w_pct,min,fgm,fga,fg_pct,fg3m,fg3a,fg3_pct,ftm,fta,ft_pct,oreb,dreb,reb,ast,stl,blk,tov,pf,pts,a_team_id,season_year,season_type,season
        20800741,2009-02-06,ATL vs. BOS,1610612737,t,W,29,22,0.569,240,19,40,0.475,5,16,0.313,18,26,0.692,8,24,32,19,5,4,18,26,111,1610612738,2008,Regular Season,2008-09
        20800741,2009-02-06,ATL vs. BOS,1610612738,f,L,29,22,0.569,240,19,40,0.475,5,16,0.313,18,26,0.692,8,24,32,19,5,4,18,26,105,1610612737,2008,Regular Season,2008-09"""

    def test_read_games(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(self.csv_data)
            temp_file_path = temp_file.name

        games = read_games(temp_file_path)

        self.assertIsInstance(games, List)
        self.assertTrue(all(isinstance(game, Game) for game in games))
        self.assertEqual(len(games), 2)

        self.assertEqual(games[0].game_id, 20800741)
        self.assertEqual(games[0].team_id, 1610612737)
        self.assertEqual(games[0].pts, 111)

        self.assertEqual(games[1].game_id, 20800741)
        self.assertEqual(games[1].team_id, 1610612738)
        self.assertEqual(games[1].pts, 105)
