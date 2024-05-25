import unittest
from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.fouls import ShootingFoul
from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.transform import convert_to_nba_play


class TestConvertToNbaPlayShootingFoul(unittest.TestCase):

    def setUp(self):
        self.game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[
                Play(
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
                    event_type="shot",
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
                    points=2,
                    possession=None,
                    reason=None,
                    result="missed",
                    steal=None,
                    type="jump shot",
                    shot_distance=None,
                    original_x=None,
                    original_y=None,
                    converted_x=None,
                    converted_y=None,
                    description="Missed jump shot by H1"
                ),
                Play(
                    game_id=1,
                    data_set="data_set",
                    date="2023-01-01",
                    a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
                    h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
                    period=1,
                    away_score=0,
                    home_score=0,
                    remaining_time="10:57",
                    elapsed="0:00:03",
                    play_length="0:00:02",
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
            ]
        )

    def test_convert_to_nba_play_shooting_foul_with_previous_shot(self):
        nba_play = convert_to_nba_play(self.game.plays[1], self.game)
        expected_play = ShootingFoul(
            play_length=2000,
            play_id=2,
            fouling_player=Player("A1"),
            field_goal_type=FieldGoalType.TWO_POINT_SHOT,
            field_goal_made=False
        )
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_shooting_foul_with_no_previous_shot(self):
        game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[
                Play(
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
                    type="shooting",
                    shot_distance=None,
                    original_x=None,
                    original_y=None,
                    converted_x=None,
                    converted_y=None,
                    description="Shooting foul on H1"
                ),
                Play(
                    game_id=1,
                    data_set="data_set",
                    date="2023-01-01",
                    a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
                    h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
                    period=1,
                    away_score=0,
                    home_score=0,
                    remaining_time="10:57",
                    elapsed="0:00:03",
                    play_length="0:00:02",
                    play_id=2,
                    team="home",
                    event_type="free throw",
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
                    points=1,
                    possession=None,
                    reason=None,
                    result="made",
                    steal=None,
                    type="free throw 1/2",
                    shot_distance=None,
                    original_x=None,
                    original_y=None,
                    converted_x=None,
                    converted_y=None,
                    description="Free throw 1 of 2 by H1"
                )
            ]
        )

        nba_play = convert_to_nba_play(game.plays[0], game)
        expected_play = ShootingFoul(
            play_length=3000,
            play_id=1,
            fouling_player=Player("H1"),
            field_goal_type=FieldGoalType.TWO_POINT_SHOT,
            field_goal_made=False
        )
        self.assertEqual(nba_play, expected_play)

    def test_convert_to_nba_play_shooting_foul_with_no_previous_shot_and_three_point_attempt(self):
        game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[
                Play(
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
                    type="shooting",
                    shot_distance=None,
                    original_x=None,
                    original_y=None,
                    converted_x=None,
                    converted_y=None,
                    description="Shooting foul on H1"
                ),
                Play(
                    game_id=1,
                    data_set="data_set",
                    date="2023-01-01",
                    a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
                    h1="H1", h2="H2", h3="H3", h4="H4", h5="H5",
                    period=1,
                    away_score=0,
                    home_score=0,
                    remaining_time="10:57",
                    elapsed="0:00:03",
                    play_length="0:00:02",
                    play_id=2,
                    team="home",
                    event_type="free throw",
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
                    points=1,
                    possession=None,
                    reason=None,
                    result="made",
                    steal=None,
                    type="free throw 1/3",
                    shot_distance=None,
                    original_x=None,
                    original_y=None,
                    converted_x=None,
                    converted_y=None,
                    description="Free throw 1 of 3 by H1"
                )
            ]
        )

        nba_play = convert_to_nba_play(game.plays[0], game)
        expected_play = ShootingFoul(
            play_length=3000,
            play_id=1,
            fouling_player=Player("H1"),
            field_goal_type=FieldGoalType.THREE_POINT_SHOT,
            field_goal_made=False
        )
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()

