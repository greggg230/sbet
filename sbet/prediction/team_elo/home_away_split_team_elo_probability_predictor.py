# sbet/prediction/team_elo/home_away_split_predictor.py

from typing import List
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity
from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor
from sbet.prediction.team_elo.calculate_home_away_split_nba_elo import calculate_home_away_split_nba_elo
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome


class HomeAwaySplitTeamEloProbabilityPredictor(BetProbabilityPredictor):
    def __init__(self, game_outcomes: List[NbaGameOutcome], k: float = 32):
        self.team_elos = calculate_home_away_split_nba_elo(game_outcomes, k=k)

    def calculate_probability_of_bet_win(self, opportunity: NbaMoneyLineBettingOpportunity) -> float:
        home_team_home_elo, home_team_away_elo = self.team_elos[opportunity.game.home_team]
        away_team_home_elo, away_team_away_elo = self.team_elos[opportunity.game.away_team]

        if opportunity.bet_on_home_team:
            expected_win_prob = 1 / (1 + 10 ** ((away_team_away_elo - home_team_home_elo) / 400))
        else:
            expected_win_prob = 1 / (1 + 10 ** ((home_team_home_elo - away_team_away_elo) / 400))

        return expected_win_prob if opportunity.bet_on_home_team else 1 - expected_win_prob
