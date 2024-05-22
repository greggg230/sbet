from dataclasses import replace
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Substitution, PeriodStart, PeriodEnd, Timeout, Foul, JumpBall, Rebound
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoul
)
from sbet.data.play_by_play.models.transform.game_state import GameState
from sbet.data.play_by_play.models.transform.player import Player
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from frozendict import frozendict


def update_game_state(game_state: GameState, play: NbaPlay) -> GameState:
    remaining_time = game_state.milliseconds_remaining_in_period - play.play_length
    state_with_updated_time = replace(game_state, milliseconds_remaining_in_period=remaining_time)

    match play:
        case FieldGoalAttempt(shot_made=True, points=points):
            new_home_score = game_state.home_score + points if game_state.home_team_has_possession else game_state.home_score
            new_away_score = game_state.away_score + points if not game_state.home_team_has_possession else game_state.away_score
            return replace(
                state_with_updated_time,
                home_score=new_home_score,
                away_score=new_away_score,
                home_team_has_possession=not game_state.home_team_has_possession
            )

        case FieldGoalAttempt(shot_made=False):
            return state_with_updated_time

        case Foul(committed_by=fouler):
            new_personal_foul_count = game_state.personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1}
            return replace(state_with_updated_time, personal_foul_count=new_personal_foul_count)

        case JumpBall(did_home_team_win=True):
            return replace(state_with_updated_time, home_team_has_possession=True)

        case JumpBall(did_home_team_win=False):
            return replace(state_with_updated_time, home_team_has_possession=False)

        case PeriodStart(period_number=period, home_team_lineup=home_lineup, away_team_lineup=away_lineup):
            return replace(
                state_with_updated_time,
                current_period=period,
                milliseconds_remaining_in_period=720000,
                home_team_lineup=home_lineup,
                away_team_lineup=away_lineup
            )

        case PeriodEnd(period_number=period):
            return replace(state_with_updated_time, current_period=period + 1, milliseconds_remaining_in_period=0)

        case Timeout(is_home=True):
            return replace(state_with_updated_time, home_timeouts=game_state.home_timeouts - 1)

        case Timeout(is_home=False):
            return replace(state_with_updated_time, away_timeouts=game_state.away_timeouts - 1)

        case Rebound(is_offensive=True):
            return state_with_updated_time

        case Rebound(is_offensive=False):
            return replace(state_with_updated_time, home_team_has_possession=not game_state.home_team_has_possession)

        case Steal(stolen_by=stealer):
            return replace(state_with_updated_time, home_team_has_possession=stealer in game_state.home_team_lineup)

        case ShotClockViolation():
            return replace(state_with_updated_time, home_team_has_possession=not game_state.home_team_has_possession)

        case OutOfBoundsTurnover():
            return replace(state_with_updated_time, home_team_has_possession=not game_state.home_team_has_possession)

        case OffensiveFoul(fouling_player=fouler):
            return replace(state_with_updated_time, home_team_has_possession=fouler not in game_state.home_team_lineup)

        case Substitution(home_team_lineup=new_home_lineup, away_team_lineup=new_away_lineup):
            return replace(state_with_updated_time, home_team_lineup=new_home_lineup, away_team_lineup=new_away_lineup)

        case _:
            raise ValueError(f"Unrecognized play type: {play}")
