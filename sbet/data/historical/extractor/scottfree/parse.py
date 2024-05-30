import csv
from typing import List

from sbet.data.historical.extractor.scottfree.models.scottfree_game_csv_row import ScottfreeGameCsvRow


def read_scottfree_game_csv(file_path: str) -> List[ScottfreeGameCsvRow]:
    rows = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row: dict[str, str]
        for row in reader:
            rows.append(ScottfreeGameCsvRow(
                season=row['season'],
                date=row['date'],
                away_team=row['away_team'],
                away_score=row['away_score'],
                away_point_spread=row['away_point_spread'],
                away_point_spread_line=row['away_point_spread_line'],
                away_money_line=row['away_money_line'],
                home_team=row['home_team'],
                home_score=row['home_score'],
                home_point_spread=row['home_point_spread'],
                home_point_spread_line=row['home_point_spread_line'],
                home_money_line=row['home_money_line'],
                over_under=row['over_under'],
                over_line=row['over_line'],
                under_line=row['under_line']
            ))
    return rows
