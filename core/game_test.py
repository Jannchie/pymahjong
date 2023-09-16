import json
import time
import unittest
import random

from . import Game, Hand


class TestGame(unittest.TestCase):
    def benchmark_hand_encode(self):
        random.seed(47)
        hand = Game.get_random_hand(14)
        hand.encode()

    def test_game(self):
        random.seed(47)
        g = Game()
        self.assertEqual(len(g.dead_wall), 14)
        self.assertEqual(len(g.wall), 70)
        self.assertEqual(len(g.players), 4)
        for i in range(4):
            self.assertEqual(len(g.players[i].hand), 13)
            self.assertEqual(len(g.players[i].kire), 0)
            self.assertEqual(len(g.players[i].furu), 0)
        self.assertEqual(g.dora_num, 1)
        g.dora_num = 2
        self.assertEqual(g.list_dora_indicator(), [g.dead_wall[0], g.dead_wall[2]])
        self.assertEqual(g.list_uradora_indicator(), [g.dead_wall[1], g.dead_wall[3]])
        # g.print_info()

    def test_calculate(self):
        random.seed(47)
        hand = Game.get_random_hand(14)
        seq = hand.encode()
        syanten = hand.get_syanten()
        print(hand.to_str())
        self.assertEqual(syanten, 4)
        self.assertEqual(
            seq,
            (
                (1,),
                (1, 1, 1),
                (1,),
                (1, 1, 1, 1, 1),
                (2,),
                (1,),
                (1,),
                (1,),
                (1,),
                (1,),
            ),
        )

    def test_get_random_hand(self):
        hand = Game.get_random_hand()
        self.assertEqual(len(hand), 13)

    def test_hand_str_format(self):
        random.seed(217321)
        for i in range(15):
            hand = Game.get_random_hand(14)
            print(hand.to_str())
            print(hand.get_syanten(), hand)
            print(hand.encode())

    def test_hand_str_format2(self):
        s = "1225889m1356p15s3z"
        self.assertEqual(s, Hand.strthand(s).to_str())
        s = "125889m1356p15s3z9m"
        self.assertEqual("125889m1356p15s3z9m", Hand.strthand(s).to_str())
        print(Hand.strthand("1226m13447p357s2z4z").encode())

    def test_suggestion(self):
        # calculate time
        start = time.time()
        s = "112288m1356p15s3z3m"
        hand = Hand.strthand(s)
        print("---")
        print(hand.strfhand(hand))
        print(hand.encode())
        print(hand.syanten)
        data = hand.suggestion
        ## prittify print
        for k, v in data.items():
            print(f"打{k}摸 {v}")
        print("---")
        end = time.time()
        print(f"Time: {end - start:.2f}s")


if __name__ == "__main__":
    unittest.main()
