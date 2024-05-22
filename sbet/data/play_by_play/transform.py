from datetime import timedelta
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Substitution, PeriodStart, PeriodEnd, Timeout, Foul, JumpBall, Rebound, NbaPlay
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoul
)
from sbet.data.play_by_play.models.transform.player import Player


def parse_play_length(play_length_str: str) -> int:
    h, m, s = map(int, play_length_str.split(':'))
    return int(timedelta(hours=h, minutes=m, seconds=s).total_seconds() * 1000)


def convert_to_nba_play(play: Play) -> NbaPlay:
    play_length = parse_play_length(play.play_length)
    match play.event_type.lower():
        case "shot":
            return FieldGoalAttempt(
                play_length=play_length,
                play_id=play.play_id,
                shot_made=play.result == "made",
                points=play.points or 0
            )

        case "rebound":
            rebounding_player = Player(play.player) if play.player else None
            is_offensive = play.type.lower() == "rebound offensive"
            return Rebound(
                play_length=play_length,
                play_id=play.play_id,
                rebounding_player=rebounding_player,
                is_offensive=is_offensive
            )

        case "foul":
            return Foul(
                play_length=play_length,
                play_id=play.play_id,
                foul_type=play.type,
                committed_by=Player(play.player) if play.player else None
            )

        case "jump ball":
            home_player = Player(play.home) if play.home else None
            away_player = Player(play.away) if play.away else None
            did_home_team_win = play.player == play.home
            return JumpBall(
                play_length=play_length,
                play_id=play.play_id,
                home_player=home_player,
                away_player=away_player,
                did_home_team_win=did_home_team_win
            )

        case "substitution":
            home_team_lineup = frozenset(
                Player(player) for player in [play.h1, play.h2, play.h3, play.h4, play.h5] if player
            )
            away_team_lineup = frozenset(
                Player(player) for player in [play.a1, play.a2, play.a3, play.a4, play.a5] if player
            )
            return Substitution(
                play_length=play_length,
                play_id=play.play_id,
                home_team_lineup=home_team_lineup,
                away_team_lineup=away_team_lineup
            )

        case "timeout":
            is_home = play.team.lower() == "home"
            return Timeout(
                play_length=play_length,
                play_id=play.play_id,
                is_home=is_home
            )

        case "turnover":
            if play.steal:
                return Steal(
                    play_length=play_length,
                    play_id=play.play_id,
                    stolen_from=Player(play.opponent) if play.opponent else None,
                    stolen_by=Player(play.steal) if play.steal else None
                )
            elif play.type.lower() == "shot clock":
                return ShotClockViolation(
                    play_length=play_length,
                    play_id=play.play_id
                )
            elif play.type.lower() == "bad pass" or play.type.lower() == "out of bounds lost ball":
                return OutOfBoundsTurnover(
                    play_length=play_length,
                    play_id=play.play_id,
                    player=Player(play.player) if play.player else None
                )
            else:
                raise ValueError(f"Unexpected turnover type: {play.type}")

        case "offensive foul":
            return OffensiveFoul(
                play_length=play_length,
                play_id=play.play_id,
                fouling_player=Player(play.player) if play.player else None
            )

        case "start of period":
            return PeriodStart(
                play_length=play_length,
                play_id=play.play_id,
                period_number=play.period
            )

        case "end of period":
            return PeriodEnd(
                play_length=play_length,
                play_id=play.play_id,
                period_number=play.period
            )

        case _:
            raise ValueError(f"Unrecognized play type: {play.event_type}")
