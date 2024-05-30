import unittest
from io import StringIO
from unittest.mock import patch


from sbet.data.historical.extractor.scottfree.models.scottfree_game_csv_row import ScottfreeGameCsvRow
from sbet.data.historical.extractor.scottfree.parse import read_scottfree_game_csv


class TestReadScottfreeNbaGameCsv(unittest.TestCase):

    @patch('builtins.open')
    def test_read_scottfree_nba_game_csv(self, mock_open):
        mock_csv_content = """season,date,away_team,away_score,away_point_spread,away_point_spread_line,away_money_line,home_team,home_score,home_point_spread,home_point_spread_line,home_money_line,over_under,over_line,under_line
2007-08,2007-10-30,portland_trail_blazers,97,13.0,-110,900,san_antonio_spurs,106,-13.0,-110,-1400,189.5,-110,-110
2007-08,2007-10-30,utah_jazz,117,1.0,-110,100,golden_state_warriors,96,-1.0,-110,-120,212.0,-110,-110
"""
        mock_open.return_value = StringIO(mock_csv_content)

        expected_rows = [
            ScottfreeGameCsvRow(
                season='2007-08',
                date='2007-10-30',
                away_team='portland_trail_blazers',
                away_score='97',
                away_point_spread='13.0',
                away_point_spread_line='-110',
                away_money_line='900',
                home_team='san_antonio_spurs',
                home_score='106',
                home_point_spread='-13.0',
                home_point_spread_line='-110',
                home_money_line='-1400',
                over_under='189.5',
                over_line='-110',
                under_line='-110'
            ),
            ScottfreeGameCsvRow(
                season='2007-08',
                date='2007-10-30',
                away_team='utah_jazz',
                away_score='117',
                away_point_spread='1.0',
                away_point_spread_line='-110',
                away_money_line='100',
                home_team='golden_state_warriors',
                home_score='96',
                home_point_spread='-1.0',
                home_point_spread_line='-110',
                home_money_line='-120',
                over_under='212.0',
                over_line='-110',
                under_line='-110'
            ),
        ]

        file_path = 'dummy_path.csv'
        rows = read_scottfree_game_csv(file_path)

        self.assertEqual(rows, expected_rows)


if __name__ == '__main__':
    unittest.main()
