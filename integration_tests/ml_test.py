import os
from typing import List

from pandas import DataFrame

from sklearn.metrics import mean_squared_error, r2_score

from integration_tests.team_elo_nba_test import test_predictor
from sbet.data.historical.extractor.scottfree.extractor import ScottfreeHistoricalBetDataExtractor
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity
from sbet.prediction import BetProbabilityPredictor
from sbet.prediction.team_elo.elo import calculate_win_probability
from sbet.prediction.team_elo.generate_game_context import generate_game_context_for_games
from sbet.prediction.team_elo.models.game_context import GameContext
from tests.prediction.ml.simple_linear_model import SimpleLinearModel, SimpleContext


class MlPredictor(BetProbabilityPredictor):
    model: SimpleLinearModel
    contexts: dict[Game, GameContext]

    def __init__(self, model: SimpleLinearModel, contexts: dict[Game, GameContext]):
        self.model = model
        self.contexts = contexts

    def _convert_context(self, context: GameContext) -> SimpleContext:
        probability = calculate_win_probability(context.home_team_elo, context.away_team_elo)
        return SimpleContext(
            home_win_elo_probability=probability,
            home_rest_days=context.home_team_rest_days,
            away_rest_days=context.away_team_rest_days,
            home_team_games_played_this_season=context.home_team_games_played_this_season,
            away_team_games_played_this_season=context.away_team_games_played_this_season
        )

    def calculate_probability_of_bet_win(self, opportunity: MoneyLineBettingOpportunity) -> float:
        context = self._convert_context(self.contexts[opportunity.game])
        home_win_prob = self.model.model.predict(DataFrame([context.__dict__]))[0]
        if opportunity.bet_on_home_team:
            return home_win_prob
        else:
            return 1 - home_win_prob


def convert_context_to_simple_context(context: GameContext) -> SimpleContext:
    probability = calculate_win_probability(context.home_team_elo, context.away_team_elo)
    return SimpleContext(
        home_win_elo_probability=probability,
        home_rest_days=context.home_team_rest_days,
        away_rest_days=context.away_team_rest_days,
        home_team_games_played_this_season=context.home_team_games_played_this_season,
        away_team_games_played_this_season=context.away_team_games_played_this_season
    )

def test_ml():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_dir, "../sbet", 'data', 'historical', 'extractor', 'scottfree', 'resources', 'nba.csv')
    extractor = ScottfreeHistoricalBetDataExtractor(csv_file_path)
    extracted_data = extractor.extract()

    for k in [50, 100, 200]:

        game_contexts_dict = generate_game_context_for_games(extracted_data.games, k=k)

        game_contexts: List[GameContext] = []
        game_outcomes: List[bool] = []

        for game, context in game_contexts_dict.items():
            game_contexts.append(context)
            game_outcomes.append(game.home_score > game.away_score)

        simple_contexts = [convert_context_to_simple_context(context) for context in game_contexts]

        training_contexts = []
        training_outcomes = []

        test_contexts = []
        test_outcomes = []

        for game, context in game_contexts_dict.items():
            simple_context = convert_context_to_simple_context(context)
            if 8 < game.game_date.month < 12:
                training_contexts.append(simple_context)
                training_outcomes.append(game.home_score > game.away_score)
            else:
                test_contexts.append(simple_context)
                test_outcomes.append(game.home_score > game.away_score)

        print(len(training_contexts))

        model = SimpleLinearModel(training_contexts, training_outcomes)

        test_data = simple_contexts[5000:]
        outcomes = game_outcomes[5000:]

        predictions = model.model.predict(DataFrame([i.__dict__ for i in test_data]))

        test_y = DataFrame([1 if outcome else 0 for outcome in outcomes])

        test_predictor(
            extractor,
            MlPredictor(model, game_contexts_dict),
            game_contexts_dict
        )


if __name__ == "__main__":
    test_ml()
