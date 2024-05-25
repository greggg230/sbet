from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType
from sbet.data.play_by_play.models.transform.fouls import OffensiveFoul, ShootingFoul, PersonalFoul, FlagrantFoul, \
    TechnicalFoul, DoubleTechnicalFoul
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

]
