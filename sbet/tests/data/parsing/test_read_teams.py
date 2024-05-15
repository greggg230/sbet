import unittest
import tempfile
from sbet.data.models.csv_models import Team
from sbet.data.parsing import read_teams
from typing import List


class TestReadTeams(unittest.TestCase):

    def setUp(self):
        self.csv_data = """league_id,team_id,min_year,max_year,abbreviation
        0,1610612737,1949,2018,ATL
        0,1610612738,1946,2018,BOS"""

    def test_read_teams(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(self.csv_data)
            temp_file_path = temp_file.name

        teams = read_teams(temp_file_path)

        self.assertIsInstance(teams, List)
        self.assertTrue(all(isinstance(team, Team) for team in teams))
        self.assertEqual(len(teams), 2)

        self.assertEqual(teams[0].team_id, 1610612737)
        self.assertEqual(teams[0].abbreviation, 'ATL')

        self.assertEqual(teams[1].team_id, 1610612738)
        self.assertEqual(teams[1].abbreviation, 'BOS')
