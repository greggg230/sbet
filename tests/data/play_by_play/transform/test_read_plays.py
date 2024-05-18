import unittest
import tempfile
import os
from sbet.data.play_by_play.parsing import parse_plays
from sbet.data.play_by_play.models.csv.play import Play


class TestPlayByPlayParsing(unittest.TestCase):

    def setUp(self):
        # Sample CSV data for testing plays
        self.sample_play_data = """game_id,data_set,date,a1,a2,a3,a4,a5,h1,h2,h3,h4,h5,period,away_score,home_score,remaining_time,elapsed,play_length,play_id,team,event_type,assist,away,home,block,entered,left,num,opponent,outof,player,points,possession,reason,result,steal,type,shot_distance,original_x,original_y,converted_x,converted_y,description
42100216,2021-22 Playoffs,2022-05-13,Al Horford,Grant Williams,Jaylen Brown,Marcus Smart,Jayson Tatum,Brook Lopez,Grayson Allen,Giannis Antetokounmpo,Jrue Holiday,Wesley Matthews,1,0,0,0:12:00,0:00:00,0:00:00,1,,start of period,,,,,,,,,,,,,,,,start of period,,,,,,
42100216,2021-22 Playoffs,2022-05-13,Al Horford,Grant Williams,Jaylen Brown,Marcus Smart,Jayson Tatum,Brook Lopez,Grayson Allen,Giannis Antetokounmpo,Jrue Holiday,Wesley Matthews,1,0,0,0:12:00,0:00:00,0:00:00,2,MIL,jump ball,,Al Horford,Brook Lopez,,,,,,,Al Horford,,Grant Williams,,,,jump ball,,,,,,Jump Ball Lopez vs. Horford: Tip to Williams
42100216,2021-22 Playoffs,2022-05-13,Al Horford,Grant Williams,Jaylen Brown,Marcus Smart,Jayson Tatum,Brook Lopez,Grayson Allen,Giannis Antetokounmpo,Jrue Holiday,Wesley Matthews,1,3,0,0:11:41,0:00:19,0:00:19,3,BOS,shot,,,,,,,,,,Jaylen Brown,3,,,made,,3pt jump shot,27,-62,267,31.2,31.700000000000003,Brown 27' 3PT Jump Shot (3 PTS)
42100216,2021-22 Playoffs,2022-05-13,Al Horford,Grant Williams,Jaylen Brown,Marcus Smart,Jayson Tatum,Brook Lopez,Grayson Allen,Giannis Antetokounmpo,Jrue Holiday,Wesley Matthews,1,3,0,0:11:22,0:00:38,0:00:19,4,MIL,shot,,,,,,,,,,Grayson Allen,0,,,missed,,3pt pullup jump shot,27,-119,242,13.1,64.8,MISS Allen 27' 3PT Pullup Jump Shot
42100216,2021-22 Playoffs,2022-05-13,Al Horford,Grant Williams,Jaylen Brown,Marcus Smart,Jayson Tatum,Brook Lopez,Grayson Allen,Giannis Antetokounmpo,Jrue Holiday,Wesley Matthews,1,3,0,0:11:19,0:00:41,0:00:03,5,BOS,rebound,,,,,,,,,,Al Horford,,,,,,rebound defensive,,,,,,Horford REBOUND (Off:0 Def:1)
"""
        # Create a temporary CSV file for plays
        self.tempfile = tempfile.NamedTemporaryFile(delete=False, mode='w')
        self.tempfile.write(self.sample_play_data)
        self.tempfile.close()

    def tearDown(self):
        # Remove the temporary file
        os.remove(self.tempfile.name)

    def test_parse_plays(self):
        # Parse the CSV data
        plays = parse_plays(self.tempfile.name)

        # Assert the number of plays parsed
        self.assertEqual(len(plays), 5)

        # Assert the type and contents of the first play
        play = plays[0]
        self.assertIsInstance(play, Play)
        self.assertEqual(play.game_id, 42100216)
        self.assertEqual(play.data_set, "2021-22 Playoffs")
        self.assertEqual(play.date, "2022-05-13")
        self.assertEqual(play.a1, "Al Horford")
        self.assertEqual(play.a2, "Grant Williams")
        self.assertEqual(play.a3, "Jaylen Brown")
        self.assertEqual(play.a4, "Marcus Smart")
        self.assertEqual(play.a5, "Jayson Tatum")
        self.assertEqual(play.h1, "Brook Lopez")
        self.assertEqual(play.h2, "Grayson Allen")
        self.assertEqual(play.h3, "Giannis Antetokounmpo")
        self.assertEqual(play.h4, "Jrue Holiday")
        self.assertEqual(play.h5, "Wesley Matthews")
        self.assertEqual(play.period, 1)
        self.assertEqual(play.away_score, 0)
        self.assertEqual(play.home_score, 0)
        self.assertEqual(play.remaining_time, "0:12:00")
        self.assertEqual(play.elapsed, "0:00:00")
        self.assertEqual(play.play_length, "0:00:00")
        self.assertEqual(play.play_id, 1)
        self.assertEqual(play.team, "")
        self.assertEqual(play.event_type, "start of period")
        self.assertEqual(play.assist, "")
        self.assertEqual(play.away, "")
        self.assertEqual(play.home, "")
        self.assertEqual(play.block, "")
        self.assertEqual(play.entered, "")
        self.assertEqual(play.left, "")
        self.assertEqual(play.num, "")
        self.assertEqual(play.opponent, "")
        self.assertEqual(play.outof, "")
        self.assertEqual(play.player, "")
        self.assertEqual(play.points, None)
        self.assertEqual(play.possession, "")
        self.assertEqual(play.reason, "")
        self.assertEqual(play.result, "")
        self.assertEqual(play.steal, "")
        self.assertEqual(play.type, "start of period")
        self.assertEqual(play.shot_distance, None)
        self.assertEqual(play.original_x, None)
        self.assertEqual(play.original_y, None)
        self.assertEqual(play.converted_x, None)
        self.assertEqual(play.converted_y, None)
        self.assertEqual(play.description, "")
