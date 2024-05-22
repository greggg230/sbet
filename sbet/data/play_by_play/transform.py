from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Foul, JumpBall, PeriodStart, PeriodEnd, Rebound, Timeout, Substitution
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoulTurnover
)
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay


def parse_play_length(play_length_str: str) -> int:
    h, m, s = map(int, play_length_str.split(':'))
    return (h * 3600 + m * 60 + s) * 1000


def convert_to_nba_play(play: Play) -> NbaPlay:
    play_length = parse_play_length(play.play_length)
    if play.event_type == "shot":
        return FieldGoalAttempt(
            play_length=play_length,
            play_id=play.play_id,
            shot_made=play.result == "made",
            points=play.points or 0
        )
    elif play.event_type == "rebound":
        return Rebound(
            play_length=play_length,
            play_id=play.play_id,
            rebounding_player=Player(play.player) if play.player else None,
            is_offensive=play.type == "rebound offensive"
        )
    elif play.event_type == "foul":
        return Foul(
            play_length=play_length,
            play_id=play.play_id,
            foul_type=play.type,
            committed_by=Player(play.player)
        )
    elif play.event_type == "turnover":
        if play.steal:
            return Steal(
                play_length=play_length,
                play_id=play.play_id,
                stolen_from=Player(play.player),
                stolen_by=Player(play.steal)
            )
        elif play.type == "shot clock":
            return ShotClockViolation(
                play_length=play_length,
                play_id=play.play_id
            )
        elif play.type in {"out of bounds lost ball", "bad pass"}:
            return OutOfBoundsTurnover(
                play_length=play_length,
                play_id=play.play_id,
                player=Player(play.player)
            )
        elif play.type == "offensive foul":
            return OffensiveFoulTurnover(
                play_length=play_length,
                play_id=play.play_id
            )
        else:
            raise ValueError(f"Unrecognized turnover type: {play.type}")
    elif play.event_type == "start of period":
        return PeriodStart(
            play_length=play_length,
            play_id=play.play_id,
            period_number=play.period,
            home_team_lineup=frozenset(Player(p) for p in [play.h1, play.h2, play.h3, play.h4, play.h5]),
            away_team_lineup=frozenset(Player(p) for p in [play.a1, play.a2, play.a3, play.a4, play.a5])
        )
    elif play.event_type == "end of period":
        return PeriodEnd(
            play_length=play_length,
            play_id=play.play_id,
            period_number=play.period
        )
    elif play.event_type == "timeout":
        return Timeout(
            play_length=play_length,
            play_id=play.play_id,
            is_home=play.team == "home"
        )
    elif play.event_type == "substitution":
        return Substitution(
            play_length=play_length,
            play_id=play.play_id,
            home_team_lineup=frozenset(Player(p) for p in [play.h1, play.h2, play.h3, play.h4, play.h5]),
            away_team_lineup=frozenset(Player(p) for p in [play.a1, play.a2, play.a3, play.a4, play.a5])
        )
    elif play.event_type == "jump ball":
        return JumpBall(
            play_length=play_length,
            play_id=play.play_id,
            home_player=Player(play.home),
            away_player=Player(play.away),
            did_home_team_win=(play.player == play.home)
        )
    else:
        raise ValueError(f"Unrecognized play type: {play.event_type}")
