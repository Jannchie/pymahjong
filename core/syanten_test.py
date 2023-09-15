import unittest

from .syanten import syanten

from . import Tile


class TestSyanten(unittest.TestCase):
    def test_syanten(self):
        test_cases = [
            (((2,), (2,)), 0),
            (((3,), (2,)), -1),
            (((3,), (2, 1, 3)), -1),
            (((1, 1, 1), (2, 1, 3)), 0),
            (((1, 1, 2), (1, 1, 3)), 1),
            (((2,), (2,)), 0),
            (((3,), (4,)), 0),
            (((1, 1, 1), (2, 1, 3)), 0),
            (
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
                4,
            ),
            (((1,), (1, 2, 2), (1, 1, 1, 2, 3), (1,), (1,), (1,), (1,), (1,)), 4),
        ]

        for input_data, expected_result in test_cases:
            self.assertEqual(syanten(input_data), expected_result)


if __name__ == "__main__":
    unittest.main()
