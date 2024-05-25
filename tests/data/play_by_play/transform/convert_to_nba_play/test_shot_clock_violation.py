import unittest
from dataclasses import replace

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.turnover import ShotClockViolation
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayShotClockViolation(unittest.TestCase):

    def setUp(self):
        self.raw_play_shot_clock_violation = Play(
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
            play_length="0:00:03",
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
            player=None,
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type="shot clock",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Shot clock violation"
        )

        self.game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[]
        )

    def test_convert_to_nba_play_shot_clock_violation(self):
        self.game = replace(self.game, plays=[self.raw_play_shot_clock_violation])
        nba_play = convert_to_nba_play(self.raw_play_shot_clock_violation, self.game)
        expected_play = ShotClockViolation(
            play_length=3000,
            play_id=1
        )
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()
