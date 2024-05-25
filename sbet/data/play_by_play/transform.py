from datetime import timedelta

from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType
from sbet.data.play_by_play.models.transform.fouls import OffensiveFoul, PersonalFoul, ShootingFoul, TechnicalFoul, \
    FlagrantFoul, DoubleTechnicalFoul
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Substitution, PeriodStart, PeriodEnd, Timeout, JumpBall, Rebound, FreeThrow, Unknown
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoulTurnover, TravelingTurnover
)


def parse_play_length(play_length_str: str) -> timedelta:
    time_parts = list(map(int, play_length_str.split(':')))
    return timedelta(hours=time_parts[0], minutes=time_parts[1], seconds=time_parts[2])


THREE_POINT_SHOT_TYPES = [
    "3pt jump shot", "3pt running pull-up jump shot", "3pt pullup jump shot", "3pt step back jump shot", "3pt running jump shot"]
LAYUP_TYPES = [
    "layup", "cutting layup shot", "driving dunk", "dunk", "cutting finger roll layup shot", "driving layup",
    "driving reverse layup", "cutting dunk shot"]
TWO_POINT_SHOT_TYPES = [
    "jump shot", "hook shot", "fadeaway jumper", "floating jump shot", "driving floating jump shot", "driving floating bank jump shot"]


def determine_field_goal_type_and_result(play: Play) -> (FieldGoalType, bool):
    if play.type in THREE_POINT_SHOT_TYPES:
        field_goal_type = FieldGoalType.THREE_POINT_SHOT
    elif play.type in LAYUP_TYPES:
        field_goal_type = FieldGoalType.LAYUP
    elif play.type in TWO_POINT_SHOT_TYPES:
        field_goal_type = FieldGoalType.TWO_POINT_SHOT
    else:
        raise ValueError(f"Unexpected shot type: {play.type}")

    shot_made = play.result == "made"
    return field_goal_type, shot_made


def next_play_is_foul(plays: list[Play], play_index: int) -> bool:
    if play_index + 1 < len(plays):
        next_play = plays[play_index + 1]
        return (
            next_play.event_type == "foul" and
            next_play.type == "shooting" and
            next_play.play_length == "0:00:00"
        )
    return False


def find_previous_shot(play_index: int, plays: list[Play]) -> (FieldGoalType, bool):
    if play_index == 0 or plays[play_index].play_length != "0:00:00":
        return None, False

    previous_play = plays[play_index - 1]

    if previous_play.event_type != "shot":
        return None, False

    return determine_field_goal_type_and_result(previous_play)


def find_next_free_throw_type(play_index: int, plays: list[Play]) -> FieldGoalType:
    for i in range(play_index + 1, len(plays)):
        if plays[i].event_type == "free throw":
            if plays[i].type == "free throw 1/2":
                return FieldGoalType.TWO_POINT_SHOT
            elif plays[i].type == "free throw 1/3":
                return FieldGoalType.THREE_POINT_SHOT
    return FieldGoalType.TWO_POINT_SHOT  # Defaulting to two-point shot if no free throw type found


def convert_to_nba_play(play: Play, game: Game) -> NbaPlay:
    play_length = int(parse_play_length(play.play_length).total_seconds() * 1000)
    event_type = play.event_type
    plays = game.plays
    play_index = plays.index(play)

    match event_type:
        case "shot":
            field_goal_type, shot_made = determine_field_goal_type_and_result(play)
            shooting_player = Player(play.player)
            assisting_player = Player(play.assist) if play.assist else None
            was_fouled = next_play_is_foul(plays, play_index)

            return FieldGoalAttempt(
                play_length=play_length,
                play_id=play.play_id,
                shot_made=shot_made,
                shooting_player=shooting_player,
                assisting_player=assisting_player,
                type=field_goal_type,
                was_fouled=was_fouled
            )

        case "foul":
            fouler = Player(play.player)

            match play.type:
                case "personal" | "loose ball" | "personal take":
                    return PersonalFoul(
                        play_length=play_length,
                        play_id=play.play_id,
                        fouling_player=fouler
                    )
                case "offensive":
                    return OffensiveFoul(
                        play_length=play_length,
                        play_id=play.play_id,
                        fouling_player=fouler
                    )
                case "shooting":
                    previous_shot_type, shot_made = find_previous_shot(play_index, plays)
                    if previous_shot_type:
                        field_goal_type = previous_shot_type
                    else:
                        field_goal_type = find_next_free_throw_type(play_index, plays)

                    return ShootingFoul(
                        play_length=play_length,
                        play_id=play.play_id,
                        fouling_player=fouler,
                        field_goal_type=field_goal_type,
                        field_goal_made=shot_made
                    )
                case "technical":
                    is_home_team = play.team == game.home_team.value
                    fouler = Player(play.player) if play.player else None
                    return TechnicalFoul(
                        play_length=play_length,
                        play_id=play.play_id,
                        fouling_player=fouler,
                        is_home_team=is_home_team
                    )
                case "flagrant-1" | "flagrant-2":
                    return FlagrantFoul(
                        play_length=play_length,
                        play_id=play.play_id,
                        fouling_player=fouler
                    )
                case _:
                    raise ValueError(f"Unexpected foul type: {play.type}")
        case "technical foul":
            match play.type:
                case "double technical":
                    return DoubleTechnicalFoul(
                        play_length=play_length,
                        play_id=play.play_id
                    )
                case _:
                    raise ValueError(f"Unexpected technical foul: {play.type}")

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
            is_home = play.team == game.home_team.value
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
            elif play.type == "traveling":
                return TravelingTurnover(
                    play_length=play_length,
                    play_id=play.play_id,
                    player=Player(play.player)
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

        case "":
            return Unknown(
                play_length=play_length,
                play_id=play.play_id
            )
        case _:
            raise ValueError(f"Unrecognized play type: {event_type}")
