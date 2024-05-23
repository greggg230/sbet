from datetime import timedelta
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, PeriodStart, PeriodEnd, Timeout, Foul, JumpBall, Rebound, FreeThrow, Substitution, NbaPlay
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoulTurnover
)
from sbet.data.play_by_play.models.transform.player import Player


def parse_play_length(play_length_str: str) -> int:
    h, m, s = map(int, play_length_str.split(':'))
    return int(timedelta(hours=h, minutes=m, seconds=s).total_seconds() * 1000)


def convert_to_nba_play(play: Play) -> NbaPlay:
    play_length = parse_play_length(play.play_length)

    if play.event_type == "shot":
        shot_made = play.result == "made"
        points = int(play.points) if play.points else 0
        return FieldGoalAttempt(play_length=play_length, play_id=play.play_id, shot_made=shot_made, points=points)

    if play.event_type == "free throw":
        shot_made = play.result == "made"
        return FreeThrow(play_length=play_length, play_id=play.play_id, shot_made=shot_made)

    if play.event_type == "foul":
        is_offensive = play.type == "offensive"
        return Foul(play_length=play_length, play_id=play.play_id, foul_type=play.type, committed_by=Player(play.player), is_offensive=is_offensive)

    if play.event_type == "jump ball":
        did_home_team_win = play.player == play.home
        return JumpBall(play_length=play_length, play_id=play.play_id, home_player=Player(play.h1), away_player=Player(play.a1), did_home_team_win=did_home_team_win)

    if play.event_type == "rebound":
        is_offensive = play.type == "rebound offensive" or play.type == "team rebound"
        rebounding_player = Player(play.player) if play.player else None
        return Rebound(play_length=play_length, play_id=play.play_id, rebounding_player=rebounding_player, is_offensive=is_offensive)

    if play.event_type == "turnover":
        if play.steal:
            return Steal(play_length=play_length, play_id=play.play_id, stolen_from=Player(play.player), stolen_by=Player(play.steal))
        if play.type == "shot clock":
            return ShotClockViolation(play_length=play_length, play_id=play.play_id)
        if play.type in ["out of bounds lost ball", "bad pass"]:
            return OutOfBoundsTurnover(play_length=play_length, play_id=play.play_id, player=Player(play.player))
        if play.type == "offensive foul":
            return OffensiveFoulTurnover(play_length=play_length, play_id=play.play_id)
        raise ValueError(f"Unrecognized turnover type: {play.type}")

    if play.event_type == "timeout":
        is_home = play.team == "home"
        return Timeout(play_length=play_length, play_id=play.play_id, is_home=is_home)

    if play.event_type == "start of period":
        home_team_lineup = frozenset([Player(play.h1), Player(play.h2), Player(play.h3), Player(play.h4), Player(play.h5)])
        away_team_lineup = frozenset([Player(play.a1), Player(play.a2), Player(play.a3), Player(play.a4), Player(play.a5)])
        return PeriodStart(play_length=play_length, play_id=play.play_id, period_number=play.period, home_team_lineup=home_team_lineup, away_team_lineup=away_team_lineup)

    if play.event_type == "end of period":
        return PeriodEnd(play_length=play_length, play_id=play.play_id, period_number=play.period)

    if play.event_type == "substitution":
        home_team_lineup = frozenset([Player(play.h1), Player(play.h2), Player(play.h3), Player(play.h4), Player(play.h5)])
        away_team_lineup = frozenset([Player(play.a1), Player(play.a2), Player(play.a3), Player(play.a4), Player(play.a5)])
        return Substitution(play_length=play_length, play_id=play.play_id, home_team_lineup=home_team_lineup, away_team_lineup=away_team_lineup)

    raise ValueError(f"Unrecognized play type: {play.event_type}")
