from dataclasses import replace
from sbet.data.play_by_play.models.transform.game_state import GameState, FreeThrowState
from sbet.data.play_by_play.models.transform.nba_play import NbaPlay
from sbet.data.play_by_play.models.transform.plays import (
    FieldGoalAttempt, Substitution, PeriodStart, PeriodEnd, Timeout, JumpBall, Rebound, FreeThrow
)
from sbet.data.play_by_play.models.transform.turnover import (
    Steal, ShotClockViolation, OutOfBoundsTurnover, OffensiveFoulTurnover, TravelingTurnover
)
from sbet.data.play_by_play.models.transform.field_goal_type import FieldGoalType
from sbet.data.play_by_play.models.transform.fouls import (
    OffensiveFoul, PersonalFoul, ShootingFoul, TechnicalFoul, FlagrantFoul
)
from sbet.data.play_by_play.models.csv.game import Game


def award_free_throws(state: GameState, award_to_home: bool, free_throw_count: int, retain_possession_afterwards: bool) -> GameState:
    return replace(
        state,
        free_throw_state=FreeThrowState(
            free_throws_remaining=free_throw_count,
            for_home_team=award_to_home,
            shooting_team_gets_possession_after=retain_possession_afterwards
        )
    )


def next_play_is_foul(game: Game, current_play_index: int) -> bool:
    if current_play_index + 1 < len(game.plays):
        next_play = game.plays[current_play_index + 1]
        return (
            next_play.event_type == "foul" and
            next_play.type == "s.foul" and
            next_play.elapsed == "0:00:00"
        )
    return False


def update_game_state(game_state: GameState, play: NbaPlay) -> GameState:
    remaining_time = game_state.milliseconds_remaining_in_period - play.play_length
    state_with_updated_time = replace(game_state, milliseconds_remaining_in_period=remaining_time)

    match play:
        case FieldGoalAttempt(shot_made=True, type=field_goal_type, was_fouled=was_fouled):
            points = 3 if field_goal_type == FieldGoalType.THREE_POINT_SHOT else 2
            new_home_score = game_state.home_score + points if game_state.home_team_has_possession else game_state.home_score
            new_away_score = game_state.away_score + points if not game_state.home_team_has_possession else game_state.away_score
            new_possession = not game_state.home_team_has_possession if not was_fouled else game_state.home_team_has_possession
            return replace(state_with_updated_time, home_score=new_home_score, away_score=new_away_score, home_team_has_possession=new_possession)

        case FieldGoalAttempt(shot_made=False):
            return state_with_updated_time

        case PersonalFoul(fouling_player=fouler):
            new_personal_foul_count = game_state.personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1}
            new_state = replace(state_with_updated_time, personal_foul_count=new_personal_foul_count)

            if game_state.home_team_has_possession:
                new_state = replace(new_state, away_team_fouls=game_state.away_team_fouls + 1)
                if game_state.away_team_fouls + 1 >= 5:
                    return award_free_throws(new_state, award_to_home=True, free_throw_count=2, retain_possession_afterwards=False)
            else:
                new_state = replace(new_state, home_team_fouls=game_state.home_team_fouls + 1)
                if game_state.home_team_fouls + 1 >= 5:
                    return award_free_throws(new_state, award_to_home=False, free_throw_count=2, retain_possession_afterwards=False)
            return new_state

        case OffensiveFoul(fouling_player=fouler):
            new_personal_foul_count = game_state.personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1}
            return replace(state_with_updated_time, personal_foul_count=new_personal_foul_count)

        case ShootingFoul(fouling_player=fouler, field_goal_type=field_goal_type, field_goal_made=field_goal_made):
            new_personal_foul_count = game_state.personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1}
            new_state = replace(state_with_updated_time, personal_foul_count=new_personal_foul_count)

            if field_goal_made:
                return award_free_throws(
                    new_state,
                    award_to_home=not game_state.home_team_has_possession,
                    free_throw_count=1,
                    retain_possession_afterwards=False,
                )
            else:
                free_throw_count = 3 if field_goal_type == FieldGoalType.THREE_POINT_SHOT else 2
                return award_free_throws(new_state, award_to_home=game_state.home_team_has_possession, free_throw_count=free_throw_count, retain_possession_afterwards=False)

        case TechnicalFoul(fouling_player=fouler, is_home_team=is_home_team):
            new_personal_foul_count = game_state.personal_foul_count
            if fouler:
                new_personal_foul_count = new_personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1}
            new_state = replace(state_with_updated_time, personal_foul_count=new_personal_foul_count)
            award_to_home = not is_home_team
            return award_free_throws(new_state, award_to_home=award_to_home, free_throw_count=1, retain_possession_afterwards=True)

        case FlagrantFoul(fouling_player=fouler):
            new_personal_foul_count = game_state.personal_foul_count | {fouler: game_state.personal_foul_count.get(fouler, 0) + 1}
            new_state = replace(state_with_updated_time, personal_foul_count=new_personal_foul_count)
            return award_free_throws(new_state, award_to_home=game_state.home_team_has_possession, free_throw_count=2, retain_possession_afterwards=True)

        case FreeThrow(shot_made=shot_made):
            if game_state.free_throw_state is None or game_state.free_throw_state.free_throws_remaining < 1:
                raise ValueError("Unexpected FreeThrow play with no free throws remaining")
            new_home_score = game_state.home_score + 1 if game_state.free_throw_state.for_home_team and shot_made else game_state.home_score
            new_away_score = game_state.away_score + 1 if not game_state.free_throw_state.for_home_team and shot_made else game_state.away_score
            free_throws_remaining = game_state.free_throw_state.free_throws_remaining - 1
            new_free_throw_state = replace(game_state.free_throw_state, free_throws_remaining=free_throws_remaining)
            possession_after_free_throw = game_state.home_team_has_possession
            if free_throws_remaining == 0:
                if not shot_made:
                    possession_after_free_throw = game_state.home_team_has_possession
                elif game_state.free_throw_state.shooting_team_gets_possession_after:
                    possession_after_free_throw = game_state.home_team_has_possession
                else:
                    possession_after_free_throw = not game_state.home_team_has_possession
            new_state = replace(state_with_updated_time, home_score=new_home_score, away_score=new_away_score, free_throw_state=new_free_throw_state if free_throws_remaining > 0 else None, home_team_has_possession=possession_after_free_throw)
            return new_state

        case JumpBall(did_home_team_win=True):
            return replace(state_with_updated_time, home_team_has_possession=True)

        case JumpBall(did_home_team_win=False):
            return replace(state_with_updated_time, home_team_has_possession=False)

        case PeriodStart(period_number=period, home_team_lineup=home_lineup, away_team_lineup=away_lineup):
            return replace(state_with_updated_time, current_period=period, milliseconds_remaining_in_period=720000, home_team_lineup=home_lineup, away_team_lineup=away_lineup)

        case PeriodEnd(period_number=period):
            return replace(state_with_updated_time, milliseconds_remaining_in_period=0)

        case Timeout(is_home=True):
            return replace(state_with_updated_time, home_timeouts=game_state.home_timeouts - 1)

        case Timeout(is_home=False):
            return replace(state_with_updated_time, away_timeouts=game_state.away_timeouts - 1)

        case Rebound(is_offensive=True):
            return state_with_updated_time

        case Rebound(is_offensive=False):
            return replace(state_with_updated_time, home_team_has_possession=not game_state.home_team_has_possession)

        case Steal() | ShotClockViolation() | OutOfBoundsTurnover() | OffensiveFoulTurnover() | TravelingTurnover():
            return replace(state_with_updated_time, home_team_has_possession=not game_state.home_team_has_possession)

        case Substitution(home_team_lineup=new_home_lineup, away_team_lineup=new_away_lineup):
            return replace(state_with_updated_time, home_team_lineup=new_home_lineup, away_team_lineup=new_away_lineup)

        case _:
            raise ValueError(f"Unrecognized play type: {play}")
