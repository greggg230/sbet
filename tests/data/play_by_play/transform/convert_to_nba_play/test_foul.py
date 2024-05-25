import unittest
from dataclasses import replace

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.fouls import PersonalFoul, OffensiveFoul, ShootingFoul, TechnicalFoul, FlagrantFoul
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType


class TestConvertToNbaPlayFoul(unittest.TestCase):

    def setUp(self):
        self.raw_play_foul = Play(
            game_id=1,
            data_set="test",
            date="2022-01-01",
            a1="A1",
            a2="A2",
            a3="A3",
            a4="A4",
            a5="A5",
            h1="H1",
            h2="H2",
            h3="H3",
            h4="H4",
            h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="0:11:00",
            elapsed="0:01:00",
            play_length="0:00:20",
            play_id=1,
            team="ATL",
            event_type="foul",
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
            type="personal",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Personal foul on H1"
        )

        self.game = Game(
            game_id=1,
            date="2022-01-01",
            home_team=NbaTeam.ATL,
            away_team=NbaTeam.BKN,
            plays=[]
        )

    def test_convert_to_nba_play_personal_foul(self):
        self.game = replace(self.game, plays=[self.raw_play_foul])
        nba_play = convert_to_nba_play(self.raw_play_foul, self.game)
        expected_play = PersonalFoul(play_length=20000, play_id=1, fouling_player=Player("H1"))
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_offensive_foul(self):
        offensive_foul_play = replace(self.raw_play_foul, type="offensive", play_id=2)
        self.game = replace(self.game, plays=[offensive_foul_play])
        nba_play = convert_to_nba_play(offensive_foul_play, self.game)
        expected_play = OffensiveFoul(play_length=20000, play_id=2, fouling_player=Player("H1"))
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_shooting_foul(self):
        shooting_foul_play = replace(self.raw_play_foul, type="shooting", play_id=3)
        self.game = replace(self.game, plays=[shooting_foul_play])
        nba_play = convert_to_nba_play(shooting_foul_play, self.game)
        expected_play = ShootingFoul(
            play_length=20000,
            play_id=3,
            fouling_player=Player("H1"),
            field_goal_type=FieldGoalType.TWO_POINT_SHOT,
            field_goal_made=False
        )
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_technical_foul(self):
        technical_foul_play = replace(self.raw_play_foul, type="technical", play_id=4)
        self.game = replace(self.game, plays=[technical_foul_play])
        nba_play = convert_to_nba_play(technical_foul_play, self.game)
        expected_play = TechnicalFoul(play_length=20000, play_id=4, fouling_player=Player("H1"), is_home_team=True)
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_flagrant_foul(self):
        flagrant_foul_play = replace(self.raw_play_foul, type="flagrant", play_id=5)
        self.game = replace(self.game, plays=[flagrant_foul_play])
        nba_play = convert_to_nba_play(flagrant_foul_play, self.game)
        expected_play = FlagrantFoul(play_length=20000, play_id=5, fouling_player=Player("H1"))
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()
