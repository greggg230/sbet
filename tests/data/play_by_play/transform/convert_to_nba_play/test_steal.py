import unittest


from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.turnover import Steal
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlaySteal(unittest.TestCase):

    def setUp(self):
        self.raw_play_steal = Play(
            game_id=1, data_set="test", date="2023-01-01", a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
            h1="H1", h2="H2", h3="H3", h4="H4", h5="H5", period=1, away_score=10, home_score=12,
            remaining_time="10:00", elapsed="2:00", play_length="0:02:00", play_id=28, team="home",
            event_type="turnover", assist=None, away=None, home=None, block=None, entered=None,
            left=None, num=None, opponent="A1", outof=None, player="A1", points=None, possession=None,
            reason=None, result="steal", steal="H1", type=None, shot_distance=None,
            original_x=None, original_y=None, converted_x=None, converted_y=None, description="H1 steals ball from A1"
        )

    def test_convert_to_nba_play_steal(self):
        nba_play = convert_to_nba_play(self.raw_play_steal)
        self.assertIsInstance(nba_play, Steal)
        self.assertEqual(nba_play.play_id, 28)
        self.assertEqual(nba_play.stolen_by, Player("H1"))
        self.assertEqual(nba_play.stolen_from, Player("A1"))
