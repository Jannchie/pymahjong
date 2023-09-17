import time
import unittest
import random

from .hand import Hand

from . import Game


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
            self.assertEqual(len(g.players[i].sute), 0)
            self.assertEqual(len(g.players[i].furu), 0)
        self.assertEqual(g.dora_num, 1)
        g.dora_num = 2
        self.assertEqual(g.list_dora_indicator(), [g.dead_wall[0], g.dead_wall[2]])
        self.assertEqual(g.list_uradora_indicator(), [g.dead_wall[1], g.dead_wall[3]])
        print(g.wall)
        print([d.code for d in g.dead_wall])
        g.print_info()

    def test_calculate(self):
        random.seed(47)
        hand = Game.get_random_hand(14)
        seq = hand.encode()
        syanten = hand.get_syanten(False)
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

    def test_hand_str_format2(self):
        s = "1225889m1356p15s3z"
        self.assertEqual(s, Hand.strthand(s).to_str())
        s = "125889m1356p15s3z9m"
        self.assertEqual("125889m1356p15s3z9m", Hand.strthand(s).to_str())

    def test_suggestion(self):
        s = "22355667788994m"
        hand = Hand.strthand(s)
        # print(hand.strfhand(hand))
        # print(hand.encode())
        # print(hand.syanten)
        data = hand.get_suggestion(False)
        # prittify print
        # for k, v in data.items():
        #     print(f"打{k}，摸{'、'.join([str(d) for d in v.keys()])}，共 {sum(v.values())} 枚")
        # print(f"共 {data.amount} 枚有效牌")
        
        self.assertEqual(len(data.keys()), 6)

    def test_start(self):
        random.seed(4123)
        Game().start()


if __name__ == "__main__":
    unittest.main()
