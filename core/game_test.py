import unittest
import random
from . import Game


class TestGame(unittest.TestCase):
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
        syanten = hand.syanten()
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
            print('---')
            print(hand.str_format())
            print(hand.syanten(), hand)
            print(hand.encode())
            print('---')

if __name__ == "__main__":
    unittest.main()
