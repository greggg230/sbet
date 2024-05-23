from datetime import timedelta
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Foul, JumpBall, PeriodStart, PeriodEnd, Rebound, Substitution, Timeout, FreeThrow
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoulTurnover
)
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay


def parse_play_length(play_length_str: str) -> timedelta:
    time_parts = list(map(int, play_length_str.split(':')))
    return timedelta(hours=time_parts[0], minutes=time_parts[1], seconds=time_parts[2])


def convert_to_nba_play(play: Play, home_team: NbaTeam, away_team: NbaTeam) -> NbaPlay:
    play_length = int(parse_play_length(play.play_length).total_seconds() * 1000)
    event_type = play.event_type

    match event_type:
        case "shot":
            shot_made = play.result == "made"
            points = int(play.points) if shot_made else 0
            return FieldGoalAttempt(
                play_length=play_length,
                play_id=play.play_id,
                shot_made=shot_made,
                points=points
            )

        case "foul":
            return Foul(
                play_length=play_length,
                play_id=play.play_id,
                foul_type=play.type,
                committed_by=Player(play.player),
                is_offensive=play.type == "offensive"
            )

        case "jump ball":
            did_home_team_win = play.player == play.home
            return JumpBall(
                play_length=play_length,
                play_id=play.play_id,
                home_player=Player(play.h1),
                away_player=Player(play.a1),
                did_home_team_win=did_home_team_win
            )

        case "start of period":
            return PeriodStart(
                play_length=play_length,
                play_id=play.play_id,
                period_number=play.period,
                home_team_lineup=frozenset([Player(play.h1), Player(play.h2), Player(play.h3), Player(play.h4), Player(play.h5)]),
                away_team_lineup=frozenset([Player(play.a1), Player(play.a2), Player(play.a3), Player(play.a4), Player(play.a5)])
            )

        case "end of period":
            return PeriodEnd(
                play_length=play_length,
                play_id=play.play_id,
                period_number=play.period
            )

        case "rebound":
            is_offensive = play.type == "rebound offensive" or play.type == "team rebound"
            rebounding_player = Player(play.player) if play.player else None
            return Rebound(
                play_length=play_length,
                play_id=play.play_id,
                rebounding_player=rebounding_player,
                is_offensive=is_offensive
            )

        case "substitution":
            home_team_lineup = frozenset(
                [Player(play.h1), Player(play.h2), Player(play.h3), Player(play.h4), Player(play.h5)]
            )
            away_team_lineup = frozenset(
                [Player(play.a1), Player(play.a2), Player(play.a3), Player(play.a4), Player(play.a5)]
            )
            return Substitution(
                play_length=play_length,
                play_id=play.play_id,
                home_team_lineup=home_team_lineup,
                away_team_lineup=away_team_lineup
            )

        case "timeout":
            is_home = play.team == home_team.value
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
                    stolen_from=Player(play.player),
                    stolen_by=Player(play.steal)
                )
            elif play.type == "shot clock":
                return ShotClockViolation(
                    play_length=play_length,
                    play_id=play.play_id
                )
            elif play.type == "out of bounds lost ball" or play.type == "bad pass":
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
                raise ValueError(f"Unexpected turnover type: {play.type}")

        case "free throw":
            shot_made = play.result == "made"
            return FreeThrow(
                play_length=play_length,
                play_id=play.play_id,
                shot_made=shot_made
            )

        case _:
            raise ValueError(f"Unrecognized play type: {event_type}")
