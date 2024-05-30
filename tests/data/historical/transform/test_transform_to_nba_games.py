import unittest
from datetime import date
from typing import List

from sbet.data.historical.models.csv import Team, Game as CsvGame
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.data.historical.transform import transform_to_nba_games


class TestTransformToNbaGames(unittest.TestCase):

    def setUp(self):
        self.teams: List[Team] = [
            Team(league_id=0, team_id=1610612737, min_year=1949.0, max_year=2018.0, abbreviation='ATL'),
            Team(league_id=0, team_id=1610612738, min_year=1946.0, max_year=2018.0, abbreviation='BOS')
        ]

        self.games: List[CsvGame] = [
            CsvGame(game_id=20800741, game_date='2009-02-06', matchup='ATL vs. BOS', team_id=1610612737, is_home=True,
                 wl='W',
                 w=29, l=22, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0, fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=111, a_team_id=1610612738, season_year=2008, season_type='Regular Season',
                 season='2008-09'),
            CsvGame(game_id=20800741, game_date='2009-02-06', matchup='ATL vs. BOS', team_id=1610612738, is_home=False,
                 wl='L',
                 w=29, l=22, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0, fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=105, a_team_id=1610612737, season_year=2008, season_type='Regular Season',
                 season='2008-09'),
            CsvGame(game_id=20800742, game_date='', matchup='ATL vs. BOS', team_id=1610612737, is_home=True, wl='W',
                 w=29, l=22, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0, fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=111, a_team_id=1610612738, season_year=2008, season_type='Regular Season',
                 season='2008-09'),
            CsvGame(game_id=20800742, game_date='', matchup='ATL vs. BOS', team_id=1610612738, is_home=False, wl='L',
                 w=29, l=22, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0, fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=105, a_team_id=1610612737, season_year=2008, season_type='Regular Season',
                 season='2008-09')
        ]

    def test_transform_to_nba_games(self):
        nba_games = transform_to_nba_games(self.games, self.teams)

        self.assertIsInstance(nba_games, List)
        self.assertTrue(all(isinstance(nba_game, Game) for nba_game in nba_games))
        self.assertEqual(len(nba_games), 1)  # Only one valid game should be transformed

        self.assertEqual(nba_games[0].game_id, 20800741)
        self.assertEqual(nba_games[0].game_date, date(2009, 2, 6))
        self.assertEqual(nba_games[0].season, '2008-09')
        self.assertEqual(nba_games[0].game_type, 'Regular Season')
        self.assertEqual(nba_games[0].home_team, "ATL")
        self.assertEqual(nba_games[0].away_team, "BOS")
        self.assertEqual(nba_games[0].home_score, 111)
        self.assertEqual(nba_games[0].away_score, 105)


if __name__ == '__main__':
    unittest.main()
