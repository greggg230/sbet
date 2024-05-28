from typing import List
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity
from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome
from sbet.prediction.team_elo.calculate_nba_elo import calculate_nba_elo
from sbet.prediction.team_elo.elo import calculate_win_probability

from sbet.prediction.bet_probability_predictor import BetProbabilityPredictor


class TeamEloProbabilityPredictor(BetProbabilityPredictor):
    def __init__(self, game_outcomes: List[NbaGameOutcome]):
        self.team_elos = calculate_nba_elo(game_outcomes)

    def calculate_probability_of_bet_win(self, opportunity: NbaMoneyLineBettingOpportunity) -> float:
        home_team = opportunity.game.home_team
        away_team = opportunity.game.away_team

        home_team_elo = self.team_elos[home_team]
        away_team_elo = self.team_elos[away_team]

        if opportunity.bet_on_home_team:
            return calculate_win_probability(home_team_elo, away_team_elo)
        else:
            return calculate_win_probability(away_team_elo, home_team_elo)
