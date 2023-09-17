import unittest

from .hand import Hand
from .syanten import syanten


class TestSyanten(unittest.TestCase):
    def test_syanten(self):
        test_cases_1 = [
            (((2,), (2,)), 0),
            (((1, 1, 1), (2, 1, 3)), 0),
            (((1, 1, 2), (1, 1, 3)), 1),
            (((2,), (2,)), 0),
            (((3,), (4,)), 0),
            (((1, 1, 1), (2, 1, 3)), 0),
            (((1, 1, 1), (1, 1, 1, 1, 1)), 0),
            (((1, 1, 1, 1, 1), (2,)), -1),
            (((1, 1, 2), (2,)), 0),
            (((3,), (2,)), -1),
            (((3,), (2, 1, 3)), -1),
            (((1,), (1, 2, 2), (1, 1, 1, 2, 3), (1,), (1,), (1,), (1,), (1,)), 4),
            (((1,), (1, 1, 3), (1, 2, 1), (1, 2, 1), (1,), (1,), (1,), (2,)), 3),
            (((1,), (1, 1, 1, 2, 2), (1,), (1, 2, 1, 2, 1, 2, 1), (1,), (1,), (2,)), 3),
            (((1,), (1, 1, 3), (1, 2, 1), (1, 2, 1), (1,), (1,), (1,), (2,)), 3),
            (((1,), (1, 1, 1, 1, 1), (2,), (1,), (1, 2, 1), (1,), (2,), (2,)), 2),
        ]
        for input_data, expected_result in test_cases_1:
            self.assertEqual(syanten(input_data), expected_result)
        test_cases_2 = (
            ("2222m3333p4444s1z2z", 2),
            ("2222m3333p4444s11z", 1),
            ("47m1p1467889s177z9p", 4),
            ("14m4555p12456s13z5m", 2),
            ("145m4555p12456s3z6m", 1),
            ("12345m", 0),
            ("1234m", 0),
            ("123m", 0),
            ("12m", 0),
            ("1m", 0),
            ("2222m", 0),
            ("5122m", 1),
            ("2223m", 0),
            ("11234566678891p", 0),
            ("11233446899993m", 1),
        )
        for input_data, expected_result in test_cases_2:
            self.assertEqual(Hand.strthand(input_data).syanten, expected_result)


if __name__ == "__main__":
    unittest.main()
