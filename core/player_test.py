import unittest

from .hand import Hand
from .tile import Tile
from .player import Player


class TestPlayer(unittest.TestCase):
    def test_can_chi(self):
        player = Player(hand=Hand.strthand("123m456p789s11z"))
        self.assertEqual(player.can_chi(Tile.from_str("3m")), True)
        self.assertEqual(player.can_chi(Tile.from_str("2m")), True)
        self.assertEqual(player.can_chi(Tile.from_str("1m")), True)
        self.assertEqual(player.can_chi(Tile.from_str("4m")), True)
        self.assertEqual(player.can_chi(Tile.from_str("5m")), False)

    def test_can_pon(self):
        player = Player(hand=Hand.strthand("123m456p789s11z"))
        self.assertEqual(player.can_pon(Tile.from_str("1z")), True)
        self.assertEqual(player.can_pon(Tile.from_str("2m")), False)
        self.assertEqual(player.can_pon(Tile.from_str("2z")), False)
        self.assertEqual(player.can_pon(Tile.from_str("5m")), False)

    def test_chi(self):
        player = Player(hand=Hand.strthand("3234556m89s11z"))
        chi_options = player.hand.chi_options(Tile.from_str("3m"))
        self.assertEqual(
            chi_options,
            (
                (Tile.from_str("2m"), Tile.from_str("4m")),
                (Tile.from_str("4m"), Tile.from_str("5m")),
            ),
        )
        player.chi(Tile.from_str("3m"), (Tile.from_str("4m"), Tile.from_str("5m")))
        self.assertEqual(player.hand, Hand.strthand("32356m89s11z"))

    def test_pon(self):
        player = Player(hand=Hand.strthand("550p"))
        pon_target = Tile.from_str("5p")
        pon_options = player.hand.pon_options(pon_target)
        self.assertEqual(
            pon_options,
            (
                (Tile.from_str("5p"), Tile.from_str("5p")),
                (Tile.from_str("5p"), Tile.from_str("0p")),
            ),
        )
        player.pon(pon_target, (Tile.from_str("5p"), Tile.from_str("5p")))
        self.assertEqual(player.hand, Hand.strthand("50p"))

    def test_kan(self):
        player = Player(hand=Hand.strthand("550p1z"))
        kan_target = Tile.from_str("5p")
        self.assertEqual(player.can_kan(kan_target), True)
        player.kan(kan_target)
        self.assertEqual(player.hand, Hand.strthand("1z"))


if __name__ == "__main__":
    unittest.main()
