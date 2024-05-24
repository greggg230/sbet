from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, PeriodStart, Foul, JumpBall, Rebound, Timeout, FreeThrow, Substitution
)
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.turnover import OutOfBoundsTurnover, Steal, OffensiveFoulTurnover

expected_plays = [
    PeriodStart(
        play_length=0,
        play_id=1,
        period_number=1,
        home_team_lineup=frozenset({Player("Kevon Looney"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry"), Player("Klay Thompson")}),
        away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Jaren Jackson Jr."), Player("Desmond Bane"), Player("Dillon Brooks")})
    ),
    JumpBall(play_length=0, play_id=2, home_player=Player("Kevon Looney"), away_player=Player("Steven Adams"), did_home_team_win=False),
    FieldGoalAttempt(play_length=20000, play_id=3, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None),
    Rebound(play_length=3000, play_id=4, rebounding_player=None, is_offensive=True),
    Foul(play_length=0, play_id=5, foul_type="loose ball", committed_by=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=6, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Desmond Bane"), assisting_player=None),
    Rebound(play_length=2000, play_id=7, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=22000, play_id=8, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Andrew Wiggins"), assisting_player=None),
    Rebound(play_length=2000, play_id=9, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    FieldGoalAttempt(play_length=13000, play_id=10, shot_made=True, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Desmond Bane"), assisting_player=None),
    FieldGoalAttempt(play_length=15000, play_id=11, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=None),
    Rebound(play_length=3000, play_id=12, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=13, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Desmond Bane"), assisting_player=None),
    FieldGoalAttempt(play_length=15000, play_id=14, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=Player("Kevon Looney")),
    FieldGoalAttempt(play_length=17000, play_id=15, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    Rebound(play_length=3000, play_id=16, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=3000, play_id=17, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Draymond Green"), assisting_player=Player("Stephen Curry")),
    FieldGoalAttempt(play_length=9000, play_id=18, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    Rebound(play_length=3000, play_id=19, rebounding_player=Player("Draymond Green"), is_offensive=False),
    Foul(play_length=5000, play_id=20, foul_type="offensive", committed_by=Player("Kevon Looney"), is_offensive=True),
    OffensiveFoulTurnover(play_length=0, play_id=21),
    FieldGoalAttempt(play_length=19000, play_id=22, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None),
    Rebound(play_length=3000, play_id=23, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    FieldGoalAttempt(play_length=2000, play_id=24, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=None),
    Rebound(play_length=2000, play_id=25, rebounding_player=Player("Klay Thompson"), is_offensive=True),
    FieldGoalAttempt(play_length=5000, play_id=26, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=None),
    Rebound(play_length=2000, play_id=27, rebounding_player=Player("Steven Adams"), is_offensive=False),
    Steal(play_length=9000, play_id=28, stolen_from=Player("Steven Adams"), stolen_by=Player("Draymond Green")),
    FieldGoalAttempt(play_length=4000, play_id=29, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=Player("Draymond Green")),
    Timeout(play_length=1000, play_id=30, is_home=False),
    FieldGoalAttempt(play_length=15000, play_id=31, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Desmond Bane"), assisting_player=None),
    Rebound(play_length=2000, play_id=32, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=33, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Draymond Green"), assisting_player=None),
    FieldGoalAttempt(play_length=17000, play_id=34, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Tyus Jones")),
    FieldGoalAttempt(play_length=21000, play_id=35, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=None),
    FieldGoalAttempt(play_length=12000, play_id=36, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Tyus Jones"), assisting_player=None),
    Rebound(play_length=2000, play_id=37, rebounding_player=Player("Andrew Wiggins"), is_offensive=False),
    FieldGoalAttempt(play_length=10000, play_id=38, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Andrew Wiggins"), assisting_player=None),
    Rebound(play_length=2000, play_id=39, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=3000, play_id=40, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Kevon Looney"), assisting_player=None),
    Rebound(play_length=2000, play_id=41, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=0, play_id=42, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Kevon Looney"), assisting_player=None),
    Rebound(play_length=0, play_id=43, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=44, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None),
    Rebound(play_length=2000, play_id=45, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    Steal(play_length=16000, play_id=46, stolen_from=Player("Klay Thompson"), stolen_by=Player("Dillon Brooks")),
    Foul(play_length=3000, play_id=47, foul_type="shooting", committed_by=Player("Stephen Curry"), is_offensive=False),
    FreeThrow(play_length=0, play_id=48, shot_made=False),
    Rebound(play_length=0, play_id=49, rebounding_player=None, is_offensive=True),
    FreeThrow(play_length=0, play_id=50, shot_made=True),
    FieldGoalAttempt(play_length=10000, play_id=51, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Draymond Green"), assisting_player=None),
    Rebound(play_length=2000, play_id=52, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=53, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Steven Adams"), assisting_player=None),
    Rebound(play_length=3000, play_id=54, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=55, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=None),
    FieldGoalAttempt(play_length=12000, play_id=56, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Tyus Jones"), assisting_player=None),
    Rebound(play_length=2000, play_id=57, rebounding_player=Player("Stephen Curry"), is_offensive=False),
    Substitution(play_length=11000, play_id=58, home_team_lineup=frozenset({Player("Jordan Poole"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry"), Player("Klay Thompson")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Jaren Jackson Jr."), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FieldGoalAttempt(play_length=5000, play_id=59, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Draymond Green"), assisting_player=None),
    Rebound(play_length=3000, play_id=60, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=9000, play_id=61, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    Rebound(play_length=2000, play_id=62, rebounding_player=Player("Dillon Brooks"), is_offensive=True),
    Foul(play_length=5000, play_id=63, committed_by=Player("Stephen Curry"), is_offensive=False, foul_type="personal"),
    FieldGoalAttempt(play_length=7000, play_id=64, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Steven Adams"), assisting_player=Player("Tyus Jones")),
    OutOfBoundsTurnover(play_length=4000, play_id=65, player=Player("Draymond Green")),
    FieldGoalAttempt(play_length=9000, play_id=66, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Tyus Jones")),
    Steal(play_length=18000, play_id=67, stolen_from=Player("Stephen Curry"), stolen_by=Player("Dillon Brooks")),
    FieldGoalAttempt(play_length=3000, play_id=68, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    Timeout(play_length=2000, play_id=69, is_home=True),
    Substitution(
        play_length=0,
        play_id=70,
        home_team_lineup=frozenset({
            Player("Jordan Poole"),
            Player("Draymond Green"),
            Player("Andrew Wiggins"),
            Player("Stephen Curry"),
            Player("Klay Thompson")
        }),
        away_team_lineup=frozenset({
            Player("Steven Adams"),
            Player("Tyus Jones"),
            Player("Kyle Anderson"),
            Player("Desmond Bane"),
            Player("Dillon Brooks")
        })
    ),
    Substitution(
        play_length=0,
        play_id=71,
        home_team_lineup=frozenset({
            Player("Jordan Poole"),
            Player("Draymond Green"),
            Player("Andrew Wiggins"),
            Player("Stephen Curry"),
            Player("Klay Thompson")
        }),
        away_team_lineup=frozenset({
            Player("Steven Adams"),
            Player("Tyus Jones"),
            Player("Kyle Anderson"),
            Player("Ziaire Williams"),
            Player("Dillon Brooks")
        })
    ),
    FieldGoalAttempt(play_length=19000, play_id=72, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=None),
    Rebound(play_length=3000, play_id=73, rebounding_player=Player("Kyle Anderson"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=74, shot_made=True, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    FieldGoalAttempt(play_length=14000, play_id=75, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Jordan Poole"), assisting_player=Player("Draymond Green")),
    FieldGoalAttempt(play_length=12000, play_id=76, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Steven Adams"), assisting_player=None),
    Rebound(play_length=2000, play_id=77, rebounding_player=Player("Andrew Wiggins"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=78, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Andrew Wiggins"), assisting_player=None),
    Rebound(play_length=2000, play_id=79, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=12000, play_id=80, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    Rebound(play_length=3000, play_id=81, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=2000, play_id=82, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Andrew Wiggins"), assisting_player=Player("Draymond Green")),
    FieldGoalAttempt(play_length=7000, play_id=83, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None),
    Rebound(play_length=3000, play_id=84, rebounding_player=Player("Stephen Curry"), is_offensive=False),
    Foul(play_length=6000, play_id=85, foul_type="shooting", committed_by=Player("Steven Adams"), is_offensive=False),
    FreeThrow(play_length=0, play_id=86, shot_made=True),
    Substitution(play_length=0, play_id=87, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Draymond Green"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=88, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=89, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Brandon Clarke"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=90, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Brandon Clarke"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Desmond Bane")})),
    FreeThrow(play_length=0, play_id=91, shot_made=False),
    Rebound(play_length=3000, play_id=92, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=0, play_id=93, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Kevon Looney"), assisting_player=None),
    Rebound(play_length=1000, play_id=94, rebounding_player=Player("Ziaire Williams"), is_offensive=False),
    FieldGoalAttempt(play_length=9000, play_id=95, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Brandon Clarke"), assisting_player=None),
    Rebound(play_length=3000, play_id=96, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    Steal(play_length=3000, play_id=97, stolen_by=Player("Ziaire Williams"), stolen_from=Player("Damion Lee")),
    FieldGoalAttempt(play_length=3000, play_id=98, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Ziaire Williams"), assisting_player=None),
    FieldGoalAttempt(play_length=19000, play_id=99, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Jordan Poole"), assisting_player=None),
    Rebound(play_length=3000, play_id=100, rebounding_player=Player("Kevon Looney"), is_offensive=True)
]
