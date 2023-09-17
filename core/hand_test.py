import unittest

from core.hand import Hand

from .syanten import syanten


class TestHand(unittest.TestCase):
    def test_strthand(self):
        s = "2222m"
        Hand.strthand(s).to_str()
        self.assertEqual([i.code for i in Hand.strthand(s)], [20, 21, 22, 23])

    def test_strfhand(self):
        s = "5550m"
        self.assertEqual(Hand.strfhand(Hand.strthand(s)), s)


if __name__ == "__main__":
    unittest.main()
