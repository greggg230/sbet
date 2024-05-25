import unittest
from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.turnover import TravelingTurnover
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayTravelingTurnover(unittest.TestCase):

    def setUp(self):
        self.raw_play_traveling_turnover = Play(
            game_id=1,
            data_set="data_set",
            date="2023-01-01",
            a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
            h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="11:00",
            elapsed="0:00:00",
            play_length="0:00:20",
            play_id=1,
            team="home",
            event_type="turnover",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player="H1",
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type="traveling",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Traveling turnover"
        )
        self.game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.ATL,
            away_team=NbaTeam.BKN,
            plays=[self.raw_play_traveling_turnover]
        )

    def test_convert_to_nba_play_traveling_turnover(self):
        nba_play = convert_to_nba_play(self.raw_play_traveling_turnover, self.game)
        expected_play = TravelingTurnover(
            play_length=20000,
            play_id=1,
            player=Player("H1")
        )
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()
