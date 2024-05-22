from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, PeriodStart, PeriodEnd, Foul, JumpBall, Rebound, Timeout, Substitution
)
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.turnover import (
    OffensiveFoul, Steal, ShotClockViolation, OutOfBoundsTurnover
)


def convert_to_nba_play(play: Play):
    play_length = int(play.play_length.split(':')[2]) * 1000 + int(play.play_length.split(':')[1]) * 60000 + int(play.play_length.split(':')[0]) * 3600000

    if play.event_type == "start of period":
        return PeriodStart(
            play_length=play_length,
            play_id=play.play_id,
            period_number=play.period,
            home_team_lineup=frozenset(Player(p) for p in [play.h1, play.h2, play.h3, play.h4, play.h5]),
            away_team_lineup=frozenset(Player(p) for p in [play.a1, play.a2, play.a3, play.a4, play.a5])
        )

    if play.event_type == "end of period":
        return PeriodEnd(
            play_length=play_length,
            play_id=play.play_id,
            period_number=play.period
        )

    if play.event_type == "shot":
        return FieldGoalAttempt(
            play_length=play_length,
            play_id=play.play_id,
            shot_made=play.result == "made",
            points=play.points
        )

    if play.event_type == "foul":
        return Foul(
            play_length=play_length,
            play_id=play.play_id,
            foul_type=play.type,
            committed_by=Player(play.player)
        )

    if play.event_type == "jump ball":
        home_player = Player(play.home)
        away_player = Player(play.away)
        did_home_team_win = Player(play.player) == home_player
        return JumpBall(
            play_length=play_length,
            play_id=play.play_id,
            home_player=home_player,
            away_player=away_player,
            did_home_team_win=did_home_team_win
        )

    if play.event_type == "rebound":
        return Rebound(
            play_length=play_length,
            play_id=play.play_id,
            rebounding_player=Player(play.player) if play.player else None,
            is_offensive=play.type == "rebound offensive"
        )

    if play.event_type == "timeout":
        return Timeout(
            play_length=play_length,
            play_id=play.play_id,
            is_home=play.team == "home"
        )

    if play.event_type == "turnover":
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
        elif play.type in ["bad pass", "out of bounds lost ball"]:
            return OutOfBoundsTurnover(
                play_length=play_length,
                play_id=play.play_id,
                player=Player(play.player)
            )
        else:
            raise ValueError(f"Unrecognized turnover type: {play.type}")

    if play.event_type == "offensive foul":
        return OffensiveFoul(
            play_length=play_length,
            play_id=play.play_id,
            fouling_player=Player(play.player)
        )

    if play.event_type == "substitution":
        home_team_lineup = frozenset(Player(p) for p in [play.h1, play.h2, play.h3, play.h4, play.h5])
        away_team_lineup = frozenset(Player(p) for p in [play.a1, play.a2, play.a3, play.a4, play.a5])
        return Substitution(
            play_length=play_length,
            play_id=play.play_id,
            home_team_lineup=home_team_lineup,
            away_team_lineup=away_team_lineup
        )

    raise ValueError(f"Unrecognized play type: {play.event_type}")
