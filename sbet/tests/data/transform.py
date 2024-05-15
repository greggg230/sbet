import unittest
from sbet.data.models import NbaGame, NbaTeam
from sbet.data.models.csv_models import Team, Game
from sbet.data.transform import transform_to_nba_games
from typing import List


class TestTransform(unittest.TestCase):

    def setUp(self):
        self.teams: List[Team] = [
            Team(league_id=0, team_id=1610612737, min_year=1949.0, max_year=2018.0, abbreviation='ATL'),
            Team(league_id=0, team_id=1610612738, min_year=1946.0, max_year=2018.0, abbreviation='BOS')
        ]

        self.games: List[Game] = [
            Game(game_id=20800741, game_date='2009-02-06', matchup='ATL vs. BOS', team_id=1610612737, is_home=True,
                 wl='W',
                 w=29.0, l=22.0, w_pct=0.569, min=240, fgm=19.0, fga=40.0, fg_pct=0.475, fg3m=5.0, fg3a=16.0,
                 fg3_pct=0.313,
                 ftm=18.0, fta=26.0, ft_pct=0.692, oreb=8.0, dreb=24.0, reb=32.0, ast=19.0, stl=5.0, blk=4.0, tov=18.0,
                 pf=26.0, pts=111.0, a_team_id=1610612738, season_year=2008, season_type='Regular Season',
                 season='2008-09'),
            Game(game_id=20800701, game_date='2009-01-31', matchup='BOS vs. ATL', team_id=1610612738, is_home=True,
                 wl='L',
                 w=26.0, l=22.0, w_pct=0.542, min=240, fgm=17.0, fga=36.0, fg_pct=0.472, fg3m=6.0, fg3a=15.0,
                 fg3_pct=0.400,
                 ftm=14.0, fta=18.0, ft_pct=0.778, oreb=7.0, dreb=30.0, reb=37.0, ast=22.0, stl=6.0, blk=0.0, tov=15.0,
                 pf=22.0, pts=108.0, a_team_id=1610612737, season_year=2008, season_type='Regular Season',
                 season='2008-09')
        ]

    def test_transform_to_nba_games(self):
        nba_games = transform_to_nba_games(self.games, self.teams)

        self.assertIsInstance(nba_games, List)
        self.assertTrue(all(isinstance(nba_game, NbaGame) for nba_game in nba_games))
        self.assertEqual(len(nba_games), 2)

        self.assertEqual(nba_games[0].game_id, 20800741)
        self.assertEqual(nba_games[0].game_date, '2009-02-06')
        self.assertEqual(nba_games[0].season, '2008-09')
        self.assertEqual(nba_games[0].game_type, 'Regular Season')
        self.assertEqual(nba_games[0].home_team, NbaTeam.ATL)
        self.assertEqual(nba_games[0].away_team, NbaTeam.BOS)

        self.assertEqual(nba_games[1].game_id, 20800701)
        self.assertEqual(nba_games[1].game_date, '2009-01-31')
        self.assertEqual(nba_games[1].season, '2008-09')
        self.assertEqual(nba_games[1].game_type, 'Regular Season')
        self.assertEqual(nba_games[1].home_team, NbaTeam.BOS)
        self.assertEqual(nba_games[1].away_team, NbaTeam.ATL)
