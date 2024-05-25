from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType
from sbet.data.play_by_play.models.transform.fouls import OffensiveFoul, ShootingFoul, PersonalFoul, FlagrantFoul, \
    DoubleTechnicalFoul
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, PeriodStart, JumpBall, Rebound, Timeout, FreeThrow, Substitution, PeriodEnd, Unknown
)
from sbet.data.play_by_play.models.transform.turnover import OutOfBoundsTurnover, Steal, OffensiveFoulTurnover, \
    TravelingTurnover, ShotClockViolation

expected_plays = [
    PeriodStart(
        play_length=0,
        play_id=1,
        period_number=1,
        home_team_lineup=frozenset({Player("Kevon Looney"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry"), Player("Klay Thompson")}),
        away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Jaren Jackson Jr."), Player("Desmond Bane"), Player("Dillon Brooks")})
    ),
    JumpBall(play_length=0, play_id=2, home_player=Player("Kevon Looney"), away_player=Player("Steven Adams"), did_home_team_win=False),
    FieldGoalAttempt(play_length=20000, play_id=3, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=4, rebounding_player=None, is_offensive=True),
    PersonalFoul(play_length=0, play_id=5, fouling_player=Player("Draymond Green")),
    FieldGoalAttempt(play_length=6000, play_id=6, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Desmond Bane"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=7, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=22000, play_id=8, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Andrew Wiggins"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=9, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    FieldGoalAttempt(play_length=13000, play_id=10, shot_made=True, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Desmond Bane"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=15000, play_id=11, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=12, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=13, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Desmond Bane"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=15000, play_id=14, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=Player("Kevon Looney"), was_fouled=False),
    FieldGoalAttempt(play_length=17000, play_id=15, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=16, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=3000, play_id=17, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Draymond Green"), assisting_player=Player("Stephen Curry"), was_fouled=False),
    FieldGoalAttempt(play_length=9000, play_id=18, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=19, rebounding_player=Player("Draymond Green"), is_offensive=False),
    OffensiveFoul(play_length=5000, play_id=20, fouling_player=Player("Kevon Looney")),
    OffensiveFoulTurnover(play_length=0, play_id=21),
    FieldGoalAttempt(play_length=19000, play_id=22, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=23, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    FieldGoalAttempt(play_length=2000, play_id=24, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=25, rebounding_player=Player("Klay Thompson"), is_offensive=True),
    FieldGoalAttempt(play_length=5000, play_id=26, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=27, rebounding_player=Player("Steven Adams"), is_offensive=False),
    Steal(play_length=9000, play_id=28, stolen_from=Player("Steven Adams"), stolen_by=Player("Draymond Green")),
    FieldGoalAttempt(play_length=4000, play_id=29, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=Player("Draymond Green"), was_fouled=False),
    Timeout(play_length=1000, play_id=30, is_home=False),
    FieldGoalAttempt(play_length=15000, play_id=31, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Desmond Bane"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=32, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=33, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Draymond Green"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=17000, play_id=34, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Tyus Jones"), was_fouled=False),
    FieldGoalAttempt(play_length=21000, play_id=35, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=12000, play_id=36, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Tyus Jones"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=37, rebounding_player=Player("Andrew Wiggins"), is_offensive=False),
    FieldGoalAttempt(play_length=10000, play_id=38, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Andrew Wiggins"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=39, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=3000, play_id=40, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Kevon Looney"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=41, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=0, play_id=42, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Kevon Looney"), assisting_player=None, was_fouled=False),
    Rebound(play_length=0, play_id=43, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=44, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=45, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    Steal(play_length=16000, play_id=46, stolen_from=Player("Klay Thompson"), stolen_by=Player("Dillon Brooks")),
    ShootingFoul(play_length=3000, play_id=47, fouling_player=Player("Stephen Curry"), field_goal_made=False, field_goal_type=FieldGoalType.TWO_POINT_SHOT),
    FreeThrow(play_length=0, play_id=48, shot_made=False),
    Rebound(play_length=0, play_id=49, rebounding_player=None, is_offensive=True),
    FreeThrow(play_length=0, play_id=50, shot_made=True),
    FieldGoalAttempt(play_length=10000, play_id=51, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Draymond Green"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=52, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=53, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Steven Adams"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=54, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=55, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Klay Thompson"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=12000, play_id=56, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Tyus Jones"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=57, rebounding_player=Player("Stephen Curry"), is_offensive=False),
    Substitution(play_length=11000, play_id=58, home_team_lineup=frozenset({Player("Jordan Poole"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry"), Player("Klay Thompson")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Jaren Jackson Jr."), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FieldGoalAttempt(play_length=5000, play_id=59, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Draymond Green"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=60, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=9000, play_id=61, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=62, rebounding_player=Player("Dillon Brooks"), is_offensive=True),
    PersonalFoul(play_length=5000, play_id=63, fouling_player=Player("Stephen Curry")),
    FieldGoalAttempt(play_length=7000, play_id=64, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Steven Adams"), assisting_player=Player("Tyus Jones"), was_fouled=False),
    OutOfBoundsTurnover(play_length=4000, play_id=65, player=Player("Draymond Green")),
    FieldGoalAttempt(play_length=9000, play_id=66, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Tyus Jones"), was_fouled=False),
    Steal(play_length=18000, play_id=67, stolen_from=Player("Stephen Curry"), stolen_by=Player("Dillon Brooks")),
    FieldGoalAttempt(play_length=3000, play_id=68, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
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
    FieldGoalAttempt(play_length=19000, play_id=72, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Stephen Curry"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=73, rebounding_player=Player("Kyle Anderson"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=74, shot_made=True, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=14000, play_id=75, shot_made=True, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Jordan Poole"), assisting_player=Player("Draymond Green"), was_fouled=False),
    FieldGoalAttempt(play_length=12000, play_id=76, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Steven Adams"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=77, rebounding_player=Player("Andrew Wiggins"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=78, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Andrew Wiggins"), assisting_player=None, was_fouled=False),
    Rebound(play_length=2000, play_id=79, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=12000, play_id=80, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=81, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=2000, play_id=82, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Andrew Wiggins"), assisting_player=Player("Draymond Green"), was_fouled=False),
    FieldGoalAttempt(play_length=7000, play_id=83, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Dillon Brooks"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=84, rebounding_player=Player("Stephen Curry"), is_offensive=False),
    ShootingFoul(play_length=6000, play_id=85, fouling_player=Player("Steven Adams"), field_goal_made=False, field_goal_type=FieldGoalType.TWO_POINT_SHOT),
    FreeThrow(play_length=0, play_id=86, shot_made=True),
    Substitution(play_length=0, play_id=87, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Draymond Green"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=88, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=89, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Brandon Clarke"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=90, home_team_lineup=frozenset({Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")}), away_team_lineup=frozenset({Player("Brandon Clarke"), Player("Tyus Jones"), Player("Kyle Anderson"), Player("Ziaire Williams"), Player("Desmond Bane")})),
    FreeThrow(play_length=0, play_id=91, shot_made=False),
    Rebound(play_length=3000, play_id=92, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=0, play_id=93, shot_made=False, type=FieldGoalType.LAYUP, shooting_player=Player("Kevon Looney"), assisting_player=None, was_fouled=False),
    Rebound(play_length=1000, play_id=94, rebounding_player=Player("Ziaire Williams"), is_offensive=False),
    FieldGoalAttempt(play_length=9000, play_id=95, shot_made=False, type=FieldGoalType.TWO_POINT_SHOT, shooting_player=Player("Brandon Clarke"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=96, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    Steal(play_length=3000, play_id=97, stolen_by=Player("Ziaire Williams"), stolen_from=Player("Damion Lee")),
    FieldGoalAttempt(play_length=3000, play_id=98, shot_made=True, type=FieldGoalType.LAYUP, shooting_player=Player("Ziaire Williams"), assisting_player=None, was_fouled=False),
    FieldGoalAttempt(play_length=19000, play_id=99, shot_made=False, type=FieldGoalType.THREE_POINT_SHOT, shooting_player=Player("Jordan Poole"), assisting_player=None, was_fouled=False),
    Rebound(play_length=3000, play_id=100, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(
        play_length=10000,
        play_id=101,
        shot_made=False,
        shooting_player=Player("Jordan Poole"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=102,
        rebounding_player=Player("Tyus Jones"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=7000,
        play_id=103,
        shot_made=False,
        shooting_player=Player("Ziaire Williams"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=2000,
        play_id=104,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=14000,
        play_id=105,
        shot_made=True,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=13000,
        play_id=106,
        shot_made=True,
        shooting_player=Player("Desmond Bane"),
        assisting_player=Player("Brandon Clarke"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=21000,
        play_id=107,
        shot_made=False,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=108,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=1000,
        play_id=109,
        shot_made=True,
        shooting_player=Player("Damion Lee"),
        assisting_player=Player("Jordan Poole"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    OffensiveFoul(
        play_length=16000,
        play_id=110,
        fouling_player=Player("Kyle Anderson")
    ),
    OffensiveFoulTurnover(
        play_length=0,
        play_id=111
    ),
    Substitution(
        play_length=0,
        play_id=112,
        home_team_lineup=frozenset({
            Player("Klay Thompson"),
            Player("Jordan Poole"),
            Player("Kevon Looney"),
            Player("Andrew Wiggins"),
            Player("Damion Lee")
        }),
        away_team_lineup=frozenset({
            Player("Brandon Clarke"),
            Player("Tyus Jones"),
            Player("Kyle Anderson"),
            Player("Ziaire Williams"),
            Player("Desmond Bane")
        })
    ),
    Substitution(
        play_length=0,
        play_id=113,
        home_team_lineup=frozenset({
            Player("Klay Thompson"),
            Player("Jordan Poole"),
            Player("Kevon Looney"),
            Player("Andrew Wiggins"),
            Player("Damion Lee")
        }),
        away_team_lineup=frozenset({
            Player("Brandon Clarke"),
            Player("De'Anthony Melton"),
            Player("Kyle Anderson"),
            Player("Ziaire Williams"),
            Player("Desmond Bane")
        })
    ),
    TravelingTurnover(
        play_length=15000,
        play_id=114,
        player=Player("Andrew Wiggins")
    ),
    FieldGoalAttempt(
        play_length=7000,
        play_id=115,
        shot_made=False,
        shooting_player=Player("Brandon Clarke"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=116,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=13000,
        play_id=117,
        shot_made=True,
        shooting_player=Player("Klay Thompson"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=14000,
        play_id=118,
        shot_made=True,
        shooting_player=Player("De'Anthony Melton"),
        assisting_player=Player("Brandon Clarke"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    PeriodEnd(
        play_length=1000,
        play_id=119,
        period_number=1
    ),
    PeriodStart(
        play_length=0,
        play_id=120,
        period_number=2,
        home_team_lineup=frozenset({
            Player("Jordan Poole"),
            Player("Nemanja Bjelica"),
            Player("Draymond Green"),
            Player("Klay Thompson"),
            Player("Damion Lee")
        }),
        away_team_lineup=frozenset({
            Player("Jaren Jackson Jr."),
            Player("Brandon Clarke"),
            Player("De'Anthony Melton"),
            Player("Desmond Bane"),
            Player("Ziaire Williams")
        })
    ),
    FieldGoalAttempt(
        play_length=18000,
        play_id=121,
        shot_made=True,
        shooting_player=Player("Jordan Poole"),
        assisting_player=Player("Nemanja Bjelica"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=14000,
        play_id=122,
        shot_made=True,
        shooting_player=Player("Jaren Jackson Jr."),
        assisting_player=Player("Brandon Clarke"),
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=True
    ),
    ShootingFoul(
        play_length=0,
        play_id=123,
        fouling_player=Player("Draymond Green"),
        field_goal_type=FieldGoalType.TWO_POINT_SHOT,
        field_goal_made=True
    ),
    FreeThrow(
        play_length=0,
        play_id=124,
        shot_made=False
    ),
    Rebound(
        play_length=2000,
        play_id=125,
        rebounding_player=Player("Draymond Green"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=20000,
        play_id=126,
        shot_made=False,
        shooting_player=Player("Jordan Poole"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=4000,
        play_id=127,
        rebounding_player=None,
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=11000,
        play_id=128,
        shot_made=False,
        shooting_player=Player("Klay Thompson"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=129,
        rebounding_player=Player("Damion Lee"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=4000,
        play_id=130,
        shot_made=False,
        shooting_player=Player("Jordan Poole"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=131,
        rebounding_player=Player("Nemanja Bjelica"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=2000,
        play_id=132,
        shot_made=True,
        shooting_player=Player("Klay Thompson"),
        assisting_player=Player("Nemanja Bjelica"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Timeout(
        play_length=1000,
        play_id=133,
        is_home=False
    ),
    ShootingFoul(
        play_length=12000,
        play_id=134,
        fouling_player=Player("Nemanja Bjelica"),
        field_goal_made=False,
        field_goal_type=FieldGoalType.TWO_POINT_SHOT
    ),
    FreeThrow(
        play_length=0,
        play_id=135,
        shot_made=True
    ),
    FreeThrow(
        play_length=0,
        play_id=136,
        shot_made=True
    ),
    FieldGoalAttempt(
        play_length=15000,
        play_id=137,
        shot_made=False,
        shooting_player=Player("Draymond Green"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=138,
        rebounding_player=Player("De'Anthony Melton"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=4000,
        play_id=139,
        shot_made=False,
        shooting_player=Player("Jaren Jackson Jr."),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=140,
        rebounding_player=Player("Klay Thompson"),
        is_offensive=False
    ),
    FieldGoalAttempt(play_length=8000, play_id=141, shot_made=True, shooting_player=Player("Klay Thompson"), assisting_player=Player("Jordan Poole"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=19000, play_id=142, shot_made=True, shooting_player=Player("De'Anthony Melton"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=15000, play_id=143, shot_made=False, shooting_player=Player("Nemanja Bjelica"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=144, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    FieldGoalAttempt(play_length=9000, play_id=145, shot_made=True, shooting_player=Player("Jaren Jackson Jr."), assisting_player=Player("Desmond Bane"), type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=16000, play_id=146, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=147, rebounding_player=Player("Jaren Jackson Jr."), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=148, shot_made=True, shooting_player=Player("Brandon Clarke"), assisting_player=Player("De'Anthony Melton"), type=FieldGoalType.LAYUP, was_fouled=False),
    Timeout(play_length=0, play_id=149, is_home=True),
    Substitution(play_length=0, play_id=150, home_team_lineup=frozenset({Player("Kevon Looney"), Player("Jordan Poole"), Player("Draymond Green"), Player("Klay Thompson"), Player("Nemanja Bjelica")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Brandon Clarke"), Player("De'Anthony Melton"), Player("Desmond Bane"), Player("Ziaire Williams")})),
    Substitution(play_length=0, play_id=151, home_team_lineup=frozenset({Player("Kevon Looney"), Player("Jordan Poole"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Nemanja Bjelica")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Brandon Clarke"), Player("De'Anthony Melton"), Player("Desmond Bane"), Player("Ziaire Williams")})),
    Substitution(play_length=0, play_id=152, home_team_lineup=frozenset({Player("Kevon Looney"), Player("Jordan Poole"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Brandon Clarke"), Player("De'Anthony Melton"), Player("Desmond Bane"), Player("Ziaire Williams")})),
    Substitution(play_length=0, play_id=153, home_team_lineup=frozenset({Player("Kevon Looney"), Player("Jordan Poole"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Stephen Curry")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Brandon Clarke"), Player("De'Anthony Melton"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FieldGoalAttempt(play_length=22000, play_id=154, shot_made=True, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=10000, play_id=155, shot_made=False, shooting_player=Player("Desmond Bane"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=156, rebounding_player=Player("Stephen Curry"), is_offensive=False),
    Steal(play_length=17000, play_id=157, stolen_from=Player("Jordan Poole"), stolen_by=Player("De'Anthony Melton")),
    FieldGoalAttempt(play_length=6000, play_id=158, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=159, rebounding_player=Player("Brandon Clarke"), is_offensive=True),
    FieldGoalAttempt(play_length=8000, play_id=160, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=161, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=162, shot_made=True, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=True),
    ShootingFoul(play_length=0, play_id=163, fouling_player=Player("Desmond Bane"), field_goal_type=FieldGoalType.LAYUP, field_goal_made=True),
    Substitution(play_length=0, play_id=164, home_team_lineup=frozenset({Player("Jordan Poole"), Player("Stephen Curry"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Kevon Looney")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Steven Adams"), Player("Brandon Clarke"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=165, home_team_lineup=frozenset({Player("Jordan Poole"), Player("Stephen Curry"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Kevon Looney")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Steven Adams"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FreeThrow(play_length=0, play_id=166, shot_made=False),
    Rebound(play_length=2000, play_id=167, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    FieldGoalAttempt(play_length=13000, play_id=168, shot_made=True, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=30000, play_id=169, shot_made=False, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=170, rebounding_player=None, is_offensive=True),
    ShotClockViolation(play_length=0, play_id=171),
    FieldGoalAttempt(play_length=11000, play_id=172, shot_made=False, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=173, rebounding_player=Player("Jordan Poole"), is_offensive=False),
    Steal(play_length=7000, play_id=174, stolen_from=Player("Andrew Wiggins"), stolen_by=Player("Tyus Jones")),
    FieldGoalAttempt(play_length=4000, play_id=175, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=176, rebounding_player=Player("Desmond Bane"), is_offensive=True),
    FieldGoalAttempt(play_length=11000, play_id=177, shot_made=True, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Steven Adams"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Timeout(play_length=1000, play_id=178, is_home=True),
    Substitution(play_length=0, play_id=179, home_team_lineup=frozenset({Player("Klay Thompson"), Player("Stephen Curry"), Player("Draymond Green"), Player("Andrew Wiggins"), Player("Kevon Looney")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Steven Adams"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FieldGoalAttempt(play_length=14000, play_id=180, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=181, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=182, shot_made=True, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=12000, play_id=183, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=2000, play_id=184, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=7000, play_id=185, shot_made=True, shooting_player=Player("Jaren Jackson Jr."), assisting_player=Player("Tyus Jones"), type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=17000, play_id=186, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=187, rebounding_player=Player("Andrew Wiggins"), is_offensive=True),
    FieldGoalAttempt(play_length=3000, play_id=188, shot_made=False, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=189, rebounding_player=Player("Andrew Wiggins"), is_offensive=True),
    FieldGoalAttempt(play_length=1000, play_id=190, shot_made=False, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=191, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    PersonalFoul(play_length=3000, play_id=192, fouling_player=Player("Kevon Looney")),
    Substitution(play_length=0, play_id=193, home_team_lineup=frozenset({Player("Klay Thompson"), Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Kevon Looney")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Steven Adams"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    ShootingFoul(play_length=3000, play_id=194, fouling_player=Player("Andrew Wiggins"), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    FreeThrow(play_length=0, play_id=195, shot_made=True),
    FreeThrow(play_length=0, play_id=196, shot_made=False),
    Rebound(play_length=1000, play_id=197, rebounding_player=None, is_offensive=False),
    FieldGoalAttempt(play_length=15000, play_id=198, shot_made=False, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=199, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    ShootingFoul(play_length=3000, play_id=200, fouling_player=Player("Damion Lee"), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    Timeout(play_length=0, play_id=201, is_home=True),
    Unknown(play_length=0, play_id=202),
    Substitution(play_length=0, play_id=203, home_team_lineup=frozenset({Player("Klay Thompson"), Player("Stephen Curry"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Draymond Green")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Steven Adams"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    Substitution(play_length=0, play_id=204, home_team_lineup=frozenset({Player("Klay Thompson"), Player("Stephen Curry"), Player("Nemanja Bjelica"), Player("Andrew Wiggins"), Player("Draymond Green")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Steven Adams"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FreeThrow(play_length=0, play_id=205, shot_made=True),
    FreeThrow(play_length=0, play_id=206, shot_made=True),
    FieldGoalAttempt(play_length=14000, play_id=207, shot_made=True, shooting_player=Player("Draymond Green"), assisting_player=Player("Stephen Curry"), type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=20000, play_id=208, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=209, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    Steal(play_length=18000, play_id=210, stolen_by=Player("Dillon Brooks"), stolen_from=Player("Draymond Green")),
    FieldGoalAttempt(play_length=8000, play_id=211, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=212, rebounding_player=None, is_offensive=False),
    FlagrantFoul(play_length=0, play_id=213, fouling_player=Player("Dillon Brooks")),
    DoubleTechnicalFoul(play_length=0, play_id=214),
    Unknown(play_length=0, play_id=215),
    FreeThrow(play_length=0, play_id=216, shot_made=True),
    FreeThrow(play_length=0, play_id=217, shot_made=False),
    Rebound(play_length=0, play_id=218, rebounding_player=None, is_offensive=True),
    Substitution(play_length=0, play_id=219, home_team_lineup=frozenset({Player("Klay Thompson"), Player("Stephen Curry"), Player("Nemanja Bjelica"), Player("Andrew Wiggins"), Player("Draymond Green")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Brandon Clarke"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    OutOfBoundsTurnover(play_length=14000, play_id=220, player=Player("Stephen Curry")),
    FieldGoalAttempt(play_length=17000, play_id=221, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=222, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=223, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=224, rebounding_player=Player("Nemanja Bjelica"), is_offensive=True),
    FieldGoalAttempt(play_length=4000, play_id=225, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=226, rebounding_player=Player("Dillon Brooks"), is_offensive=False),
    FieldGoalAttempt(play_length=13000, play_id=227, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=228, rebounding_player=Player("Stephen Curry"), is_offensive=False),
    OutOfBoundsTurnover(play_length=3000, play_id=229, player=Player("Klay Thompson")),
    Substitution(play_length=0, play_id=230, home_team_lineup=frozenset({Player("Jordan Poole"), Player("Stephen Curry"), Player("Klay Thompson"), Player("Andrew Wiggins"), Player("Draymond Green")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Brandon Clarke"), Player("Desmond Bane"), Player("Dillon Brooks")})),
    FieldGoalAttempt(play_length=9000, play_id=231, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=232, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    FieldGoalAttempt(play_length=12000, play_id=233, shot_made=False, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=4000, play_id=234, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    FieldGoalAttempt(play_length=3000, play_id=235, shot_made=False, shooting_player=Player("Brandon Clarke"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=2000, play_id=236, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    ShootingFoul(play_length=2000, play_id=237, fouling_player=Player("Desmond Bane"), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    FreeThrow(play_length=0, play_id=238, shot_made=True),
    Substitution(play_length=0, play_id=239, home_team_lineup=frozenset({Player("Jordan Poole"), Player("Stephen Curry"), Player("Klay Thompson"), Player("Andrew Wiggins"), Player("Draymond Green")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Brandon Clarke"), Player("Desmond Bane"), Player("Ziaire Williams")})),
    FreeThrow(play_length=0, play_id=240, shot_made=True),
    Steal(play_length=12000, play_id=241, stolen_from=Player("Tyus Jones"), stolen_by=Player("Stephen Curry")),
    FieldGoalAttempt(play_length=4000, play_id=242, shot_made=True, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=11000, play_id=243, shot_made=False, shooting_player=Player("Desmond Bane"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=2000, play_id=244, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=245, shot_made=False, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=246, rebounding_player=Player("Andrew Wiggins"), is_offensive=True),
    FieldGoalAttempt(play_length=4000, play_id=247, shot_made=False, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=248, rebounding_player=Player("Jaren Jackson Jr."), is_offensive=False),
    FieldGoalAttempt(play_length=7000, play_id=249, shot_made=False, shooting_player=Player("Desmond Bane"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=0, play_id=250, rebounding_player=None, is_offensive=False),
    ShootingFoul(play_length=6000, play_id=251, fouling_player=Player("Jaren Jackson Jr."), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    FreeThrow(play_length=0, play_id=252, shot_made=True),
    Substitution(play_length=0, play_id=253, home_team_lineup=frozenset({Player("Kevon Looney"), Player("Stephen Curry"), Player("Jordan Poole"), Player("Andrew Wiggins"), Player("Klay Thompson")}), away_team_lineup=frozenset({Player("Jaren Jackson Jr."), Player("Tyus Jones"), Player("Brandon Clarke"), Player("Desmond Bane"), Player("Ziaire Williams")})),
    Substitution(play_length=0, play_id=254, home_team_lineup=frozenset({Player("Kevon Looney"), Player("Stephen Curry"), Player("Jordan Poole"), Player("Andrew Wiggins"), Player("Klay Thompson")}), away_team_lineup=frozenset({Player("Dillon Brooks"), Player("Jaren Jackson Jr."), Player("Brandon Clarke"), Player("Desmond Bane"), Player("Ziaire Williams")})),
    FreeThrow(play_length=0, play_id=255, shot_made=True),
    FieldGoalAttempt(play_length=22000, play_id=256, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=2000, play_id=257, rebounding_player=Player("Brandon Clarke"), is_offensive=True),
    FieldGoalAttempt(play_length=2000, play_id=258, shot_made=False, shooting_player=Player("Brandon Clarke"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=259, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=17000, play_id=260, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=261, rebounding_player=None, is_offensive=True),
    PeriodEnd(play_length=0, play_id=262, period_number=2),
    PeriodStart(play_length=0, play_id=263, period_number=3, home_team_lineup=frozenset({Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Klay Thompson"), Player("Kevon Looney")}), away_team_lineup=frozenset({Player("Steven Adams"), Player("Dillon Brooks"), Player("Desmond Bane"), Player("Jaren Jackson Jr."), Player("Tyus Jones")})),
    FieldGoalAttempt(play_length=20000, play_id=264, shot_made=False, shooting_player=Player("Draymond Green"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=265, rebounding_player=Player("Steven Adams"), is_offensive=False),
    FieldGoalAttempt(play_length=23000, play_id=266, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=267, rebounding_player=Player("Dillon Brooks"), is_offensive=True),
    FieldGoalAttempt(play_length=0, play_id=268, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=0, play_id=269, rebounding_player=None, is_offensive=True),
    ShotClockViolation(play_length=1000, play_id=270),
    FieldGoalAttempt(play_length=16000, play_id=271, shot_made=False, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=272, rebounding_player=Player("Andrew Wiggins"), is_offensive=True),
    FieldGoalAttempt(play_length=5000, play_id=273, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=274, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=275, shot_made=True, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Desmond Bane"), type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=16000, play_id=276, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=277, rebounding_player=Player("Jaren Jackson Jr."), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=278, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=279, rebounding_player=None, is_offensive=True),
    FieldGoalAttempt(play_length=7000, play_id=280, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=281, rebounding_player=Player("Steven Adams"), is_offensive=True),
    ShootingFoul(play_length=0, play_id=282, fouling_player=Player("Klay Thompson"), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    FreeThrow(play_length=0, play_id=283, shot_made=False),
    Rebound(play_length=0, play_id=284, rebounding_player=None, is_offensive=True),
    FreeThrow(play_length=0, play_id=285, shot_made=True),
    FieldGoalAttempt(play_length=14000, play_id=286, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=287, rebounding_player=Player("Andrew Wiggins"), is_offensive=True),
    FieldGoalAttempt(play_length=2000, play_id=288, shot_made=True, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=14000, play_id=289, shot_made=False, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=2000, play_id=290, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=1000, play_id=291, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=292, rebounding_player=None, is_offensive=False),
    PersonalFoul(play_length=12000, play_id=293, fouling_player=Player("Andrew Wiggins")),
    FieldGoalAttempt(play_length=6000, play_id=294, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=295, rebounding_player=Player("Draymond Green"), is_offensive=False),
    Steal(play_length=8000, play_id=296, stolen_by=Player("Tyus Jones"), stolen_from=Player("Draymond Green")),
    ShootingFoul(play_length=4000, play_id=297, fouling_player=Player("Klay Thompson"), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    FreeThrow(play_length=0, play_id=298, shot_made=False),
    Rebound(play_length=0, play_id=299, rebounding_player=None, is_offensive=True),
    FreeThrow(play_length=0, play_id=300, shot_made=True),
    FieldGoalAttempt(play_length=19000, play_id=301, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=302, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    FieldGoalAttempt(play_length=10000, play_id=303, shot_made=False, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=5000, play_id=304, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=4000, play_id=305, shot_made=True, shooting_player=Player("Klay Thompson"), assisting_player=Player("Draymond Green"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=23000, play_id=306, shot_made=True, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Steven Adams"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=9000, play_id=307, shot_made=True, shooting_player=Player("Klay Thompson"), assisting_player=Player("Draymond Green"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=23000, play_id=308, shot_made=False, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=309, rebounding_player=None, is_offensive=False),
    FieldGoalAttempt(play_length=7000, play_id=310, shot_made=True, shooting_player=Player("Klay Thompson"), assisting_player=Player("Stephen Curry"), type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=20000, play_id=311, shot_made=True, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=20000, play_id=312, shot_made=True, shooting_player=Player("Kevon Looney"), assisting_player=Player("Draymond Green"), type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=16000, play_id=313, shot_made=True, shooting_player=Player("Desmond Bane"), assisting_player=Player("Tyus Jones"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=16000, play_id=314, shot_made=True, shooting_player=Player("Draymond Green"), assisting_player=Player("Stephen Curry"), type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=21000, play_id=315, shot_made=True, shooting_player=Player("Desmond Bane"), assisting_player=Player("Tyus Jones"), type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=6000, play_id=316, shot_made=True, shooting_player=Player("Klay Thompson"), assisting_player=Player("Draymond Green"), type=FieldGoalType.LAYUP, was_fouled=False),
    OffensiveFoul(play_length=4000, play_id=317, fouling_player=Player("Tyus Jones")),
    OffensiveFoulTurnover(play_length=0, play_id=318),
    Timeout(play_length=0, play_id=319, is_home=True),
    Substitution(play_length=0, play_id=320, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Klay Thompson"), Player("Kevon Looney")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("Desmond Bane"), Player("Jaren Jackson Jr."), Player("Tyus Jones")])),
    FieldGoalAttempt(play_length=11000, play_id=321, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=322, rebounding_player=None, is_offensive=True),
    PersonalFoul(play_length=0, play_id=323, fouling_player=Player("Tyus Jones")),
    Substitution(play_length=0, play_id=324, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Klay Thompson"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("Desmond Bane"), Player("Jaren Jackson Jr."), Player("Tyus Jones")])),
    OutOfBoundsTurnover(play_length=8000, play_id=325, player=Player("Stephen Curry")),
    FieldGoalAttempt(play_length=13000, play_id=326, shot_made=False, shooting_player=Player("Brandon Clarke"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=327, rebounding_player=Player("Draymond Green"), is_offensive=False),
    OutOfBoundsTurnover(play_length=4000, play_id=328, player=Player("Draymond Green")),
    FieldGoalAttempt(play_length=12000, play_id=329, shot_made=True, shooting_player=Player("Jaren Jackson Jr."), assisting_player=Player("Dillon Brooks"), type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=15000, play_id=330, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=331, rebounding_player=Player("Tyus Jones"), is_offensive=False),
    FieldGoalAttempt(play_length=5000, play_id=332, shot_made=False, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=333, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    OutOfBoundsTurnover(play_length=2000, play_id=334, player=Player("Klay Thompson")),
    Substitution(play_length=0, play_id=335, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Klay Thompson"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Jaren Jackson Jr."), Player("Tyus Jones")])),
    FieldGoalAttempt(play_length=13000, play_id=336, shot_made=False, shooting_player=Player("Jaren Jackson Jr."), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=337, rebounding_player=Player("Draymond Green"), is_offensive=False),
    FieldGoalAttempt(play_length=11000, play_id=338, shot_made=True, shooting_player=Player("Andrew Wiggins"), assisting_player=Player("Stephen Curry"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=16000, play_id=339, shot_made=False, shooting_player=Player("Brandon Clarke"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=340, rebounding_player=Player("Jordan Poole"), is_offensive=False),
    FieldGoalAttempt(play_length=6000, play_id=341, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=342, rebounding_player=Player("Jaren Jackson Jr."), is_offensive=False),
    FieldGoalAttempt(play_length=5000, play_id=343, shot_made=False, shooting_player=Player("De'Anthony Melton"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=0, play_id=344, rebounding_player=Player("De'Anthony Melton"), is_offensive=True),
    OutOfBoundsTurnover(play_length=0, play_id=345, player=Player("De'Anthony Melton")),
    PersonalFoul(play_length=3000, play_id=346, fouling_player=Player("Jaren Jackson Jr.")),
    Substitution(play_length=0, play_id=347, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Damion Lee"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Jaren Jackson Jr."), Player("Tyus Jones")])),
    FieldGoalAttempt(play_length=11000, play_id=348, shot_made=False, shooting_player=Player("Damion Lee"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=349, rebounding_player=Player("Dillon Brooks"), is_offensive=False),
    Timeout(play_length=3000, play_id=350, is_home=False),
    Substitution(play_length=0, play_id=351, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Damion Lee"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Kyle Anderson"), Player("Tyus Jones")])),
    FieldGoalAttempt(play_length=10000, play_id=352, shot_made=False, shooting_player=Player("Tyus Jones"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=353, rebounding_player=None, is_offensive=False),
    FieldGoalAttempt(play_length=11000, play_id=354, shot_made=True, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    ShootingFoul(play_length=20000, play_id=355, fouling_player=Player("Draymond Green"), field_goal_type=FieldGoalType.TWO_POINT_SHOT, field_goal_made=False),
    FreeThrow(play_length=0, play_id=356, shot_made=True),
    Substitution(play_length=0, play_id=357, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Andrew Wiggins"), Player("Kevon Looney"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Kyle Anderson"), Player("Tyus Jones")])),
    Substitution(play_length=0, play_id=358, home_team_lineup=frozenset([Player("Draymond Green"), Player("Stephen Curry"), Player("Nemanja Bjelica"), Player("Kevon Looney"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Kyle Anderson"), Player("Tyus Jones")])),
    Substitution(play_length=0, play_id=359, home_team_lineup=frozenset([Player("Klay Thompson"), Player("Stephen Curry"), Player("Nemanja Bjelica"), Player("Kevon Looney"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Kyle Anderson"), Player("Tyus Jones")])),
    Substitution(play_length=0, play_id=360, home_team_lineup=frozenset([Player("Klay Thompson"), Player("Stephen Curry"), Player("Nemanja Bjelica"), Player("Kevon Looney"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Brandon Clarke"), Player("Dillon Brooks"), Player("De'Anthony Melton"), Player("Kyle Anderson"), Player("Desmond Bane")])),
    FreeThrow(play_length=0, play_id=361, shot_made=True),
    FieldGoalAttempt(play_length=15000, play_id=362, shot_made=False, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=363, rebounding_player=Player("Kyle Anderson"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=364, shot_made=True, shooting_player=Player("Desmond Bane"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    OutOfBoundsTurnover(play_length=13000, play_id=365, player=Player("Jordan Poole")),
    FieldGoalAttempt(play_length=15000, play_id=366, shot_made=True, shooting_player=Player("Desmond Bane"), assisting_player=Player("Kyle Anderson"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=19000, play_id=367, shot_made=True, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=11000, play_id=368, shot_made=False, shooting_player=Player("De'Anthony Melton"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=369, rebounding_player=Player("Klay Thompson"), is_offensive=False),
    FieldGoalAttempt(play_length=8000, play_id=370, shot_made=True, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=17000, play_id=371, shot_made=True, shooting_player=Player("De'Anthony Melton"), assisting_player=Player("Brandon Clarke"), type=FieldGoalType.LAYUP, was_fouled=False),
    PersonalFoul(play_length=18000, play_id=372, fouling_player=Player("De'Anthony Melton")),
    FieldGoalAttempt(play_length=5000, play_id=373, shot_made=False, shooting_player=Player("Stephen Curry"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=1000, play_id=374, rebounding_player=Player("Desmond Bane"), is_offensive=False),
    PeriodEnd(play_length=0, play_id=375, period_number=3),
    PeriodStart(play_length=0, play_id=376, period_number=4, home_team_lineup=frozenset([Player("Kevon Looney"), Player("Klay Thompson"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("De'Anthony Melton"), Player("Desmond Bane"), Player("Steven Adams"), Player("Kyle Anderson"), Player("Ziaire Williams")])),
    FieldGoalAttempt(play_length=15000, play_id=377, shot_made=False, shooting_player=Player("De'Anthony Melton"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=378, rebounding_player=Player("Kevon Looney"), is_offensive=False),
    FieldGoalAttempt(play_length=16000, play_id=379, shot_made=False, shooting_player=Player("Klay Thompson"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=380, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=3000, play_id=381, shot_made=False, shooting_player=Player("Kevon Looney"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=382, rebounding_player=Player("Kevon Looney"), is_offensive=True),
    FieldGoalAttempt(play_length=0, play_id=383, shot_made=False, shooting_player=Player("Kevon Looney"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=384, rebounding_player=Player("Damion Lee"), is_offensive=True),
    FieldGoalAttempt(play_length=7000, play_id=385, shot_made=True, shooting_player=Player("Andrew Wiggins"), assisting_player=Player("Klay Thompson"), type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=15000, play_id=386, shot_made=True, shooting_player=Player("Desmond Bane"), assisting_player=Player("Steven Adams"), type=FieldGoalType.LAYUP, was_fouled=False),
    FieldGoalAttempt(play_length=13000, play_id=387, shot_made=False, shooting_player=Player("Jordan Poole"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=2000, play_id=388, rebounding_player=Player("Kyle Anderson"), is_offensive=False),
    FieldGoalAttempt(play_length=15000, play_id=389, shot_made=False, shooting_player=Player("Desmond Bane"), assisting_player=None, type=FieldGoalType.LAYUP, was_fouled=False),
    Rebound(play_length=1000, play_id=390, rebounding_player=None, is_offensive=True),
    Substitution(play_length=0, play_id=391, home_team_lineup=frozenset([Player("Kevon Looney"), Player("Klay Thompson"), Player("Damion Lee"), Player("Andrew Wiggins"), Player("Jordan Poole")]), away_team_lineup=frozenset([Player("Dillon Brooks"), Player("Desmond Bane"), Player("Steven Adams"), Player("Kyle Anderson"), Player("Ziaire Williams")])),
    FieldGoalAttempt(play_length=4000, play_id=392, shot_made=True, shooting_player=Player("Dillon Brooks"), assisting_player=Player("Kyle Anderson"), type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=27000, play_id=393, shot_made=True, shooting_player=Player("Andrew Wiggins"), assisting_player=None, type=FieldGoalType.TWO_POINT_SHOT, was_fouled=False),
    FieldGoalAttempt(play_length=17000, play_id=394, shot_made=False, shooting_player=Player("Dillon Brooks"), assisting_player=None, type=FieldGoalType.THREE_POINT_SHOT, was_fouled=False),
    Rebound(play_length=3000, play_id=395, rebounding_player=Player("Andrew Wiggins"), is_offensive=False),
    FieldGoalAttempt(
        play_length=14000,
        play_id=396,
        shot_made=False,
        shooting_player=Player("Andrew Wiggins"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=397,
        rebounding_player=Player("Steven Adams"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=3000,
        play_id=398,
        shot_made=False,
        shooting_player=Player("Dillon Brooks"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=0,
        play_id=399,
        rebounding_player=None,
        is_offensive=False
    ),
    Substitution(
        play_length=0,
        play_id=400,
        home_team_lineup=frozenset([
            Player("Kevon Looney"),
            Player("Klay Thompson"),
            Player("Draymond Green"),
            Player("Andrew Wiggins"),
            Player("Jordan Poole")
        ]),
        away_team_lineup=frozenset([
            Player("Dillon Brooks"),
            Player("Desmond Bane"),
            Player("Steven Adams"),
            Player("Kyle Anderson"),
            Player("Ziaire Williams")
        ])
    ),
    Substitution(
        play_length=0,
        play_id=401,
        home_team_lineup=frozenset([
            Player("Kevon Looney"),
            Player("Klay Thompson"),
            Player("Draymond Green"),
            Player("Andrew Wiggins"),
            Player("Jordan Poole")
        ]),
        away_team_lineup=frozenset([
            Player("Dillon Brooks"),
            Player("Desmond Bane"),
            Player("Steven Adams"),
            Player("Jaren Jackson Jr."),
            Player("Ziaire Williams")
        ])
    ),
    FieldGoalAttempt(
        play_length=9000,
        play_id=402,
        shot_made=False,
        shooting_player=Player("Jordan Poole"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=6000,
        play_id=403,
        rebounding_player=Player("Andrew Wiggins"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=0,
        play_id=404,
        shot_made=False,
        shooting_player=Player("Jordan Poole"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=405,
        rebounding_player=Player("Draymond Green"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=1000,
        play_id=406,
        shot_made=False,
        shooting_player=Player("Klay Thompson"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=1000,
        play_id=407,
        rebounding_player=None,
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=25000,
        play_id=408,
        shot_made=True,
        shooting_player=Player("Dillon Brooks"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    ShootingFoul(
        play_length=10000,
        play_id=409,
        fouling_player=Player("Steven Adams"),
        field_goal_type=FieldGoalType.TWO_POINT_SHOT,
        field_goal_made=False
    ),
    FreeThrow(
        play_length=0,
        play_id=410,
        shot_made=True
    ),
    Substitution(
        play_length=0,
        play_id=411,
        home_team_lineup=frozenset([
            Player("Kevon Looney"),
            Player("Klay Thompson"),
            Player("Draymond Green"),
            Player("Stephen Curry"),
            Player("Jordan Poole")
        ]),
        away_team_lineup=frozenset([
            Player("Dillon Brooks"),
            Player("Desmond Bane"),
            Player("Steven Adams"),
            Player("Jaren Jackson Jr."),
            Player("Ziaire Williams")
        ])
    ),
    Substitution(
        play_length=0,
        play_id=412,
        home_team_lineup=frozenset([
            Player("Kevon Looney"),
            Player("Klay Thompson"),
            Player("Draymond Green"),
            Player("Stephen Curry"),
            Player("Jordan Poole")
        ]),
        away_team_lineup=frozenset([
            Player("Dillon Brooks"),
            Player("Desmond Bane"),
            Player("Steven Adams"),
            Player("Jaren Jackson Jr."),
            Player("Tyus Jones")
        ])
    ),
    FreeThrow(
        play_length=0,
        play_id=413,
        shot_made=True
    ),
    FieldGoalAttempt(
        play_length=19000,
        play_id=414,
        shot_made=True,
        shooting_player=Player("Dillon Brooks"),
        assisting_player=Player("Tyus Jones"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=14000,
        play_id=415,
        shot_made=False,
        shooting_player=Player("Draymond Green"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=2000,
        play_id=416,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=9000,
        play_id=417,
        shot_made=True,
        shooting_player=Player("Draymond Green"),
        assisting_player=Player("Kevon Looney"),
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=13000,
        play_id=418,
        shot_made=False,
        shooting_player=Player("Tyus Jones"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=419,
        rebounding_player=Player("Jordan Poole"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=7000,
        play_id=420,
        shot_made=False,
        shooting_player=Player("Klay Thompson"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
Rebound(
        play_length=3000,
        play_id=421,
        rebounding_player=Player("Steven Adams"),
        is_offensive=False
    ),
    Timeout(
        play_length=3000,
        play_id=422,
        is_home=False
    ),
    Substitution(
        play_length=0,
        play_id=423,
        home_team_lineup=frozenset([
            Player("Kevon Looney"),
            Player("Klay Thompson"),
            Player("Draymond Green"),
            Player("Stephen Curry"),
            Player("Andrew Wiggins")
        ]),
        away_team_lineup=frozenset([
            Player("Dillon Brooks"),
            Player("Desmond Bane"),
            Player("Steven Adams"),
            Player("Jaren Jackson Jr."),
            Player("Tyus Jones")
        ])
    ),
    FieldGoalAttempt(
        play_length=13000,
        play_id=424,
        shot_made=True,
        shooting_player=Player("Desmond Bane"),
        assisting_player=Player("Tyus Jones"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=26000,
        play_id=425,
        shot_made=True,
        shooting_player=Player("Andrew Wiggins"),
        assisting_player=Player("Kevon Looney"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Steal(
        play_length=15000,
        play_id=426,
        stolen_from=Player("Dillon Brooks"),
        stolen_by=Player("Andrew Wiggins")
    ),
    FieldGoalAttempt(
        play_length=4000,
        play_id=427,
        shot_made=True,
        shooting_player=Player("Andrew Wiggins"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=20000,
        play_id=428,
        shot_made=False,
        shooting_player=Player("Dillon Brooks"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=429,
        rebounding_player=Player("Draymond Green"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=2000,
        play_id=430,
        shot_made=True,
        shooting_player=Player("Stephen Curry"),
        assisting_player=Player("Draymond Green"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Timeout(
        play_length=2000,
        play_id=431,
        is_home=False
    ),
    FieldGoalAttempt(
        play_length=18000,
        play_id=432,
        shot_made=False,
        shooting_player=Player("Dillon Brooks"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=433,
        rebounding_player=None,
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=18000,
        play_id=434,
        shot_made=True,
        shooting_player=Player("Draymond Green"),
        assisting_player=Player("Kevon Looney"),
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    ShootingFoul(
        play_length=18000,
        play_id=435,
        fouling_player=Player("Stephen Curry"),
        field_goal_type=FieldGoalType.TWO_POINT_SHOT,
        field_goal_made=False
    ),
    FreeThrow(
        play_length=0,
        play_id=436,
        shot_made=True
    ),
    FreeThrow(
        play_length=0,
        play_id=437,
        shot_made=False
    ),
    Rebound(
        play_length=2000,
        play_id=438,
        rebounding_player=Player("Andrew Wiggins"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=16000,
        play_id=439,
        shot_made=False,
        shooting_player=Player("Draymond Green"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=3000,
        play_id=440,
        shot_made=False,
        shooting_player=Player("Draymond Green"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    Rebound(
        play_length=0,
        play_id=441,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=True
    ),
    Rebound(
        play_length=0,
        play_id=442,
        rebounding_player=Player("Draymond Green"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=2000,
        play_id=443,
        shot_made=True,
        shooting_player=Player("Kevon Looney"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=10000,
        play_id=444,
        shot_made=True,
        shooting_player=Player("Tyus Jones"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=18000,
        play_id=445,
        shot_made=True,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
FieldGoalAttempt(
        play_length=17000,
        play_id=446,
        shot_made=False,
        shooting_player=Player("Tyus Jones"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=447,
        rebounding_player=Player("Stephen Curry"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=17000,
        play_id=448,
        shot_made=False,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=449,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=12000,
        play_id=450,
        shot_made=False,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=451,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=2000,
        play_id=452,
        shot_made=True,
        shooting_player=Player("Klay Thompson"),
        assisting_player=Player("Kevon Looney"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Timeout(
        play_length=1000,
        play_id=453,
        is_home=False
    ),
    Substitution(
        play_length=0,
        play_id=454,
        home_team_lineup=frozenset([
            Player("Kevon Looney"),
            Player("Klay Thompson"),
            Player("Draymond Green"),
            Player("Stephen Curry"),
            Player("Andrew Wiggins")
        ]),
        away_team_lineup=frozenset([
            Player("Dillon Brooks"),
            Player("Desmond Bane"),
            Player("Brandon Clarke"),
            Player("Jaren Jackson Jr."),
            Player("Tyus Jones")
        ])
    ),
    FieldGoalAttempt(
        play_length=19000,
        play_id=455,
        shot_made=False,
        shooting_player=Player("Jaren Jackson Jr."),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=2000,
        play_id=456,
        rebounding_player=Player("Stephen Curry"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=17000,
        play_id=457,
        shot_made=False,
        shooting_player=Player("Draymond Green"),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=2000,
        play_id=458,
        rebounding_player=Player("Tyus Jones"),
        is_offensive=False
    ),
    PersonalFoul(
        play_length=7000,
        play_id=459,
        fouling_player=Player("Kevon Looney")
    ),
    FieldGoalAttempt(
        play_length=7000,
        play_id=460,
        shot_made=False,
        shooting_player=Player("Brandon Clarke"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=2000,
        play_id=461,
        rebounding_player=Player("Kevon Looney"),
        is_offensive=False
    ),
    FieldGoalAttempt(
        play_length=15000,
        play_id=462,
        shot_made=False,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=463,
        rebounding_player=Player("Draymond Green"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=4000,
        play_id=464,
        shot_made=True,
        shooting_player=Player("Stephen Curry"),
        assisting_player=Player("Klay Thompson"),
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=7000,
        play_id=465,
        shot_made=False,
        shooting_player=Player("Desmond Bane"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=0,
        play_id=466,
        rebounding_player=Player("Brandon Clarke"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=0,
        play_id=467,
        shot_made=True,
        shooting_player=Player("Brandon Clarke"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=True
    ),
    ShootingFoul(
        play_length=0,
        play_id=468,
        fouling_player=Player("Kevon Looney"),
        field_goal_type=FieldGoalType.LAYUP,
        field_goal_made=True
    ),
    FreeThrow(
        play_length=0,
        play_id=469,
        shot_made=False
    ),
    Rebound(
        play_length=2000,
        play_id=470,
        rebounding_player=Player("Tyus Jones"),
        is_offensive=True
    ),
    ShootingFoul(
        play_length=0,
        play_id=471,
        fouling_player=Player("Draymond Green"),
        field_goal_type=FieldGoalType.TWO_POINT_SHOT,
        field_goal_made=False
    ),
    FreeThrow(
        play_length=0,
        play_id=472,
        shot_made=True
    ),
    FreeThrow(
        play_length=0,
        play_id=473,
        shot_made=True
    ),
    Steal(
        play_length=13000,
        play_id=474,
        stolen_from=Player("Kevon Looney"),
        stolen_by=Player("Brandon Clarke")
    ),
    FieldGoalAttempt(
        play_length=5000,
        play_id=475,
        shot_made=False,
        shooting_player=Player("Jaren Jackson Jr."),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=1000,
        play_id=476,
        rebounding_player=Player("Andrew Wiggins"),
        is_offensive=False
    ),
    PersonalFoul(
        play_length=3000,
        play_id=477,
        fouling_player=Player("Desmond Bane")
    ),
    FieldGoalAttempt(
        play_length=21000,
        play_id=478,
        shot_made=True,
        shooting_player=Player("Stephen Curry"),
        assisting_player=None,
        type=FieldGoalType.LAYUP,
        was_fouled=False
    ),
    FieldGoalAttempt(
        play_length=14000,
        play_id=479,
        shot_made=False,
        shooting_player=Player("Brandon Clarke"),
        assisting_player=None,
        type=FieldGoalType.TWO_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=3000,
        play_id=480,
        rebounding_player=Player("Brandon Clarke"),
        is_offensive=True
    ),
    FieldGoalAttempt(
        play_length=3000,
        play_id=481,
        shot_made=False,
        shooting_player=Player("Jaren Jackson Jr."),
        assisting_player=None,
        type=FieldGoalType.THREE_POINT_SHOT,
        was_fouled=False
    ),
    Rebound(
        play_length=2000,
        play_id=482,
        rebounding_player=Player("Stephen Curry"),
        is_offensive=False
    ),
    ShotClockViolation(
        play_length=24000,
        play_id=483
    ),
    PeriodEnd(
        play_length=1000,
        play_id=484,
        period_number=4
    )
]
