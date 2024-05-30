from datetime import datetime

from frozendict import frozendict

from sbet.data.historical.extractor.base import HistoricalBetDataExtractor
from sbet.data.historical.extractor.models.game_betting_opportunities import GameBettingOpportunities
from sbet.data.historical.extractor.models.historical_bet_data import HistoricalBetData
from sbet.data.historical.extractor.scottfree.parse import read_scottfree_game_csv
from sbet.data.historical.models.transform.game import Game
from sbet.data.historical.models.transform.money_line_betting_opportunity import MoneyLineBettingOpportunity


class ScottfreeHistoricalBetDataExtractor(HistoricalBetDataExtractor):
    csv_file_path: str

    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path

    def extract(self) -> HistoricalBetData:
        # Read CSV data
        rows = read_scottfree_game_csv(self.csv_file_path)

        games = []
        money_line_data = {}

        fake_teams = ["all_star_lebron"]

        for row in rows:
            if row.home_team in fake_teams or row.away_team in fake_teams:
                continue

            home_team = row.home_team
            away_team = row.away_team

            game = Game(
                game_id=f"{row.date.replace('-', '')}{home_team}{away_team}",
                game_date=datetime.strptime(row.date, '%Y-%m-%d').date(),
                season=row.season,
                game_type='Regular Season',  # Assuming all games are regular season
                home_team=home_team,
                away_team=away_team,
                home_score=int(row.home_score),
                away_score=int(row.away_score)
            )
            games.append(game)

            if row.home_money_line in ("NL", "0"):
                home_opportunity = None
            else:
                home_opportunity = MoneyLineBettingOpportunity(
                    game=game,
                    book_name="Scottfree",
                    bet_on_home_team=True,
                    price=float(row.home_money_line)
                )

            if row.away_money_line in ("NL", "0"):
                away_opportunity = None
            else:
                away_opportunity = MoneyLineBettingOpportunity(
                    game=game,
                    book_name="Scottfree",
                    bet_on_home_team=False,
                    price=float(row.away_money_line)
                )

            money_line_data[game] = GameBettingOpportunities(
                home=home_opportunity,
                away=away_opportunity
            )

        return HistoricalBetData(
            games=games,
            money_line_data=frozendict(money_line_data)
        )
