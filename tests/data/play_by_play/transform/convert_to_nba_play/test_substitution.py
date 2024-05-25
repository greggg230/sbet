import unittest
from dataclasses import replace

from sbet.data.historical.models import NbaTeam
from sbet.data.play_by_play.models.csv.play import Play
from sbet.data.play_by_play.models.csv.game import Game
from sbet.data.play_by_play.models.transform.plays import Substitution
from sbet.data.play_by_play.transform import convert_to_nba_play
from sbet.data.play_by_play.models.transform.player import Player


class TestConvertToNbaPlaySubstitution(unittest.TestCase):

    def setUp(self):
        self.raw_play_substitution = Play(
            game_id=1,
            data_set="data_set",
            date="2023-01-01",
            a1="A1", a2="A2", a3="A3", a4="A4", a5="A5",
            h1="H1", h2="H2", h3="H3", h4="H4", h5="H6",
            period=1,
            away_score=0,
            home_score=0,
            remaining_time="11:00",
            elapsed="0:00:00",
            play_length="0:00:03",
            play_id=1,
            team="home",
            event_type="substitution",
            assist=None,
            away=None,
            home=None,
            block=None,
            entered="H6",
            left="H5",
            num=None,
            opponent=None,
            outof=None,
            player=None,
            points=None,
            possession=None,
            reason=None,
            result=None,
            steal=None,
            type=None,
            shot_distance=None,
            original_x=None,
            original_y=None,
            converted_x=None,
            converted_y=None,
            description="Substitution H6 in, H5 out"
        )

        self.game = Game(
            game_id=1,
            date="2023-01-01",
            home_team=NbaTeam.GSW,
            away_team=NbaTeam.MEM,
            plays=[]
        )

    def test_convert_to_nba_play_substitution(self):
        self.game = replace(self.game, plays=[self.raw_play_substitution])
        nba_play = convert_to_nba_play(self.raw_play_substitution, self.game)
        expected_play = Substitution(
            play_length=3000,
            play_id=1,
            home_team_lineup=frozenset({Player("H1"), Player("H2"), Player("H3"), Player("H4"), Player("H6")}),
            away_team_lineup=frozenset({Player("A1"), Player("A2"), Player("A3"), Player("A4"), Player("A5")})
        )
        self.assertEqual(nba_play, expected_play)


if __name__ == '__main__':
    unittest.main()
