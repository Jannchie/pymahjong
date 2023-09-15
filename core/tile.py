from random import randint
from typing import Self


from .utils import (
    ALL,
    get_str,
    is_aka,
    is_same,
    is_same_suit,
    is_same_val,
    is_valid,
    get_suit,
    get_val,
)


class Tile:
    def __init__(self, code: int) -> None:
        if not is_valid(code):
            raise ValueError("Invalid Tile", code)
        self.code = code

    @property
    def suit(self) -> int:
        return get_suit(self.code)

    @property
    def val(self) -> int:
        return get_val(self.code)

    @staticmethod
    def get_random():
        return Tile(ALL[randint(0, len(ALL) - 1)])

    def is_same(self, b: Self):
        return is_same(self.code, b.code)

    def is_same_suit(self, b: Self):
        return is_same_suit(self.code, b.code)

    def is_same_val(self, b: Self):
        return is_same_val(self.code, b.code)

    def is_aka(self):
        return is_aka(self.code)

    def dora(self) -> list[Self]:
        """如果它是宝牌指示牌牌的话，他所指示的宝牌列表

        Returns:
            list[Self]: 它所指示的宝牌列表
        """
        if self.suit >= 3:
            if self.suit == 9:
                return [Tile(300 + i) for i in range(4)]
            else:
                return [Tile(self.code + 100 + i) for i in range(4)]
        else:
            val = self.val
            if val == 9:  # 如果是字牌，7 的下一个是 1，否则 9 的下一个是 1
                val = 1
            else:
                val += 1
            code = self.suit * 100 + val * 10
            return [Tile(code + i) for i in range(4)]

    def __str__(self) -> str:
        return get_str(self.code)

    def __value__(self) -> int:
        return self.code

    def __eq__(self, o: object) -> bool:
        return self.code == o.code

    def __hash__(self) -> int:
        return self.code

    def __repr__(self) -> str:
        return str(self.code)

    def __lt__(self, o: object) -> bool:
        return self.code < o.code
