def calculate_elo(winner_elo: float, loser_elo: float, k: int) -> (float, float):
    expected_win_prob = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    new_winner_elo = winner_elo + k * (1 - expected_win_prob)
    new_loser_elo = loser_elo - k * (1 - expected_win_prob)
    return new_winner_elo, new_loser_elo


def calculate_win_probability(team_elo: float, opponent_elo: float) -> float:
    """
    Calculate the probability of a team winning against an opponent based on their Elo ratings.

    :param team_elo: Elo rating of the team
    :param opponent_elo: Elo rating of the opponent
    :return: Probability of the team winning
    """
    return 1 / (1 + 10 ** ((opponent_elo - team_elo) / 400))
