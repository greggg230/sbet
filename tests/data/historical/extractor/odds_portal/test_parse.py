import unittest
from typing import Dict, Any, FrozenSet

from sbet.data.historical.extractor.odds_portal.models.odds_portal_page import OddsPortalPage
from sbet.data.historical.extractor.odds_portal.models.odds_portal_row import OddsPortalRow
from sbet.data.historical.extractor.odds_portal.parse import parse_odds_portal_json


class TestParseOddsPortalJson(unittest.TestCase):
    def setUp(self):
        self.json_data: Dict[str, Any] = {
            "s": 1,
            "d": {
                "total": 234,
                "onePage": 50,
                "page": 1,
                "rows": [
                    {
                        "id": 7247345,
                        "home-name": "Atlanta Utd",
                        "away-name": "Charlotte",
                        "date-start-timestamp": 1717361100,
                        "homeResult": "2",
                        "awayResult": "3",
                        "odds": [
                            {"avgOdds": 1.81},
                            {"avgOdds": 3.68},
                            {"avgOdds": 4.07}
                        ]
                    },
                    {
                        "id": 7247343,
                        "home-name": "Los Angeles FC",
                        "away-name": "FC Dallas",
                        "date-start-timestamp": 1717295400,
                        "homeResult": "1",
                        "awayResult": "0",
                        "odds": [
                            {"avgOdds": 1.33},
                            {"avgOdds": 5.22},
                            {"avgOdds": 8.17}
                        ]
                    }
                ]
            }
        }

    def test_parse_odds_portal_json(self):
        expected_rows: FrozenSet[OddsPortalRow] = frozenset([
            OddsPortalRow(
                home_team="Atlanta Utd",
                away_team="Charlotte",
                date_start_timestamp=1717361100,
                home_score=2,
                away_score=3,
                home_moneyline_price=1.81,
                draw_moneyline_price=3.68,
                away_moneyline_price=4.07
            ),
            OddsPortalRow(
                home_team="Los Angeles FC",
                away_team="FC Dallas",
                date_start_timestamp=1717295400,
                home_score=1,
                away_score=0,
                home_moneyline_price=1.33,
                draw_moneyline_price=5.22,
                away_moneyline_price=8.17
            )
        ])

        expected_page = OddsPortalPage(
            page=1,
            pageCount=50,
            rows=expected_rows
        )

        parsed_page = parse_odds_portal_json(self.json_data)
        self.assertEqual(parsed_page, expected_page)


if __name__ == '__main__':
    unittest.main()
