import unittest

from . import Tile


class TestTile(unittest.TestCase):
    def test_tile(self):
        self.assertRaises(ValueError, Tile, 1)
        self.assertRaises(ValueError, Tile, 2)

        t1 = Tile(110)
        t2 = Tile(112)
        self.assertTrue(t1.is_same(t2))

        t3 = Tile(210)
        self.assertTrue(t1.is_same_val(t3))
        self.assertFalse(t1.is_same(t3))

        sorted_tile_code = [
            d.code for d in (sorted([Tile.get_random() for _ in range(10)]))
        ]
        self.assertEqual(sorted_tile_code, sorted(sorted_tile_code))

        # test dora
        t4 = Tile(292)
        self.assertEqual(t4.dora(), [Tile(210), Tile(211), Tile(212), Tile(213)])
        t5 = Tile(300)
        self.assertEqual(t5.dora(), [Tile(400), Tile(401), Tile(402), Tile(403)])
        t6 = Tile(902)
        self.assertEqual(t6.dora(), [Tile(300), Tile(301), Tile(302), Tile(303)])
        t7 = Tile(400)
        self.assertEqual(t7.dora(), [Tile(500), Tile(501), Tile(502), Tile(503)])


if __name__ == "__main__":
    unittest.main()
