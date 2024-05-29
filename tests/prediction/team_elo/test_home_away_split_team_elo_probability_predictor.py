import unittest
from datetime import date

from sbet.data.historical.models import NbaMoneyLineBettingOpportunity, NbaGame
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.prediction.team_elo.home_away_split_team_elo_probability_predictor import \
    HomeAwaySplitTeamEloProbabilityPredictor
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome


class TestHomeAwaySplitTeamEloProbabilityPredictor(unittest.TestCase):

    def setUp(self):
        self.game_outcomes = [
            NbaGameOutcome(home_team=NbaTeam.GSW, away_team=NbaTeam.LAL, did_home_team_win=True),
            NbaGameOutcome(home_team=NbaTeam.LAL, away_team=NbaTeam.GSW, did_home_team_win=False),
            NbaGameOutcome(home_team=NbaTeam.GSW, away_team=NbaTeam.LAL, did_home_team_win=False),
        ]

        self.predictor = HomeAwaySplitTeamEloProbabilityPredictor(self.game_outcomes)

        self.game1 = NbaGame(
            game_id=1,
            game_date=date(2022, 1, 1),
            season="2021-2022",
            game_type="Regular",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.LAL,
            home_score=100,
            away_score=90
        )
        self.game2 = NbaGame(
            game_id=2,
            game_date=date(2022, 1, 2),
            season="2021-2022",
            game_type="Regular",
            home_team=NbaTeam.LAL,
            away_team=NbaTeam.GSW,
            home_score=90,
            away_score=100
        )

    def test_calculate_probability_of_bet_win(self):
        opportunity1 = NbaMoneyLineBettingOpportunity(
            game=self.game1,
            book_name="BookA",
            bet_on_home_team=True,
            price=150
        )
        opportunity2 = NbaMoneyLineBettingOpportunity(
            game=self.game2,
            book_name="BookB",
            bet_on_home_team=False,
            price=-120
        )

        probability1 = self.predictor.calculate_probability_of_bet_win(opportunity1)
        probability2 = self.predictor.calculate_probability_of_bet_win(opportunity2)

        # Expected win probability for GSW vs. LAL game at GSW's home
        gsw_home_elo, lal_away_elo = self.predictor.team_elos[NbaTeam.GSW][0], self.predictor.team_elos[NbaTeam.LAL][1]
        expected_prob1 = 1 / (1 + 10 ** ((lal_away_elo - gsw_home_elo) / 400))
        self.assertAlmostEqual(probability1, expected_prob1, places=5)

        # Expected win probability for GSW vs. LAL game at LAL's home
        lal_home_elo, gsw_away_elo = self.predictor.team_elos[NbaTeam.LAL][0], self.predictor.team_elos[NbaTeam.GSW][1]
        expected_prob2 = 1 / (1 + 10 ** ((gsw_away_elo - lal_home_elo) / 400))
        self.assertAlmostEqual(probability2, expected_prob2, places=5)


if __name__ == '__main__':
    unittest.main()
