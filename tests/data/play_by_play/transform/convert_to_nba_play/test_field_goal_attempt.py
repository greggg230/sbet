import unittest
from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.plays import FieldGoalAttempt
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType


class TestConvertToNbaPlayFieldGoalAttempt(unittest.TestCase):

    def setUp(self):
        self.raw_play_field_goal_attempt = Play(
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
            event_type="shot",
            assist="H2",
            away=None,
            home=None,
            block=None,
            entered=None,
            left=None,
            num=None,
            opponent=None,
            outof=None,
            player="H1",
            points=2,
            possession=None,
            reason=None,
            result="made",
            steal=None,
            type="jump shot",
            shot_distance=15,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Made shot"
        )

        self.raw_play_foul_after_shot = Play(
            game_id=1,
            data_set="data_set",
            date="2023-01-01",
            a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
            h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="10:40",
            elapsed="0:00:15",
            play_length="0:00:00",
            play_id=2,
            team="away",
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
            player="A1",
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type="shooting",
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Shooting foul on A1"
        )

        self.game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.ATL,
            away_team=NbaTeam.BKN,
            plays=[self.raw_play_field_goal_attempt]
        )

        self.game_with_foul = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.ATL,
            away_team=NbaTeam.BKN,
            plays=[self.raw_play_field_goal_attempt, self.raw_play_foul_after_shot]
        )

    def test_convert_to_nba_play_field_goal_attempt(self):
        nba_play = convert_to_nba_play(self.raw_play_field_goal_attempt, self.game)
        expected_play = FieldGoalAttempt(
            play_length=20000,
            play_id=1,
            shot_made=True,
            shooting_player=Player("H1"),
            assisting_player=Player("H2"),
            type=FieldGoalType.TWO_POINT_SHOT,
            was_fouled=False
        )
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_field_goal_attempt_with_foul(self):
        nba_play = convert_to_nba_play(self.raw_play_field_goal_attempt, self.game_with_foul)
        expected_play = FieldGoalAttempt(
            play_length=20000,
            play_id=1,
            shot_made=True,
            shooting_player=Player("H1"),
            assisting_player=Player("H2"),
            type=FieldGoalType.TWO_POINT_SHOT,
            was_fouled=True
        )
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()
