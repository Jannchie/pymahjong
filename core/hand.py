from .syanten import syanten
from .tile import Tile
from .utils import ALL_DIFFERENT


from collections import Counter, defaultdict
from typing import Self


def get_str_list(x: list[Tile]):
    return " ".join([str(i) for i in x])


class Hand(list[Tile]):
    def __str__(self) -> str:
        return get_str_list(self)

    @property
    def syanten(self) -> int:
        return self.get_syanten()

    def get_syanten(self) -> int:
        return syanten(self.encode())

    def to_str(self) -> str:
        return Hand.strfhand(self)

    def copy(self) -> Self:
        return Hand(self.copy())

    @property
    def suggestion(self) -> defaultdict[Tile, set[Tile]]:
        cur_syanten = self.syanten
        res = defaultdict(set)
        hand = Hand(sorted(self[:]))
        for i in range(len(self)):
            tile = self[i]
            hand.remove(tile)
            for code in ALL_DIFFERENT:
                t = Tile(code)
                hand.append(t)
                hand.sort()
                if hand.syanten < cur_syanten:
                    res[tile].add(Tile(t.code))
                hand.remove(t)
            hand.append(tile)
        return res

    def list_yukouhai(self) -> defaultdict[Tile, set[Tile]]:
        cur_syanten = self.syanten
        res = defaultdict(set)
        for i in range(len(self)):
            tile = self[i]
            self.remove(tile)
            for code in ALL_DIFFERENT:
                t = Tile(code)
                self.append(t)
                if self.syanten < cur_syanten:
                    res[tile].add(t)
                self.remove(t)
            self.append(tile)
        return res

    @staticmethod
    def strthand(s: str) -> "Hand":
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

    def encode(self) -> tuple[tuple[int]]:
        """
        将手牌编码为一个列表
        时间复杂度 O(log(n))

        Returns:
            list[list[int]]: _description_
        """

        # 检查是否已经排序
        flag = True
        for i in range(1, len(self)):
            if self[i].code < self[i - 1].code:
                flag = False
                hand = sorted(self)
                break
        if flag:
            hand = self
        prev_suit = hand[0].suit
        prev_val = hand[0].val
        res = []
        cur = [1]
        for i in range(1, len(self)):
            if hand[i].suit == prev_suit:
                if hand[i].val == prev_val:
                    cur[-1] += 1
                elif abs(hand[i].val - prev_val) <= 2:
                    cur += [abs(hand[i].val - prev_val), 1]
                else:
                    res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
                    cur = [1]
            else:
                res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
                cur = [1]
            prev_suit = hand[i].suit
            prev_val = hand[i].val
        res.append(tuple(cur) if cur < cur[::-1] else tuple(cur[::-1]))
        return tuple(res)
