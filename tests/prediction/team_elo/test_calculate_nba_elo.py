import unittest
from sbet.data.historical.models.transform.nba_team import NbaTeam
from sbet.prediction.team_elo.calculate_nba_elo import calculate_nba_elo
from sbet.prediction.team_elo.models.nba_game_outcome import NbaGameOutcome


class TestCalculateNbaElo(unittest.TestCase):
    def setUp(self):
        self.initial_elo = 1500.0
        self.k = 32

    def test_single_game(self):
        game_outcomes = [
            NbaGameOutcome(home_team=NbaTeam.GSW, away_team=NbaTeam.LAL, did_home_team_win=True)
        ]
        elos = calculate_nba_elo(game_outcomes)

        # Calculate expected values
        home_team_initial_elo = self.initial_elo
        away_team_initial_elo = self.initial_elo
        expected_home_elo, expected_away_elo = self.calculate_expected_elos(home_team_initial_elo,
                                                                            away_team_initial_elo, home_team_won=True)

        self.assertAlmostEqual(elos[NbaTeam.GSW], expected_home_elo, places=5)
        self.assertAlmostEqual(elos[NbaTeam.LAL], expected_away_elo, places=5)

    def test_multiple_games(self):
        game_outcomes = [
            NbaGameOutcome(home_team=NbaTeam.GSW, away_team=NbaTeam.LAL, did_home_team_win=True),
            NbaGameOutcome(home_team=NbaTeam.LAL, away_team=NbaTeam.GSW, did_home_team_win=False),
            NbaGameOutcome(home_team=NbaTeam.GSW, away_team=NbaTeam.LAL, did_home_team_win=False),
        ]
        elos = calculate_nba_elo(game_outcomes)

        # Calculate expected values
        home_team_elo, away_team_elo = self.initial_elo, self.initial_elo
        home_team_elo, away_team_elo = self.calculate_expected_elos(home_team_elo, away_team_elo, home_team_won=True)
        away_team_elo, home_team_elo = self.calculate_expected_elos(away_team_elo, home_team_elo, home_team_won=False)
        home_team_elo, away_team_elo = self.calculate_expected_elos(home_team_elo, away_team_elo, home_team_won=False)

        self.assertAlmostEqual(elos[NbaTeam.GSW], home_team_elo, places=5)
        self.assertAlmostEqual(elos[NbaTeam.LAL], away_team_elo, places=5)

    def calculate_expected_elos(self, home_elo, away_elo, home_team_won):
        expected_win_prob_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
        if home_team_won:
            new_home_elo = home_elo + self.k * (1 - expected_win_prob_home)
            new_away_elo = away_elo - self.k * (1 - expected_win_prob_home)
        else:
            new_home_elo = home_elo - self.k * expected_win_prob_home
            new_away_elo = away_elo + self.k * expected_win_prob_home
        return new_home_elo, new_away_elo


if __name__ == '__main__':
    unittest.main()
