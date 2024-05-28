import unittest
from sbet.prediction.team_elo.elo import calculate_elo, calculate_win_probability


class TestCalculateElo(unittest.TestCase):
    def setUp(self):
        self.k = 32

    def test_calculate_elo_winner_loser(self):
        winner_elo = 1600.0
        loser_elo = 1400.0
        new_winner_elo, new_loser_elo = calculate_elo(winner_elo, loser_elo, self.k)

        expected_win_prob_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        expected_new_winner_elo = winner_elo + self.k * (1 - expected_win_prob_winner)
        expected_new_loser_elo = loser_elo - self.k * (1 - expected_win_prob_winner)

        self.assertAlmostEqual(new_winner_elo, expected_new_winner_elo, places=5)
        self.assertAlmostEqual(new_loser_elo, expected_new_loser_elo, places=5)

    def test_calculate_elo_equal_elos(self):
        winner_elo = 1500.0
        loser_elo = 1500.0
        new_winner_elo, new_loser_elo = calculate_elo(winner_elo, loser_elo, self.k)

        expected_win_prob_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        expected_new_winner_elo = winner_elo + self.k * (1 - expected_win_prob_winner)
        expected_new_loser_elo = loser_elo - self.k * (1 - expected_win_prob_winner)

        self.assertAlmostEqual(new_winner_elo, expected_new_winner_elo, places=5)
        self.assertAlmostEqual(new_loser_elo, expected_new_loser_elo, places=5)

    def test_calculate_win_probability(self):
        team_elo = 1600.0
        opponent_elo = 1400.0

        win_probability = calculate_win_probability(team_elo, opponent_elo)
        expected_probability = 1 / (1 + 10 ** ((1400.0 - 1600.0) / 400))

        self.assertAlmostEqual(win_probability, expected_probability, places=5)

    def test_calculate_elo_close_elos(self):
        winner_elo = 1520.0
        loser_elo = 1480.0
        new_winner_elo, new_loser_elo = calculate_elo(winner_elo, loser_elo, self.k)

        expected_win_prob_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        expected_new_winner_elo = winner_elo + self.k * (1 - expected_win_prob_winner)
        expected_new_loser_elo = loser_elo - self.k * (1 - expected_win_prob_winner)

        self.assertAlmostEqual(new_winner_elo, expected_new_winner_elo, places=5)
        self.assertAlmostEqual(new_loser_elo, expected_new_loser_elo, places=5)


if __name__ == '__main__':
    unittest.main()
