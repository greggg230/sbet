from dataclasses import replace
from frozendict import frozendict
from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Substitution, PeriodStart, PeriodEnd, Timeout, Foul, JumpBall
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoul
)


class UnrecognizedPlayException(Exception):
    pass


def update_game_state(game_state: GameState, play: NbaPlay) -> GameState:
    remaining_time = game_state.milliseconds_remaining_in_period - play.play_length
    state_with_updated_time = replace(game_state, milliseconds_remaining_in_period=remaining_time)

    match play:
        case FieldGoalAttempt(shot_made=True, points=points):
            if game_state.home_team_has_possession:
                home_score = game_state.home_score + points
                away_score = game_state.away_score
            else:
                home_score = game_state.home_score
                away_score = game_state.away_score + points
            return replace(state_with_updated_time,
                           home_team_has_possession=not game_state.home_team_has_possession,
                           home_score=home_score,
                           away_score=away_score)

        case FieldGoalAttempt(shot_made=False):
            return replace(state_with_updated_time,
                           home_team_has_possession=not game_state.home_team_has_possession)

        case Substitution(home_team_lineup=home_lineup, away_team_lineup=away_lineup):
            return replace(state_with_updated_time,
                           home_team_lineup=home_lineup,
                           away_team_lineup=away_lineup)

        case PeriodStart(period_number=period):
            return replace(state_with_updated_time,
                           current_period=period,
                           personal_foul_count=frozendict(),
                           milliseconds_remaining_in_period=720000 if period <= 4 else 300000)

        case PeriodEnd():
            return replace(state_with_updated_time,
                           milliseconds_remaining_in_period=0)

        case Timeout(is_home=True):
            return replace(state_with_updated_time,
                           home_timeouts=game_state.home_timeouts - 1)

        case Timeout(is_home=False):
            return replace(state_with_updated_time,
                           away_timeouts=game_state.away_timeouts - 1)

        case Foul(committed_by=player):
            new_personal_foul_count = frozendict(game_state.personal_foul_count | {player: game_state.personal_foul_count.get(player, 0) + 1})
            return replace(state_with_updated_time,
                           personal_foul_count=new_personal_foul_count)

        case JumpBall(did_home_team_win=home_win):
            return replace(state_with_updated_time,
                           home_team_has_possession=home_win)

        case Steal():
            return replace(state_with_updated_time,
                           home_team_has_possession=not game_state.home_team_has_possession)

        case ShotClockViolation():
            return replace(state_with_updated_time,
                           home_team_has_possession=not game_state.home_team_has_possession)

        case OutOfBoundsTurnover():
            return replace(state_with_updated_time,
                           home_team_has_possession=not game_state.home_team_has_possession)

        case OffensiveFoul(fouling_player=fouler):
            new_personal_foul_count = frozendict(game_state.personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1})
            return replace(state_with_updated_time,
                           home_team_has_possession=not game_state.home_team_has_possession,
                           personal_foul_count=new_personal_foul_count)

        case _:
            raise UnrecognizedPlayException(f"Unrecognized play type: {type(play)}")
