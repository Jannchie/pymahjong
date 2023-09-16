from collections import Counter
from random import shuffle
from typing import Self

from .syanten import syanten
from .utils import ALL
from .tile import Tile


def get_str_list(x: list[Tile]):
    return " ".join([str(i) for i in x])


class Hand(list[Tile]):
    def __str__(self) -> str:
        return get_str_list(self)

    def syanten(self) -> int:
        return syanten(self.encode())

    def to_str(self) -> str:
        return Hand.strfhand(self)

    @staticmethod
    def strthand(s: str) -> Self:
        """
        将  https://tenhou.net/2/ 格式的字符串转换成手牌

        Returns:
            str: 手牌
        """
        cur = []
        ans = []
        keys = {
            "m": 0,
            "p": 1,
            "s": 2,
            "z": 3,
            "M": 0,
            "P": 1,
            "S": 2,
            "Z": 3,
        }
        cnt = Counter()
        for ch in s:
            if ch in keys:
                if cur:
                    base_code = keys[ch] * 100 if keys[ch] < 3 else keys[ch] * 100 - 100
                    code_multiplier = 10 if keys[ch] < 3 else 100
                    ans += [
                        Tile(
                            base_code
                            + i * code_multiplier
                            + cnt[base_code + i * code_multiplier]
                        )
                        for i in cur
                    ]
                    for i in cur:
                        cnt[base_code + i * code_multiplier] += 1
                    cur = []
            else:
                cur.append(int(ch))
        if cur:
            ans += [Tile(keys[ch] * 100 + i * 10) for i in cur]
        return Hand(ans)

    @staticmethod
    def strfhand(hand: Self) -> str:
        """
        将手牌转换为字符串，使用 https://tenhou.net/2/ 的格式

        Returns:
            str: 字符串手牌
        """
        prev_suit = hand[0].suit
        prev_val = hand[0].val
        res = ""
        cur = [prev_val]
        key = {
            0: "m",
            1: "p",
            2: "s",
        }
        for i in range(1, len(hand)):
            if hand[i].suit == prev_suit:
                if key.get(prev_suit, "z") == "z":
                    cur.append(hand[i].suit - 2)
                else:
                    cur.append(hand[i].val)
            else:
                res += "".join([str(i) for i in cur]) + key.get(prev_suit, "z")
                if key.get(hand[i].suit, "z") == "z":
                    cur = [hand[i].suit - 2]
                else:
                    cur = [hand[i].val]
                prev_suit = hand[i].suit
        res += "".join([str(i) for i in cur]) + key.get(prev_suit, "z")
        return res

    def encode(self) -> list[list[int]]:
        """
        将手牌编码为一个列表
        时间复杂度 O(n)

        Returns:
            list[list[int]]: _description_
        """
        prev_suit = self[0].suit
        prev_val = self[0].val
        res = []
        cur = [1]
        for i in range(1, len(self)):
            if self[i].suit == prev_suit:
                if self[i].val == prev_val:
                    cur[-1] += 1
                elif abs(self[i].val - prev_val) <= 2:
                    cur += [abs(self[i].val - prev_val), 1]
                else:
                    res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
                    cur = [1]
            else:
                res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
                cur = [1]
            prev_suit = self[i].suit
            prev_val = self[i].val
        res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
        return tuple(res)

    def syanten(self) -> int:
        return syanten(self.encode())


class Player:
    hand: Hand
    kire: list[Tile]
    furu: list[list[Tile]]

    def __init__(
        self, hand: Hand = [], kire: list[Tile] = [], furu: list[list[Tile]] = []
    ):
        self.hand = hand
        self.kire = kire
        self.furu = furu


class Game:
    def __init__(self, bakaze: int = 0, kyoku: int = 0, honba: int = 1):
        self.tiles = [Tile(i) for i in ALL]
        shuffle(self.tiles)
        self.dora_num = 1
        self.bakaze = bakaze
        self.kyoku = kyoku
        self.honba = honba
        self.dead_wall = self.tiles[-14:]
        self.wall = self.tiles[:-14]
        self.players: list[Player] = []
        for _ in range(4):
            p = Player(hand=Hand(self.wall[:13]))
            self.wall = self.wall[13:]
            p.hand.sort()
            self.players.append(p)

    def print_info(self):
        bakaze = ["東", "南", "西", "北"][self.bakaze]
        kyoku = ["一", "二", "三", "四"][self.kyoku]
        print(f"=====================================")
        print(f"{bakaze}{kyoku}局: {self.honba} 本場")
        print(f"親: {self.oya()}")
        print(f"宝牌指示牌: {get_str_list(self.list_dora_indicator())}")
        print(f"里宝牌指示牌: {get_str_list(self.list_uradora_indicator())}")
        print(f"宝牌: {get_str_list(self.list_dora())}")
        print(f"牌山: {get_str_list(self.wall)}")
        print(f"王牌: {get_str_list(self.dead_wall)}")
        for i in range(4):
            print(f"玩家{i}的手牌: {get_str_list(self.players[i].hand)}")
            print(f"玩家{i}的副露: {get_str_list(self.players[i].furu)}")
            print(f"玩家{i}的切牌: {get_str_list(self.players[i].kire)}")

    def oya(self) -> int:
        """获取庄家

        Returns:
            int: 庄家的 Player ID
        """
        return self.kyoku % 4

    def list_dora_indicator(self) -> list[Tile]:
        """获取宝牌指示牌

        Returns:
            list[Tile]: 宝牌指示牌列表
        """
        return self.dead_wall[: self.dora_num * 2 : 2]

    def list_uradora_indicator(self):
        """获取里宝牌指示牌

        Returns:
            list[Tile]: 里宝牌指示牌列表
        """
        return self.dead_wall[1 : self.dora_num * 2 : 2]

    def list_dora(self):
        return [item for t in self.list_dora_indicator() for item in t.dora()]

    @staticmethod
    def get_random_hand(n=13):
        code_list = ALL[::]
        shuffle(code_list)
        return Hand(sorted([Tile(i) for i in code_list[:n]]))
