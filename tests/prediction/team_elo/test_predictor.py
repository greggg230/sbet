import unittest
from sbet.prediction.team_elo.predictor import TeamEloProbabilityPredictor
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome
from sbet.data.historical.models.transform.nba_game import NbaGame
from sbet.data.historical.models import NbaMoneyLineBettingOpportunity
from sbet.data.historical.models.transform.nba_team import NbaTeam


class TestTeamEloProbabilityPredictor(unittest.TestCase):
    def setUp(self):
        # Sample game outcomes
        game_outcomes = [
            NbaGameOutcome(home_team=NbaTeam.GSW, away_team=NbaTeam.CLE, did_home_team_win=True),
            NbaGameOutcome(home_team=NbaTeam.LAL, away_team=NbaTeam.BOS, did_home_team_win=False),
            NbaGameOutcome(home_team=NbaTeam.MIA, away_team=NbaTeam.SAS, did_home_team_win=True),
        ]

        self.predictor = TeamEloProbabilityPredictor(game_outcomes)

    def test_calculate_probability_of_bet_win_home_team(self):
        game = NbaGame(game_id=1, game_date="2023-01-01", season="2023", game_type="Regular", home_team=NbaTeam.GSW,
                       away_team=NbaTeam.CLE, home_score=0, away_score=0)
        opportunity = NbaMoneyLineBettingOpportunity(game=game, book_name="BookA", bet_on_home_team=True, price=1.8)

        probability = self.predictor.calculate_probability_of_bet_win(opportunity)

        home_team_elo = self.predictor.team_elos[NbaTeam.GSW]
        away_team_elo = self.predictor.team_elos[NbaTeam.CLE]

        expected_probability = 1 / (1 + 10 ** ((away_team_elo - home_team_elo) / 400))

        self.assertAlmostEqual(probability, expected_probability, places=5)

    def test_calculate_probability_of_bet_win_away_team(self):
        game = NbaGame(game_id=2, game_date="2023-01-01", season="2023", game_type="Regular", home_team=NbaTeam.GSW,
                       away_team=NbaTeam.CLE, home_score=0, away_score=0)
        opportunity = NbaMoneyLineBettingOpportunity(game=game, book_name="BookB", bet_on_home_team=False, price=2.2)

        probability = self.predictor.calculate_probability_of_bet_win(opportunity)

        home_team_elo = self.predictor.team_elos[NbaTeam.GSW]
        away_team_elo = self.predictor.team_elos[NbaTeam.CLE]

        expected_probability = 1 / (1 + 10 ** ((home_team_elo - away_team_elo) / 400))

        self.assertAlmostEqual(probability, expected_probability, places=5)


if __name__ == '__main__':
    unittest.main()
