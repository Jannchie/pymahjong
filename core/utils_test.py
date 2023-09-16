import unittest

from . import utils


def devide(n: int, max=4):
    ans = []
    for i in range(1, max + 1):
        ans.append([i] + devide(n - i, max))
    return ans


class TestUtils(unittest.TestCase):
    def test_code(self):
        data = (
            (10, "一萬"),
            (110, "一筒"),
            (210, "一條"),
            (293, "九條"),
            (300, "東"),
            (400, "南"),
            (500, "西"),
            (600, "北"),
            (700, "白"),
            (801, "發"),
            (902, "中"),
            (903, "中"),
        )
        for d in data:
            self.assertEqual(utils.get_str(d[0]), d[1])

        self.assertRaises(ValueError, utils.get_str, 476)
        self.assertRaises(ValueError, utils.get_str, 512)
        self.assertRaises(ValueError, utils.get_str, 275)

    def test_is_same(self):
        self.assertTrue(utils.is_same_suit(110, 120))
        self.assertTrue(utils.is_same_suit(110, 130))
        self.assertTrue(utils.is_same_suit(110, 140))
        self.assertTrue(utils.is_same_val(110, 111))
        self.assertTrue(utils.is_same_val(210, 112))
        self.assertTrue(utils.is_same(111, 110))


if __name__ == "__main__":
    unittest.main()
