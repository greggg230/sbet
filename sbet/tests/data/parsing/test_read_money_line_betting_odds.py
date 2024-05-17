import unittest
import tempfile
from sbet.data.historical.models import MoneyLineBettingOdds
from sbet.data.historical.parsing import read_money_line_betting_odds
from typing import List


class TestReadMoneyLineBettingOdds(unittest.TestCase):

    def setUp(self):
        self.csv_data = """game_id,book_name,book_id,team_id,a_team_id,price1,price2
        20800741,Book1,1,1610612737,1610612738,150.0,-150.0
        20800701,Book2,2,1610612738,1610612737,200.0,-200.0"""

    def test_read_money_line_betting_odds(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.write(self.csv_data)
            temp_file_path = temp_file.name

        odds = read_money_line_betting_odds(temp_file_path)

        self.assertIsInstance(odds, List)
        self.assertTrue(all(isinstance(odd, MoneyLineBettingOdds) for odd in odds))
        self.assertEqual(len(odds), 2)

        self.assertEqual(odds[0].game_id, 20800741)
        self.assertEqual(odds[0].book_name, 'Book1')
        self.assertEqual(odds[0].price1, 150.0)
        self.assertEqual(odds[0].price2, -150.0)

        self.assertEqual(odds[1].game_id, 20800701)
        self.assertEqual(odds[1].book_name, 'Book2')
        self.assertEqual(odds[1].price1, 200.0)
        self.assertEqual(odds[1].price2, -200.0)
