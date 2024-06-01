from dataclasses import dataclass
from typing import List

from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge


@dataclass(frozen=True)
class SimpleContext:
    home_win_elo_probability: float
    home_rest_days: int
    away_rest_days: int
    home_team_games_played_this_season: int
    away_team_games_played_this_season: int


class SimpleLinearModel:
    model: RandomForestRegressor

    def __init__(self, training_set: List[SimpleContext], training_results: List[bool]):
        self.model = RandomForestRegressor()
        training_df = DataFrame(map(lambda x: x.__dict__, training_set))
        results_df = DataFrame(map(lambda x: 1 if x else 0, training_results))

        self.model.fit(training_df, results_df)

    def predict(self, context: SimpleContext) -> float:
        return self.model.predict(DataFrame([context.__dict__]))
