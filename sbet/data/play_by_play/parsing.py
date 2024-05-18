import csv
from typing import List

from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.csv.play import Play


def parse_plays(csv_path: str) -> List[Play]:
    plays = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        row: dict[str, str]
        for row in reader:
            play = Play(
                game_id=int(row['game_id']),
                data_set=row['data_set'],
                date=row['date'],
                a1=row['a1'],
                a2=row['a2'],
                a3=row['a3'],
                a4=row['a4'],
                a5=row['a5'],
                h1=row['h1'],
                h2=row['h2'],
                h3=row['h3'],
                h4=row['h4'],
                h5=row['h5'],
                period=int(row['period']),
                away_score=int(row['away_score']),
                home_score=int(row['home_score']),
                remaining_time=row['remaining_time'],
                elapsed=row['elapsed'],
                play_length=row['play_length'],
                play_id=int(row['play_id']),
                team=row['team'],
                event_type=row['event_type'],
                assist=row.get('assist'),
                away=row.get('away'),
                home=row.get('home'),
                block=row.get('block'),
                entered=row.get('entered'),
                left=row.get('left'),
                num=row.get('num'),
                opponent=row.get('opponent'),
                outof=row.get('outof'),
                player=row.get('player'),
                points=int(row['points']) if row['points'] else None,
                possession=row.get('possession'),
                reason=row.get('reason'),
                result=row.get('result'),
                steal=row.get('steal'),
                type=row.get('type'),
                shot_distance=int(row['shot_distance']) if row['shot_distance'] else None,
                original_x=int(row['original_x']) if row['original_x'] else None,
                original_y=int(row['original_y']) if row['original_y'] else None,
                converted_x=float(row['converted_x']) if row['converted_x'] else None,
                converted_y=float(row['converted_y']) if row['converted_y'] else None,
                description=row['description']
            )
            plays.append(play)
    return plays


def parse_game(csv_path: str, game_id: str, date: str, home_team: str, away_team: str) -> Game:
    plays = parse_plays(csv_path)
    return Game(
        game_id=game_id,
        date=date,
        home_team=home_team,
        away_team=away_team,
        plays=plays
    )
