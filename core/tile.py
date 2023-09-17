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
    get_ver,
)


class Tile:
    def __init__(self, code: int) -> None:
        if not is_valid(code):
            raise ValueError("Invalid Tile", code)
        self.code = code

    @staticmethod
    def is_neighboring(a: "Tile", b: "Tile"):
        return abs(a.val - b.val) == 1

    @staticmethod
    def from_str(s: str) -> Self:
        k = {
            "m": 0,
            "p": 1,
            "s": 2,
        }
        key = s[1]
        val = int(s[0])
        if key in ["z", "Z"]:
            return Tile(200 + int(val) * 100)
        elif val == 0:
            # 赤宝牌
            return Tile(k[key] * 100 + 53)
        else:
            return Tile(k[key] * 100 + int(val) * 10)

    @staticmethod
    def get_random():
        return Tile(ALL[randint(0, len(ALL) - 1)])

    @property
    def emoji(self) -> str:
        if self.suit >= 3:
            return ["🀀", "🀁", "🀂", "🀃", "🀆", "🀅", "🀄"][self.suit - 3]
        elif self.suit == 0:
            return ["🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"][self.val - 1]
        elif self.suit == 1:
            return ["🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"][self.val - 1]
        elif self.suit == 2:
            return ["🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"][self.val - 1]
        raise ValueError("Invalid Tile")

    @property
    def suit(self) -> int:
        return get_suit(self.code)

    @property
    def val(self) -> int:
        return get_val(self.code)

    @property
    def ver(self) -> int:
        return get_ver(self.code)

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

    def __eq__(self, o: Self) -> bool:
        if self.val == 5:
            return self.code // 10 == o.code // 10 and not (self.ver ^ o.ver)
        return self.code // 10 == o.code // 10

    def __hash__(self) -> int:
        return self.code // 10

    def __repr__(self) -> str:
        return f'Tile("{self}")'

    def __lt__(self, o: object) -> bool:
        return self.code < o.code
