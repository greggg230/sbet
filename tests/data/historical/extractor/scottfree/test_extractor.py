import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch

from frozendict import frozendict

from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.extractor.scottfree.extractor import ScottfreeHistoricalBetDataExtractor
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity


class TestScottfreeHistoricalBetDataExtractor(unittest.TestCase):

    @patch('builtins.open')
    @patch('sbet.data.historical.extractor.scottfree.parse.read_scottfree_game_csv')
    def test_extract(self, mock_read_csv, mock_open):
        mock_csv_content = """season,date,away_team,away_score,away_point_spread,away_point_spread_line,away_money_line,home_team,home_score,home_point_spread,home_point_spread_line,home_money_line,over_under,over_line,under_line
2007-08,2007-10-30,portland_trail_blazers,97,13.0,-110,900,san_antonio_spurs,106,-13.0,-110,-1400,189.5,-110,-110
2007-08,2007-10-30,utah_jazz,117,1.0,-110,100,golden_state_warriors,96,-1.0,-110,-120,212.0,-110,-110
"""
        mock_open.return_value = StringIO(mock_csv_content)
        mock_read_csv.return_value = [
            {
                "season": "2007-08",
                "date": "2007-10-30",
                "away_team": "portland_trail_blazers",
                "away_score": "97",
                "away_point_spread": "13.0",
                "away_point_spread_line": "-110",
                "away_money_line": "900",
                "home_team": "san_antonio_spurs",
                "home_score": "106",
                "home_point_spread": "-13.0",
                "home_point_spread_line": "-110",
                "home_money_line": "-1400",
                "over_under": "189.5",
                "over_line": "-110",
                "under_line": "-110",
            },
            {
                "season": "2007-08",
                "date": "2007-10-30",
                "away_team": "utah_jazz",
                "away_score": "117",
                "away_point_spread": "1.0",
                "away_point_spread_line": "-110",
                "away_money_line": "100",
                "home_team": "golden_state_warriors",
                "home_score": "96",
                "home_point_spread": "-1.0",
                "home_point_spread_line": "-110",
                "home_money_line": "-120",
                "over_under": "212.0",
                "over_line": "-110",
                "under_line": "-110",
            }
        ]

        extractor = ScottfreeHistoricalBetDataExtractor('dummy/path/to/csv')
        bet_data = extractor.extract()

        expected_games = [
            Game(
                game_id=f"20071030san_antonio_spursportland_trail_blazers",
                game_date=datetime.strptime('2007-10-30', '%Y-%m-%d').date(),
                season='2007-08',
                game_type='Regular Season',
                home_team="san_antonio_spurs",
                away_team="portland_trail_blazers",
                home_score=106,
                away_score=97
            ),
            Game(
                game_id=f"20071030golden_state_warriorsutah_jazz",
                game_date=datetime.strptime('2007-10-30', '%Y-%m-%d').date(),
                season='2007-08',
                game_type='Regular Season',
                home_team="golden_state_warriors",
                away_team="utah_jazz",
                home_score=96,
                away_score=117
            )
        ]

        expected_money_line_data = frozendict({
            expected_games[0]: GameBettingOpportunities(
                home=MoneyLineBettingOpportunity(
                    game=expected_games[0],
                    book_name="Scottfree",
                    bet_on_home_team=True,
                    price=-1400
                ),
                away=MoneyLineBettingOpportunity(
                    game=expected_games[0],
                    book_name="Scottfree",
                    bet_on_home_team=False,
                    price=900
                )
            ),
            expected_games[1]: GameBettingOpportunities(
                home=MoneyLineBettingOpportunity(
                    game=expected_games[1],
                    book_name="Scottfree",
                    bet_on_home_team=True,
                    price=-120
                ),
                away=MoneyLineBettingOpportunity(
                    game=expected_games[1],
                    book_name="Scottfree",
                    bet_on_home_team=False,
                    price=100
                )
            )
        })

        self.assertEqual(bet_data.games, expected_games)
        self.assertEqual(bet_data.money_line_data, expected_money_line_data)


if __name__ == '__main__':
    unittest.main()
